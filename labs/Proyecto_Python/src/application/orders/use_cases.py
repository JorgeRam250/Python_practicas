"""Casos de uso de ordenes."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.application.errors import (
    ApplicationConflictError,
    ApplicationDependencyError,
    ApplicationNotFoundError,
    ApplicationValidationError,
)
from src.application.ports import (
    CustomerRepositoryPort,
    EventPublisherPort,
    OrderRepositoryPort,
    ProductRepositoryPort,
    UnitOfWorkPort,
)
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.orders.exceptions import DomainValidationError, InvalidOrderStateTransitionError

from .dto import (
    CreateOrderCommand,
    GetOrderQuery,
    ListOrdersQuery,
    OrderDTO,
    OrderItemDTO,
    UpdateOrderStatusCommand,
)


class CreateOrderUseCase:
    """Crea una orden y publica evento de creacion."""

    def __init__(
        self,
        customer_repository: CustomerRepositoryPort,
        product_repository: ProductRepositoryPort,
        order_repository: OrderRepositoryPort,
        event_publisher: EventPublisherPort,
        unit_of_work: UnitOfWorkPort,
    ) -> None:
        self._customer_repository = customer_repository
        self._product_repository = product_repository
        self._order_repository = order_repository
        self._event_publisher = event_publisher
        self._unit_of_work = unit_of_work

    def execute(self, command: CreateOrderCommand) -> OrderDTO:
        """Ejecuta el caso de uso de creacion de orden."""
        customer = self._customer_repository.get_by_id(command.customer_id)
        if customer is None:
            raise ApplicationNotFoundError("No existe el customer solicitado.")

        if not command.items:
            raise ApplicationValidationError("La orden debe tener al menos un item.")

        try:
            order_items = self._build_order_items(command)
            order = Order(
                order_id=uuid4(),
                customer=customer,
                branch_id=command.branch_id,
                items=order_items,
                shipping_cost=command.shipping_cost,
                tax_rate=command.tax_rate,
            )

            self._order_repository.add(order)
            self._event_publisher.publish(
                event_name="orders.created.v1",
                payload=self._build_created_event_payload(order),
            )
            self._unit_of_work.commit()
            return _to_order_dto(order)
        except (ApplicationConflictError, ApplicationNotFoundError):
            raise
        except DomainValidationError as exc:
            self._unit_of_work.rollback()
            raise ApplicationValidationError(str(exc)) from exc
        except Exception as exc:  # pragma: no cover - proteccion defensiva.
            self._unit_of_work.rollback()
            raise ApplicationDependencyError(
                "No fue posible crear la orden por una falla tecnica."
            ) from exc

    def _build_order_items(self, command: CreateOrderCommand) -> list[OrderItem]:
        """Resuelve productos y construye snapshots para la orden."""
        order_items: list[OrderItem] = []
        for line in command.items:
            product = self._product_repository.get_by_id(line.product_id)
            if product is None:
                raise ApplicationNotFoundError(
                    f"No existe el producto solicitado: {line.product_id}."
                )
            if not product.is_active:
                raise ApplicationConflictError(
                    f"El producto {product.product_id} esta inactivo y no se puede ordenar."
                )
            order_items.append(OrderItem.from_product(product=product, quantity=line.quantity))
        return order_items

    @staticmethod
    def _build_created_event_payload(order: Order) -> dict[str, Any]:
        """Serializa payload simple para evento de creacion."""
        return {
            "order_id": str(order.order_id),
            "customer_id": str(order.customer.customer_id),
            "status": order.status.value,
            "total": str(order.total),
            "item_count": len(order.items),
        }


class GetOrderUseCase:
    """Obtiene una orden por identificador."""

    def __init__(self, order_repository: OrderRepositoryPort) -> None:
        self._order_repository = order_repository

    def execute(self, query: GetOrderQuery) -> OrderDTO:
        """Ejecuta consulta de detalle de orden."""
        order = self._order_repository.get_by_id(query.order_id)
        if order is None:
            raise ApplicationNotFoundError("No existe la orden solicitada.")
        return _to_order_dto(order)


class ListOrdersUseCase:
    """Lista ordenes con filtro opcional de estado."""

    def __init__(self, order_repository: OrderRepositoryPort) -> None:
        self._order_repository = order_repository

    def execute(self, query: ListOrdersQuery) -> list[OrderDTO]:
        """Ejecuta consulta de listado de ordenes."""
        orders = self._order_repository.list(status=query.status)
        return [_to_order_dto(order) for order in orders]


class UpdateOrderStatusUseCase:
    """Actualiza estado de ordenes y publica evento de cambio de estado."""

    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        event_publisher: EventPublisherPort,
        unit_of_work: UnitOfWorkPort,
    ) -> None:
        self._order_repository = order_repository
        self._event_publisher = event_publisher
        self._unit_of_work = unit_of_work

    def execute(self, command: UpdateOrderStatusCommand) -> OrderDTO:
        """Ejecuta el cambio de estado de una orden."""
        order = self._order_repository.get_by_id(command.order_id)
        if order is None:
            raise ApplicationNotFoundError("No existe la orden solicitada.")

        try:
            self._apply_transition(order, command)
            self._order_repository.update(order)
            self._event_publisher.publish(
                event_name="orders.status_changed.v1",
                payload={
                    "order_id": str(order.order_id),
                    "status": order.status.value,
                    "cancellation_reason": order.cancellation_reason,
                },
            )
            self._unit_of_work.commit()
            return _to_order_dto(order)
        except ApplicationValidationError:
            raise
        except InvalidOrderStateTransitionError as exc:
            self._unit_of_work.rollback()
            raise ApplicationConflictError(str(exc)) from exc
        except DomainValidationError as exc:
            self._unit_of_work.rollback()
            raise ApplicationValidationError(str(exc)) from exc
        except Exception as exc:  # pragma: no cover - proteccion defensiva.
            self._unit_of_work.rollback()
            raise ApplicationDependencyError(
                "No fue posible actualizar la orden por una falla tecnica."
            ) from exc

    def _apply_transition(self, order: Order, command: UpdateOrderStatusCommand) -> None:
        """Mapea comando de aplicacion a metodos del agregado."""
        if command.target_status is OrderStatus.PENDING:
            raise ApplicationValidationError("No se permite regresar una orden a PENDING.")
        if command.target_status is OrderStatus.IN_PROGRESS:
            order.start_processing()
            return
        if command.target_status is OrderStatus.SHIPPED:
            order.mark_shipped()
            return
        if command.target_status is OrderStatus.COMPLETED:
            order.complete()
            return

        # Para CANCELLED, sin razon explicita se aplica la regla de pago fallido.
        if command.cancellation_reason is None:
            order.cancel_due_payment_failure()
            return

        cleaned_reason = command.cancellation_reason.strip()
        if not cleaned_reason:
            raise ApplicationValidationError("cancellation_reason no puede ser vacio.")
        order.cancel(cleaned_reason)


def _to_order_dto(order: Order) -> OrderDTO:
    """Mapea una orden de dominio a DTO de salida."""
    item_dtos = tuple(
        OrderItemDTO(
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            subtotal=item.subtotal,
        )
        for item in order.items
    )
    return OrderDTO(
        order_id=order.order_id,
        customer_id=order.customer.customer_id,
        customer_email=order.customer.email,
        branch_id=order.branch_id,
        status=order.status,
        cancellation_reason=order.cancellation_reason,
        items=item_dtos,
        shipping_cost=order.shipping_cost,
        tax_rate=order.tax_rate,
        subtotal=order.subtotal,
        tax_total=order.tax_total,
        total=order.total,
    )

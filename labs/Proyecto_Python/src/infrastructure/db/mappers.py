"""Mappers entre entidades ORM y entidades de dominio."""

from __future__ import annotations

from src.application.ports import InvoiceRecord
from src.domain.customers.entities import Customer
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.products.entities import Product

from .models import CustomerModel, InvoiceRecordModel, OrderItemModel, OrderModel, ProductModel


def to_customer_model(customer: Customer) -> CustomerModel:
    """Convierte entidad de dominio Customer a modelo ORM."""
    return CustomerModel(
        customer_id=customer.customer_id,
        full_name=customer.full_name,
        email=customer.email,
    )


def to_product_model(product: Product) -> ProductModel:
    """Convierte entidad de dominio Product a modelo ORM."""
    return ProductModel(
        product_id=product.product_id,
        sku=product.sku,
        name=product.name,
        unit_price=product.unit_price,
        is_active=product.is_active,
    )


def to_order_model(order: Order) -> OrderModel:
    """Convierte agregado Order a modelo ORM con sus lineas."""
    model = OrderModel(
        order_id=order.order_id,
        customer_id=order.customer.customer_id,
        branch_id=order.branch_id,
        shipping_cost=order.shipping_cost,
        tax_rate=order.tax_rate,
        status=order.status.value,
        cancellation_reason=order.cancellation_reason,
    )
    model.items = [
        OrderItemModel(
            order_id=order.order_id,
            line_number=index,
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
        )
        for index, item in enumerate(order.items, start=1)
    ]
    return model


def to_invoice_record_model(record: InvoiceRecord) -> InvoiceRecordModel:
    """Convierte registro de factura a modelo ORM."""
    return InvoiceRecordModel(
        order_id=record.order_id,
        external_invoice_id=record.external_invoice_id,
        total_amount=record.total_amount,
    )


def to_customer_domain(model: CustomerModel) -> Customer:
    """Convierte modelo ORM CustomerModel a dominio."""
    return Customer(
        customer_id=model.customer_id,
        full_name=model.full_name,
        email=model.email,
    )


def to_product_domain(model: ProductModel) -> Product:
    """Convierte modelo ORM ProductModel a dominio."""
    return Product(
        product_id=model.product_id,
        sku=model.sku,
        name=model.name,
        unit_price=model.unit_price,
        is_active=model.is_active,
    )


def to_order_domain(model: OrderModel) -> Order:
    """Convierte modelo ORM OrderModel a agregado de dominio."""
    customer_model = model.customer
    customer = to_customer_domain(customer_model)
    items = [
        OrderItem(
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
        )
        for item in model.items
    ]
    status = OrderStatus(model.status)
    return Order(
        order_id=model.order_id,
        customer=customer,
        branch_id=model.branch_id,
        items=items,
        shipping_cost=model.shipping_cost,
        tax_rate=model.tax_rate,
        status=status,
        cancellation_reason=model.cancellation_reason,
    )


def to_invoice_record_domain(model: InvoiceRecordModel) -> InvoiceRecord:
    """Convierte modelo ORM InvoiceRecordModel a DTO de aplicacion."""
    return InvoiceRecord(
        order_id=model.order_id,
        external_invoice_id=model.external_invoice_id,
        total_amount=model.total_amount,
    )

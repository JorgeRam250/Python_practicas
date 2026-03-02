(() => {
  "use strict";

  const STORAGE_KEY = "dc_ui_base_url";

  const state = {
    baseUrl: localStorage.getItem(STORAGE_KEY) || "http://127.0.0.1:8000",
    customers: [],
    products: [],
  };

  const elements = {
    statusBar: document.getElementById("status-bar"),
    baseUrlForm: document.getElementById("base-url-form"),
    baseUrlInput: document.getElementById("base-url-input"),
    tabButtons: [...document.querySelectorAll(".tab-btn")],
    panels: [...document.querySelectorAll(".panel")],

    ordersStatusFilter: document.getElementById("orders-status-filter"),
    ordersRefreshBtn: document.getElementById("orders-refresh-btn"),
    ordersTableBody: document.querySelector("#orders-table tbody"),
    orderDetailCard: document.getElementById("order-detail-card"),
    orderStatusForm: document.getElementById("order-status-form"),
    statusOrderId: document.getElementById("status-order-id"),
    statusTarget: document.getElementById("status-target"),
    statusReason: document.getElementById("status-reason"),

    customersRefreshBtn: document.getElementById("customers-refresh-btn"),
    customersApiNote: document.getElementById("customers-api-note"),
    customersTableBody: document.querySelector("#customers-table tbody"),
    createCustomerForm: document.getElementById("create-customer-form"),
    customerFullName: document.getElementById("customer-full-name"),
    customerEmail: document.getElementById("customer-email"),

    productsRefreshBtn: document.getElementById("products-refresh-btn"),
    productsApiNote: document.getElementById("products-api-note"),
    productsTableBody: document.querySelector("#products-table tbody"),
    createProductForm: document.getElementById("create-product-form"),
    productSku: document.getElementById("product-sku"),
    productName: document.getElementById("product-name"),
    productPrice: document.getElementById("product-price"),
    productActive: document.getElementById("product-active"),

    createOrderForm: document.getElementById("create-order-form"),
    orderCustomerSelect: document.getElementById("order-customer-select"),
    orderBranchId: document.getElementById("order-branch-id"),
    orderShippingCost: document.getElementById("order-shipping-cost"),
    orderTaxRate: document.getElementById("order-tax-rate"),
    addOrderItemBtn: document.getElementById("add-order-item-btn"),
    orderItemsContainer: document.getElementById("order-items-container"),
    orderItemTemplate: document.getElementById("order-item-template"),
    createOrderCustomersTableBody: document.querySelector("#create-order-customers-table tbody"),
    createOrderProductsTableBody: document.querySelector("#create-order-products-table tbody"),
  };

  function setStatus(message, isError = false) {
    elements.statusBar.textContent = message;
    elements.statusBar.style.color = isError ? "#a40d0d" : "#5d5548";
  }

  function setBaseUrl(newUrl) {
    state.baseUrl = newUrl.replace(/\/$/, "");
    localStorage.setItem(STORAGE_KEY, state.baseUrl);
    elements.baseUrlInput.value = state.baseUrl;
    setStatus(`Base URL actualizada: ${state.baseUrl}`);
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function getCustomerLabel(customer) {
    return `${customer.full_name} (${customer.email})`;
  }

  function getProductLabel(product) {
    return `${product.name} [${product.sku}] - $${product.unit_price}`;
  }

  function findCustomerById(customerId) {
    return state.customers.find((customer) => customer.customer_id === customerId) || null;
  }

  function populateCustomerSelect(selectedCustomerId = "") {
    const select = elements.orderCustomerSelect;
    const currentValue = selectedCustomerId || select.value;
    select.innerHTML = "";

    if (!state.customers.length) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "Sin clientes registrados";
      select.appendChild(option);
      select.disabled = true;
      return;
    }

    select.disabled = false;
    state.customers.forEach((customer) => {
      const option = document.createElement("option");
      option.value = customer.customer_id;
      option.textContent = getCustomerLabel(customer);
      select.appendChild(option);
    });

    if (currentValue && state.customers.some((customer) => customer.customer_id === currentValue)) {
      select.value = currentValue;
      return;
    }
    select.selectedIndex = 0;
  }

  function populateProductSelect(selectElement, selectedProductId = "") {
    const currentValue = selectedProductId || selectElement.value;
    selectElement.innerHTML = "";

    if (!state.products.length) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "Sin productos registrados";
      selectElement.appendChild(option);
      selectElement.disabled = true;
      return;
    }

    selectElement.disabled = false;
    state.products.forEach((product) => {
      const option = document.createElement("option");
      option.value = product.product_id;
      option.textContent = getProductLabel(product);
      selectElement.appendChild(option);
    });

    if (currentValue && state.products.some((product) => product.product_id === currentValue)) {
      selectElement.value = currentValue;
      return;
    }
    selectElement.selectedIndex = 0;
  }

  function refreshProductSelectors() {
    const selectors = elements.orderItemsContainer.querySelectorAll(".order-item-product-select");
    selectors.forEach((selectElement) => {
      populateProductSelect(selectElement);
    });
  }

  async function requestJson(path, options = {}) {
    const url = `${state.baseUrl}${path}`;
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
      },
      ...options,
    });

    let data = null;
    try {
      data = await response.json();
    } catch (_error) {
      data = null;
    }

    if (!response.ok) {
      const apiMessage = data && data.error && data.error.message ? data.error.message : response.statusText;
      const error = new Error(`HTTP ${response.status}: ${apiMessage}`);
      error.status = response.status;
      throw error;
    }

    return data;
  }

  function buildCell(content) {
    const td = document.createElement("td");
    td.textContent = content ?? "";
    return td;
  }

  function renderRows(tbody, rows) {
    tbody.innerHTML = "";
    if (!rows.length) {
      const tr = document.createElement("tr");
      tr.appendChild(buildCell("Sin resultados"));
      tbody.appendChild(tr);
      return;
    }
    rows.forEach((row) => tbody.appendChild(row));
  }

  function activatePanel(panelId) {
    elements.tabButtons.forEach((button) => {
      button.classList.toggle("is-active", button.dataset.view === panelId);
    });
    elements.panels.forEach((panel) => {
      panel.classList.toggle("is-active", panel.id === panelId);
    });
  }

  function createOrderItemRow(initial = {}) {
    const fragment = elements.orderItemTemplate.content.cloneNode(true);
    const row = fragment.querySelector(".order-item-row");
    const productSelect = row.querySelector(".order-item-product-select");
    const quantityInput = row.querySelector(".order-item-quantity");
    const removeBtn = row.querySelector(".remove-item-btn");

    populateProductSelect(productSelect, initial.product_id || "");
    quantityInput.value = initial.quantity || 1;

    removeBtn.addEventListener("click", () => {
      // Se impide eliminar todos los items para mantener payload valido.
      if (elements.orderItemsContainer.children.length <= 1) {
        setStatus("La orden requiere al menos un item.", true);
        return;
      }
      row.remove();
    });

    elements.orderItemsContainer.appendChild(row);
  }

  async function refreshOrders() {
    try {
      const statusValue = elements.ordersStatusFilter.value;
      const query = statusValue ? `?status=${encodeURIComponent(statusValue)}` : "";
      const data = await requestJson(`/orders${query}`);

      const rows = data.map((order) => {
        const customer = findCustomerById(order.customer_id);
        const customerDisplay = customer ? customer.full_name : order.customer_email;
        const tr = document.createElement("tr");
        tr.appendChild(buildCell(order.order_id));
        tr.appendChild(buildCell(customerDisplay));
        tr.appendChild(buildCell(order.status));
        tr.appendChild(buildCell(order.total));

        tr.addEventListener("click", async () => {
          elements.statusOrderId.value = order.order_id;
          await loadOrderDetail(order.order_id);
        });
        return tr;
      });

      renderRows(elements.ordersTableBody, rows);
      setStatus(`Orders cargadas: ${data.length}`);
    } catch (error) {
      setStatus(`Error al cargar orders: ${error.message}`, true);
    }
  }

  async function loadOrderDetail(orderId) {
    try {
      const order = await requestJson(`/orders/${orderId}`);
      const customer = findCustomerById(order.customer_id);
      const customerDisplay = customer
        ? `${customer.full_name} (${customer.email})`
        : order.customer_email;
      const renderedItems = order.items.length
        ? order.items
            .map(
              (item) =>
                `<li>${escapeHtml(item.product_name)} x${escapeHtml(item.quantity)} - ${escapeHtml(item.subtotal)}</li>`
            )
            .join("")
        : "<li>Sin items</li>";
      elements.orderDetailCard.innerHTML = `
        <h3>Detalle de orden</h3>
        <p><strong>Order ID:</strong> ${escapeHtml(order.order_id)}</p>
        <p><strong>Cliente:</strong> ${escapeHtml(customerDisplay)}</p>
        <p><strong>Status:</strong> ${escapeHtml(order.status)}</p>
        <p><strong>Total:</strong> ${escapeHtml(order.total)}</p>
        <p><strong>Branch:</strong> ${escapeHtml(order.branch_id)}</p>
        <p><strong>Items:</strong></p>
        <ul>${renderedItems}</ul>
      `;
      setStatus(`Detalle cargado para orden ${orderId}`);
    } catch (error) {
      setStatus(`No se pudo cargar detalle de orden: ${error.message}`, true);
    }
  }

  async function refreshCustomers() {
    elements.customersApiNote.textContent = "";
    try {
      const data = await requestJson("/customers");
      state.customers = data;
      populateCustomerSelect();
      const rows = data.map((customer) => {
        const tr = document.createElement("tr");
        tr.appendChild(buildCell(customer.customer_id));
        tr.appendChild(buildCell(customer.full_name));
        tr.appendChild(buildCell(customer.email));
        return tr;
      });
      renderRows(elements.customersTableBody, rows);
      const createOrderRows = data.map((customer) => {
        const tr = document.createElement("tr");
        tr.appendChild(buildCell(customer.customer_id));
        tr.appendChild(buildCell(customer.full_name));
        tr.appendChild(buildCell(customer.email));
        return tr;
      });
      renderRows(elements.createOrderCustomersTableBody, createOrderRows);
      setStatus(`Customers cargados: ${data.length}`);
    } catch (error) {
      if (error.status === 404 || error.status === 405) {
        elements.customersApiNote.textContent =
          "N/A: la API actual no expone GET /customers en esta version.";
        state.customers = [];
        populateCustomerSelect();
        renderRows(elements.customersTableBody, []);
        renderRows(elements.createOrderCustomersTableBody, []);
        setStatus("Customers list no disponible en contrato API actual.", true);
        return;
      }
      setStatus(`Error al cargar customers: ${error.message}`, true);
    }
  }

  async function createCustomer(event) {
    event.preventDefault();
    const payload = {
      full_name: elements.customerFullName.value.trim(),
      email: elements.customerEmail.value.trim(),
    };

    try {
      const data = await requestJson("/customers", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setStatus(`Cliente creado: ${data.customer_id}`);
      event.target.reset();
      await refreshCustomers();
    } catch (error) {
      setStatus(`Error al crear cliente: ${error.message}`, true);
    }
  }

  async function refreshProducts() {
    elements.productsApiNote.textContent = "";
    try {
      const data = await requestJson("/products");
      state.products = data;
      refreshProductSelectors();
      const rows = data.map((product) => {
        const tr = document.createElement("tr");
        tr.appendChild(buildCell(product.product_id));
        tr.appendChild(buildCell(product.sku));
        tr.appendChild(buildCell(product.name));
        tr.appendChild(buildCell(product.unit_price));
        tr.appendChild(buildCell(String(product.is_active)));
        return tr;
      });
      renderRows(elements.productsTableBody, rows);
      const createOrderRows = data.map((product) => {
        const tr = document.createElement("tr");
        tr.appendChild(buildCell(product.product_id));
        tr.appendChild(buildCell(product.sku));
        tr.appendChild(buildCell(product.name));
        tr.appendChild(buildCell(product.unit_price));
        tr.appendChild(buildCell(String(product.is_active)));
        return tr;
      });
      renderRows(elements.createOrderProductsTableBody, createOrderRows);
      setStatus(`Products cargados: ${data.length}`);
    } catch (error) {
      if (error.status === 404 || error.status === 405) {
        elements.productsApiNote.textContent =
          "N/A: la API actual no expone GET /products en esta version.";
        state.products = [];
        refreshProductSelectors();
        renderRows(elements.productsTableBody, []);
        renderRows(elements.createOrderProductsTableBody, []);
        setStatus("Products list no disponible en contrato API actual.", true);
        return;
      }
      setStatus(`Error al cargar products: ${error.message}`, true);
    }
  }

  async function createProduct(event) {
    event.preventDefault();
    const payload = {
      sku: elements.productSku.value.trim(),
      name: elements.productName.value.trim(),
      unit_price: elements.productPrice.value,
      is_active: elements.productActive.value === "true",
    };

    try {
      const data = await requestJson("/products", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setStatus(`Producto creado: ${data.product_id}`);
      event.target.reset();
      elements.productActive.value = "true";
      await refreshProducts();
    } catch (error) {
      setStatus(`Error al crear producto: ${error.message}`, true);
    }
  }

  function buildCreateOrderPayload() {
    const itemRows = [...elements.orderItemsContainer.querySelectorAll(".order-item-row")];

    const items = itemRows.map((row) => ({
      product_id: row.querySelector(".order-item-product-select").value,
      quantity: Number(row.querySelector(".order-item-quantity").value),
    }));

    return {
      customer_id: elements.orderCustomerSelect.value,
      branch_id: elements.orderBranchId.value.trim(),
      shipping_cost: elements.orderShippingCost.value,
      tax_rate: elements.orderTaxRate.value,
      items,
    };
  }

  async function createOrder(event) {
    event.preventDefault();
    try {
      if (!elements.orderCustomerSelect.value) {
        throw new Error("No hay clientes disponibles para crear la orden.");
      }
      const payload = buildCreateOrderPayload();
      if (!payload.items.length || payload.items.some((item) => !item.product_id)) {
        throw new Error("Debes seleccionar al menos un producto valido.");
      }
      const data = await requestJson("/orders", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      const customer = findCustomerById(data.customer_id);
      const customerLabel = customer ? customer.full_name : data.customer_email;
      setStatus(`Orden creada: ${data.order_id} para ${customerLabel}`);
      elements.statusOrderId.value = data.order_id;
      await refreshOrders();
      await loadOrderDetail(data.order_id);
    } catch (error) {
      setStatus(`Error al crear orden: ${error.message}`, true);
    }
  }

  async function updateOrderStatus(event) {
    event.preventDefault();
    const orderId = elements.statusOrderId.value.trim();
    const payload = {
      target_status: elements.statusTarget.value,
    };
    const reasonValue = elements.statusReason.value.trim();
    if (reasonValue) {
      payload.cancellation_reason = reasonValue;
    }

    try {
      const data = await requestJson(`/orders/${orderId}/status`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      });
      setStatus(`Status actualizado: ${data.status}`);
      await refreshOrders();
      await loadOrderDetail(orderId);
    } catch (error) {
      setStatus(`Error al actualizar status: ${error.message}`, true);
    }
  }

  function bindEvents() {
    elements.baseUrlForm.addEventListener("submit", (event) => {
      event.preventDefault();
      setBaseUrl(elements.baseUrlInput.value.trim());
    });

    elements.tabButtons.forEach((button) => {
      button.addEventListener("click", () => activatePanel(button.dataset.view));
    });

    elements.ordersRefreshBtn.addEventListener("click", refreshOrders);
    elements.ordersStatusFilter.addEventListener("change", refreshOrders);
    elements.customersRefreshBtn.addEventListener("click", refreshCustomers);
    elements.productsRefreshBtn.addEventListener("click", refreshProducts);

    // Comentario para junior: la API actual solo soporta alta/listado de clientes, no edicion.
    elements.createCustomerForm.addEventListener("submit", createCustomer);
    elements.createProductForm.addEventListener("submit", createProduct);
    elements.createOrderForm.addEventListener("submit", createOrder);
    elements.orderStatusForm.addEventListener("submit", updateOrderStatus);

    elements.addOrderItemBtn.addEventListener("click", () => createOrderItemRow());
  }

  async function bootstrap() {
    setBaseUrl(state.baseUrl);
    bindEvents();

    // Se inicia con un item para no dejar la forma vacia.
    createOrderItemRow();

    await refreshCustomers();
    await refreshProducts();
    await refreshOrders();
  }

  bootstrap().catch((error) => {
    setStatus(`Fallo inicial de UI: ${error.message}`, true);
  });
})();

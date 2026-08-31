initNav("productos");

let productosCache = [];
let filtroActual = "todo";

async function cargarProductos() {
  const tbody = document.getElementById("tabla-productos");
  try {
    productosCache = await api("/products");
    const stockBajo = await api("/products/stock-bajo");
    const idsStockBajo = new Set(stockBajo.map((p) => p.id));

    document.getElementById("kpi-total-productos").textContent = productosCache.length;
    document.getElementById("kpi-stock-critico").textContent = stockBajo.length;
    document.getElementById("kpi-categorias").textContent = new Set(productosCache.map((p) => p.categoria)).size;

    renderTabla(idsStockBajo);
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty-state">${err.message}</td></tr>`;
  }
}

function renderTabla(idsStockBajo) {
  const tbody = document.getElementById("tabla-productos");
  let lista = productosCache;
  if (filtroActual === "bajo") lista = lista.filter((p) => idsStockBajo.has(p.id));

  if (!lista.length) {
    tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No hay productos para mostrar.</td></tr>';
    return;
  }

  tbody.innerHTML = lista
    .map((p) => {
      const critico = idsStockBajo.has(p.id);
      return `
      <tr>
        <td>${p.nombre}</td>
        <td>${p.sku}</td>
        <td>${p.categoria}</td>
        <td>${formatoQ(p.precio)}</td>
        <td class="${critico ? "text-danger" : ""}">${p.stock_actual} und.</td>
        <td>${p.lead_time_dias_china} días</td>
        <td>${critico ? '<span class="badge badge-critico">Stock bajo</span>' : '<span class="badge badge-ok">Estable</span>'}</td>
      </tr>`;
    })
    .join("");
}

document.querySelectorAll(".filtro-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filtro-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    filtroActual = btn.dataset.filtro;
    cargarProductos();
  });
});

document.getElementById("btn-recibir-stock").addEventListener("click", () => {
  const select = document.getElementById("stock-producto");
  select.innerHTML = productosCache.map((p) => `<option value="${p.id}">${p.nombre} (stock: ${p.stock_actual})</option>`).join("");
  document.getElementById("modal-stock").hidden = false;
});
document.getElementById("cerrar-modal-stock").addEventListener("click", () => {
  document.getElementById("modal-stock").hidden = true;
});

document.getElementById("form-stock").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorEl = document.getElementById("stock-error");
  errorEl.hidden = true;
  try {
    await api("/inventory/receive", {
      method: "POST",
      body: JSON.stringify({
        product_id: Number(document.getElementById("stock-producto").value),
        cantidad: Number(document.getElementById("stock-cantidad").value),
        nota: document.getElementById("stock-nota").value,
      }),
    });
    document.getElementById("modal-stock").hidden = true;
    document.getElementById("form-stock").reset();
    await cargarProductos();
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  }
});

const btnNuevoProducto = document.getElementById("btn-nuevo-producto");
if (btnNuevoProducto) {
  btnNuevoProducto.addEventListener("click", () => {
    document.getElementById("modal-producto").hidden = false;
  });
}
document.getElementById("cerrar-modal-producto").addEventListener("click", () => {
  document.getElementById("modal-producto").hidden = true;
});

document.getElementById("form-producto").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorEl = document.getElementById("producto-error");
  errorEl.hidden = true;
  try {
    await api("/products", {
      method: "POST",
      body: JSON.stringify({
        nombre: document.getElementById("prod-nombre").value,
        sku: document.getElementById("prod-sku").value,
        categoria: document.getElementById("prod-categoria").value,
        precio: Number(document.getElementById("prod-precio").value),
        costo: Number(document.getElementById("prod-costo").value),
        stock_actual: Number(document.getElementById("prod-stock").value),
        stock_minimo: Number(document.getElementById("prod-stock-minimo").value),
        lead_time_dias_china: Number(document.getElementById("prod-lead-time").value),
      }),
    });
    document.getElementById("modal-producto").hidden = true;
    document.getElementById("form-producto").reset();
    await cargarProductos();
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  }
});

cargarProductos();

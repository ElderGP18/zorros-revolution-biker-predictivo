initNav("ventas");

let productosCache = [];

async function cargarProductos() {
  productosCache = await api("/products");
}

function filaItem() {
  const opciones = productosCache
    .map(
      (p) =>
        `<option value="${escapeHtml(p.id)}">${escapeHtml(p.nombre)} (Q${p.precio.toFixed(2)}) — stock: ${escapeHtml(p.stock_actual)}</option>`
    )
    .join("");
  return `
    <div class="item-venta">
      <select class="item-producto">${opciones}</select>
      <input type="number" class="item-cantidad" min="1" value="1" />
      <button type="button" class="btn-icon quitar-item">✕</button>
    </div>`;
}

function agregarItem() {
  document.getElementById("items-venta").insertAdjacentHTML("beforeend", filaItem());
}

document.getElementById("btn-agregar-item").addEventListener("click", agregarItem);

document.getElementById("items-venta").addEventListener("click", (e) => {
  if (e.target.classList.contains("quitar-item")) {
    e.target.closest(".item-venta").remove();
  }
});

document.getElementById("btn-nueva-venta").addEventListener("click", async () => {
  document.getElementById("items-venta").innerHTML = "";
  if (!productosCache.length) await cargarProductos();
  agregarItem();
  document.getElementById("modal-venta").hidden = false;
});

document.getElementById("btn-cerrar-modal").addEventListener("click", () => {
  document.getElementById("modal-venta").hidden = true;
});

document.getElementById("form-venta").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorEl = document.getElementById("venta-error");
  errorEl.hidden = true;

  const items = Array.from(document.querySelectorAll(".item-venta")).map((fila) => ({
    product_id: Number(fila.querySelector(".item-producto").value),
    cantidad: Number(fila.querySelector(".item-cantidad").value),
  }));

  if (!items.length) {
    errorEl.textContent = "Agrega al menos un producto.";
    errorEl.hidden = false;
    return;
  }

  try {
    await api("/sales", {
      method: "POST",
      body: JSON.stringify({
        metodo_pago: document.getElementById("metodo-pago").value,
        canal: "Tienda",
        items,
      }),
    });
    document.getElementById("modal-venta").hidden = true;
    await cargarVentas();
    await cargarProductos();
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  }
});

async function cargarVentas() {
  const tbody = document.getElementById("tabla-ventas");
  try {
    const ventas = await api("/sales?limit=100");
    if (!ventas.length) {
      tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Aún no hay ventas registradas.</td></tr>';
      return;
    }
    tbody.innerHTML = ventas
      .map(
        (v) => `
        <tr>
          <td>#${escapeHtml(v.id)}</td>
          <td>${escapeHtml(new Date(v.fecha_hora).toLocaleString("es-GT"))}</td>
          <td>${escapeHtml(v.cajero_nombre)}</td>
          <td>${v.items.map((i) => `${escapeHtml(i.cantidad)}× ${escapeHtml(i.producto_nombre)}`).join(", ")}</td>
          <td>${formatoQ(v.total)}</td>
          <td>${escapeHtml(v.metodo_pago)}</td>
        </tr>`
      )
      .join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state">${escapeHtml(err.message)}</td></tr>`;
  }
}

cargarProductos();
cargarVentas();

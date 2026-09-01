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
      <select class="item-producto" aria-label="Producto">${opciones}</select>
      <input type="number" class="item-cantidad" min="1" value="1" aria-label="Cantidad" />
      <button type="button" class="btn-icon quitar-item" aria-label="Quitar producto">${iconSvg("trash")}</button>
    </div>`;
}

function agregarItem() {
  document.getElementById("items-venta").insertAdjacentHTML("beforeend", filaItem());
}

document.getElementById("btn-agregar-item").addEventListener("click", agregarItem);

document.getElementById("items-venta").addEventListener("click", (e) => {
  const boton = e.target.closest(".quitar-item");
  if (boton) boton.closest(".item-venta").remove();
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
  const boton = document.getElementById("btn-registrar-venta");
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

  setButtonLoading(boton, true, "Registrando venta");
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
    showToast("Venta registrada correctamente.");
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  } finally {
    setButtonLoading(boton, false);
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
          <td data-label="Número">#${escapeHtml(v.id)}</td>
          <td data-label="Fecha">${escapeHtml(new Date(v.fecha_hora).toLocaleString("es-GT"))}</td>
          <td data-label="Cajero">${escapeHtml(v.cajero_nombre)}</td>
          <td data-label="Productos">${v.items.map((i) => `${escapeHtml(i.cantidad)}× ${escapeHtml(i.producto_nombre)}`).join(", ")}</td>
          <td data-label="Total">${formatoQ(v.total)}</td>
          <td data-label="Pago">${escapeHtml(v.metodo_pago)}</td>
        </tr>`
      )
      .join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state">${escapeHtml(err.message)}</td></tr>`;
  } finally {
    tbody.setAttribute("aria-busy", "false");
  }
}

cargarProductos();
cargarVentas();

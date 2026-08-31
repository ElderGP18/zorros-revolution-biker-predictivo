initNav("predicciones");

if (getRol() !== "admin") {
  window.location.href = "/dashboard.html";
}

let chartInstancia = null;

const EVENTOS_GT = [
  { nombre: "Caravana del Zorro", mes: 2, dia: 14 },
  { nombre: "Bono 14", mes: 7, dia: 1 },
  { nombre: "Diciembre / Aguinaldo", mes: 12, dia: 1 },
];

function proximoEvento() {
  const hoy = new Date();
  let mejor = null;
  for (const ev of EVENTOS_GT) {
    let fecha = new Date(hoy.getFullYear(), ev.mes - 1, ev.dia);
    if (fecha < hoy) fecha = new Date(hoy.getFullYear() + 1, ev.mes - 1, ev.dia);
    const dias = Math.ceil((fecha - hoy) / (1000 * 60 * 60 * 24));
    if (!mejor || dias < mejor.dias) mejor = { nombre: ev.nombre, dias };
  }
  return mejor;
}

async function cargarPronostico() {
  const horizonte = document.getElementById("horizonte").value;
  try {
    const puntos = await api(`/predictions/forecast?horizonte=${horizonte}`);
    const labels = puntos.map((p) => p.fecha);
    const real = puntos.map((p) => p.real);
    const pronostico = puntos.map((p) => p.pronostico);

    const total = puntos.reduce((acc, p) => acc + (p.pronostico || 0), 0);
    document.getElementById("kpi-volumen-proyectado").textContent = formatoQ(total);

    if (chartInstancia) chartInstancia.destroy();
    chartInstancia = new Chart(document.getElementById("chart-pronostico"), {
      type: "line",
      data: {
        labels,
        datasets: [
          { label: "Histórico (Real)", data: real, borderColor: "#e11d2e", backgroundColor: "rgba(225,29,46,0.12)", spanGaps: true, tension: 0.25 },
          { label: "Predicción IA", data: pronostico, borderColor: "#f2b705", borderDash: [6, 4], spanGaps: true, tension: 0.25 },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: "#c9ced8" } } },
        scales: {
          x: { ticks: { color: "#8b93a7", maxTicksLimit: 12 }, grid: { color: "rgba(255,255,255,0.05)" } },
          y: { ticks: { color: "#8b93a7" }, grid: { color: "rgba(255,255,255,0.05)" } },
        },
      },
    });
  } catch (err) {
    console.error(err);
  }
}

async function cargarSenales() {
  const contenedor = document.getElementById("lista-senales");
  try {
    const senales = await api("/predictions/signals");
    if (!senales.length) {
      contenedor.innerHTML = '<p class="empty-state">Sin variaciones relevantes esta semana.</p>';
      return;
    }
    contenedor.innerHTML = senales
      .map(
        (s) => `
      <div class="reco-item">
        <span class="badge ${s.tendencia === "alta_demanda" ? "badge-alta" : "badge-baja"}">
          ${s.tendencia === "alta_demanda" ? "ALTA DEMANDA" : "BAJA DEMANDA"}
        </span>
        <strong>${s.nombre}</strong>
        <p>Categoría: ${s.categoria}</p>
        <span>${s.magnitud_pct > 0 ? "+" : ""}${s.magnitud_pct}% vs. periodo anterior</span>
      </div>`
      )
      .join("");
  } catch (err) {
    contenedor.innerHTML = `<p class="empty-state">${err.message}</p>`;
  }
}

async function cargarRecomendaciones() {
  const contenedor = document.getElementById("lista-recos");
  try {
    const recos = await api("/predictions/recommendations");
    if (!recos.length) {
      contenedor.innerHTML = '<p class="empty-state">No hay alertas de reabastecimiento.</p>';
      return;
    }
    contenedor.innerHTML = recos
      .map(
        (r) => `
      <div class="reco-item reco-${r.urgencia}">
        <strong>${r.nombre} <small>(${r.sku})</small></strong>
        <p>${r.mensaje}</p>
        <span>Stock actual: ${r.stock_actual} · Sugerido: ${r.cantidad_sugerida} und. · Lead time: ${r.lead_time_dias_china} días</span>
      </div>`
      )
      .join("");
  } catch (err) {
    contenedor.innerHTML = `<p class="empty-state">${err.message}</p>`;
  }
}

function mostrarProximoEvento() {
  const ev = proximoEvento();
  document.getElementById("kpi-proximo-evento").textContent = `${ev.nombre} (${ev.dias} días)`;
}

document.getElementById("btn-recalibrar").addEventListener("click", async () => {
  const boton = document.getElementById("btn-recalibrar");
  boton.disabled = true;
  boton.textContent = "Entrenando…";
  try {
    const resultado = await api("/predictions/retrain", { method: "POST" });
    document.getElementById("kpi-ultimo-modelo").textContent = resultado.algoritmo;
    document.getElementById("kpi-metricas").textContent =
      `MASE: ${resultado.mase} · WAPE: ${resultado.wape}% · Mejora vs. base: ${resultado.mejora_vs_baseline_pct}%`;
    await cargarPronostico();
    await cargarRecomendaciones();
  } catch (err) {
    alert("No se pudo recalibrar: " + err.message);
  } finally {
    boton.disabled = false;
    boton.textContent = "⟳ Recalibrar Modelo";
  }
});

document.getElementById("horizonte").addEventListener("change", cargarPronostico);

cargarPronostico();
cargarSenales();
cargarRecomendaciones();
mostrarProximoEvento();

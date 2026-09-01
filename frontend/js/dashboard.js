initNav("dashboard");

async function cargarResumen() {
  try {
    const data = await api("/dashboard/summary");
    document.getElementById("kpi-ventas-dia").textContent = formatoQ(data.ventas_dia);
    document.getElementById("kpi-ventas-mes").textContent = formatoQ(data.ventas_mes);

    const variacion = data.variacion_mes_pct;
    const variacionEl = document.getElementById("kpi-variacion-mes");
    variacionEl.textContent = `${variacion >= 0 ? "+" : ""}${variacion}% vs mes anterior`;
    variacionEl.className = "kpi-delta " + (variacion >= 0 ? "delta-up" : "delta-down");

    document.getElementById("kpi-cantidad-ventas").textContent = data.cantidad_ventas_mes;
    document.getElementById("kpi-ticket").textContent = formatoQ(data.ticket_promedio);
    document.getElementById("kpi-productos-vendidos").textContent = data.productos_vendidos_mes;
    document.getElementById("kpi-stock-bajo").textContent = data.stock_critico;
    document.getElementById("kpi-proyeccion").textContent = formatoQ(data.proyeccion_proximo_mes);
    document.getElementById("kpi-confianza").textContent =
      data.confianza_modelo != null ? `Confianza del modelo: ${data.confianza_modelo}%` : "Modelo aún no entrenado";
  } catch (err) {
    console.error(err);
  }
}

async function cargarTendencia() {
  try {
    const puntos = await api("/dashboard/trend?meses=12");
    const labels = puntos.map((p) => p.fecha);
    const real = puntos.map((p) => p.real);
    const proyectado = puntos.map((p) => p.proyectado);

    new Chart(document.getElementById("chart-tendencia"), {
      type: "line",
      data: {
        labels,
        datasets: [
          { label: "Real", data: real, borderColor: "#e11d2e", backgroundColor: "rgba(225,29,46,0.15)", spanGaps: true, tension: 0.3 },
          { label: "Proyectado", data: proyectado, borderColor: "#8b93a7", borderDash: [6, 4], spanGaps: true, tension: 0.3 },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: "#c9ced8" } } },
        scales: {
          x: { ticks: { color: "#8b93a7" }, grid: { color: "rgba(255,255,255,0.05)" } },
          y: { ticks: { color: "#8b93a7" }, grid: { color: "rgba(255,255,255,0.05)" } },
        },
      },
    });
  } catch (err) {
    console.error(err);
  }
}

async function cargarRecomendaciones() {
  const contenedor = document.getElementById("lista-recomendaciones");
  if (getRol() !== "admin") {
    contenedor.innerHTML = '<p class="empty-state">Disponible solo para administradores.</p>';
    return;
  }
  try {
    const recos = await api("/predictions/recommendations");
    if (!recos.length) {
      contenedor.innerHTML = '<p class="empty-state">Sin alertas de reabastecimiento por ahora.</p>';
      return;
    }
    contenedor.innerHTML = recos
      .slice(0, 6)
      .map(
        (r) => `
        <div class="reco-item reco-${escapeHtml(r.urgencia)}">
          <strong>${escapeHtml(r.nombre)}</strong>
          <p>${escapeHtml(r.mensaje)}</p>
          <span>Sugerido: ${escapeHtml(r.cantidad_sugerida)} unidades · Lead time China: ${escapeHtml(r.lead_time_dias_china)} días</span>
        </div>`
      )
      .join("");
  } catch (err) {
    contenedor.innerHTML = `<p class="empty-state">${escapeHtml(err.message)}</p>`;
  }
}

cargarResumen();
cargarTendencia();
cargarRecomendaciones();

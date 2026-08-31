const API_BASE = ""; // mismo origen: FastAPI sirve tanto la API como este frontend

function getToken() {
  return localStorage.getItem("zorros_token");
}

function getRol() {
  return localStorage.getItem("zorros_rol");
}

function getNombre() {
  return localStorage.getItem("zorros_nombre");
}

function setSession(token, rol, nombre) {
  localStorage.setItem("zorros_token", token);
  localStorage.setItem("zorros_rol", rol);
  localStorage.setItem("zorros_nombre", nombre);
}

function clearSession() {
  localStorage.removeItem("zorros_token");
  localStorage.removeItem("zorros_rol");
  localStorage.removeItem("zorros_nombre");
}

async function api(path, options = {}) {
  const headers = options.headers || {};
  headers["Content-Type"] = "application/json";
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const response = await fetch(API_BASE + path, { ...options, headers });

  if (response.status === 401) {
    clearSession();
    window.location.href = "/index.html";
    throw new Error("Sesión expirada");
  }

  if (!response.ok) {
    let detail = "Ocurrió un error";
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch (e) {
      /* respuesta sin cuerpo JSON */
    }
    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
}

function requireAuth() {
  const token = getToken();
  if (!token) {
    window.location.href = "/index.html";
  }
}

function formatoQ(valor) {
  const num = Number(valor || 0);
  return "Q " + num.toLocaleString("es-GT", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function initNav(paginaActual) {
  requireAuth();
  const rol = getRol();

  document.querySelectorAll("[data-nav]").forEach((el) => {
    if (el.dataset.nav === paginaActual) el.classList.add("active");
    else el.classList.remove("active");
  });

  document.querySelectorAll("[data-roles]").forEach((el) => {
    const roles = el.dataset.roles.split(",");
    if (!roles.includes(rol)) el.style.display = "none";
  });

  const nombreEl = document.getElementById("nombre-usuario");
  if (nombreEl) nombreEl.textContent = getNombre() || "";

  const rolEl = document.getElementById("rol-usuario");
  if (rolEl) rolEl.textContent = rol === "admin" ? "Administrador" : "Cajero";

  const logoutBtn = document.getElementById("btn-logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      clearSession();
      window.location.href = "/index.html";
    });
  }
}

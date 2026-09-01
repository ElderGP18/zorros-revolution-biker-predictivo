from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Auth ----------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    nombre: str


class UserOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str = "cajero"


# ---------- Productos ----------
class ProductBase(BaseModel):
    sku: str
    nombre: str
    categoria: str
    precio: float
    costo: float = 0
    stock_minimo: int = 5
    lead_time_dias_china: int = 60


class ProductCreate(ProductBase):
    stock_actual: int = 0


class ProductUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    precio: Optional[float] = None
    costo: Optional[float] = None
    stock_minimo: Optional[int] = None
    lead_time_dias_china: Optional[int] = None
    activo: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    stock_actual: int
    activo: bool

    class Config:
        from_attributes = True


# ---------- Ventas ----------
class SaleItemCreate(BaseModel):
    product_id: int
    cantidad: int = Field(gt=0)


class SaleCreate(BaseModel):
    canal: str = "Tienda"
    metodo_pago: str = "Efectivo"
    items: List[SaleItemCreate]


class SaleItemOut(BaseModel):
    product_id: int
    producto_nombre: str
    cantidad: int
    precio_unitario: float


class SaleOut(BaseModel):
    id: int
    fecha_hora: datetime
    cajero_nombre: str
    canal: str
    total: float
    metodo_pago: str
    items: List[SaleItemOut]


# ---------- Inventario ----------
class StockReceiveRequest(BaseModel):
    product_id: int
    cantidad: int = Field(gt=0)
    nota: Optional[str] = None


class StockAdjustRequest(BaseModel):
    product_id: int
    cantidad: int
    nota: Optional[str] = None


class PurchaseOrderOut(BaseModel):
    id: int
    product_id: int
    producto_nombre: str
    cantidad: int
    fecha_pedido: datetime
    fecha_estimada_llegada: Optional[datetime]
    estado: str
    origen: str


# ---------- Dashboard ----------
class DashboardSummary(BaseModel):
    ventas_dia: float
    ventas_mes: float
    variacion_mes_pct: float
    cantidad_ventas_mes: int
    ticket_promedio: float
    productos_vendidos_mes: int
    stock_critico: int
    proyeccion_proximo_mes: float
    confianza_modelo: Optional[float]


class TrendPoint(BaseModel):
    fecha: str
    real: Optional[float] = None
    proyectado: Optional[float] = None


# ---------- Predicciones ----------
class ForecastPoint(BaseModel):
    fecha: str
    real: Optional[float] = None
    pronostico: Optional[float] = None
    intervalo_inf: Optional[float] = None
    intervalo_sup: Optional[float] = None


class ProductSignal(BaseModel):
    product_id: int
    nombre: str
    categoria: str
    tendencia: str  # "alta_demanda" | "baja_demanda"
    magnitud_pct: float


class RecommendationOut(BaseModel):
    product_id: int
    nombre: str
    sku: str
    stock_actual: int
    punto_reorden: float
    demanda_diaria_pronosticada: float
    lead_time_dias_china: int
    cantidad_sugerida: int
    urgencia: str  # "critico" | "atencion" | "ok"
    mensaje: str


class RetrainResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_run_id: int
    algoritmo: str
    version: str
    mase: Optional[float]
    wape: Optional[float]
    mejora_vs_baseline_pct: Optional[float]


# ---------- Perfilamiento de series ----------
class SeriesProfileOut(BaseModel):
    product_id: int
    sku: str
    nombre: str
    categoria: str
    dias_historial: int
    unidades_totales: float
    media_diaria: float
    proporcion_ceros: float
    adi: float  # Average Demand Interval: días por cada día con demanda
    cv2: float  # Coeficiente de variación al cuadrado de las cantidades positivas
    clasificacion: str  # "regular" | "erratica" | "intermitente" | "grumosa"
    estrategia_sugerida: str


class SeriesProfileSummary(BaseModel):
    productos_con_ventas: int
    regular: int
    erratica: int
    intermitente: int
    grumosa: int
    pct_series_intermitentes: float
    pct_volumen_modelable_directo: float


class SeriesProfileResponse(BaseModel):
    resumen: SeriesProfileSummary
    series: List[SeriesProfileOut]

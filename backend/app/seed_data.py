"""Genera datos de demostración: usuarios, catálogo de motoaccesorios y ~24 meses
de ventas sintéticas con estacionalidad de Guatemala (diciembre, Bono 14 en julio,
Caravana del Zorro en febrero), para que el dashboard y las predicciones muestren
resultados reales desde el primer arranque.

Uso:
    python -m app.seed_data
"""
import random
import secrets
import string
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import models
from .database import Base, SessionLocal, engine
from .ml import calendar_features as cf
from .security import hash_password

# sku, nombre, categoria, precio, costo, stock_actual, lead_time_dias_china
CATALOGO = [
    ("CAS-XR700", "Casco Integral XR-700 Matte Black", "Protección", 850.0, 520.0, 45, 60),
    ("CAS-AGV-PISTA", "Casco AGV Pista", "Protección", 3200.0, 2100.0, 25, 75),
    ("CAS-ABIERTO-01", "Casco Abierto Urbano", "Protección", 420.0, 260.0, 60, 55),
    ("CHQ-VMAX-PRO", "Chaqueta Armadura V-Max Pro", "Indumentaria", 980.0, 610.0, 40, 65),
    ("CHQ-CUERO-CL", "Chaqueta de Cuero Clásica", "Indumentaria", 1150.0, 700.0, 30, 70),
    ("CHQ-LLUVIA", "Chaqueta Impermeable de Lluvia", "Indumentaria", 350.0, 190.0, 55, 50),
    ("GTE-ALPINE", "Guantes Alpinestars", "Indumentaria", 320.0, 180.0, 70, 45),
    ("GTE-INVIERNO", "Guantes de Invierno Térmicos", "Indumentaria", 280.0, 150.0, 50, 45),
    ("FRE-BREMBO", "Pastillas de Freno Brembo", "Consumibles", 380.0, 210.0, 90, 40),
    ("FRE-ORG", "Pastillas de Freno Orgánicas", "Consumibles", 190.0, 95.0, 100, 40),
    ("LLA-LLUVIA", "Llanta para Lluvia 120/70", "Consumibles", 750.0, 460.0, 35, 55),
    ("LLA-DEPORTIVA", "Llanta Deportiva 180/55", "Consumibles", 1450.0, 950.0, 20, 60),
    ("ACC-CANDADO", "Candado de Disco Antirrobo", "Accesorios", 210.0, 110.0, 80, 35),
    ("ACC-MALETA", "Maleta Lateral Rígida", "Accesorios", 1650.0, 1050.0, 15, 70),
    ("ACC-PARABRISAS", "Parabrisas Deportivo Ahumado", "Accesorios", 480.0, 290.0, 25, 60),
    ("ACC-ESPEJOS", "Espejos Retrovisores CNC", "Accesorios", 260.0, 140.0, 60, 40),
    ("ACC-LUCES-LED", "Kit de Luces LED", "Accesorios", 390.0, 210.0, 50, 45),
    ("ACC-COVER", "Funda Cobertora para Moto", "Accesorios", 220.0, 120.0, 65, 35),
    ("BOT-RACING", "Botas Racing Reforzadas", "Indumentaria", 890.0, 540.0, 30, 65),
    ("BOT-URBANA", "Botas Urbanas Casual Biker", "Indumentaria", 540.0, 320.0, 40, 55),
    ("ACC-BAUL", "Baúl Trasero 45L", "Accesorios", 720.0, 430.0, 20, 65),
    ("ACC-PORTA", "Portaequipaje Trasero", "Accesorios", 310.0, 170.0, 35, 40),
    ("CAS-VISOR", "Visera de Repuesto para Casco", "Protección", 150.0, 70.0, 90, 30),
    ("GTE-VERANO", "Guantes de Verano Ventilados", "Indumentaria", 190.0, 95.0, 60, 40),
    ("FRE-DISCO", "Disco de Freno Flotante", "Consumibles", 620.0, 380.0, 25, 55),
]

USUARIOS_DEMO = [
    {"nombre": "Administrador Principal", "email": "admin@zorrosrevolution.com", "rol": "admin"},
    {"nombre": "Cajero de Turno", "email": "cajero@zorrosrevolution.com", "rol": "cajero"},
]

MESES_HISTORIAL = 24


def _password_aleatoria(longitud: int = 16) -> str:
    """Contraseña fuerte que cumple la política, generada al azar.

    Antes las contraseñas estaban escritas en este archivo y publicadas en el
    README, de modo que cualquiera que viera el repositorio podía entrar a una
    instancia desplegada. Ahora se generan una sola vez, se imprimen y solo
    queda su hash en la base: no viven ni en el código ni en el .env.
    """
    alfabeto = string.ascii_letters + string.digits
    while True:
        clave = "".join(secrets.choice(alfabeto) for _ in range(longitud))
        if any(c.isalpha() for c in clave) and any(c.isdigit() for c in clave):
            return clave


def _crear_usuarios(db: Session) -> dict:
    """Crea los usuarios que falten y devuelve las contraseñas generadas."""
    generadas = {}
    for u in USUARIOS_DEMO:
        if db.query(models.User).filter(models.User.email == u["email"]).first():
            continue
        clave = _password_aleatoria()
        generadas[u["email"]] = clave
        db.add(
            models.User(
                nombre=u["nombre"],
                email=u["email"],
                password_hash=hash_password(clave),
                rol=models.RolUsuario(u["rol"]),
            )
        )
    db.commit()
    return generadas


def _crear_catalogo(db: Session):
    productos = []
    for sku, nombre, categoria, precio, costo, stock, lead_time in CATALOGO:
        producto = db.query(models.Product).filter(models.Product.sku == sku).first()
        if not producto:
            producto = models.Product(
                sku=sku,
                nombre=nombre,
                categoria=categoria,
                precio=precio,
                costo=costo,
                stock_actual=stock,
                stock_minimo=max(8, int(stock * 0.15)),
                lead_time_dias_china=lead_time,
            )
            db.add(producto)
        productos.append(producto)
    db.commit()
    for p in productos:
        db.refresh(p)
    return productos


def _factor_estacional(fecha) -> float:
    factor = 1.0
    if cf.es_temporada_diciembre(fecha):
        factor *= 1.9 if fecha.day >= 10 else 1.4
    if cf.es_semana_bono14(fecha):
        factor *= 1.6
    if cf.es_caravana_del_zorro(fecha):
        factor *= 1.7
    if fecha.weekday() >= 5:
        factor *= 1.25
    return factor


def _generar_ventas(db: Session, productos, admin_id: int, cajero_id: int):
    """Genera un histórico sintético de ventas. No afecta stock_actual: representa
    demanda histórica de entrenamiento, independiente del inventario físico actual."""
    if db.query(models.Sale).first():
        return  # ya existen ventas, no duplicar

    random.seed(42)
    hoy = datetime.utcnow().date()
    inicio = hoy - timedelta(days=MESES_HISTORIAL * 30)

    popularidad = {p.id: random.uniform(0.4, 1.6) for p in productos}
    dia_actual = inicio
    ventas_creadas = 0
    total_dias = max((hoy - inicio).days, 1)

    while dia_actual <= hoy:
        factor = _factor_estacional(dia_actual)
        progreso = (dia_actual - inicio).days / total_dias
        tendencia = 1 + progreso * 0.3  # leve crecimiento a lo largo del histórico
        num_ventas_dia = max(0, int(random.gauss(6 * factor * tendencia, 2)))

        for _ in range(num_ventas_dia):
            n_items = random.choice([1, 1, 1, 2, 2, 3])
            productos_venta = random.sample(productos, k=min(n_items, len(productos)))
            hora = random.randint(9, 19)
            fecha_hora = datetime(dia_actual.year, dia_actual.month, dia_actual.day, hora, random.randint(0, 59))
            cajero_id_venta = cajero_id if random.random() < 0.8 else admin_id

            venta = models.Sale(
                fecha_hora=fecha_hora,
                cajero_id=cajero_id_venta,
                canal=random.choice(["Tienda", "Tienda", "Tienda", "En línea"]),
                metodo_pago=random.choice(["Efectivo", "Tarjeta", "Transferencia", "Crédito"]),
                total=0,
            )
            db.add(venta)
            db.flush()

            total_venta = 0.0
            for producto in productos_venta:
                peso = popularidad[producto.id]
                if random.random() > (0.5 * peso):
                    continue
                cantidad = 1 if random.random() < 0.85 else 2
                subtotal = producto.precio * cantidad
                total_venta += subtotal
                db.add(
                    models.SaleItem(
                        sale_id=venta.id,
                        product_id=producto.id,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                    )
                )

            if total_venta == 0:
                producto = random.choice(productos_venta)
                db.add(models.SaleItem(sale_id=venta.id, product_id=producto.id, cantidad=1, precio_unitario=producto.precio))
                total_venta = producto.precio

            venta.total = round(total_venta, 2)
            ventas_creadas += 1

        if ventas_creadas and ventas_creadas % 400 == 0:
            db.commit()

        dia_actual += timedelta(days=1)

    db.commit()
    print(f"Se generaron {ventas_creadas} ventas sintéticas ({MESES_HISTORIAL} meses de historial).")


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        generadas = _crear_usuarios(db)
        productos = _crear_catalogo(db)
        admin = db.query(models.User).filter(models.User.rol == models.RolUsuario.admin).first()
        cajero = db.query(models.User).filter(models.User.rol == models.RolUsuario.cajero).first()
        _generar_ventas(db, productos, admin.id, cajero.id)

        print("\nDatos de demostración creados correctamente.")
        if generadas:
            print("\n" + "=" * 68)
            print("CONTRASEÑAS GENERADAS — SE MUESTRAN UNA SOLA VEZ")
            print("=" * 68)
            for email, clave in generadas.items():
                print(f"  {email}\n    {clave}")
            print("=" * 68)
            print("Anótalas ahora: solo queda su hash en la base de datos.")
            print("Cámbialas desde Administración → Usuarios al primer ingreso.")
            print("=" * 68)
        else:
            print("Los usuarios ya existían: sus contraseñas no se modificaron.")
            print("Si perdiste el acceso, usa:  python -m app.manage_users")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

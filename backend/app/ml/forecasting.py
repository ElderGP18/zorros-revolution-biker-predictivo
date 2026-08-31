"""Motor de pronóstico de ventas: entrena el modelo y sirve predicciones al dashboard.

Enfoque:
  - Baseline obligatorio: naive estacional (mismo día de la semana, 7 días atrás).
  - Modelo principal: GradientBoostingRegressor (scikit-learn) sobre features de
    calendario (incluida la estacionalidad de Guatemala) + rezagos + medias móviles.
  - El modelo se persiste con joblib y cada entrenamiento queda registrado en
    la tabla model_runs con sus métricas (MASE / WAPE) para trazabilidad.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from . import calendar_features as cf

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "sales_model.joblib")
MIN_DIAS_ENTRENAMIENTO = 60

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

FEATURE_COLUMNS = [
    "dia_semana", "es_fin_de_semana", "mes", "mes_sin", "mes_cos", "dia_mes",
    "is_diciembre", "is_semana_bono14", "is_caravana_zorro",
    "lag_1", "lag_7", "lag_14", "lag_30", "media_movil_7", "media_movil_30",
]


def _ventas_diarias(db: Session) -> pd.DataFrame:
    """Serie de ventas totales por día (rellenando días sin ventas con 0)."""
    filas = (
        db.query(
            func.date(models.Sale.fecha_hora).label("fecha"),
            func.sum(models.Sale.total).label("total"),
        )
        .group_by(func.date(models.Sale.fecha_hora))
        .order_by(func.date(models.Sale.fecha_hora))
        .all()
    )
    if not filas:
        return pd.DataFrame(columns=["fecha", "total"])

    df = pd.DataFrame(filas, columns=["fecha", "total"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.set_index("fecha").asfreq("D", fill_value=0.0).reset_index()
    df["total"] = df["total"].astype(float)
    return df


def _construir_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    cal = df["fecha"].apply(lambda d: pd.Series(cf.features_dict(d)))
    df = pd.concat([df, cal], axis=1)

    for lag in (1, 7, 14, 30):
        df[f"lag_{lag}"] = df["total"].shift(lag)
    df["media_movil_7"] = df["total"].shift(1).rolling(7).mean()
    df["media_movil_30"] = df["total"].shift(1).rolling(30).mean()
    return df


def _wape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denom = np.sum(np.abs(y_true))
    if denom == 0:
        return 0.0
    return float(np.sum(np.abs(y_true - y_pred)) / denom * 100)


def _mase(y_true: np.ndarray, y_pred: np.ndarray, y_naive: np.ndarray) -> float:
    mae_modelo = float(np.mean(np.abs(y_true - y_pred)))
    mae_naive = float(np.mean(np.abs(y_true - y_naive)))
    if mae_naive == 0:
        return 0.0
    return mae_modelo / mae_naive


def entrenar_modelo(db: Session) -> schemas.RetrainResponse:
    """Entrena (o recalibra) el modelo de pronóstico con todo el histórico disponible."""
    df = _ventas_diarias(db)
    if len(df) < MIN_DIAS_ENTRENAMIENTO:
        raise ValueError(
            f"Se necesitan al menos {MIN_DIAS_ENTRENAMIENTO} días de historial de ventas para entrenar el modelo."
        )

    feats = _construir_features(df).dropna().reset_index(drop=True)
    if len(feats) < 30:
        raise ValueError("No hay suficientes datos históricos (tras calcular rezagos) para entrenar el modelo.")

    corte = max(int(len(feats) * 0.85), len(feats) - 30)
    corte = min(corte, len(feats) - 1)
    train, test = feats.iloc[:corte], feats.iloc[corte:]

    X_train, y_train = train[FEATURE_COLUMNS], train["total"]
    X_test, y_test = test[FEATURE_COLUMNS], test["total"]

    modelo = GradientBoostingRegressor(random_state=42, n_estimators=200, max_depth=3, learning_rate=0.05)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    y_naive = test["lag_7"].to_numpy()  # baseline: naive estacional (mismo día de la semana anterior)

    wape = _wape(y_test.to_numpy(), y_pred)
    mase = _mase(y_test.to_numpy(), y_pred, y_naive)

    mae_naive_test = float(np.mean(np.abs(y_test.to_numpy() - y_naive))) or 1.0
    mae_modelo_test = float(np.mean(np.abs(y_test.to_numpy() - y_pred)))
    mejora_pct = (1 - (mae_modelo_test / mae_naive_test)) * 100

    # Se re-entrena con TODO el histórico antes de publicar el modelo final que se usará para pronosticar.
    modelo_final = GradientBoostingRegressor(random_state=42, n_estimators=200, max_depth=3, learning_rate=0.05)
    modelo_final.fit(feats[FEATURE_COLUMNS], feats["total"])
    joblib.dump(modelo_final, MODEL_PATH)

    version = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    run = models.ModelRun(
        algoritmo="GradientBoostingRegressor",
        version=version,
        mase=round(mase, 4),
        wape=round(wape, 2),
        parametros_json=json.dumps({"n_estimators": 200, "max_depth": 3, "learning_rate": 0.05}),
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    return schemas.RetrainResponse(
        model_run_id=run.id,
        algoritmo=run.algoritmo,
        version=run.version,
        mase=run.mase,
        wape=run.wape,
        mejora_vs_baseline_pct=round(mejora_pct, 1),
    )


def _cargar_modelo():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def _pronosticar_dias(df_hist: pd.DataFrame, dias: int) -> List[Tuple[pd.Timestamp, float]]:
    """Pronostica día a día hacia adelante, realimentando los rezagos con sus propias predicciones."""
    modelo = _cargar_modelo()
    resultados: List[Tuple[pd.Timestamp, float]] = []

    if df_hist.empty:
        return resultados

    ultima_fecha = df_hist["fecha"].max()

    if modelo is None:
        # Sin modelo entrenado todavía: promedio móvil reciente ajustado por estacionalidad conocida.
        base = df_hist["total"].tail(28).mean()
        for i in range(1, dias + 1):
            fecha = ultima_fecha + timedelta(days=i)
            factor = 1.0
            if cf.es_temporada_diciembre(fecha):
                factor = 1.35
            elif cf.es_semana_bono14(fecha):
                factor = 1.25
            elif cf.es_caravana_del_zorro(fecha):
                factor = 1.2
            resultados.append((fecha, round(float(base * factor), 2)))
        return resultados

    historial = df_hist[["fecha", "total"]].copy()
    for i in range(1, dias + 1):
        fecha = ultima_fecha + timedelta(days=i)
        serie = historial["total"]

        fila = {"fecha": fecha}
        fila.update(cf.features_dict(fecha))
        fila["lag_1"] = float(serie.iloc[-1])
        fila["lag_7"] = float(serie.iloc[-7]) if len(serie) >= 7 else float(serie.iloc[-1])
        fila["lag_14"] = float(serie.iloc[-14]) if len(serie) >= 14 else float(serie.iloc[-1])
        fila["lag_30"] = float(serie.iloc[-30]) if len(serie) >= 30 else float(serie.iloc[-1])
        fila["media_movil_7"] = float(serie.tail(7).mean())
        fila["media_movil_30"] = float(serie.tail(30).mean())

        X = pd.DataFrame([fila])[FEATURE_COLUMNS]
        pred = max(0.0, float(modelo.predict(X)[0]))
        resultados.append((fecha, round(pred, 2)))

        historial = pd.concat([historial, pd.DataFrame([{"fecha": fecha, "total": pred}])], ignore_index=True)

    return resultados


def proyeccion_proximo_mes(db: Session) -> Tuple[float, Optional[float]]:
    df = _ventas_diarias(db)
    if df.empty:
        return 0.0, None
    pronostico = _pronosticar_dias(df, 30)
    total = round(sum(v for _, v in pronostico), 2)

    modelo = _cargar_modelo()
    ultimo_run = db.query(models.ModelRun).order_by(models.ModelRun.fecha.desc()).first()
    confianza = None
    if modelo is not None and ultimo_run and ultimo_run.wape is not None:
        confianza = round(max(0.0, min(99.0, 100 - ultimo_run.wape)), 1)
    return total, confianza


def tendencia_mensual(db: Session, meses: int = 12) -> List[schemas.TrendPoint]:
    df = _ventas_diarias(db)
    if df.empty:
        return []

    df = df.copy()
    df["periodo"] = df["fecha"].dt.to_period("M")
    real_mensual = df.groupby("periodo")["total"].sum().tail(meses)

    pronostico = _pronosticar_dias(df, 30)
    df_pron = pd.DataFrame(pronostico, columns=["fecha", "total"])
    df_pron["periodo"] = pd.to_datetime(df_pron["fecha"]).dt.to_period("M")
    proyectado_mensual = df_pron.groupby("periodo")["total"].sum()

    periodos = list(real_mensual.index) + [p for p in proyectado_mensual.index if p not in real_mensual.index]
    puntos: List[schemas.TrendPoint] = []
    for periodo in periodos:
        puntos.append(
            schemas.TrendPoint(
                fecha=str(periodo),
                real=round(float(real_mensual[periodo]), 2) if periodo in real_mensual.index else None,
                proyectado=round(float(proyectado_mensual[periodo]), 2) if periodo in proyectado_mensual.index else None,
            )
        )
    return puntos


def serie_historica_y_pronostico(db: Session, horizonte: int = 30) -> List[schemas.ForecastPoint]:
    df = _ventas_diarias(db)
    puntos: List[schemas.ForecastPoint] = []
    if df.empty:
        return puntos

    historico = df.tail(60)
    for _, fila in historico.iterrows():
        puntos.append(schemas.ForecastPoint(fecha=fila["fecha"].strftime("%Y-%m-%d"), real=round(float(fila["total"]), 2)))

    pronostico = _pronosticar_dias(df, horizonte)
    for fecha, valor in pronostico:
        margen = valor * 0.15
        puntos.append(
            schemas.ForecastPoint(
                fecha=fecha.strftime("%Y-%m-%d"),
                pronostico=valor,
                intervalo_inf=round(max(0.0, valor - margen), 2),
                intervalo_sup=round(valor + margen, 2),
            )
        )
    return puntos


def senales_por_producto(db: Session, dias_recientes: int = 14) -> List[schemas.ProductSignal]:
    """Compara ventas recientes vs. el periodo previo por producto para detectar alta/baja demanda."""
    hoy = datetime.utcnow()
    inicio_reciente = hoy - timedelta(days=dias_recientes)
    inicio_previo = inicio_reciente - timedelta(days=dias_recientes)

    def _ventas_por_producto(desde: datetime, hasta: datetime) -> dict:
        filas = (
            db.query(models.SaleItem.product_id, func.sum(models.SaleItem.cantidad))
            .join(models.Sale)
            .filter(models.Sale.fecha_hora >= desde, models.Sale.fecha_hora < hasta)
            .group_by(models.SaleItem.product_id)
            .all()
        )
        return {pid: cant for pid, cant in filas}

    recientes = _ventas_por_producto(inicio_reciente, hoy)
    previas = _ventas_por_producto(inicio_previo, inicio_reciente)

    productos = {p.id: p for p in db.query(models.Product).filter(models.Product.activo == True).all()}  # noqa: E712

    señales: List[schemas.ProductSignal] = []
    for pid, cant_reciente in recientes.items():
        producto = productos.get(pid)
        if not producto:
            continue
        cant_previa = previas.get(pid, 0)
        if cant_previa == 0:
            magnitud = 100.0 if cant_reciente > 0 else 0.0
        else:
            magnitud = ((cant_reciente - cant_previa) / cant_previa) * 100

        if abs(magnitud) < 15:
            continue

        señales.append(
            schemas.ProductSignal(
                product_id=pid,
                nombre=producto.nombre,
                categoria=producto.categoria,
                tendencia="alta_demanda" if magnitud > 0 else "baja_demanda",
                magnitud_pct=round(magnitud, 1),
            )
        )

    señales.sort(key=lambda s: abs(s.magnitud_pct), reverse=True)
    return señales[:8]

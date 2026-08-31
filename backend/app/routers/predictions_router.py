from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..deps import get_db, require_role
from ..ml import forecasting, reorder

router = APIRouter(prefix="/predictions", tags=["predicciones"])


@router.get("/forecast", response_model=List[schemas.ForecastPoint])
def forecast(horizonte: int = 30, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    return forecasting.serie_historica_y_pronostico(db, horizonte)


@router.get("/signals", response_model=List[schemas.ProductSignal])
def signals(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    return forecasting.senales_por_producto(db)


@router.post("/retrain", response_model=schemas.RetrainResponse)
def retrain(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    try:
        return forecasting.entrenar_modelo(db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/recommendations", response_model=List[schemas.RecommendationOut])
def recommendations(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    return reorder.generar_recomendaciones(db)

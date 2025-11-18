# app/routes/api_routes.py

from fastapi import APIRouter
from app.collectors.market_collector import collector
from app.collectors.sports_scraper import get_sports_data
from app.fire.firestore_client import save_market_data
from app.ml.model import ai_predict

router = APIRouter()

@router.get("/market")
def route_market():
    data = collector()
    save_market_data("market_data", data)
    return {"message": "market collected", "data": data}

@router.get("/sports")
def route_sports():
    data = get_sports_data()
    save_market_data("sports_data", data)
    return {"message": "sports collected", "data": data}

@router.get("/predict")
def route_predict():
    return ai_predict()

from fastapi import FastAPI
from app.collectors.market_collector import collector
from app.collectors.sports_scraper import get_sports_data
from app.fire.firestore_client import save_market_data
from app.ml.model import ai_predict

app = FastAPI()

@app.get("/")
def root():
    return {"status": "AI Data Mining Backend Running"}

@app.get("/collect/market")
def collect_market():
    data = collector()
    save_market_data("market_data", data)
    return {"message": "market collected", "data": data}

@app.get("/collect/sports")
def collect_sports():
    data = get_sports_data()
    save_market_data("sports_data", data)
    return {"message": "sports collected", "data": data}

@app.get("/predict/market")
def predict_market():
    prediction = ai_predict()
    return {"prediction": prediction}

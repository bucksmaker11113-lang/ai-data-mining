# ===============================================================
# ML API ENDPOINTS - AI DATA MINING
# MZ/X Trader + Tippmester ML tanítás és előrejelzés
# ===============================================================

from fastapi import APIRouter
from ml.dataset_builder import builder
from ml.feature_engineering import eng
from ml.model_training import trainer
import joblib
import pandas as pd
import os

router = APIRouter(prefix="/ml", tags=["ML API"])


# ---------------------------------------------------------------
# TRAIN - MARKET MODEL (MZ/X Trader AI)
# ---------------------------------------------------------------
@router.post("/train/market")
def train_market_model():

    df = builder.build_market_dataset(limit=1000)
    if df.empty:
        return {"status": "error", "msg": "Nincs elég market adat!"}

    df = eng.market_features(df)

    score = trainer.train_market_model(df)
    return {"status": "ok", "model": "mzx_model.pkl", "score": score}


# ---------------------------------------------------------------
# TRAIN - SPORTS MODEL (Tippmester AI)
# ---------------------------------------------------------------
@router.post("/train/sports")
def train_sports_model():

    df = builder.build_sports_dataset(limit=1500)
    if df.empty:
        return {"status": "error", "msg": "Nincs elég sport adat!"}

    df = eng.sports_features(df)

    score = trainer.train_sports_model(df)
    return {"status": "ok", "model": "tipp_model.pkl", "score": score}


# ---------------------------------------------------------------
# MARKET PREDICTION
# ---------------------------------------------------------------
@router.post("/predict/market")
def predict_market(data: dict):

    model_path = "models/mzx_model.pkl"
    if not os.path.exists(model_path):
        return {"status": "error", "msg": "A modell nincs betanítva!"}

    model = joblib.load(model_path)

    df = pd.DataFrame([data])
    df = eng.market_features(df)

    pred = model.predict(df)[0]

    return {"status": "ok", "prediction": float(pred)}


# ---------------------------------------------------------------
# SPORTS PREDICTION (Tippmester előrejelzés)
# ---------------------------------------------------------------
@router.post("/predict/sports")
def predict_sports(data: dict):

    model_path = "models/tipp_model.pkl"
    if not os.path.exists(model_path):
        return {"status": "error", "msg": "A modell nincs betanítva!"}

    model = joblib.load(model_path)

    df = pd.DataFrame([data])
    df = eng.sports_features(df)

    pred = model.predict_proba(df)[0].tolist()

    return {
        "status": "ok",
        "home_win_prob": float(pred[1]),
        "away_win_prob": float(pred[0])
    }


# ---------------------------------------------------------------
# MODEL STATUS
# ---------------------------------------------------------------
@router.get("/model/status")
def model_status():
    return {
        "market_model": os.path.exists("models/mzx_model.pkl"),
        "sports_model": os.path.exists("models/tipp_model.pkl")
    }

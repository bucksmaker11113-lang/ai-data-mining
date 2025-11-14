# ============================================================
# AI DATA MINING BACKEND - MAIN API
# FastAPI + Firestore + Cloud Storage + Unified ML Pipeline
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore, storage
from pydantic import BaseModel
import datetime
import uvicorn
import json
import os

# ============================================================
# CONFIG INIT
# ============================================================

GOOGLE_APPLICATION_CREDENTIALS = "gcloud-key.json"

if not os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
    raise Exception("""
    ❌ MISSING gcloud-key.json !!!
    - Lépj be: Google Cloud → IAM → Service Accounts → Create Key (JSON)
    - Töltsd le → töltsd fel a GitHub repositoryba
    """)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

# Firestore
db = firestore.Client()

# Storage bucket
BUCKET_NAME = "data-mining1"   # Ezt te hoztad létre!
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# ============================================================
# FASTAPI INIT
# ============================================================

app = FastAPI(
    title="AI DATA MINING API",
    description="Adatgyűjtő és AI-előkészítő rendszer – Tippmester + MZ/X",
    version="1.0"
)

# Engedélyezett CORS (frontend + mobilapp)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELS
# ============================================================

class SportsData(BaseModel):
    sport: str
    league: str
    home: str
    away: str
    odds_home: float
    odds_away: float
    timestamp: float

class MarketData(BaseModel):
    symbol: str
    price: float
    volume: float
    trend: float
    timestamp: float

# ============================================================
# FIRESTORE OPERATIONS
# ============================================================

def save_to_firestore(collection: str, data: dict):
    """Mentés Firestore-ba időbélyeggel."""
    ts = datetime.datetime.utcnow().isoformat()
    ref = db.collection(collection).document(ts)
    ref.set(data)
    return {"status": "ok", "id": ts}

# ============================================================
# CLOUD STORAGE OPERATIONS
# ============================================================

def save_raw_to_storage(path: str, content: dict):
    """Nyers JSON mentése Storage-ba."""
    blob = bucket.blob(path)
    blob.upload_from_string(json.dumps(content), content_type="application/json")
    return True

# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/")
def root():
    return {"status": "AI Data Mining backend OK", "service": "v1.0"}

# --------------------------
# SPORT DATA ENDPOINT (Tippmester számára)
# --------------------------

@app.post("/sports/push")
def push_sport_data(data: SportsData):
    payload = data.dict()

    save_to_firestore("sports_live", payload)
    save_raw_to_storage(f"sports_raw/{payload['timestamp']}.json", payload)

    return {"ok": True, "msg": "Sport adat tárolva"}

# --------------------------
# CRYPTO / MARKET DATA (MZ/X számára)
# --------------------------

@app.post("/market/push")
def push_market_data(data: MarketData):
    payload = data.dict()

    save_to_firestore("market_live", payload)
    save_raw_to_storage(f"market_raw/{payload['timestamp']}.json", payload)

    return {"ok": True, "msg": "Piaci adat tárolva"}

# --------------------------
# UNIFIED ML DATASET EXPORT
# (mindkét AI használja)
# --------------------------

@app.get("/dataset/{dtype}")
def get_dataset(dtype: str):
    """
    dtype lehet:
    - sports
    - market
    """
    if dtype == "sports":
        docs = db.collection("sports_live").order_by("__name__", direction=firestore.Query.DESCENDING).limit(500).stream()
    elif dtype == "market":
        docs = db.collection("market_live").order_by("__name__", direction=firestore.Query.DESCENDING).limit(500).stream()
    else:
        raise HTTPException(400, "Invalid dataset type")

    result = [doc.to_dict() for doc in docs]
    return {"dataset": result}


# ============================================================
# RUN (Railway recognizes automatically)
# ============================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

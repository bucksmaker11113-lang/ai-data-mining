# ============================================================
# AI DATA MINING - FŐ BACKEND API
# Firestore + Storage + ML + Collectors
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Collector modulok
from collectors.market_collector import collector
from collectors.sports_scraper import scraper

# ML API router
from routes.ml_api import router as ml_router

# Firestore teszt import
from fire.firestore_utils import save_market_record

import uvicorn


app = FastAPI(
    title="AI Data Mining Engine",
    description="MZ/X Trader + Tippmester AI közös adatbázis és ML motor",
    version="1.0.0"
)

# ------------------------------------------------------------
# CORS beállítás (frontend + mobil + railway)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # később szűkíthetjük
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------
# STATUS OK
# ------------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "msg": "AI Data Mining fut",
        "modules": {
            "market_collector": True,
            "sports_scraper": True,
            "ml_api": True,
            "firestore": True
        }
    }


# ------------------------------------------------------------
# COLLECTORS - manuális futtatás API-ból
# ------------------------------------------------------------
@app.get("/collect/market")
def collect_market():
    data = collector.collect_once()
    return {"status": "ok", "collected": data}


@app.get("/collect/sports")
def collect_sports():
    data = scraper.collect_all()
    return {"status": "ok", "collected": data}


# ------------------------------------------------------------
# ML API integráció
# ------------------------------------------------------------
app.include_router(ml_router)


# ------------------------------------------------------------
# FIRESTORE teszt endpoint
# (ellenőrzi, hogy Firestore kulcs helyesen működik)
# ------------------------------------------------------------
@app.get("/fire/test")
def test_firestore():
    test_data = {
        "symbol": "TEST",
        "price": 123.45,
        "timestamp": 999999999
    }
    save_market_record(test_data)
    return {"status": "ok", "msg": "Firestore írás működik!"}


# ------------------------------------------------------------
# LOCAL RUN (Railway nem használja)
# ------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

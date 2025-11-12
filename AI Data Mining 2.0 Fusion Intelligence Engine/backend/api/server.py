from fastapi import FastAPI
from .routes_sports import router as sports_router
from .routes_market import router as market_router
from .routes_feedback import router as feedback_router

app = FastAPI(title="AI Data Mining 2.0 Fusion API")

app.include_router(sports_router, prefix="/sports", tags=["Sports"])
app.include_router(market_router, prefix="/market", tags=["Market"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])

@app.get("/")
def root():
    return {"status": "ok", "message": "AI Data Mining 2.0 Fusion Intelligence Engine API működik."}

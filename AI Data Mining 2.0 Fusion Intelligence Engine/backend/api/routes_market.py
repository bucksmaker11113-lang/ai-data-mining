from fastapi import APIRouter
from backend.database import DatabaseHandler, MarketRecord

router = APIRouter()

@router.get("/latest")
def get_latest_market(limit: int = 10):
    db = DatabaseHandler()
    session = db.get_session()
    recs = session.query(MarketRecord).order_by(MarketRecord.timestamp.desc()).limit(limit).all()
    return [{"symbol": r.symbol, "trend": r.trend, "volatility": r.volatility} for r in recs]

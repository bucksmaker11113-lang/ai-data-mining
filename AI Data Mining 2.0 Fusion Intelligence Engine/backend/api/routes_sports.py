from fastapi import APIRouter
from backend.database import DatabaseHandler, SportRecord

router = APIRouter()

@router.get("/latest")
def get_latest_sports(limit: int = 10):
    db = DatabaseHandler()
    session = db.get_session()
    recs = session.query(SportRecord).order_by(SportRecord.date.desc()).limit(limit).all()
    return [{"match": r.match, "value_score": r.value_score, "bias": r.bias} for r in recs]

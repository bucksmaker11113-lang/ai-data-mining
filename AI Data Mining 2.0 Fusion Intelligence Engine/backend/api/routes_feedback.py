from fastapi import APIRouter
from backend.database import DatabaseHandler, FeedbackRecord

router = APIRouter()

@router.post("/")
def post_feedback(system: str, accuracy: float, roi: float):
    db = DatabaseHandler()
    session = db.get_session()
    rec = FeedbackRecord(system=system, accuracy=accuracy, roi=roi)
    session.add(rec)
    session.commit()
    return {"message": f"Feedback received from {system}", "accuracy": accuracy, "roi": roi}

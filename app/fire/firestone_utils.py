# ============================================================
# FIRESTORE UTILS - AI DATA MINING
# Mentés sport és market adatok számára
# ============================================================

from google.cloud import firestore
import datetime

# Firestore inicializálás
db = firestore.Client()


def save_sport_record(data: dict):
    """
    Sport adatok mentése Firestore-ba.
    Tippmester AI adatbázisa.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    ref = db.collection("sports_live").document(timestamp)
    ref.set(data)
    return True


def save_market_record(data: dict):
    """
    Market adatok mentése Firestore-ba.
    MZ/X Trader AI adatbázisa.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    ref = db.collection("market_live").document(timestamp)
    ref.set(data)
    return True


def load_latest_market(limit=300):
    """
    Legutóbbi árfolyami adatok lekérése ML modellekhez.
    """
    docs = (
        db.collection("market_live")
        .order_by("__name__", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [doc.to_dict() for doc in docs]


def load_latest_sports(limit=300):
    """
    Legutóbbi sport adatok lekérése Tippmester AI-hez.
    """
    docs = (
        db.collection("sports_live")
        .order_by("__name__", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [doc.to_dict() for doc in docs]

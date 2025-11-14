# ============================================================
# CLOUD STORAGE UTILS - AI DATA MINING
# Nyers adatmentés sport + market számára
# ============================================================

from google.cloud import storage
import json
import time

BUCKET_NAME = "data-mining1"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)


def save_sport_raw(data: dict):
    """
    Sport nyers adatok tárolása Cloud Storage-ban.
    """
    ts = str(time.time())
    blob = bucket.blob(f"sports_raw/{ts}.json")

    blob.upload_from_string(
        json.dumps(data),
        content_type="application/json"
    )

    return True


def save_market_raw(data: dict):
    """
    Piaci nyers adatok tárolása Cloud Storage-ban.
    """
    ts = str(time.time())
    blob = bucket.blob(f"market_raw/{ts}.json")

    blob.upload_from_string(
        json.dumps(data),
        content_type="application/json"
    )

    return True

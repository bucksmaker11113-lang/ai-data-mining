# app/cron/cron_jobs.py

import time
from app.collectors.market_collector import collector
from app.collectors.sports_scraper import get_sports_data
from app.fire.firestore_client import save_market_data
from app.preprocess.data_cleaner import cleaner


def run_market_job():
    """
    Piaci adatok ütemezett gyűjtése (MZ/X használja)
    """
    raw = collector()
    cleaned = cleaner(raw)
    save_market_data("market_data", cleaned)
    return {"status": "market_job_ok", "items": len(cleaned)}


def run_sports_job():
    """
    Sportfogadási adatok ütemezett gyűjtése (Tippmester használja)
    """
    raw = get_sports_data()
    cleaned = cleaner(raw)
    save_market_data("sports_data", cleaned)
    return {"status": "sports_job_ok"}


def run_all():
    """
    Mindkét adatgyűjtés 15 percenként.
    A Renderen NEM fut, csak Railway CRON vagy külső scheduler alatt.
    """
    while True:
        print("Running scheduled jobs...")
        try:
            print(run_market_job())
            print(run_sports_job())
        except Exception as e:
            print("Cron error:", str(e))

        time.sleep(900)  # 15 perc

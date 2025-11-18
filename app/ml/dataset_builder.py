# ============================================================
# DATASET BUILDER - AI DATA MINING
# Sport + Market adatok egységes ML dataset építése
# ============================================================

from fire.firestore_utils import load_latest_market, load_latest_sports
from preprocess.data_cleaner import cleaner
import pandas as pd


class DatasetBuilder:

    # --------------------------------------------------------
    # Market dataset – MZ/X Trader AI
    # --------------------------------------------------------
    def build_market_dataset(self, limit=500):
        raw = load_latest_market(limit)
        cleaned = cleaner.clean_market_data(raw)

        if not cleaned:
            return pd.DataFrame()

        df = pd.DataFrame(cleaned)
        return df

    # --------------------------------------------------------
    # Sport dataset – Tippmester AI
    # --------------------------------------------------------
    def build_sports_dataset(self, limit=500):
        raw = load_latest_sports(limit)
        cleaned = cleaner.clean_sport_data(raw)

        if not cleaned:
            return pd.DataFrame()

        df = pd.DataFrame(cleaned)
        return df

    # --------------------------------------------------------
    # Exportálás CSV-be (opcionális)
    # --------------------------------------------------------
    def export_to_csv(self, df: pd.DataFrame, path: str):
        if df.empty:
            return False
        df.to_csv(path, index=False)
        return True


builder = DatasetBuilder()

# ============================================================
# DATA CLEANER MODULE - AI DATA MINING
# Sport + Market ML Dataset Cleaner
# ============================================================

import numpy as np
import pandas as pd
import json
import os
from datetime import datetime

class DataCleaner:

    def clean_sport_data(self, raw_entries: list):
        """
        Sport adatok tisztítása ML felhasználáshoz.
        Tippmester AI ebben tanul.
        """

        df = pd.DataFrame(raw_entries)

        if df.empty:
            return []

        # Idő átalakítása
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

        # Odds normalizálás
        df["home_norm"] = 1 / df["odds_home"]
        df["away_norm"] = 1 / df["odds_away"]

        # Különbség – sport ML-ben ez fontos
        df["strength_diff"] = df["home_norm"] - df["away_norm"]

        # Sorbarendezés
        df = df.sort_values("timestamp")

        return df.to_dict(orient="records")

    def clean_market_data(self, raw_entries: list):
        """
        Kriptó adatok tisztítása ML-hez.
        MZ/X Trader ebben tanul.
        """

        df = pd.DataFrame(raw_entries)

        if df.empty:
            return []

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

        # Árváltozás számítása
        df["price_change"] = df["price"].diff().fillna(0)

        # Volatilitás
        df["volatility"] = df["price"].rolling(10).std().fillna(0)

        # Trend erősség (egyik fő input a trader AI-nak)
        df["trend_strength"] = df["price_change"].rolling(5).mean().fillna(0)

        df = df.sort_values("timestamp")

        return df.to_dict(orient="records")

cleaner = DataCleaner()

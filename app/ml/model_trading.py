# ============================================================
# MODEL TRAINING - AI DATA MINING
# ML modellek tréningje (Trader AI + Tippmester AI)
# ============================================================

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import numpy as np
import os


class ModelTraining:

    # --------------------------------------------------------
    # MZ/X Trader regressziós modell (ármozgás predikció)
    # --------------------------------------------------------
    def train_market_model(self, df):
        if df.empty:
            return False

        df = df.dropna()

        X = df[["price", "momentum", "roll_vol", "funding_norm", "trend_strength", "volatility"]]
        y = df["future_return"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestRegressor(n_estimators=150)
        model.fit(X_train, y_train)

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/mzx_model.pkl")

        return model.score(X_test, y_test)

    # --------------------------------------------------------
    # Tippmester sport classifier modell
    # --------------------------------------------------------
    def train_sports_model(self, df):
        if df.empty:
            return False

        df = df.dropna()

        X = df[["strength_diff", "home_norm", "away_norm"]]
        y = (df["home_norm"] > df["away_norm"]).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestClassifier(n_estimators=150)
        model.fit(X_train, y_train)

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/tipp_model.pkl")

        return model.score(X_test, y_test)


trainer = ModelTraining()

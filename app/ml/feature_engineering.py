# ============================================================
# FEATURE ENGINEERING - AI DATA MINING
# Extra ML feature-ök generálása a modellezéshez
# ============================================================

import pandas as pd


class FeatureEngineering:

    # --------------------------------------------------------
    # Market feature-ök MZ/X AI-hez
    # --------------------------------------------------------
    def market_features(self, df: pd.DataFrame):
        if df.empty:
            return df

        df = df.copy()

        # Momentum
        df["momentum"] = df["price"].pct_change().fillna(0)

        # Funding rate z-score jellegű normalizálás
        df["funding_norm"] = (df["funding"] - df["funding"].mean()) / df["funding"].std()

        # Rolling volatility augment
        df["roll_vol"] = df["price"].rolling(10).std().fillna(0)

        # Future return (célváltozó)
        df["future_return"] = df["price"].shift(-3) - df["price"]

        return df

    # --------------------------------------------------------
    # Sport feature-ök Tippmester AI-hez
    # --------------------------------------------------------
    def sports_features(self, df: pd.DataFrame):
        if df.empty:
            return df

        df = df.copy()

        # Odds logit transform
        df["log_home"] = -pd.Series(df["odds_home"]).apply(lambda x: pd.np.log(x))
        df["log_away"] = -pd.Series(df["odds_away"]).apply(lambda x: pd.np.log(x))

        # Strength difference
        df["strength"] = df["home_norm"] - df["away_norm"]

        return df


eng = FeatureEngineering()

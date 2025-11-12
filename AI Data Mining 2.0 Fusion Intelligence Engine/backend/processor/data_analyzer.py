import numpy as np
import pandas as pd

class DataAnalyzer:
    def __init__(self):
        self.bias_threshold = 0.05

    def compute_value(self, odds, probability):
        """Value számítása"""
        return (odds * probability) - 1

    def analyze_sport(self, df):
        """Sportadatok elemzése (value + bias felismerés)"""
        try:
            df["value_score"] = df.apply(lambda x: self.compute_value(
                x.get("odds", 1.0), x.get("probability", 0.5)
            ), axis=1)
            df["bias"] = np.where(df["value_score"] > self.bias_threshold, "positive",
                           np.where(df["value_score"] < -self.bias_threshold, "negative", "neutral"))
            return df
        except Exception as e:
            print("[Analyzer ERROR - sport]", e)
            return df

    def analyze_market(self, df):
        """Tőzsdei idősorok trend- és volatilitás-elemzése"""
        try:
            df["returns"] = df["close"].pct_change()
            df["volatility"] = df["returns"].rolling(window=5).std()
            df["trend"] = np.where(df["returns"] > 0, "bullish", "bearish")
            return df.dropna()
        except Exception as e:
            print("[Analyzer ERROR - market]", e)
            return df

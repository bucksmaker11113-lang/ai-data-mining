import pandas as pd
import numpy as np

class CrossIntelligence:
    def __init__(self):
        pass

    def correlate(self, sport_df, market_df):
        """Kiszámolja a sport value és piaci volatilitás közti kapcsolatot"""
        try:
            merged = pd.DataFrame({
                "sport_value": sport_df["value_score"].rolling(window=3).mean(),
                "market_vol": market_df["volatility"].rolling(window=3).mean()
            }).dropna()
            corr = merged["sport_value"].corr(merged["market_vol"])
            print(f"[CrossIntelligence] Sport–piac korreláció: {corr:.2f}")
            return corr
        except Exception as e:
            print("[CrossIntelligence ERROR]", e)
            return 0.0

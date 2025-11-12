import requests
import pandas as pd
from datetime import datetime
import os

class ProptCollector:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SPORTS_API_KEY", "")
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3/players"
        self.headers = {"X-RapidAPI-Key": self.api_key}

    def collect_players(self, league_id=39, season=2023):
        """Collect player statistics for given league and season"""
        try:
            r = requests.get(
                self.base_url,
                headers=self.headers,
                params={"league": league_id, "season": season},
                timeout=15
            )
            data = r.json()
            players = data.get("response", [])
            df = pd.json_normalize(players)
            os.makedirs("data/raw/propt/", exist_ok=True)
            path = f"data/raw/propt/players_{league_id}_{season}.csv"
            df.to_csv(path, index=False)
            return df
        except Exception as e:
            print(f"[ERROR] Player data collection failed:", e)
            return pd.DataFrame()

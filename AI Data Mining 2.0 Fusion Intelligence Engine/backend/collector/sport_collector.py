import requests
import pandas as pd
from datetime import datetime, timedelta
import os

class SportsCollector:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SPORTS_API_KEY", "")
        self.base_urls = {
            "football": "https://api-football-v1.p.rapidapi.com/v3/",
            "basketball": "https://api-basketball.p.rapidapi.com/",
            "hockey": "https://api-hockey.p.rapidapi.com/",
            "tennis": "https://api-tennis.p.rapidapi.com/"
        }
        self.headers = {"X-RapidAPI-Key": self.api_key}

    def collect(self, sport="football", days_back=3):
        """Collect matches, odds and stats for a sport"""
        if sport not in self.base_urls:
            raise ValueError(f"Unsupported sport: {sport}")
        url = self.base_urls[sport] + "fixtures"
        params = {"from": (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")}
        try:
            r = requests.get(url, headers=self.headers, params=params, timeout=15)
            data = r.json()
            matches = data.get("response", [])
            df = pd.json_normalize(matches)
            os.makedirs(f"data/raw/{sport}/", exist_ok=True)
            path = f"data/raw/{sport}/{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(path, index=False)
            return df
        except Exception as e:
            print(f"[ERROR] {sport} data collection failed:", e)
            return pd.DataFrame()

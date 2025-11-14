# ============================================================
# SPORTS SCRAPER MODULE - AI DATA MINING
# Élő sportfogadási adatok gyűjtése Tippmester AI számára
# ============================================================

import requests
import time
from datetime import datetime
from data_cleaner import cleaner


class SportsScraper:

    def __init__(self):
        # Ha majd lesz hivatalos API kulcs → ide kerül
        self.API_KEY = ""
        self.source_url = "https://api.the-odds-api.com/v4/sports"

    # --------------------------------------------------------
    # Alap sportlista lekérése
    # --------------------------------------------------------
    def fetch_sports(self):
        url = f"{self.source_url}?apiKey={self.API_KEY}"
        r = requests.get(url)

        if r.status_code != 200:
            return []

        return r.json()

    # --------------------------------------------------------
    # Élő odds lekérése sportáganként
    # --------------------------------------------------------
    def fetch_live_odds(self, sport_key: str):
        url = f"{self.source_url}/{sport_key}/odds?regions=eu&markets=h2h&apiKey={self.API_KEY}"
        r = requests.get(url)

        if r.status_code != 200:
            return []

        return r.json()

    # --------------------------------------------------------
    # Adatok feldolgozása AI számára
    # --------------------------------------------------------
    def process_odds_data(self, raw_data):
        processed = []

        for game in raw_data:
            if "bookmakers" not in game or not game["bookmakers"]:
                continue

            odds = game["bookmakers"][0]["markets"][0]["outcomes"]

            if len(odds) < 2:
                continue

            event = {
                "sport": game.get("sport_key", ""),
                "league": game.get("sport_title", ""),
                "home": odds[0]["name"],
                "away": odds[1]["name"],
                "odds_home": odds[0]["price"],
                "odds_away": odds[1]["price"],
                "timestamp": time.time()
            }

            processed.append(event)

        return cleaner.clean_sport_data(processed)

    # --------------------------------------------------------
    # MAIN: teljes sport scraping ciklus
    # --------------------------------------------------------
    def collect_all(self):
        sports = ["soccer_epl", "basketball_nba", "icehockey_nhl", "tennis_atp"]

        results = []

        for sport in sports:
            raw = self.fetch_live_odds(sport)
            cleaned = self.process_odds_data(raw)
            results.extend(cleaned)

        return results


scraper = SportsScraper()

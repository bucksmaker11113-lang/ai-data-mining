# app/collectors/sports_scraper.py

def get_sports_data():
    """
    Dummy sportadat gyűjtő modul.
    Később ide jön az:
      - odds API integráció
      - live event stream
      - soccer / tennis / basketball stat collectors
    """
    return {
        "source": "sports_scraper",
        "status": "ok",
        "message": "sports data collected successfully",
        "sample_data": {
            "match": "FC Barcelona vs Real Madrid",
            "odds_home": 1.85,
            "odds_draw": 3.40,
            "odds_away": 4.20,
            "timestamp": "2025-11-14"
        }
    }

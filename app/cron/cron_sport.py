# ============================================================
# CRON - SPORTS SCRAPER
# Tippmester sportadat frissítés 2 percenként
# ============================================================

from collectors.sports_scraper import scraper

def run():
    data = scraper.collect_all()
    print("Sports update OK:", data)

if __name__ == "__main__":
    run()

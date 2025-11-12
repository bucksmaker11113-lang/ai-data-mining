from backend.core import FusionLearningCore, MetaMind, SmartCache
from backend.collector import SportsCollector, MarketCollector, ProptCollector
from backend.processor import DeepCleaner, DataAnalyzer, FeedbackLoop, CrossIntelligence
from backend.database import DatabaseHandler, SportRecord, MarketRecord, ReportLog
from backend.reports import ReportGenerator, ReportMailer, GrowthTracker
from backend.api.server import app
import os, pandas as pd
from datetime import datetime

def main():
    print("\n🚀 AI Data Mining 2.0 Fusion Intelligence Engine indul...\n")

    # Adatbázis inicializálás
    db = DatabaseHandler()
    db.create_tables()
    session = db.get_session()

    # Modulok inicializálása
    cache = SmartCache()
    ai_core = FusionLearningCore(cache)
    meta = MetaMind()
    collector_sport = SportsCollector()
    collector_market = MarketCollector()
    cleaner = DeepCleaner()
    analyzer = DataAnalyzer()
    feedback = FeedbackLoop()
    crossintel = CrossIntelligence()
    reporter = ReportGenerator()
    mailer = ReportMailer()
    growth = GrowthTracker()

    # 1️⃣ Adatgyűjtés
    sport_data = collector_sport.collect("football")
    market_data = collector_market.collect_yahoo()

    # 2️⃣ Tisztítás és elemzés
    sport_clean = cleaner.clean(sport_data)
    sport_analyzed = analyzer.analyze_sport(sport_clean)
    market_analyzed = analyzer.analyze_market(market_data)

    # 3️⃣ Kereszt-intelligencia elemzés
    correlation = crossintel.correlate(sport_analyzed, market_analyzed)

    # 4️⃣ AI tanulás (modell frissítés)
    if len(sport_analyzed) > 5:
        X = sport_analyzed[["odds", "probability"]].fillna(0).values
        y = sport_analyzed["value_score"].fillna(0).values
        ai_core.train(X, y)
        acc = ai_core.meta_stats["last_accuracy"]
        meta.analyze_performance(ai_core.meta_stats)
    else:
        acc = 0.0

    # 5️⃣ Fejlődés naplózás
    growth.log_growth(acc, roi=0.05, bias_shift=0.02)
    feedback_data = feedback.get_average_feedback()

    # 6️⃣ Riport generálás és küldés
    stats = {"accuracy": acc, "bias_shift": 0.02, "roi_stability": 0.05, "engine": "FusionCore", "train_count": ai_core.meta_stats["train_count"]}
    report_text = reporter.create_report(stats, feedback_data, correlation)
    mailed = mailer.send_report("AI Data Mining 2.0 – Napi Riport", report_text)

    # 7️⃣ Riport mentése DB-be
    log = ReportLog(
        accuracy=acc,
        value_bias=0.02,
        roi=0.05,
        meta_comment="Automatikus napi riport generálva",
        json_data=stats,
        emailed=mailed
    )
    session.add(log)
    session.commit()

    print("\n✅ Futtatás befejezve, riport elküldve és mentve.\n")

if __name__ == "__main__":
    main()

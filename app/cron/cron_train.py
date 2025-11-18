# ============================================================
# CRON - DAILY ML TRAINING
# Trader + Tippmester modellek újratanítása naponta
# ============================================================

from ml.dataset_builder import builder
from ml.feature_engineering import eng
from ml.model_training import trainer


def run():
    print("Training started...")

    # Market model
    market_df = builder.build_market_dataset(limit=2000)
    if not market_df.empty:
        market_df = eng.market_features(market_df)
        score1 = trainer.train_market_model(market_df)
        print("MZ/X Market Model OK:", score1)

    # Sports model
    sports_df = builder.build_sports_dataset(limit=3000)
    if not sports_df.empty:
        sports_df = eng.sports_features(sports_df)
        score2 = trainer.train_sports_model(sports_df)
        print("Tippmester Sports Model OK:", score2)

    print("Training finished.")


if __name__ == "__main__":
    run()

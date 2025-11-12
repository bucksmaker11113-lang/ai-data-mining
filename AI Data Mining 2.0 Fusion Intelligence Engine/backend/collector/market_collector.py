import yfinance as yf
import pandas as pd
import requests, os
from datetime import datetime, timedelta

class MarketCollector:
    def __init__(self):
        self.crypto_symbols = ["BTC-USD", "ETH-USD"]
        self.stocks = ["AAPL", "TSLA", "NVDA"]
        self.indices = ["^GSPC", "^IXIC", "^DJI"]
        self.binance_url = "https://api.binance.com/api/v3/klines"

    def collect_yahoo(self, days_back=30):
        tickers = self.crypto_symbols + self.stocks + self.indices
        frames = []
        for t in tickers:
            try:
                df = yf.download(t, period=f"{days_back}d", interval="1d")
                df["Symbol"] = t
                frames.append(df)
            except Exception as e:
                print(f"[WARN] Yahoo data for {t} failed:", e)
        result = pd.concat(frames)
        os.makedirs("data/raw/market/", exist_ok=True)
        path = f"data/raw/market/market_{datetime.now().strftime('%Y%m%d')}.csv"
        result.to_csv(path)
        return result

    def collect_binance(self, symbol="BTCUSDT", limit=500):
        """Collect recent crypto candle data from Binance"""
        try:
            r = requests.get(self.binance_url, params={"symbol": symbol, "interval": "1h", "limit": limit})
            data = r.json()
            df = pd.DataFrame(data, columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "qav", "num_trades", "taker_base_vol", "taker_quote_vol", "ignore"
            ])
            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
            df["symbol"] = symbol
            os.makedirs("data/raw/binance/", exist_ok=True)
            df.to_csv(f"data/raw/binance/{symbol}_{datetime.now().strftime('%Y%m%d')}.csv", index=False)
            return df
        except Exception as e:
            print(f"[ERROR] Binance data fetch failed:", e)
            return pd.DataFrame()

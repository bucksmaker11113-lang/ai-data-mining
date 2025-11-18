# app/collectors/market_collector.py

def collector():
    """
    Dummy market collector.
    Később ide kerül a TradingView, Binance, Forex, Betfair adatgyűjtés.
    """
    return {
        "source": "market_collector",
        "status": "ok",
        "message": "market data collected successfully",
        "sample_data": {
            "symbol": "BTCUSD",
            "price": 43000,
            "timestamp": "2025-11-14"
        }
    }

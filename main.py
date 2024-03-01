import pandas as pd
from demo import backtester_demo
from strategies import MACrossStrategy


# Example usage
if __name__ == "__main__":
    # Ticker
    nasdaq_futures = 'NQ=F'

    # Simple Moving Average Demo (5-20 cross by default)
    SMA_strategy = MACrossStrategy()
    backtester_demo(nasdaq_futures, SMA_strategy, period="2y")

    # Exponential Moving Average Demo
    EMA_strategy = MACrossStrategy(ma_func=pd.Series.ewm)
    backtester_demo(nasdaq_futures, EMA_strategy, period="2y")

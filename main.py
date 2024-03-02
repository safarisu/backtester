import pandas as pd
from demo import backtester_demo
from strategies import MACrossStrategy
from utils import calculate_ema


# Example usage
if __name__ == "__main__":
    # Ticker
    nasdaq_futures = 'NQ=F'

    # Simple Moving Average Demo (10-50 cross by default)
    SMA_strategy = MACrossStrategy(short_window=5, long_window=20)
    backtester_demo(nasdaq_futures, SMA_strategy, period="1y", interval='1d')

    # Exponential Moving Average Demo
    # EMA_strategy = MACrossStrategy(ma_func=pd.DataFrame.ewm, short_window=5, long_window=20)
    # backtester_demo(nasdaq_futures, EMA_strategy, period="3y", interval='1d')

import pandas as pd
from demo import backtester_demo
from strategies import MACrossStrategy
from utils import calculate_ema


# Example usage
if __name__ == "__main__":
    # Ticker
    nasdaq_futures = 'NQ=F'
    eurusd = 'EURUSD=X'

    short_ma = 10
    long_ma = 50

    # Simple Moving Average Demo (10-50 cross by default)
    SMA_strategy = MACrossStrategy(short_window=short_ma, long_window=long_ma)
    backtester_demo(nasdaq_futures, SMA_strategy, period="3y", interval='1d',
                    equity_curve_title=f"Equity Curve for {short_ma}-{long_ma} SMA crossover strategy on {nasdaq_futures}")


    # Exponential Moving Average Demo
    EMA_strategy = MACrossStrategy(ma_func=pd.DataFrame.ewm, short_window=short_ma, long_window=long_ma)
    backtester_demo(eurusd, EMA_strategy, period="3y", interval='1d',
                    equity_curve_title=f"Equity Curve for {short_ma}-{long_ma} EMA crossover strategy on {eurusd}")

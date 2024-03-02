import pandas as pd


def moving_average(data: pd.DataFrame, window: int, ma_func):
    return ma_func(data['Close'], window, min_periods=window).mean()


class MACrossStrategy:
    """Simple strategy based on Moving Average crossovers - enter long on a bullish crossover and short on a bearish one"""
    def __init__(self, short_window=10, long_window=50, ma_func=pd.Series.rolling):
        self.short_window = short_window
        self.long_window = long_window
        self.ma_func = ma_func

    def generate_order(self, data, i):
        if i < max(self.short_window, self.long_window):
            return None

        data['short_ma'] = moving_average(data, self.short_window, self.ma_func)
        data['long_ma'] = moving_average(data, self.long_window, self.ma_func)

        if data['short_ma'].iloc[i] > data['long_ma'].iloc[i] and (data['short_ma'].iloc[i - 1] <= data['long_ma'].iloc[i - 1] or i == self.long_window):
            data.loc[data.index[i], 'signal'] = 'Buy'
            return 'Enter Long'
        elif data['short_ma'].iloc[i] < data['long_ma'].iloc[i] and (data['short_ma'].iloc[i - 1] >= data['long_ma'].iloc[i - 1] or i == self.long_window):
            data.loc[data.index[i], 'signal'] = 'Sell'
            return 'Enter Short'
        else:
            data.loc[data.index[i], 'signal'] = 'Neutral'
            return 'Neutral'
import pandas as pd
import matplotlib.pyplot as plt
from fetchdata import fetch_data as fd


def calculate_signals(data, short_window, long_window):
    data['short_ma'] = data['Close'].rolling(window=short_window).mean()
    data['long_ma'] = data['Close'].rolling(window=long_window).mean()

    # Apply rolling window smoothing to moving averages
    data['short_ma'] = data['short_ma'].rolling(window=5, min_periods=1).mean()
    data['long_ma'] = data['long_ma'].rolling(window=5, min_periods=1).mean()

    # Initialize the signal column
    data['signal'] = 'Neutral'

    # Generate signals only at the time of a crossover
    for i in range(1, len(data)):
        if data['short_ma'].iloc[i] > data['long_ma'].iloc[i] and data['short_ma'].iloc[i - 1] <= data['long_ma'].iloc[
            i - 1]:
            data.loc[data.index[i], 'signal'] = 'Buy'
        elif data['short_ma'].iloc[i] < data['long_ma'].iloc[i] and data['short_ma'].iloc[i - 1] >= \
                data['long_ma'].iloc[i - 1]:
            data.loc[data.index[i], 'signal'] = 'Sell'

    return data


def plot_chart(data, ticker, interval):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_facecolor("black")

    # Plot price line
    ax1.plot(data.index, data['Close'], label='Close Price', color='white')
    ax1.plot(data.index, data['short_ma'], label='Short MA', color='blue')
    ax1.plot(data.index, data['long_ma'], label='Long MA', color='red')

    # Plot buy signals
    buy_signals = data[data['signal'] == 'Buy']
    ax1.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', zorder=5)

    # Plot sell signals
    sell_signals = data[data['signal'] == 'Sell']
    ax1.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', zorder=5)

    ax1.set_title(f'{ticker} | {interval}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, color='grey')

    # # Create a second subplot for volume
    # ax2 = ax1.twinx()
    # ax2.bar(data.index, data['Volume'], color='gray', alpha=0.5, width=0.5)
    # ax2.set_ylabel('Volume')

    plt.show()


if __name__ == "__main__":
    # Parameters
    ticker = 'BTC-USD'  # Ticker symbol of the equity
    start_date = '2023-01-01'
    end_date = '2024-02-20'
    interval = '1d'  # Data frequency (e.g., 1d for daily, 1wk for weekly, 1mo for monthly)
    short_window = 10  # Short moving average window
    long_window = 50  # Long moving average window

    # Fetch equity data
    equity_data = fd(ticker, interval, start_date, end_date)

    # Calculate signals
    signals_data = calculate_signals(equity_data, short_window, long_window)

    # Plot chart
    plot_chart(signals_data, ticker, interval)

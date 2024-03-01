import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from adjustText import adjust_text
from matplotlib.collections import PathCollection

plt.style.use('dark_background')
plt.rcParams['grid.color'] = '#333333'
plt.rcParams.update({'figure.autolayout': True})
plt.rcParams['axes.facecolor'] = '#0E0E10'
figsize=(15, 9)

def ma_chart(data, trades, ticker, interval):
    plt.figure(figsize=figsize)

    # Plot price line
    plt.plot(data.index, data['Close'], label='Close Price', color='royalblue')
    # plt.xticks(data.index, data['Datetime'])

    # Set the locator for the x-axis ticker
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    # Plot short and long moving averages
    plt.plot(data.index, data['short_ma'], label='Short MA', color='orange', linewidth=1)
    plt.plot(data.index, data['long_ma'], label='Long MA', color='magenta', linewidth=1)

    # Plot buy and sell signals
    buy_signals = data[data['signal'] == 'Buy']
    sell_signals = data[data['signal'] == 'Sell']
    # Extract x and y coordinates of buy signals
    buy_offsets = plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal',
                              zorder=3).get_offsets()
    buy_x = buy_offsets[:, 0]
    buy_y = buy_offsets[:, 1]

    # Extract x and y coordinates of sell signals
    sell_offsets = plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal',
                               zorder=3).get_offsets()
    sell_x = sell_offsets[:, 0]
    sell_y = sell_offsets[:, 1]

    merged_x = np.concatenate((buy_x, sell_x))
    merged_y = np.concatenate((buy_y, sell_y))

    texts = []
    for trade in trades:
        if trade[0].startswith('Enter'):
            texts.append(plt.text(trade[1], trade[2], trade[0], ha='right', va='bottom'))

    plt.title(f'Ticker: {ticker} | Interval: {interval}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Adjust the positions of annotations to avoid overlap
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='white'), zorder=5, y=data['Close'],
                force_static=(0, 5), force_text=(0.5, 0.5), min_arrow_len=10)
    plt.show()


def equity_curve(portfolio_values, title='Equity Curve'):
    plt.figure(figsize=figsize)

    # Fix days issues
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.plot(portfolio_values['date'], portfolio_values['value'], label='Equity Curve', color='purple')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_return_distribution(data, ticker=None, interval=None):
    # Calculate daily returns
    data['Daily Return'] = data['Adj Close'].pct_change() * 100

    # Remove NaN values
    daily_returns = data['Daily Return'].dropna()

    # Calculate mean and standard deviation of daily returns
    mu = daily_returns.mean()
    sigma = daily_returns.std()

    # Plot histogram of daily returns:tho
    plt.figure(figsize=figsize)
    plt.hist(daily_returns, bins=100, density=True, alpha=0.6, color='b', label='Daily Returns')

    # Generate random normal bell curve
    x = np.linspace(mu - 6*sigma, mu + 6*sigma, 100)
    plt.plot(x, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2),
             color='black', linewidth=1, label='Normal Distribution')

    plt.title(f'{ticker} Daily Return Distribution')
    plt.xlabel('Daily Return (%)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()

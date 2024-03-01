from fetchdata import fetch_data as fd
from plotting import plot_return_distribution

if __name__ == "__main__":
    # Parameters
    ticker = '^GSPC'  # S&P 500 index ticker symbol
    period = 'max'
    interval = '1d'

    # Fetch S&P 500 data
    sp500_data = fd(ticker, interval, period=period)

    # Plot daily return distribution
    plot_return_distribution(sp500_data, ticker=ticker)

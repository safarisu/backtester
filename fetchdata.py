import os
import yfinance as yf
import pandas as pd


def fetch_data(ticker, interval, period="max", start_date=None, end_date=None):
    # Format filename
    filename = f"{ticker}_{interval}_{period}.csv"
    filepath = os.path.join('data', filename)

    # Check if the file already exists
    if os.path.exists(filepath):
        # Load data from file
        data = pd.read_csv(filepath, index_col=0)
        print(f"Data loaded from {filename}")
    else:
        # Create data folder if it does not exist
        if not os.path.exists('data'):
            os.makedirs('data')

        # Download data
        data = yf.download(ticker, interval=interval, period=period)

        # Save data to file
        data.to_csv(filepath)
        print(f"Data saved to {filename}")

    return data

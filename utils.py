import numpy as np


def calculate_ema(data, window):
    alpha = 2 / (window + 1)  # Calculate the smoothing factor

    # Calculate SMA for the first window data points
    sma_values = calculate_sma(data, window)

    # Initialize EMA with None values for the initial data points
    ema_values = [None] * (window - 1) + [sma_values[window - 1]]

    # Calculate EMA for subsequent data points
    for i in range(window, len(data)):
        ema = alpha * data.iloc[i] + (1 - alpha) * ema_values[-1]
        ema_values.append(ema)

    return ema_values


def calculate_sma(data, window):
    sma_values = [None] * (window - 1)

    # Calculate SMA for each window of data points
    for i in range(window, len(data) + 1):
        sma = data.iloc[i - window:i].mean()
        sma_values.append(sma)

    return sma_values
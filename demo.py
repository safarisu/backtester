import pandas

from Backtester import Backtester
from fetchdata import fetch_data
from plotting import ma_chart, equity_curve


def backtester_demo(ticker, strategy, initial_capital=100000, interval='1d', period='1y', equity_curve_title=None):
    equity_data = fetch_data(ticker, interval, period=period)
    backtester = Backtester(equity_data, initial_capital=initial_capital, strategy=strategy, position_sizing="percent")

    backtester.backtest()

    # Get the backtesting report
    backtesting_report = backtester.generate_report()
    trades = backtester.get_trades()
    portfolio_values = backtester.get_portfolio_values()

    print(backtesting_report)
    # print(backtester.get_portfolio_values())
    # print(pandas.DataFrame(trades))

    # To-do integrate charting with Backtester
    # Plot chart with buy and sell signals
    ma_chart(equity_data, trades, ticker, interval, period)

    # Plot portfolio's equity curve
    equity_curve(portfolio_values, title=equity_curve_title)



import pandas as pd


class Backtester:
    def __init__(self, equity_data, initial_capital=10000, strategy=None, short_selling=True, position_sizing="percent", position_size='max'):
        self.initial_capital = initial_capital
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []
        self.portfolio_values = []
        self.short_selling = short_selling
        self.equity_data = equity_data
        self.position_sizing = position_sizing
        self.position_size = position_size

    def execute_trade(self, trade_type, price, date):

        contract_size = 0
        if self.position_sizing == "percent":
            if self.position_size == 'max':
                contract_size = self.capital / price
            else:
                contract_size = self.position_size * self.capital / price
        elif self.position_sizing == "fixed":
            if self.position_size == 'max':
                contract_size = int(self.capital / price)
            else:
                contract_size = self.position_size

        if trade_type == 'Enter Long':
            self.position += contract_size
            self.capital -= contract_size * price
        elif trade_type == 'Enter Short':
            self.position -= contract_size
            self.capital += contract_size * price
        elif trade_type.startswith('Exit'):
            self.capital += self.position * price
            self.position = 0

        self.trades.append((trade_type, date, price, self.position))

        # Realize PnL of the trade on exit
        if trade_type.startswith('Exit'):
            value = self.capital + self.position * price
            pnl = value - self.portfolio_values[-1]['value']
            pnl_percent = pnl/self.portfolio_values[-1]['value']
            self.portfolio_values.append({'value': self.capital + self.position * price, 'date': date, 'pnl': pnl,
                                          'pnl_percent': pnl_percent, 'comment': trade_type})

    def backtest(self):
        data = self.equity_data
        # Initialize portfolio
        self.portfolio_values.append({'value': self.capital, 'date': data.index[0], 'comment': 'Initial Investment'})

        for i in range(len(data)):
            order_type = self.strategy.generate_order(data, i)

            if order_type == "Enter Long" and self.position == 0:
                self.execute_trade('Enter Long', data['Close'].iloc[i], data.index[i])

            elif order_type == "Enter Short" and self.position == 0:
                if self.short_selling:
                    self.execute_trade('Enter Short', data['Close'].iloc[i], data.index[i])

            elif order_type == "Enter Long" and self.position < 0:
                self.execute_trade('Exit Short', data['Close'].iloc[i], data.index[i])
                self.execute_trade('Enter Long', data['Close'].iloc[i], data.index[i])

            elif order_type == "Enter Short" and self.position > 0:
                self.execute_trade('Exit Long', data['Close'].iloc[i], data.index[i])
                if self.short_selling:
                    self.execute_trade('Enter Short', data['Close'].iloc[i], data.index[i])

            # Allow for strategies to generate exit signals that are acted on only if there's an appropriate position

        # exit position at the last datapoint
        if self.position != 0:
            self.execute_trade('Exit Backtest', data['Close'].iloc[-1], data.index[-1])

    def get_final_value(self):
        return self.capital

    def get_profit(self):
        return (self.get_final_value() - self.initial_capital)/self.initial_capital

    def get_trades(self):
        return self.trades

    def get_portfolio_values(self):
        return pd.DataFrame(self.portfolio_values)

    def get_buy_n_hold(self):
        data = self.equity_data
        final_close_price = data['Close'].iloc[-1]
        first_close_price = data['Close'].iloc[0]
        price_difference = final_close_price - first_close_price
        return price_difference/first_close_price

    def generate_report(self):
        report_str = "************\n"
        report_str += f"Initial capital: {self.initial_capital}\n"
        report_str += f"Final portfolio value: {self.get_final_value():.2f}\n"
        report_str += f"Gross Profit: {self.get_profit():.2%}\n"
        report_str += f"Buy-n-hold return {self.get_buy_n_hold():.2%}\n"

        portfolio_values = self.get_portfolio_values()
        report_str += f"Two-way trades executed: {len(portfolio_values) - 1}\n"

        average_pnl = portfolio_values['pnl'].mean()
        report_str += f"Average PnL: {average_pnl:.2f}\n"

        report_str += "************\n"

        return report_str



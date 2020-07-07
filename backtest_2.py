from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

from backtesting.test import SMA

stock = "TSLA"

class SmaCross(Strategy):
    n1 = 10
    n2 = 60

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

df = pd.read_csv(f"data/{stock}.csv", skiprows=1, names=("Date", "Open", "High", "Low", "Close","Adj Close", "Volume"), index_col=0)
df = df.interpolate()
df.index = pd.to_datetime(df.index)


bt = Backtest(df, SmaCross, cash=1000000, commission=.004)

bt.optimize(SmaCross,maximize="SQN", constraint=None, return_heatmap=True)

output = bt.run()

print(output)

bt.plot(filename=stock)
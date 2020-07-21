from backtesting import Backtest, Strategy #引入回測和交易策略功能

from backtesting.lib import crossover #引入判斷均線交會功能
from backtesting.test import SMA #引入繪製均線功能

import pandas as pd #引入pandas讀取股價歷史資料CSV檔

class SmaCross(Strategy): #交易策略命名為SmaClass，使用backtesting.py的Strategy功能
    n1 = 5 #設定第一條均線日數為5日(周線)
    n2 = 20 #設定第二條均線日數為20日(月線)，這邊的日數可自由調整

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1) #定義第一條均線為sma1，使用backtesting.py的SMA功能算繪
        self.sma2 = self.I(SMA, self.data.Close, self.n2) #定義第二條均線為sma2，使用backtesting.py的SMA功能算繪

    def next(self):
        if crossover(self.sma1, self.sma2): #如果周線衝上月線，表示近期是上漲的，則買入
            self.buy()
        elif crossover(self.sma2, self.sma1): #如果周線再與月線交叉，表示開始下跌了，則賣出
            self.sell()

stock = "TSLA" #設定要測試的股票標的名稱

df = pd.read_csv(f"data/{stock}.csv", index_col=0) #pandas讀取資料，並將第1欄作為索引欄
df = df.interpolate() #CSV檔案中若有缺漏，會使用內插法自動補值，不一定需要的功能
df.index = pd.to_datetime(df.index) #將索引欄資料轉換成pandas的時間格式，backtesting才有辦法排序


test = Backtest(df, SmaCross, cash=10000, commission=.002)
# 指定回測程式為test，在Backtest函數中依序放入(資料來源、策略、現金、手續費)

result = test.run() #原始結果

opt_result_equity = test.optimize(n1=range(5, 50, 5),  #將回測機器加入optimize屬性，定義短均線的周期為5~50(每次加5)，長均線的周期為10~120(每次加5)
                    n2=range(10, 120, 5),
                    maximize='Equity Final [$]',  #最佳化目標為最終資產最大化
                    constraint=lambda p: p.n1 < p.n2)  #限制n1及n2的範圍，只會計算n1小於n2的情況

opt_result_sqn = test.optimize(n1=range(5, 50, 5),  #將回測機器加入optimize屬性，定義短均線的周期為5~50(每次加5)，長均線的周期為10~120(每次加5)
                    n2=range(10, 120, 5),
                    maximize='Calmar Ratio',  #最佳化目標為SQN最大化
                    constraint=lambda p: p.n1 < p.n2)  #限制n1及n2的範圍，只會計算n1小於n2的情況
      
print("Original strategy")
print(result) #印出result結果
print() #空一行
print("Optimize strategy 1")
print(opt_result_equity)  #印出opt_result_equity結果
print() #空一行
print("Optimize strategy 2")
print(opt_result_sqn)  #印出opt_result_sqn結果

# test.plot(filename=f"./backtest_result/{stock}.html") #將線圖網頁依照指定檔名保存
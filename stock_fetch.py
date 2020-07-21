import yfinance as yf
import pandas as pd
from pandas_datareader import data
from datetime import datetime

yf.pdr_override() #以pandasreader常用的格式覆寫

target_stock = 'TLSA'  #股票代號變數

start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 6, 30) #設定資料起訖日期

df = data.get_data_yahoo([target_stock], start_date, end_date) #將資料放到Dataframe裡面

filename = f'./data/{target_stock}.csv' #以股票名稱命名檔案，放在data資料夾下面

df.to_csv(filename) #將df轉成CSV保存
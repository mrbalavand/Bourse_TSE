from tkinter import Text

import keras
import numpy as np
import pandas as pd
import pyodbc
import finpy_tse as fpy
import jdatetime
from datetime import datetime
# import keras as ker
# from keras import Input
# from keras.models import Model
# from keras.layers import Dense, Conv2D, Flatten, MaxPool2D
import sqlalchemy
from sqlalchemy import Integer, NVARCHAR




from sklearn import datasets
from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold, train_test_split
from sklearn.tree import DecisionTreeClassifier

import matplotlib.pyplot as plt
import pandas_ta as ta
import pytse_client as tse
from pytse_client import download_client_types_records
Name_SQL1=[]
AllStocks = []
Stock1 = fpy.Get_MarketWatch()
Stock2 = Stock1[0].Market
count = 0
url = "mssql+pyodbc://balavand:123456@localhost/BourseAnalysis?driver=SQL Server"
engine = sqlalchemy.create_engine(url, use_setinputsizes=False, fast_executemany=True)
conn1 = engine.connect()
i1 = 0

for item in Stock2.keys():
    print(Stock2[count])
    if Stock2[count] == "بورس":
        AllStocks.append(item)
        print(item.index)
    count = count + 1


for stockname in AllStocks:
    i1=i1+1
    try:

        Stock = fpy.Get_Price_History(
            stock=stockname,
            start_date='1401-12-01',
            end_date='1402-02-28',
            ignore_date=False,
            adjust_price=False,
            show_weekday=False,
            double_date=False)
    except:
        continue

    if Stock is None:
        continue
    try:
        # print(Stock["Close"])
        # exceldata=Stock['Close']ريال%،چپ            #exceldata.to_excel("data.xlsx")
        # print(DF4['Open'])
        label1 = []
        label2 = []
        Sname = pd.DataFrame()
        Sname1 = pd.DataFrame()
        # print(len(Stock['Close']))
        for i in range(0, len(Stock['Close']) + 1):
            # print(Stock['Close'][i+1])
            if i == len(Stock['Close']) - 1:
                break
            if Stock['Close'][i + 1] <= Stock['Close'][i]:
                label1.append(0)
            else:
                label1.append(1)

        # print(sum(label1))
        for i in range(0, len(label1) + 1):
            Sname.loc[i, 0] = stockname
            if sum(label1[i:i + 5]) >= 4:
                label2.append(stockname)
            else:
                label2.append(stockname)

        label3 = pd.DataFrame(label2)
        # print(label2)

        MFI = ta.mfi(Stock['High'], Stock['Low'], Stock['Close'], Stock['Volume'])

        STOCKRSI = ta.stochrsi(Stock['Close'])
        STOCKRSI.set_axis(['RSI1', 'RSI2'], axis='columns', inplace=True)
        MACD = ta.macd(Stock['Close'])
        MACD.set_axis(['MACD1', 'MACD2','MACD3'], axis='columns', inplace=True)
        SMA = ta.sma(Stock['Close'])

        Bollinger = ta.bbands(Stock['Close'])
        Bollinger.set_axis(['Bollinger1', 'Bollinger2', 'Bollinger3', 'Bollinger4', 'Bollinger5'], axis='columns', inplace=True)
        MOM = ta.mom(Stock['Close'])
        RSI = ta.rsi(Stock['Close'])



        for sn in range(0, len(RSI.index)):
            Name_SQL1.append(stockname)

        Name_SQL1 = pd.Series(Name_SQL1)

        # plt.plot(Stock['Close'],label = 'Price')
        # plt.plot(MFI,label = 'MFI')
        # plt.plot(STOCKRSI,label = 'STOCKRSI')
        # plt.plot(MACD,label = 'MACD')
        # plt.plot(SMA,label = 'SMA')
        # plt.plot(Bollinger,label = 'Bollinger')
        # plt.plot(MOM,label = 'MOM')
        # plt.plot(RSI,label = 'RSI')
        # plt.legend()
        # plt.show()

        Sname1 = pd.DataFrame(Sname)
        Sname2 = Sname1.drop(Sname1)
        print(Sname2)

        MainData = pd.concat([MFI, STOCKRSI.RSI1,STOCKRSI.RSI2, MACD.MACD1,MACD.MACD2,MACD.MACD3, SMA, Bollinger.Bollinger1,Bollinger.Bollinger2,Bollinger.Bollinger3,Bollinger.Bollinger4,Bollinger.Bollinger5, MOM, RSI, Stock['Close'] ,Name_SQL1], axis=1,ignore_index=True)

        MainData = MainData.fillna(0)
        MainData.set_axis(['A', 'B', 'C' ,'D', 'E', 'F' ,'G', 'H', 'I' ,'J', 'K', 'L' ,'M', 'N', 'O' ,'P'], axis='columns', inplace=True)

        Maindata1 = pd.concat([MainData.reset_index(), Sname1.reset_index()], axis=1)

        print(MainData.shape[1])
        row = MainData.shape[0]
        col = MainData.shape[1]

        # conn = pyodbc.connect('Driver={SQL Server};'
        # 'Server=.;'
        # 'Database=BourseAnalysis;'
        # 'Trusted_Connection=yes;')

        # cursor = conn.cursor()
        MainData.to_sql(name="Data1", con=engine, schema="dbo", if_exists="append", index=False)
        engine.dispose()
        print(f"stockname is {stockname} {i1}")
    except Exception as e:
        print(e)
    continue
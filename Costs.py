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

start_date1 = "1401-12-29"
end_date1 = "1402-01-31"

SD = start_date1.split("-")
ED = end_date1.split("-")

start_date2 = jdatetime.date(int(SD[0]), int(SD[1]), int(SD[2])).togregorian().strftime("%Y-%m-%d %H:%M:%S")

end_date2 = jdatetime.date(int(ED[0]), int(ED[1]), int(ED[2])).togregorian().strftime("%Y-%m-%d %H:%M:%S")






Stock1 = fpy.Get_MarketWatch()
Stock2 = Stock1[0].Market
count = 0
AllStocks = []

for item in Stock2.keys():
    print(Stock2[count])
    if Stock2[count] == "بورس":
        AllStocks.append(item)
        print(item.index)
    count = count + 1

# save_excel=True,
# save_path=
stockdate = []
stockname1 = []
i1 = 0

url = "mssql+pyodbc://balavand:123456@localhost/BourseAnalysis?driver=SQL Server"
engine = sqlalchemy.create_engine(url, use_setinputsizes=False, fast_executemany=True)
conn1 = engine.connect()

for stockname in AllStocks:
    i1 = i1 + 1
    try:

        tickers = tse.download(symbols=stockname, write_to_csv=True)
    except:
        continue

    try:

        ticker = tse.Ticker(stockname)

    except:
        continue

    try:

        Price_Stock = ticker.history
    except:
        continue

    for data_tse1 in Price_Stock:
        if data_tse1 == "date":

            date_tse1 = Price_Stock[data_tse1]
            date_tse1 = date_tse1
            for date1 in date_tse1:
                if len(str(date1.month)) == 1:
                    month1 = "0" + str(date1.month)
                else:
                    month1 = str(date1.month)

                if len(str(date1.day)) == 1:
                    day1 = "0" + str(date1.day)
                else:
                    day1 = str(date1.day)

                stockdate.append(str(date1.year) + month1 + day1)
                stockname1.append(stockname)
        elif data_tse1 == "close":
            close_price = Price_Stock[data_tse1]
            percent_price = close_price.pct_change() * 100
            percent_price = percent_price.fillna(0)

            percent_price = percent_price.round(0)

    stockdate1 = pd.DataFrame(stockdate)
    stockname2 = pd.DataFrame(stockname1)

    Tse_Data1 = pd.concat(
        [stockdate1, close_price, percent_price, stockname2], axis=1)

    Tse_Data1 = Tse_Data1.fillna(0)

    Tse_Data1.set_axis(['date_tse1', 'close_price', 'percent_price', 'Name_Sql'], axis='columns', inplace=True)

    # conn = pyodbc.connect('Driver={SQL Server};'
    # 'Server=.;'
    # 'Database=BourseAnalysis;'
    # 'Trusted_Connection=yes;')

    # server='localhost'
    # cursor = conn.cursor()

    Tse_Data1.to_sql(name="Tse_Price", con=engine, schema="dbo", if_exists="append", index=False)

    # for index, row in Tse_Data1.iterrows():
    # cursor.execute(f'''
    # INSERT INTO Tse_Price
    # (date_tse1,close_price,percent_price,Name_Sql)

    # VALUES(
    # N'{row[0]}',
    # {row["close"][0]},
    # {row["close"][1]},

    # N'{stockname}'
    # )
    # ''')
    # conn.commit()

    # conn.close()
    print(f"{stockname} {i1} is completed")
    engine.dispose()


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
i1 = 0

for stockname in AllStocks:
    i1 =i1+1
    Name_SQL = []
    Name_SQL1 = []
    try:

        tickers = tse.download(symbols=stockname, write_to_csv=True)
    except:
        continue

    try:

        ticker = tse.Ticker(stockname)

    except:
        continue

    try:
        Data2 = ticker.client_types

    except:
        continue

    for data_tse in Data2:
        if data_tse == "date":

            date_tse = Data2[data_tse]
        elif data_tse == "corporate_buy_count":
            corporate_buy_count = Data2[data_tse]

        elif data_tse == "corporate_buy_mean_price":
            corporate_buy_mean_price = Data2[data_tse]
        elif data_tse == "corporate_buy_value":
            corporate_buy_value = Data2[data_tse]
        elif data_tse == "corporate_buy_vol":
            corporate_buy_vol = Data2[data_tse]
        elif data_tse == "corporate_sell_count":
            corporate_sell_count = Data2[data_tse]
        elif data_tse == "corporate_sell_mean_price":
            corporate_sell_mean_price = Data2[data_tse]
        elif data_tse == "corporate_sell_value":
            corporate_sell_value = Data2[data_tse]

        elif data_tse == "corporate_sell_vol":
            corporate_sell_vol = Data2[data_tse]




        elif data_tse == "individual_buy_count":
            individual_buy_count = Data2[data_tse]

        elif data_tse == "individual_buy_mean_price":
            individual_buy_mean_price = Data2[data_tse]
        elif data_tse == "individual_buy_value":
            individual_buy_value = Data2[data_tse]
        elif data_tse == "individual_buy_vol":
            individual_buy_vol = Data2[data_tse]
        elif data_tse == "individual_sell_count":
            individual_sell_count = Data2[data_tse]
        elif data_tse == "individual_sell_mean_price":
            individual_sell_mean_price = Data2[data_tse]
        elif data_tse == "individual_sell_value":
            individual_sell_value = Data2[data_tse]

        elif data_tse == "individual_sell_vol":
            individual_sell_vol = Data2[data_tse]




    for sn in range(0, len(individual_sell_vol)):
        Name_SQL.append(stockname)

    Name_SQL=pd.DataFrame(Name_SQL)

    Tse_Data = pd.concat(
        [date_tse, corporate_buy_count, corporate_buy_mean_price, corporate_buy_value,
         corporate_buy_vol, corporate_sell_count, corporate_sell_mean_price,
         corporate_sell_value,
         corporate_sell_vol, individual_buy_count, individual_buy_mean_price,
         individual_buy_value, individual_buy_vol, individual_sell_count,
         individual_sell_mean_price, individual_sell_value, individual_sell_vol,Name_SQL], axis=1)

    Tse_Data = Tse_Data.fillna(0)


    #conn = pyodbc.connect('Driver={SQL Server};'
                          #'Server=.;'
                          #'Database=BourseAnalysis;'
                          #'Trusted_Connection=yes;')

    #cursor = conn.cursor()
    Tse_Data.to_sql(name="Tse_Data", con=engine, schema="dbo", if_exists="append", index=False)


    engine.dispose()



  


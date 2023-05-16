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
            corporate_buy_count_tse = Data2[data_tse]

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

    Tse_Data = pd.concat(
        [date_tse, corporate_buy_count_tse, corporate_buy_mean_price, corporate_buy_value,
         corporate_buy_vol, corporate_sell_count, corporate_sell_mean_price,
         corporate_sell_value,
         corporate_sell_vol, individual_buy_count, individual_buy_mean_price,
         individual_buy_value, individual_buy_vol, individual_sell_count,
         individual_sell_mean_price, individual_sell_value, individual_sell_vol], axis=1)

    Tse_Data = Tse_Data.fillna(0)

    #conn = pyodbc.connect('Driver={SQL Server};'
                          #'Server=.;'
                          #'Database=BourseAnalysis;'
                          #'Trusted_Connection=yes;')

    #cursor = conn.cursor()
    Tse_Data.to_sql(name="Tse_Data", con=engine, schema="dbo", if_exists="append", index=False)

    for index, row in Tse_Data.iterrows():
        cursor.execute(f'''
                   INSERT INTO Tse_Data
                   (date_tse,corporate_buy_count_tse,corporate_buy_mean_price_tse,corporate_buy_value_tse,
                   corporate_buy_vol_tse,corporate_sell_count_tse,corporate_sell_mean_price_tse,corporate_sell_value_tse,
                   corporate_sell_vol_tse,individual_buy_count_tse,individual_buy_mean_price_tse,
                   individual_buy_value_tse,individual_buy_vol_tse,
                   individual_sell_count_tse,individual_sell_mean_price_tse,individual_sell_value_tse,individual_sell_vol_tse,Name_SQL
                   )
                   VALUES
                   ({row[0]},
                    {row[1]},
                    {row[2]},
                    {row[3]},
                    {row[4]},
                    {row[5]},
                    {row[6]},
                    {row[7]},
                    {row[8]},
                    {row[9]},
                    {row[10]},
                    {row[11]},
                    {row[12]},
                    {row[13]},
                    {row[14]},
                    {row[15]},
                    {row[16]},

                    N'{stockname}'
                    )
                    ''')
        conn.commit()
    conn.close()



    try:

        Stock = fpy.Get_Price_History(
            stock=stockname,
            start_date='1400-10-30',
            end_date='1402-01-19',
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
        MACD = ta.macd(Stock['Close'])
        SMA = ta.sma(Stock['Close'])
        Bollinger = ta.bbands(Stock['Close'])
        MOM = ta.mom(Stock['Close'])
        RSI = ta.rsi(Stock['Close'])

        st1 = Bollinger.iloc[:, 1]

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

        MainData = pd.concat([MFI, STOCKRSI, MACD, SMA, Bollinger, MOM, RSI, Stock['Close']], axis=1)

        MainData = MainData.fillna(0)
        Maindata1 = pd.concat([MainData.reset_index(), Sname1.reset_index()], axis=1)

        print(MainData.shape[1])
        row = MainData.shape[0]
        col = MainData.shape[1]

        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.;'
                              'Database=BourseAnalysis;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        MainData.to_sql(name="Tse_Price", con=engine, schema="dbo", if_exists="append", index=False)
        for index, row in MainData.iterrows():
            cursor.execute(f'''
                       INSERT INTO Data1
                       (MFI_SQL
                       ,STOCKRSI1_SQL
                       ,STOCKRSI2_SQL
                       ,MACD1_SQL
                       ,MACD2_SQL
                       ,MACD3_SQL
                       ,SMA_SQL
                       ,Bollinger1_SQL
                       ,Bollinger2_SQL
                       ,Bollinger3_SQL
                       ,Bollinger4_SQL
                       ,Bollinger5_SQL
                       ,MOM_SQL
                       ,RSI_SQL
                       ,Price_SQL
                       ,Name_SQL)
                       VALUES
                       ({row[0]},
                        {row[1]},
                        {row[2]},
                        {row[3]},
                        {row[4]},
                        {row[5]},
                        {row[6]},
                        {row[7]},
                        {row[8]},
                        {row[9]},
                        {row[10]},
                        {row[11]},
                        {row[12]},
                        {row[13]},
                        {row[14]},
                        N'{stockname}'
                        )
                        ''')
            conn.commit()
        conn.close()
        print(f"stockname is {stockname}")
    except:
        continue


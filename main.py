import keras
import numpy as np
import pandas as pd
import pyodbc
import finpy_tse as fpy
#import keras as ker
#from keras import Input
#from keras.models import Model
#from keras.layers import Dense, Conv2D, Flatten, MaxPool2D
import sqlalchemy as sqlalchemy
from sklearn import datasets
from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold, train_test_split
from sklearn.tree import DecisionTreeClassifier
import sqlalchemy


import matplotlib.pyplot as plt
import pandas_ta as ta


Stock1=fpy.Get_MarketWatch(
    save_excel=True,
    save_path='D:/Bourse/Stocks.xlsx');


for stocking in Stock1:
    for j in stocking:
        if j=="Name":
           for stockgroup in stocking["Name"].axes:
               for stockname in stockgroup:

                print(stocking["Name"].axes)

                Stock = fpy.Get_Price_History(
                    stock=stockname,
                    start_date='1400-11-30',
                    end_date='1401-12-28',
                    ignore_date=False,
                    adjust_price=False,
                    show_weekday=False,
                    double_date=False)

                if len(Stock["Close"])==0:
                    break
                print(Stock["Close"])
    #exceldata=Stock['Close']ريال%،چپ            #exceldata.to_excel("data.xlsx")
                    #print(DF4['Open'])
                label1=[];
                label2=[];
                Sname=pd.DataFrame();
                Sname1=pd.DataFrame();
                #print(len(Stock['Close']))
                for i in range(0,len(Stock['Close'])+1):
                    #print(Stock['Close'][i+1])
                    if i==len(Stock['Close'])-1:
                        break
                    if Stock['Close'][i+1]<=Stock['Close'][i]:
                        label1.append(0)
                    else:
                        label1.append(1)

                #print(sum(label1))
                for i in range(0,len(label1)+1):
                    Sname.loc[i,0]=stockname
                    if sum(label1[i:i+5]) >= 4:
                        label2.append(stockname)
                    else:
                        label2.append(stockname)


                label3=pd.DataFrame(label2)
                #print(label2)

                ALMA=ta.alma(Stock['Close'])
                DEMA=ta.dema(Stock['Close'])
                EMA=ta.ema(Stock['Close'])
                FWMA=ta.fwma(Stock['Close'])

                HL2=ta.hl2(Stock['High'],Stock['Low'])
                HLC3=ta.hlc3(Stock['High'],Stock['Low'],Stock['Close'])
                HMA=ta.hma(Stock['Close'])
                HWMA=ta.hwma(Stock['Close'])
                #PSAR=ta.psar(Stock['High'],Stock['Low'],Stock['Close'])
                #JMA=ta.jma(Stock['Close'])
                KAMA=ta.kama(Stock['Close'])
                LINREG=ta.linreg(Stock['Close'])
                MCGD=ta.mcgd(Stock['Close'])
                MIDPOINT=ta.midpoint(Stock['Close'])
                MIDPRICE=ta.midprice(Stock['High'],Stock['Low'])
                OHLC4=ta.ohlc4(Stock['Open'],Stock['High'],Stock['Low'],Stock['Close'])
                PWMA=ta.pwma(Stock['Close'])
                RMA=ta.rma(Stock['Close'])
                SSF=ta.ssf(Stock['Close'])

                SWMA=ta.swma(Stock['Close'])
                T3=ta.t3(Stock['Close'])
                TEMA=ta.tema(Stock['Close'])
                TRIMA=ta.trima(Stock['Close'])
                VIDYA=ta.vidya(Stock['Close'])
                #VWAP=ta.vwap(Stock['High'],Stock['Low'],Stock['Close'],Stock['Volume'])
                WCP=ta.wcp(Stock['High'],Stock['Low'],Stock['Close'])
                WMA=ta.wma(Stock['Close'])
                ZELMA=ta.zlma(Stock['Close'])
                ZLMA1 = ta.zlma(Sname1)


                #volume
                AD=ta.ad(Stock['High'],Stock['Low'],Stock['Close'],Stock['Volume'])
                ADOSC=ta.adosc(Stock['High'],Stock['Low'],Stock['Close'],Stock['Volume'])

                CMF=ta.cmf(Stock['High'],Stock['Low'],Stock['Close'],Stock['Volume'])
                EFI=ta.efi(Stock['Close'],Stock['Volume'])
                EOM=ta.eom(Stock['High'],Stock['Low'],Stock['Close'],Stock['Volume'])
                KVO=ta.kvo(Stock['High'],Stock['Low'],Stock['Close'],Stock['Volume'])
                MFI=ta.mfi(Stock['High'],Stock['Low'],Stock['Close'],Stock['Volume'])
                NVI=ta.nvi(Stock['Close'],Stock['Volume'])
                OBV=ta.obv(Stock['Close'],Stock['Volume'])
                PVI=ta.pvi(Stock['Close'],Stock['Volume'])


                #Momentum
                MOM = ta.mom(Stock['Close'])
                RSI=ta.rsi(Stock['Close'])


                #Trend
                ADX = ta.adx(Stock['High'],Stock['Low'],Stock['Close'])

                #Volatility
                ATR = ta.atr(Stock['High'], Stock['Low'], Stock['Close'])


                #Price
                Price=Stock['Close']
                #PVR=ta.pvr(Stock['Close'],Stock['Volume'])
                #PVT=ta.pvi(Stock['Close'],Stock['Volume'])
                #VP=ta.vp(Stock['Close'],Stock['Volume'])

                LOG_RETURN=ta.percent_return(Stock['Close'])
                Sname1=pd.DataFrame(Sname);
                Sname2=Sname1.drop(Sname1)
                print(Sname2)


                MainData=pd.concat([ALMA,DEMA,EMA,FWMA,HL2,HLC3,HMA,HWMA,KAMA,LINREG,MCGD,MIDPOINT,MIDPRICE,OHLC4,PWMA,RMA,SSF,SWMA,T3,TEMA,TRIMA,VIDYA,WCP,WMA,ZELMA,AD,
                                    ADOSC,CMF,EFI,EOM,KVO,MFI,NVI,OBV,PVI,
                                    MOM,RSI,ADX,ATR,Price],axis=1)



                MainData=MainData.fillna(0)
                Maindata1 = pd.concat([MainData.reset_index(), Sname1.reset_index()],axis=1)

                print(MainData.shape[1])
                row=MainData.shape[0]
                col=MainData.shape[1]

                conn = pyodbc.connect('Driver={SQL Server};'
                                      #'Server=.;'
                                      #'Database=BourseAnalysis;'
                                      #'Trusted_Connection=yes;')



                engine = sqlalchemy.create_engine("mssql+pyodbc://.@BourseAnalysis")

                # write the DataFrame to a table in the sql database
                Maindata1.to_sql("Data", engine)

                with pd.ExcelWriter('Data1.xlsx', engine="openpyxl", mode='a') as writer:
                    Maindata1.to_excel(writer,sheet_name="name")

                Maindata1.to_excel("Data1.xlsx")
                #Sname1.to_excel("Data2.xlsx")



MainData=MainData.to_numpy()
label3=label3.to_numpy()

n_split=3
for train_index,test_index in KFold(n_split).split(label3):
  x_train,x_test=MainData[train_index,1:],MainData[test_index,1:]
  y_train,y_test=label3[train_index,:],label3[test_index,:]
#train the model


#add model layers
myMoodel=Sequential()
myMoodel.add(Dense(500,activation="relu",input_shape=(15,)))
myMoodel.add(Dense(100,activation="relu"))
myMoodel.add(Dense(1,activation="softmax"))
myMoodel.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
              loss=keras.losses.categorical_crossentropy,metrics=["accuracy"])


netwrok_history=myMoodel.fit(x_train,y_train,epochs=100)
test_loss,test_accu=myMoodel.evaluate(x_test,y_test)
test_label=myMoodel.predict(x_test)


#model.fit(x_train, y_train, epochs=3)


plt.plot(Stock['Close'])
plt.plot(CCI)
plt.plot(STOCH)
plt.plot(RSI)
plt.show()







import keras
import numpy as np
import pandas as pd

import finpy_tse as fpy
import keras as ker
from keras import Input
from keras.models import Model
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D
from sklearn import datasets
from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold, train_test_split
from sklearn.tree import DecisionTreeClassifier


import matplotlib.pyplot as plt
import pandas_ta as ta




Stock = fpy.Get_Price_History(
    stock='خودرو',
    start_date='1400-01-01',
    end_date='1401-01-01',
    ignore_date=False,
    adjust_price=False,
    show_weekday=False,
    double_date=False)


#exceldata=Stock['Close']
#exceldata.to_excel("data.xlsx")
#print(DF4['Open'])
label1=[];
label2=[];
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

    if sum(label1[i:i+5]) >= 4:
        label2.append(1)
    else:
        label2.append(0)


label3=pd.DataFrame(label2)
#print(label2)

MACD=ta.macd(Stock['Close'])
SMA=ta.sma(Stock['Close'])
RSI=ta.rsi(Stock['Close'])
MOM=ta.mom(Stock['Close'])
MA=ta.ma(Stock['Close'])
STOCH=ta.stoch(Stock['High'],Stock['Low'],Stock['Close'])
VOL=Stock['Volume']
STD=ta.stdev(Stock['Close'])
PSAR=ta.psar(Stock['High'],Stock['Low'],Stock['Close'])
ENTROPY=ta.entropy(Stock['Close'])
WILL=ta.willr(Stock['High'],Stock['Low'],Stock['Close'])
OBV=ta.obv(Stock['Close'],Stock['Volume'])
CCI=ta.cci(Stock['High'],Stock['Low'],Stock['Close'])



MainData=pd.DataFrame()
MainData=pd.concat([MACD,SMA,RSI,MOM,MA,VOL,STD,PSAR,ENTROPY,WILL,OBV,CCI],axis=1)
MainData=MainData.fillna(0)
print(MainData.shape)
#print(MainData)
#print(type(label2))

#kfold cross validation




#print(len(MACD))
#print(len(SMA))
#print(len(RSI))
#print(len(MOM))
#print(len(SMA))
#print(len(STOCH))
#print(len(VOL))
#print(len(STD))
#print(len(PSAR))
#print(len(ENTROPY))
#print(len(WILL))
#print(len(OBV))
#print(len(CCI))
#print(len(MA))
#Main_Data=pd.merge(MACD,SMA,RSI)

print(MainData.shape)





n_split=3
for train_index,test_index in KFold(n_split).split(label3):
  x_train,x_test=MainData.iloc[train_index,:],MainData.iloc[test_index,:]
  y_train,y_test=label3.iloc[train_index,:],label3.iloc[test_index,:]
#train the model


#add model layers
myInput=Input(shape=(len(x_train),16,1))
conv1=Conv2D(16,3, activation='relu')(myInput)
pool1=MaxPool2D(pool_size=2)(conv1)
conv2=Conv2D(32,3, activation='relu')(pool1)
pool2=MaxPool2D(pool_size=2)(conv2)
flat=Flatten()(pool2)
outLayer=Dense(10,activation='softmax')(flat)

myModel=Model(myInput,outLayer)
myModel.summary()
myModel.compile()
n_rows=print(len(x_train))

#model.fit(x_train, y_train, epochs=3)


plt.plot(Stock['Close'])
plt.plot(CCI)
plt.plot(STOCH)
plt.plot(RSI)
plt.show()







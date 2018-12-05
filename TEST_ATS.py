
import numpy as np
import urllib.request, json 
import pandas as pd
import matplotlib.pyplot as plt
#1.  sma algorithme

def sma_algo(data,window):
	weights=np.repeat(1.0,window)
	sma=np.convolve(data,weights/window,'valid')
	return(sma)


#2 Import data

with urllib.request.urlopen("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo)") as url:
    data = json.loads(url.read().decode())
   


#3

def average_price(date):

    high=data['Time Series (Daily)'][date]['2. high']
    low=data['Time Series (Daily)'][date]['3. low']
    average_price=(float(high)+float(low))/2
    print(average_price)

#4


data=data['Time Series (Daily)']
df1 = pd.DataFrame(data).T
#rename columns
df1 = df1.rename(columns={'2. high':'Hight','3. low':'Low'})
#change data type
df1['Hight']=df1['Hight'].astype(float)
df1['Low']=df1['Low'].astype(float)
df1['Averge Price']=(df1['Hight'] + df1['Low'])/2
#Calculate SMA values
sma=sma_algo(df1['Averge Price'],5)
sma =pd.DataFrame(sma)

#5
#Extract date
date=pd.DataFrame(df1.index)
date=date.drop(axis=1,index=[0,1,2,3])
date.index = np.arange(len(date.index))
#create new dataframe with sma values and the date
df= pd.concat([date,sma], axis=1,ignore_index=True).transpose()
df= df.T.set_index(0)[1].rename('sma').astype(float)
df1['SMA']=df
print(df1)
#visualize data
df1[['Averge Price','SMA']].plot(grid=True)
plt.title('SMA and Averge Price')
plt.show()

#Calculate the profit
buy_actions= df1.loc[df1['SMA'] < df1['Averge Price'],'Averge Price'].sum()
sell_action= df1.loc[df1['SMA'] > df1['Averge Price'],'SMA'].sum()
profit=sell_action-buy_actions
print("user's profit:",profit)
print(profit)
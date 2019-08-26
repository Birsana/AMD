import pandas as pd
from datetime import datetime
from secScraper import earningDates


#this code is VERY messy

url1 = 'https://raw.githubusercontent.com/Birsana/AMD/master/amdData.csv'
dfAMD= pd.read_csv(url1)

url2= 'https://raw.githubusercontent.com/Birsana/AMD/master/INTC.csv'
dfINT = pd.read_csv(url2)

url3 = 'https://raw.githubusercontent.com/Birsana/AMD/master/%5EGSPC.csv'
dfSP = pd.read_csv(url3)




dfINT.drop(dfINT.tail(1).index,inplace=True)
dfSP.drop(dfSP.tail(1).index,inplace=True)


ocPercentAMD = [None]
hlPercentAMD = [None]
ocPercentINT = [None]
hlPercentINT = [None]
ocPercentSP = [None]
hlPercentSP = [None]

for i in range(1,dfAMD.Open.count()):
    open = dfAMD.iloc[i-1]['Open']
    close = dfAMD.iloc[i-1]['Close']

    high = dfAMD.iloc[i-1]['High']
    low = dfAMD.iloc[i-1]['Low']
    ocPercentAMD.append((close/open-1)*100)
    hlPercentAMD.append((high/low- 1)*100)


for i in range(1,dfINT.Open.count()):
    open = dfINT.iloc[i-1]['Open']
    close = dfINT.iloc[i-1]['Close']

    high = dfINT.iloc[i-1]['High']
    low = dfINT.iloc[i-1]['Low']
    ocPercentINT.append((close/open-1)*100)
    hlPercentINT.append((high/low- 1)*100)


for i in range(1,dfSP.Open.count()):
    open = dfSP.iloc[i-1]['Open']
    close = dfSP.iloc[i-1]['Close']

    high = dfSP.iloc[i-1]['High']
    low = dfSP.iloc[i-1]['Low']
    ocPercentSP.append((close/open-1)*100)
    hlPercentSP.append((high/low- 1)*100)

dates = []
for i in range(dfAMD.Date.count()):
    dates.append(dfAMD.iloc[i]['Date'])

dateFormat = "%Y-%m-%d"

for i in range(len(dates)):
    dates[i] = datetime.strptime(dates[i], dateFormat)

pElect = ["11/3/2020", "11/8/2016", "11/6/2012", "11/4/2008", "11/2/2004", "11/7/2000", "11/5/1996"]
for i in range(len(pElect)):
    dateForm = "%m/%d/%Y"
    pElect[i] = datetime.strptime(pElect[i], dateForm)

daysFromPElect = []

weekdays = []
for i in range(len(dates)):
    weekdays.append(dates[i].weekday())

daysToEarnings = []

for i in range(len(dates)):
    daysSinceEarnings = 1000000
    for j in range(len(earningDates)):
        if 0 < (dates[i] - earningDates[j]).days < daysSinceEarnings:
            daysSinceEarnings = (dates[i]-earningDates[j]).days
    daysToEarnings.append(daysSinceEarnings)
for i in range(len(dates)):
    daysSinceElect = 1000000
    for j in range(len(pElect)):
        if 0 < (dates[i] - pElect[j]).days < daysSinceElect:
            daysSinceElect = (dates[i]-pElect[j]).days
    daysFromPElect.append(daysSinceElect)


tyPercentAMD = [None]
tyPercentSP = [None]
tyPercentINT = [None]

label = []

for i in range(1, dfAMD.Open.count()):
    open = dfAMD.iloc[i]['Open']
    clo =  dfAMD.iloc[i-1 ]['Close']
    tyPercentAMD.append((open/clo-1)*100)

for i in range(dfAMD.Open.count()):
    open = dfAMD.iloc[i]['Open']
    clo = dfAMD.iloc[i]['Close']
    if open < clo:
        label.append(1)
    else:
        label.append(0)

for i in range(1, dfINT.Open.count()):
    open = dfINT.iloc[i]['Open']
    clo =  dfINT.iloc[i-1 ]['Close']
    tyPercentINT.append((open/clo-1)*100)


for i in range(1, dfSP.Open.count()):
    open = dfSP.iloc[i]['Open']
    clo =  dfSP.iloc[i-1]['Close']
    tyPercentSP.append((open/clo-1)*100)

dfAMD.rename(columns = {"Open": "OpenAMD", "Close": "CloseAMD", "Volume": "VolumeAMD"})
dfINT.rename(columns = {"Open": "OpenINT", "Close": "CloseINT", "Volume": "VolumeINT"})
dfINT.rename(columns = {"Open": "OpenSP", "Close": "CloseSP"})

dfAMD = dfAMD.drop(['Adj Close', 'Date', 'Open', 'Close', 'High', 'Low', 'Adj Close'], axis = 1)
dfINT = dfINT.drop(['Adj Close', 'Date' ,'Open', 'High', 'Close', 'Low', 'Adj Close'], axis = 1)
dfSP = dfSP.drop(['Adj Close', 'Date', 'Volume', 'Open', 'Close', 'High', 'Low', 'Adj Close'], axis = 1)

dfAMD['ocPercentAMD'] = ocPercentAMD
dfAMD['ocPercentINT'] = ocPercentINT
dfAMD['ocPercentSP'] = ocPercentSP

dfAMD['hlPercentAMD'] = hlPercentAMD
dfAMD['hlPercentINT'] = hlPercentINT
dfAMD['hlPercentSP'] = hlPercentSP

dfAMD['Days to Earnings'] = daysToEarnings

dfAMD['tyPercentAMD'] = tyPercentAMD
dfAMD['tyPercentINT'] = tyPercentINT
dfAMD['tyPercentSP'] = tyPercentSP

dfAMD = pd.concat([dfAMD, dfSP, dfINT], axis = 1)

dfAMD['What Day'] = weekdays
dfAMD['Labels'] = label

dfAMD["Days Since Election"] = daysFromPElect

dfAMD.to_csv('AMDMLDATA.csv')



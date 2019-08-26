import pandas as pd
from datetime import datetime
from datetime import datetime



url1 = 'https://raw.githubusercontent.com/Birsana/AMD/master/amdData.csv'
dfAMD= pd.read_csv(url1)
dates = []
for i in range(dfAMD.Date.count()):
    dates.append(dfAMD.iloc[i]['Date'])

dateFormat = "%Y-%m-%d"

for i in range(len(dates)):
    dates[i] = datetime.strptime(dates[i], dateFormat)

url = "https://raw.githubusercontent.com/Birsana/AMD/master/bitcoindata.csv"
dfBTC = pd.read_csv(url)


realVolume = []
days = []

for i in range(dfBTC.Price.count()):
    days.append(dfBTC.iloc[i]["Date"])

for i in range(len(days)):
    days[i] = days[i].replace("Jan", "January")
    days[i] = days[i].replace("Feb", "February")
    days[i] = days[i].replace("Mar", "March")
    days[i] = days[i].replace("Apr", "April")
    days[i] = days[i].replace("Jun", "June")
    days[i] = days[i].replace("Jul", "July")
    days[i] = days[i].replace("Aug", "August")
    days[i] = days[i].replace("Sep", "September")
    days[i] = days[i].replace("Oct", "October")
    days[i] = days[i].replace("Nov", "November")
    days[i] = days[i].replace("Dec", "December")
    dayForm = "%B %d, %Y"
    days[i] = datetime.strptime(days[i], dayForm)

containColumn = []

for i in range(len(days)):
    if days[i] in dates:
        containColumn.append(1)
    else:
        containColumn.append(0)

containColumn.reverse()


for i in range(dfBTC.Price.count()):
    dayVol = dfBTC.iloc[i]["Vol."].replace("K", "")
    dayVol = dayVol.replace("M", "")

    dayVol = float(dayVol)*1000
    realVolume.append(dayVol)


dfBTC = dfBTC.drop(["Date", "Vol.", "Change %"], axis = 1)
dfBTC["Price"] = dfBTC["Price"].str.replace(",", "")
dfBTC["Price"] = dfBTC["Price"].astype(float)
dfBTC["Open"] = dfBTC["Open"].str.replace(",", "")
dfBTC["Open"] = dfBTC["Open"].astype(float)
dfBTC["High"] = dfBTC["High"].str.replace(",", "")
dfBTC["High"] = dfBTC["High"].astype(float)
dfBTC["Low"] = dfBTC["Low"].str.replace(",", "")
dfBTC["Low"] = dfBTC["Low"].astype(float)

dfBTC["Valid_Days"] = containColumn

ocPercentBTC = [None]
hlPercentBTC = [None]

for i in range(1,dfBTC.Price.count()):
    open = dfBTC.iloc[i-1]['Open']
    close = dfBTC.iloc[i-1]['Price']

    high = dfBTC.iloc[i-1]['High']
    low = dfBTC.iloc[i-1]['Low']
    ocPercentBTC.append((close/open-1)*100)
    hlPercentBTC.append((high/low- 1)*100)



dfBTC = dfBTC.drop(['Open', 'High', 'Low', 'Price'], axis = 1)

dfBTC['ocPercentBTC'] = ocPercentBTC
dfBTC['hlPercentBTC'] = hlPercentBTC

dfBTC = dfBTC[dfBTC.Valid_Days != 0]

dfBTC = dfBTC.drop(["Valid_Days"], axis = 1)

dfML = pd.read_csv("/Users/andreb/PycharmProjects/AMDPredict/AMDMLDATA.csv")

dfML = dfML.iloc[::-1]
#dfML.reindex(index=dfML.index[::-1])

while len(ocPercentBTC) < len(dfML.index):
    ocPercentBTC.append(None)
    hlPercentBTC.append(None)

dfML["ocPercentBTC"] = ocPercentBTC
dfML["hlPercentBTC"] = hlPercentBTC

dfML = dfML.drop(["Unnamed: 0"], axis = 1)
dfML.to_csv('AMDINTBTCSP.csv')

from locale import D_FMT
from pydoc import resolve
import requests
import time
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import pymysql
import json
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
from datetime import datetime
from sqlalchemy import create_engine


#Useful Links
#https://towardsdatascience.com/how-to-convert-json-into-a-pandas-dataframe-100b2ae1e0d8
#https://stackoverflow.com/questions/19231871/convert-unix-time-to-readable-date-in-pandas-dataframe

#Define Variables and Tables
instrumentTypes = ["FUTURES","SPOT","SWAP", "OPTION"]  
optionuly = ["BTC-USD", "ETH-USD"]  
instrumentEconomics = pd.DataFrame()
marketTickr = pd.DataFrame()
newData = []
newData2 = []
newData3 = []

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Step 1 : Extracting the Tickr Info and Data Attributes
#-----------------------------------------------------------------------------------------------------------------------------------------------

#Looping through instrument types
for i in instrumentTypes:

    url = ("https://www.okx.com/api/v5/market/tickers?instType=" + i)
    payload = ""
    headers = {'8e6497fd-9a0e-4407-a847-baeb0663372d': '5B532F8EDCC358A12FF244F821D14203','Cookie': 'locale=en-US'}
    response = requests.request("GET", url, headers=headers, data=payload)

    #JSON Loading and adding iterative data to dictionary
    data = json.loads(response.text)
    newData.append(data)

#Extracting nested data and putting it into a dataframe
df = pd.json_normalize(newData, record_path =['data'])
marketTickr = df[['instId','instType','volCcy24h','vol24h','askPx','askSz','bidPx','bidSz']]

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Step 2 : Extracting the Instrument and Contract Economic Attributes
#-----------------------------------------------------------------------------------------------------------------------------------------------

#Looping through instrument types
for i in instrumentTypes:

    #for option contracts we require an additional input i.e. uly 
    if i == "OPTION":
        for uly in optionuly:
            url = ("https://www.okx.com/api/v5/public/instruments?instType=" + i + "&uly=" + uly)
            payload = ""
            headers = {'8e6497fd-9a0e-4407-a847-baeb0663372d': '5B532F8EDCC358A12FF244F821D14203','Cookie': 'locale=en-US'}
            response = requests.request("GET", url, headers=headers, data=payload)
             
            #Load JSON and add iterative data to dictionary
            data = json.loads(response.text)
            newData2.append(data)    
            
    #iterate through all the other instrument types except options
    else:
        url = ("https://www.okx.com/api/v5/public/instruments?instType=" + i)
        payload = ""
        headers = {'8e6497fd-9a0e-4407-a847-baeb0663372d': '5B532F8EDCC358A12FF244F821D14203','Cookie': 'locale=en-US'}
        response = requests.request("GET", url, headers=headers, data=payload)

        #Load JSON and add iterative data to dictionary
        data = json.loads(response.text)
        newData2.append(data)

#Extracting nested data in dict and saving it into a panda dataframe
df = pd.json_normalize(newData2, record_path =['data'])
df['expTime'] = pd.to_datetime(df['expTime'], unit='ms')
df['listTime'] = pd.to_datetime(df['listTime'], unit='ms')

instrumentEconomics = df[['instId','instType','uly','state','ctType','stk','optType','quoteCcy','baseCcy','ctValCcy','settleCcy','listTime','expTime']]

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Step 3 : Extracting the Open Interest of each Derivative Contract
#-----------------------------------------------------------------------------------------------------------------------------------------------

#Looping through instrument types
for i in instrumentTypes:
    if i != "SPOT" :
        url = ("https://www.okx.com/api/v5/public/open-interest?instType=" + i)
        payload = ""
        headers = {'8e6497fd-9a0e-4407-a847-baeb0663372d': '5B532F8EDCC358A12FF244F821D14203','Cookie': 'locale=en-US'}
        response = requests.request("GET", url, headers=headers, data=payload)
            
        #JSON Loading and adding iterative data to dictionary
        data = json.loads(response.text)
        newData3.append(data)

#Extracting nested data and putting it into a dataframe
df = pd.json_normalize(newData3, record_path =['data'])
openInterest = df[['instId','oi','oiCcy']]

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Step 4 : Merging them all and output to excel 
#-----------------------------------------------------------------------------------------------------------------------------------------------

result = pd.merge(pd.merge(marketTickr,instrumentEconomics, on='instId',how='left' ), openInterest , on='instId', how='left' )

#Need to re-format all the data types so the sql db accurately captures it. 

print(result.info())

result['volCcy24h'] = result['volCcy24h'].astype(float)
result['vol24h'] = result['vol24h'].astype(float)
result['askPx'] = result['askPx'].astype(float)
result['askSz'] = result['askSz'].astype(float)
result['bidPx'] = result['bidPx'].str.replace(' ', '').astype(float)
result['bidSz'] = result['bidSz'].str.replace(' ', '').astype(float)
result['stk'] = result['volCcy24h'].astype(int)
result['oi'] = result['oi'].astype(float)
result['oiCcy'] = result['oiCcy'].astype(float)

print(result.info())

result.to_excel("/Users/siddharthdesai/documents/dataAnalysis/result.xlsx")

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Step 5 : Write data to SQL database
#-----------------------------------------------------------------------------------------------------------------------------------------------


#engine = create_engine('mysql+pymysql://{user}:{pw}@localhost/{db}'.format(user="root",pw="iDATAsql22",db="okxanalytics1"))
#result.to_sql('24hrVol', con = engine, if_exists = 'append')

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Step 6 : Testing to avoid data translation loss
#-----------------------------------------------------------------------------------------------------------------------------------------------

# print(marketTickr.head())
# print(marketTickr.info())

# print(instrumentEconomics.head())
# print(instrumentEconomics.info())

# print(openInterest.head())
# print(openInterest.info())

# print(result.head())
# print(result.info())


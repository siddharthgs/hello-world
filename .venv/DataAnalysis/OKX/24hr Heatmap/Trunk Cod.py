from locale import D_FMT
from pydoc import resolve
import requests
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import json
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize


#Useful Links
#https://towardsdatascience.com/how-to-convert-json-into-a-pandas-dataframe-100b2ae1e0d8

#Define Variables and Tables
instrumentTypes = ["FUTURES","SPOT","SWAP", "OPTION","MARGIN"]  
optionuly = ["BTC-USD", "ETH-USD"]  
instrumentEconomics = pd.DataFrame()
marketTickr = pd.DataFrame()
newData = []
newData2 = []

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
marketTickr = df[['instType','instId','volCcy24h','vol24h','askPx','askSz','bidPx','bidSz']]

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Step 2 : Extracting the Instrument and Contract Economic Attributes
#-----------------------------------------------------------------------------------------------------------------------------------------------

#Looping through instrument types
for i in instrumentTypes:

    #we require an additional input i.e. uly for option contracts
    if i == "OPTION":
        for uly in optionuly:
            url = ("https://www.okex.com/api/v5/public/instruments?instType=" + i + "&uly=" + uly)
            payload = ""
            headers = {'8e6497fd-9a0e-4407-a847-baeb0663372d': '5B532F8EDCC358A12FF244F821D14203','Cookie': 'locale=en-US'}
            response = requests.request("GET", url, headers=headers, data=payload)
             
             #Load JSON and add iterative data to dictionary
            data = json.loads(response.text)
            newData2.append(data)    
            
    #iterate through all the other instrument types except options
    else:
        url = ("https://www.okex.com/api/v5/public/instruments?instType=" + i)
        payload = ""
        headers = {'8e6497fd-9a0e-4407-a847-baeb0663372d': '5B532F8EDCC358A12FF244F821D14203','Cookie': 'locale=en-US'}
        response = requests.request("GET", url, headers=headers, data=payload)

        #Load JSON and add iterative data to dictionary
        data = json.loads(response.text)
        newData2.append(data)

#Extracting nested data in dict and saving it into a panda dataframe
df = pd.json_normalize(newData2, record_path =['data'])
instrumentEconomics = df[['instType','instId','uly','state','quoteCcy','baseCcy','ctValCcy','settleCcy','listTime','expTime']]


print(marketTickr.head())
print(marketTickr.info())

marketTickr.to_excel("/Users/siddharthdesai/documents/dataAnalysis/marketTickr.xlsx")


print(instrumentEconomics.head())
print(instrumentEconomics.info())

instrumentEconomics.to_excel("/Users/siddharthdesai/documents/dataAnalysis/instrumentEconomics.xlsx")



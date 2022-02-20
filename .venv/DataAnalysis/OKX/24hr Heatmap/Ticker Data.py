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
instrumentTypes = ["FUTURES","SPOT","SWAP", "OPTION"]  
instrumentData = pd.DataFrame()
newData = []

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

instrumentData = df[['instType','instId','volCcy24h','vol24h','askPx','askSz','bidPx','bidSz']]
#Exporting dataframe to excel 
#df.to_excel("/Users/siddharthdesai/documents/dataAnalysis/OKXTickerData.xlsx")


print(df.info())
print(instrumentData.info())



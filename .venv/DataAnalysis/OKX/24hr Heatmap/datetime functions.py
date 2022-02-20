from pydoc import resolve
import requests
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import json
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
from datetime import datetime
import time
from datetime import datetime, timezone

#Define Variables and Tables
instrumentTypes = ["FUTURES"]  
optionuly = ["BTC-USD", "ETH-USD"]  
instrumentEconomics = pd.DataFrame()
marketTickr = pd.DataFrame()
newData = []
newData2 = []
newData3 = []

#Looping through instrument types
for i in instrumentTypes:
        url = ("https://www.okex.com/api/v5/public/instruments?instType=" + i)
        payload = ""
        headers = {'8e6497fd-9a0e-4407-a847-baeb0663372d': '5B532F8EDCC358A12FF244F821D14203','Cookie': 'locale=en-US'}
        response = requests.request("GET", url, headers=headers, data=payload)

        #Load JSON and add iterative data to dictionary
        data = json.loads(response.text)
        newData2.append(data)

#Extracting nested data in dict and saving it into a panda dataframe
df = pd.json_normalize(newData2, record_path =['data'])

print(df['expTime'])

df['expTime'] = pd.to_datetime(df['expTime'], unit='ms')

print(df.head())
print(df.info())

#df['expTimeR'] = datetime.utcfromtimestamp(df['expTime']).strftime('%Y-%m-%d %H:%M:%S')
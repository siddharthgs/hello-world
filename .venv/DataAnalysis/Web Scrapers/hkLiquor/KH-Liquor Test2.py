import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

productlinks = []
t={}
data=[]
c=0

for x in range(1,3):
    k = requests.get('https://www.hkliquorstore.com/index.php/liquor-liqueurs.html?p='+str(x), timeout=100).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("div",{"class":"products"})


print(productlist)
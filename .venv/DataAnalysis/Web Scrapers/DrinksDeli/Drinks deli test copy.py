import requests
import openpyxl
import locale
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

productlinks = []
t={}
data=[]
c=0

baseurl = "https://drinksdeli.asia/"

# ?product_list_limit=all
for x in range(1,2):
    k = requests.get('https://drinksdeli.asia/collections/all?page='+str(x), timeout=100).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("a",{"class":"product-name"})

    for product in productlist:
        link = product.find("a",{"class":"product-name"})
        productlinks.append(link)

print(soup.prettify)
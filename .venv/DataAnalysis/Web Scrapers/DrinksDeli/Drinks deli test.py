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


# ?product_list_limit=all
for x in range(1,2):
    k = requests.get('https://drinksdeli.asia/collections/all?page='+str(x), timeout=100).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("li",{"class":"item product product-item"})

    for product in productlist:
        link = product.find("a",{"class":"product-item-link"}).get('href')
        productlinks.append(link)

for link in productlinks:
    f = requests.get(link,headers=headers).text
    hun=BeautifulSoup(f,'html.parser')

    try:
        name=hun.find("span",{"class":"base"}).text.replace('\n',"")
    except:
        name=None

    try:
        category1=hun.find("li",{"class":"item 1"}).text.replace('\n',"")
    except:
        category1=None

    try:
        category2=hun.find("li",{"class":"item 2"}).text.replace('\n',"")
    except:
        category2=None

    try:
        category3=hun.find("li",{"class":"item 3"}).text.replace('\n',"")
    except:
        category3=None

    try:
        sku=hun.find("div",{"class":"value"},{"itemprop":"sku"}).text.replace('\n',"")
    except:
        sku=None

    try:
        availability=hun.find("div",{"class":"stock available"}).text.replace('\n',"")
    except:
        availability=None

    #try:
    #    description=hun.find("div",{"class":"product attribute description"}).text.replace('\n',"")
    #except:
    #    description=None

    try:
        currentprice=hun.find("span",{"class":"price"}).text.replace('\n',"")
        currentprice = float(currentprice.replace('HK$',""))
    except:
        currentprice = None

    try:
        oldprice=hun.find("span",{"class":"old-price"}).text.replace('\n',"")
        oldprice = float(oldprice.replace('Regular PriceHK$',""))
    except:
        oldprice=None

    try:
        tag=hun.find("div",{"class":"label-content"}).text.replace('\n',"")
    except:
        tag=None

    #Create a table
    product = {"category1":category1,"category2":category2,"category3":category3,"name":name,"sku":sku,"availability":availability,"currentprice":currentprice,"oldprice":oldprice,"tag":tag,"link":link}

    data.append(product)
    c=c+1
    print("completed",c)

df = pd.DataFrame(data)
#df.to_excel("hkliquorcatalogue.xlsx")
print(df)
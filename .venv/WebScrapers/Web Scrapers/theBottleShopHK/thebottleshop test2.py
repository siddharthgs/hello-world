import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

productlinks = []
t={}
data=[]
c=0

for x in range(1,2):
    k = requests.get('https://www.thebottleshop.hk/in-store/spirits/page'+str(x)+'.html', timeout=100).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("p",{"class":"m-a5-b"})

    for product in productlist:
        link = product.find("a",{"class":"bold fs-12"}).get('href')
        productlinks.append(link)

for link in productlinks:
    f = requests.get(link,headers=headers).text
    hun=BeautifulSoup(f,'html.parser')

    try:
        name=hun.find("h1",{"class":"reg"}).text.replace('\n',"")
    except:
        name=None

    try:
        currentprice=hun.find("span",{"class":"price price-update"}).text.replace('\n',"")
        currentprice = float(currentprice.replace('HK$',""))
    except:
        currentprice = None

    try:
        description=hun.find("div",{"class":"desc p-20-t p-30-b"}).text.replace('\n',"")
    except:
        description=None

    #Create a table
    product = {"name":name,"currentprice":currentprice,"link":link,"description":description}

    data.append(product)
    c=c+1
    print("completed",c)

df = pd.DataFrame(data)
#df.to_excel("thebottleshop.xlsx")
print(df)

import requests
from bs4 import BeautifulSoup
import time, random
from fake_useragent import UserAgent
import csv

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.61'}
user = UserAgent()
headers['UserAgent'] = user.random
k = 0 
image = None
with open('123parser.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(('Номер','Название','Цена','Описание','Фото'))

proxy = {
    "https": "socks5://109.245.236.109:4145",
    "http": "socks5://109.245.236.109:4145"
}

url = 'https://www.avito.ru/moskva/bytovaya_elektronika?q=чехол+на+samsung+а51'
response = requests.get(url, headers = headers, proxies = proxy, verify = False)
# response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.text, 'lxml')
# print(soup)
items = soup.find('div', attrs = {'data-marker':'catalog-serp'})
pages = soup.find('div', class_ = 'pagination-hidden-zHaij')
urls = []
links = pages.find_all('a', class_ = 'pagination-page')
for link in links:
    pageNum = int(link.text) if link.text.isdigit() else None
    if pageNum != None:
        hrefval = link.get('href')
        urls.append(hrefval)

items
itemsinfo = items.find_all('a', attrs = {'target':'_blank', 'data-marker':'item-title'})
info = []
for itemsinf in itemsinfo:
    info.append(itemsinf.get('href'))

for xuy in urls:
    pagesURL = url.replace('/moskva/bytovaya_elektronika?q=чехол+на+samsung+а51', xuy)
    response = requests.get(pagesURL)
    for n, i in enumerate(items, start = 1):
        try:
            itemname = i.find('a', attrs = {'data-marker':'item-title'}).text
            itemprice = i.find('span', attrs = {'data-marker':'item-price'}).text
            item_image = i.find('img', attrs = {'itemprop':'image'})
            try:
                image = item_image.get('src')
            except:
                pass
            infoURL = url.replace('/moskva/bytovaya_elektronika?q=чехол+на+samsung+а51', info[k])
            response2 = requests.get(infoURL)
            soup2 = BeautifulSoup(response2.text, 'lxml')
            pidoras = soup2.find('div', attrs ={'itemprop': 'description'})
            if pidoras != None:
                k += 1    
                pidoras2 = pidoras.find('p').text
                print(f'{k}:  {itemname} за {itemprice}\nОписание: {pidoras2}\nФото: {image}')
                with open('123parser.csv', 'a', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter = ' ')
                    writer.writerow((k, itemname, itemprice, pidoras2, image))
        except Exception as e:
            print(e)
            pass

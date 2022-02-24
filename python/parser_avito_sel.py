from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import lxml
import openpyxl
import threading
import pandas

book = openpyxl.Workbook()
sheet = book.active
sheet.append(('Имя товара', 'цена', 'адресс', 'описание', 'ссылка'))
url = 'https://www.avito.ru/?/'
driver = webdriver.Chrome()
driver.set_window_size(1280,1024)
driver.get(url)
# time.sleep(5)
# print(driver.title)
elem = driver.find_element_by_xpath('//input[@data-marker ="search-form/suggest"]')
elem.send_keys('чехол на samsung galaxy a51')
elem.send_keys(Keys.RETURN)
elem = driver.find_element_by_xpath("//div[@data-marker='catalog-serp']")
html = elem.get_attribute("innerHTML")
soup = BeautifulSoup(html,'lxml')
links = []
items = {}
for i in range(100):
	try:
		# name = soup.findAll('div', attrs = {'data-marker':'item'})[i].find('h3', attrs = {'itemprop':'name'}).text
		# price = soup.findAll('div', attrs = {'data-marker':'item'})[i].find('span', attrs = {'data-marker':'item-price'}).text
		href = soup.findAll('div', attrs = {'data-marker':'item'})[i].find('a', attrs = {'data-marker':"item-title", 'itemprop':"url"})
		link = href.get('href')
		links.append(link)
	except IndexError:
		# print(links)
		break
# for i, link in enumerate(links, start = 1):
for i in range(3):
	link = links[i]
	itemURL = url.replace('/?/', link)
	# print(pizda)
	driver.get(itemURL)
	elem = driver.find_element_by_xpath('//div[@class="item-view js-item-view  "]')
	html = elem.get_attribute("innerHTML")
	soup = BeautifulSoup(html,'lxml')
	name = soup.find('div', class_="item-view-content-left").find('span', attrs={'class':"title-info-title-text",'itemprop':"name"}).text
	price = soup.find('div', class_="item-view-content-right").find('span', attrs={'class':"js-item-price", 'itemprop':"price"}).text
	adress = soup.find('div', class_="item-view-content-left").find('div', attrs={"itemprop":"address"}).text
	info = soup.find('div', class_="item-view-content-left").find('div', class_="item-description").text
	print(name, price, adress, info)
	itemsinfo = {i:[name, price, adress, info, itemURL]}
	items.update(itemsinfo)
	o_o = items.get(i)
	sheet.append(o_o)
	book.save('selenium.xlsx')
	# driver.close()
# print('#'*30)
# print(items)

# def start(items, arg):

# for i in range(3):
# 	x = threading.Thread(target=start, args=(items, 'foo'))
# 	x.start()


print('#'*8 + 'THE END' + '#'*8)
time.sleep(10)
driver.close()

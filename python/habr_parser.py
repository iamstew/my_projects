import requests
from bs4 import BeautifulSoup
import openpyxl
import threading
import lxml
import sqlite3
import time
import json
import csv

lock = threading.Lock()
url = 'https://habr.com/ru/all/page'
book = openpyxl.Workbook()
sheet = book.active
sheet.append(('Загаловок','Текст статьи','Лайки','Просмотры','Закладки','Коментарии','Хабы','Тэги'))
conn = sqlite3.connect("mydatabase.db", check_same_thread=False)
cursor = conn.cursor()
try:
	cursor.execute('CREATE TABLE Parser (title text, hubtext text, likes text, watches text, bookmarks text, comments text, hubs text, tags text)')
except:
	pass

with open('123parser.csv', 'w') as f:
	writer = csv.writer(f, delimiter=' ')
	writer.writerow(['Загаловок','Текст статьи','Лайки','Просмотры','Закладки','Коментарии','Хабы','Тэги'])

def start2(URL, title, icon, iconW, iconB, iconC):
	# try:
			k = 0
			aaa = ''
			bbb = ''
			response2 = requests.get(URL)
			soup2 = BeautifulSoup(response2.text, 'lxml')
			hubsANDtags = soup2.findAll('div', class_='tm-separated-list tm-article-presenter__meta-list')[0]
			tags = hubsANDtags.find_all('a', class_ = 'tm-tags-list__link')
			for t in tags:
				aaa += (f' {t.text}')
			hubsANDtags = soup2.findAll('div', class_='tm-separated-list tm-article-presenter__meta-list')[1]
			hubs = hubsANDtags.find_all('a', class_ = 'tm-hubs-list__link')
			for h in hubs:
				bbb += (f' {h.text}')
			hubtext = soup2.select_one('article', class_='tm-article-presenter__content tm-article-presenter__content_narrow').text
			sheet.append([title, hubtext, icon, iconW, iconB, iconC, bbb, aaa])	
			book.save('XUY.xlsx')
			# print(title)
			try:
				lock.acquire(True)	
				cursor.execute("INSERT INTO Parser VALUES('"+str(title)+"','"+str(hubtext)+"','"+str(icon)+"','"+str(iconW)+"','"+str(iconB)+"','"+str(iconC)+"','"+str(bbb)+"','"+str(aaa)+"')")		
				conn.commit()
				# print('#'*30)
			finally:
				lock.release()
			data = {
				'Заголовок' : title,
				'Текст статьи' : hubtext,
				'Лайки' : icon,
				'Просмотры' : iconW,
				'Закладки' : iconB,
				'Коментарии' : iconC,
				'Хабы': bbb,
				'Тэги' : aaa,
			}
			with open("1.json", "w", encoding = 'utf-8') as write_file:
				json.dump(data, write_file)
			with open('123parser.csv', 'a', encoding='utf-8') as f:
				writer = csv.writer(f, delimiter = ';')
				writer.writerow([title, hubtext, icon, iconW, iconB, iconC, bbb, aaa])
			print(title)
	# except:
	# 	pass
	

def start(j, arg):
	try:
			response = requests.get(url + str(j))
			soup = BeautifulSoup(response.text, 'lxml')
			titlesHtml = soup.find('div', class_='tm-articles-list')
			titles = titlesHtml.find_all('article', class_='tm-articles-list__item')
			for i in titles:
				title = i.find('a', class_='tm-article-snippet__title-link').find('span').text
				icon = i.find('div', class_='tm-votes-meter tm-data-icons__item').find('span').text.strip()
				iconW = i.find('div', class_='tm-data-icons').find('span', class_='tm-icon-counter__value').text.strip()
				iconB = i.find('button', class_='bookmarks-button tm-data-icons__item').find('span', class_='bookmarks-button__counter').text.strip()
				iconC = i.find('div', class_='tm-article-comments-counter-link tm-data-icons__item').find('span', class_='tm-article-comments-counter-link__value').text.strip()
				readmore = i.find('a', class_= 'tm-article-snippet__title-link').get('href')
				URL = url.replace('/ru/all/page', readmore)
				z = threading.Thread(target=start2, args=(URL, title, icon, iconW, iconB, iconC))
				z.start()
	except:
		pass
for j in range(1, 3):
	time.sleep(0.5)
	x = threading.Thread(target=start, args=(j, 'foo'))
	x.start()
# book.save('XUY.xlsx')

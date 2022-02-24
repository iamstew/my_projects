import threading
import requests
from bs4 import BeautifulSoup
import openpyxl
from time import sleep
from fake_useragent import UserAgent
import lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

potok = 250
book = openpyxl.Workbook()
sheet = book.active
sheet.append(('Телефон', 'Почта', 'Страна', 'Город', 'Язык общения','ФИО'))

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.61'}
user = UserAgent()
headers['UserAgent'] = user.random

# EU
url_for_page = 'https://prian.ru/europe/'
href="/europe/?next="# следующая страница
urls = [url_for_page] 
urls_for_parser_eu = {}
# href="/europe/?next=74136" # переход с 3089 на 3090

# Кипр
# url_for_page_kipr = 'https://prian.ru/search/?full=0&acountry%5B1%5D=7&aarea%5B1%5D=&aregion%5B1%5D=&adistrict%5B1%5D=&maphash=&type%5B%5D=1&where%5B1%5D=Кипр&search_currency=3&square_land_unit2=128&square_land_unit=128'
# href_kipr="//prian.ru/search/?where[1]=%D0%9A%D0%B8%D0%BF%D1%80&acountry[1]=7&type[]=1&search_currency=3&next="#следуйющая страница
# urls_for_parser_kipr = {}
# urls_kipr = [url_for_page_kipr]
# href="//prian.ru/search/?where[1]=%D0%9A%D0%B8%D0%BF%D1%80&acountry[1]=7&type[]=1&search_currency=3&next=8688"# переход с 362 на 363 страницу

url_id = 0

for i in range(3080):
	url_id += 24 
	urls.append(url_for_page.replace('/europe/', (href+str(url_id))))
	# if i <= 361:
	# 	urls_kipr.append(url_for_page_kipr.replace(
	# 		'//prian.ru/search/?full=0&acountry%5B1%5D=7&aarea%5B1%5D=&aregion%5B1%5D=&adistrict%5B1%5D=&maphash=&type%5B%5D=1&where%5B1%5D=Кипр&search_currency=3&square_land_unit2=128&square_land_unit=128',
	# 		(href_kipr+str(url_id))
	# 		))


def pages_urls(index, url):
	response = requests.get(url, headers = headers)
	soup = BeautifulSoup(response.text, 'lxml')
	list_url_to_parser = []
	flag = False
	for i in range(30):
		try:
			url_for_parser_eu = soup.findAll('div', class_="list_object")[i].find('a')
			href = url_for_parser_eu.get('href')
			if href != None:
				list_url_to_parser.append(href)
			flag = True
		except IndexError:
			break
		except:
			print('ERROR')
			pass
		finally:
			urls_for_parser_eu[index] = list_url_to_parser
			print('#'*30+'END'+'#'*30)
	# 		if flag == True:
	# 			global potok
	# 			potok += 1
	# 			break
	# if flag == False:
	# 	potok += 1

pages_urls(1, urls[20])
# for index, value in enumerate(urls, start = 1):
# 	while True:
# 		sleep(0.2)
# 		if potok > 0:
# 			x = threading.Thread(target=pages_urls, args=(index, value))
# 			x.start()
# 			potok -= 1
# 			break

driver = webdriver.Firefox(executable_path='C:/Users/lanak/Desktop/python/webdriver/geckodriver.exe')
driver.set_window_size(1280,1024)

for j in range(1,3100):
	# try:
		links_on_page = urls_for_parser_eu[j]
		for i in links_on_page:
			# try:
				link = url_for_page.replace('//prian.ru/europe/', i)
				for k in range(10):
					try:
						driver.get(link)
						elem = driver.find_element_by_xpath('//div[@class="card company-page"]')
						sleep(1)
						break
					except:
						sleep(3)
				elem = driver.find_element_by_xpath('//a[@class="c-contacts__showmore collapsed"]')
				elem.click()
				for q in range(20):
					try:
						elem = driver.find_element_by_tag_name('u') 
						elem.click()
					except:
						sleep(0.2)
				elem = driver.find_element_by_xpath('//div[@class="card company-page"]')
				html = elem.get_attribute("innerHTML")
				soup = BeautifulSoup(html,'lxml')
				sleep(0.2)
				title = soup.find('h1', class_="c-header__title").text.split()
				title.reverse()
				if title[0] == 'м2':
					country = title[2].replace(',',' ')
					city = title[3].replace(',',' ')
				else:
					country = title[0].replace(',',' ')
					city = title[1].replace(',',' ')

				try:
					name = soup.findAll('div', class_="c-block__div c-block__div_third")[2].find('span',class_="c-contacts__name").text.strip()
				except:
					name = ' '

				try:
					language = soup.findAll('div', class_="c-block__div c-block__div_third")[2].findAll('div',class_="c-contacts__capture")[1].find('span', class_="c-contacts__position").text.strip()
				except:
					language = ' '

				try:
					phone = soup.findAll('div', class_="c-block__div c-block__div_third")[3].findAll('a',class_="c-contacts__social clickYaEvent")[1].text.strip()
					print(phone)
				except:
					phone = soup.findAll('div', class_="c-block__div c-block__div_third")[2].findAll('div', class_="c-contacts__info")[2].text.strip()#('a',class_="clickYaEvent").text.strip()
					print(phone)
				try:
					mail = soup.findAll('div', class_="c-block__div c-block__div_third")[2].find('a',class_="c-contacts__social c-contacts__social_last").text.strip()
				except:
					mail = soup.findAll('div',class_="c-block__div c-block__div_third")[1].find('div', class_="c-contacts__info").get('href')
				
				data = [phone, mail, country, city, language, name]
				sheet.append(data)
				book.save('prian_parser4.xlsx')
			# except:
			# 	pass
	# except IndexError:
	# 	break
	# except:
	# 	pass

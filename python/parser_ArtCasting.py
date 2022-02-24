from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import openpyxl
import lxml
from time import sleep
from http import cookies

book = openpyxl.Workbook()
sheet = book.active
sheet.append(('Ссылка на страницу','Ф.И.О.','Возраст','Основной телефон','Instagram','Viber','Telegram','Whatsapp','Facebook','ВКонтакте','Email','Дополнительный телефон'))

url = 'https://artcasting.tv/login'
driver = webdriver.Firefox(executable_path='C:/Users/lanak/Desktop/python/webdriver/geckodriver.exe')
driver.set_window_size(1280,1024)
driver.get(url)
sleep(2)

elem = driver.find_element_by_xpath('//input[@name="login"]')
elem.send_keys('alexa00guard@gmail.com')

elem = driver.find_element_by_xpath('//input[@name="password"]')
elem.send_keys('r.9u9MjkwHCbfiQ')
elem.send_keys(Keys.RETURN)
sleep(5)
cookies = driver.get_cookies()

url = 'https://artcasting.tv/aspirants?gender=1&age=20%2C50&page=1&custom=true&city_id=&country_code=-1'
driver.get(url)
sleep(5)


ActorsLinks = []
for i in range(481):
	for j in range(20):
		try:
			elem = driver.find_element_by_xpath('//div[@class="results-wrapper"]')
			html = elem.get_attribute("innerHTML")
			soup = BeautifulSoup(html,'lxml')
			link = soup.findAll('div', class_="item")[j].find('figure').find('a')
			href = link.get('href')
			ActorsLinks.append(href)
		except IndexError:
			break
	elem = driver.find_element_by_xpath('//a[@rel="next"]')
	elem.click()
	sleep(5)

for i in ActorsLinks:
	driver.get(i)
	sleep(2)
	for cookie in cookies:
		driver.add_cookie(cookie)
	elem = driver.find_element_by_xpath('//div[@class="aspirant-general"]')
	html = elem.get_attribute("innerHTML")
	soup = BeautifulSoup(html,'lxml')
	name = soup.find('div', class_="aspirant-name").text
	age = soup.find('div', class_="aspirant-data-content").find('div', class_ = 'item').text
	age.replace('Возраст', ' ')
	age.replace('Лет', ' ')
	datalist = [i, name, age,' ',' ',' ',' ',' ',' ',' ',' ',]
	for k in range(100):
		try:	
			contacts = soup.find('div', class_="aspirant-contacts-bottom").findAll('div', class_='item')[k]
			contacts_text = contacts.find('p').text
			if contacts_text.lower() == 'основной телефон':
				phone = contacts.find('a').text
				datalist[3] = phone
			elif contacts_text.lower() == 'instagram':
				inst = contacts.find('a').text
				datalist[4] = inst
			elif contacts_text.lower() == 'viber':
				viber = contacts.find('a').text
				datalist[5] = viber
			elif contacts_text.lower() == 'telegram':
				tg = contacts.find('a').text
				datalist[6] = tg
			elif contacts_text.lower() == 'whatsapp':
				app = contacts.find('a').text
				datalist[7] = app
			elif contacts_text.lower() == 'facebook':
				face = contacts.find('a').text
				datalist[8] = face
			elif contacts_text.lower() == 'вконтакте':
				vk = contacts.find('a').text
				datalist[9] = vk
			elif contacts_text.lower() == 'e-mail':
				mail = contacts.find('a').text
				datalist[10] = mail
			elif contacts_text.lower() == 'дополнительный телефон':
				number = contacts.find('a').text 
				datalist[11] = number
		except IndexError:
			break
	sheet.append(xuy)
	book.save('ArtCasting.xlsx')
driver.close()
input('Процесс завершен, нажмите ENTER')

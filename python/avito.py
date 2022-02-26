from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import openpyxl
from fake_useragent import UserAgent
import lxml
import datetime
import random

book = openpyxl.Workbook()
sheet = book.active
sheet.append((
    'Название',
    'Ссылки на фотографии',
    'Описание',
    'Цена',
    'Дата публикации',
    'Имя',
    'Ссылка на объявление',
    'Тип продавца',
    'Контактное лицо',
    'Адрес',
    'Ссылка на лого/фото',
    'Опыт',
    'Количество объявлений',
    'Общий рейтинг',
    'Количество оценок'))
'''
Если вам нужно будет список прокси то раскоментите строчки снизу
и закоментите строчку 38, в котором сейчас ваш прокси
'''
proxies_list = []
with open('proxy.txt', 'r') as file:
	for line in file:
		proxies_list.append(line)
proxy = random.choice(proxies_list)
proxies = {
    "http":f"SOCKS5://{proxy}",
    "https": f"SOCKS5://{proxy}"
}


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.61'}
user = UserAgent()
headers['UserAgent'] = user.random

src = 'https://www.avito.ru/chelyabinskaya_oblast/produkty_pitaniya?q=%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%84%D0%B5%D0%BB%D1%8C'

pages_urls = []
response = requests.get(url=src, headers = headers)
soup = BeautifulSoup(response.text, 'lxml')
numbers_pages = []
for i in range(10):   
    try:
        pages = soup.find('div', attrs={"data-marker":"pagination-button"}).findAll('span')[i].text
        numbers_pages.append(pages)
    except IndexError:
        break
numbers_pages.reverse()
for i in range(1,int(numbers_pages[1])+1):
    try:
        pages_urls.append(src.replace('?q',f'?p={i}&q'))
    except:
        pages_urls.append(src+'?p='+str(i))

urls = []
for page_url in pages_urls:
    try:
        '''
        76 строчка для парсинга со своего ip
        77 строчка для парсинга через прокси
        уберите комментрий с той строчки, которую вы хотите использовать
        не рекомендуется использовать парсинг без прокси, чтобы избежать блокировку айпи
        но если нет хороших прокси, то пару раз использовать можно, но не очень часто (примерно 10 запусков в день гарантированно без бана)
        '''
        # response = requests.get(url=page_url, headers = headers)
        # response = requests.get(url=page_url, headers = headers, proxies=proxies, verify=False)
        soup = BeautifulSoup(response.text, 'lxml')
        items_on_page = soup.find('div', attrs={"data-marker":"catalog-serp"})
        for i in range(50):
            try:
                items = items_on_page.findAll('div', attrs={'data-marker':'item'})[i].find('a', attrs={'itemprop':'url','rel':'noopener'})
                item_url = items.get('href')
                urls.append(item_url)
            except IndexError:
                break
    except:
        break

driver = webdriver.Firefox(executable_path='C:/Users/lanak/Desktop/code/webdriver/geckodriver.exe'')

driver.get(src)
cookies = driver.get_cookies()
for cookie in cookies:
    driver.add_cookie(cookie)

for url in urls:
    try:
        link = 'https://www.avito.ru'+url
        img = ''
        contact_face = ''
        driver.get(link)
        elem = driver.find_element_by_xpath('//div[@class="item-view js-item-view  "]')
        html = elem.get_attribute("innerHTML")
        soup = BeautifulSoup(html,'lxml')
        title = soup.find('span', class_="title-info-title-text").text.strip()
        try:
            reviews = soup.find('span', class_="js-item-rating-caption-button seller-info-rating-caption-blue seller-info-rating-caption").get('data-summary')
        except:
            reviews = 'Отсутствует'
        try:
            seller_items = soup.find('div', class_="js-favorite-seller-buttons seller-info-favorite-seller-buttons").find('a').text.strip()[0]
        except:
            seller_items = 'Отсутствует'
        for i in range(10):
            try:
                img += soup.findAll('li', class_="gallery-list-item js-gallery-list-item")[i].find('img').get('src') + '  '
            except:
                break
        description = soup.find('div', class_="item-description").text
        adress = soup.find('span', class_='item-address__string').text.strip()
        try:
            price = soup.find('span', class_="js-item-price").get('content')
        except:
            price ='Не указано'
        date = soup.find('div', class_="title-info-metadata-item-redesign").text.strip()
        name = soup.find('div', class_="seller-info-name js-seller-info-name").find('a').text.strip()
        try:
            rating = soup.find('span', class_="seller-info-rating-score").text.strip()
        except:
            rating = 'Отсутствует'
        reg_date = soup.findAll('div', class_="seller-info-value")[1].find('div').text.strip()
        seller_type = soup.find('div', attrs={'data-marker':"seller-info/label"}).text.strip()
        if seller_type == 'Компания':
            try:
                contact_face = soup.find('div', class_="seller-info-prop seller-info-prop_short_margin").find('div',class_="seller-info-value").text.strip()
            except:
                contact_face = 'Не указано'
        try:    
            seller_photo = soup.find('a', class_="seller-info-avatar-image").get('style').replace("background-image: url('",'').replace("')", '')
        except:
            try:
                seller_photo = soup.find('img', class_="seller-info-shop-img").get('src')   
            except:
                seller_photo = 'Не удалось достать' 
        sheet.append([title,img,description,price,date,name,link,seller_type,contact_face,adress,seller_photo,reg_date,seller_items,rating,reviews])
        book.save(f'{datetime.date.today()}.xlsx')
    except:
        pass
driver.quit()
print('Процесс завершен')

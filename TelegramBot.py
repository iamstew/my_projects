import telebot
from telebot import types 

# Создание бота с токеном от BotFather
bot = telebot.TeleBot ("2017163099:AAH96IQ3SNLVI987PV7YYuKlkdT8W2Q2Gpc")
# Переменная для кнопок 
keyboard1 = types.ReplyKeyboardMarkup()
# Кнопки
keyboard1.row('Приветствие', 'Помощь')
# Словарь для счетчика
a = {0:0}

# Бот обрабатывает команду /start
@bot.message_handler(commands =['start'])
# Функция, которую выполняет бот получив команду /start
def start_message(message):
	# Бот отправляет пользователю 'Бот активен', и добавляет кнопки пользователю
	bot.send_message(message.chat.id, 'Бот активен', reply_markup = keyboard1)

# Бот обрабатывает команду /help
@bot.message_handler(commands = ['help'])
# Функция, которую выполняет бот после полученя команды /help
def help(message):
	# Бот отправляет сообщение пользователю 'Мне самому помощь нужна', и добавляет кнопки пользователю 
	bot.send_message(message.chat.id, 'Мне самому помощь нужна', reply_markup = keyboard1)

# Бот обрабатывает сообщения от пользовтеля с типом текст 
@bot.message_handler(content_types = ['text'])
# Функция, которую выполняет бот после получения текстового сообщения 
def echo_all(message):
	# Добавляет в словарь ключ с id пользователя и увеличивает значение для данного ключа на 1
	a[message.from_user.id] = a.get(message.from_user.id, 0) + 1
	
	# Если значение словаря с ключом равным id пользователя > 3
	# то оно приравнивается 0 
	# и бот отправляет пользователю сообщение 'Пошел нахуй'
	if a[message.from_user.id] > 3:
		a[message.from_user.id] = 0
		bot.send_message(message.chat.id, 'Пошел нахуй')

	# Пользователь нажимает на кнопку 'Приветствие', после чего бот отправляет сообщение 'Привет', добавля кнопки пользователю
	if (message.text.lower() == 'приветствие'):
		bot.send_message(message.chat.id, 'Привет ', reply_markup = keyboard1)
	# Пользователь нажимает на кнопку 'Помощь', после чего бот 
	# отправляет сообщение 'И какой помощи ты ждешь? Я простой эхо бот, я бесполезный<3' пользователю 
	# снова добавляет кнопки
	elif(message.text.lower() == 'помощь'):
		bot.send_message(message.chat.id, 'И какой помощи ты ждешь? Я простой эхо бот, я бесполезный<3', reply_markup = keyboard1)
	# Если пользователь не нажал на кнопку а написал текст, то бот отправляет сообщение с  таким же текстом обратно
	else:
		bot.send_message(message.chat.id, message.text)

# Бот обрабатывает сообщения с типом документ
@bot.message_handler(content_types = ['document'])
def document(message):
	try:
		# Добавляет переменную chat_id для того чтобы написать в 73 и 74 строчке вместо 'message.chat.id'
		chat_id = message.chat.id
		# Создается переменная в которую закладывается id файла 
		file_info = bot.get_file(message.document.file_id)
		# Создается переменная в которую закладывается команда бота для скачивания файла на компутатор
		downloaded_file = bot.download_file(file_info.file_path)
		# Переменная в которой указан путь скачивания файла + название документа 
		src = 'C:/Users/lanak/desktop/python/telebot' + message.document.file_name
		# Осуществляется загрузка файла 
		with open(src, 'wb') as new_file:
			new_file.write(downloaded_file)
		bot.send_message(chat_id, "Пожалуй, я сохраню это")
		# Отправляется файл 
		bot.send_document(chat_id, open(src, 'rb'))
	# Если воpникает какая-то ошибка в данной функции, бот отвечает пользователю на сообщение с текстом ошибки 
	except Exception as e:
		bot.reply_to(message,e )

# Бот обрабатывает тип - фото
@bot.message_handler(content_types = ['photo'])
# Функция, которую бот делает с типом фотографии
def photo(message):
	# Переменная в которую закладывается id фоточки 
	file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
	# Создается переменная в которую закладывается команда бота для скачивания фоточки на компутатор
	downloaded_file = bot.download_file(file_info.file_path)
	# Переменная в которой указан путь скачивания файла + название фоточки 
	src='C:/Users/lanak/Desktop/python/'+file_info.file_path
	# Осуществляется загрузка фоточки
	with open(src, 'wb') as new_file:
		new_file.write(downloaded_file)
	bot.reply_to(message,"Фото добавлено") 
	# Отправляется эта фоточка
	bot.send_photo(message.chat.id, open(src, 'rb'))

@bot.message_handler(content_types = ['video'])
def video(message):
	bot.send_message(message.chat.id, 'Классный видос, правда,  я его не воспринимаю')

bot.polling()

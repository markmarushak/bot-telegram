# -*- coding: utf-8 -*-
# !/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
from telebot import types
from telebot import util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import re
from _functions import *
from keyboard import *
import time

# основной бот
# API_TOKEN = '724197308:AAEeHcxWTH-CGUxokIHZBYm-_5P2rrIHKpA'
# для тестов чтоб не мешать главному
API_TOKEN = '633808414:AAGgQ3vSO6-7vdRj4YFnLTGuh1P302bmCuM'

bot = telebot.TeleBot(API_TOKEN)

chat_bot = 'callback_query'
# host = "https://rezway.com.ua"
# api = host + '/index.php?route=api/product/'
# method = 'get'
user = fullname = phone = currentTotal = currentProduct = search = category = ""
# normal / fast / call phone
operation = 'normal'
repository = {
    'name': '',
    'data': ''
}

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_bot
    chat_bot = message.chat.id
    try:
        api('&chat_id='+str(message.chat.id), 'add_account')
        text = "Предлагаем выбрать сезонность автомобильной шины"
        bot.send_message(message.chat.id, text, reply_markup=seasson())
    except Exception as e:
        bot.send_message(chat_bot, e)
    
@bot.message_handler(commands=['news_spam'])
def send_spam(message):
    global chat_bot
    chat_bot = message.chat.id
    bot.send_message(message.chat.id, 'Начинаеться спам новстей, Мухахах')
    try:
        data_news = api('', 'news_spam')# берем последнюю новость 
        users = api('', 'get_accounts')# берем список пользователей 
        # по очередно отправляем новость 
        for i in users.get('data'):
            bot.send_message(i.get('chat_id'), data_news.get('data'))

    except Exception as e:
        bot.send_message(chat_bot, e)

# надо убрать весь лишний код из echo_message 
# за счет того что создать отдельно функции проверки для каждой кнопки
def main_menu(message):
    getCart(message)
    getNews(message)
    getSetting(message)

def back_to_home(message):
    pass

def news_week(message):
    try:
        result = api('', 'news_week')
        for article in result.get('data'):
            bot.send_message(message.chat.id, article)
    except Exception as e:
        bot.send_message(message.chat.id, 'news a week not loaded, sorry')

def news_last(message):
    try:
        result = api('', 'news_last')
        for article in result.get('data'):
            bot.send_message(message.chat.id, article)
    except Exception as e:
        bot.send_message(message.chat.id, 'news a week not loaded, sorry')

def change_fio(message):
    try:
        query = '&chat_id='+str(chat_bot)+'&fio='+message.text
        api(query, 'change_fio')
    except Exception as e:
        bot.send_message(chat_bot, 'не удалось изменить ФИО')

def change_phone(message):
    try:
        query = '&chat_id='+str(chat_bot)+'&phone='+message.text
        api(query, 'change_phone')
    except Exception as e:
        bot.send_message(chat_bot, 'не удалось изменить Номер телефона')

def filters(t):
    global search
    text = t.replace(' ','')
    search = text[:6]+' '+text[6:]

def change_total(message, id):
    try:
        query = '&chat_id='+str(chat_bot)+'&id='+id+'&total='+message.text
        api(query, 'change_total')
        getCart()
    except Exception as e:
        bot.send_message(chat_bot, 'не удалось изменить кол-во')


def send_to_manager(button_name, message, text = 'null'):
    checkAuth()
    try:
        if text == 'null':
            bot.send_message(chat_bot, user.get('fullname') + ' с Вами свяжеться менеждер', reply_markup=seasson())
            text = 'Telebot Api ' + button_name + ' \r\n Заказчик: ' + user.get(
                'fullname') + '\r\n телефон: ' + user.get('phone') + '\r\n Товар: ' + currentProduct.get('name')

            if currentTotal != '':
                text = text + '\r\n Кол-во ' + currentTotal

        msg = bot.send_message('-374993145', text, parse_mode='HTML')
        bot.register_next_step_handler(msg, send_welcome)
    except Exception as e:
        bot.send_message(chat_bot, 'Отправка менежру прервалась')

def fast_buy(message):
    global currentTotal
    currentTotal = message.text
    if user != 0:
        send_to_manager('Быстрая покупка', message)
    else:
        msg = bot.send_message(chat_bot, 'Введите ваше имя')
        bot.register_next_step_handler(msg, get_fullname)

def getWays(message):
    global category
    if message.text in "☀ Летняя ♻ Всесезонная ❄ Зимняя":
        category = message.text
        text = "Вы выбрали " + category + " \r\n Введите ваш типоразмер по данному примеру 190/50 R13 \r\n где: 190 - ширина, 50 - профиль, R13 - Диаметр"
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, parameters_tire)

def getSetting(message):
    global operation
    if message.text in "Настройки":
        try:
            if user != 0:
                bot.send_message(message.chat.id, 'Ваши персональные настройки \r ФИО: '+user.get('fullname')+'\r Номер телефона: '+ user.get('phone'), reply_markup=setting())
            else:
                operation = 'Register'
                get_fullname()

        except Exception as e:
            bot.send_message(chat_bot, 'error get setting')

def getNews(message):
    if message.text in "Новости 📰":
        try:
            # see next to CallBack_functions
            bot.send_message(message.chat.id, 'Какие новости вы хотите увидеть?', reply_markup=news_btn())

        except Exception as e:
            bot.send_message(chat_bot, 'error get news_btn')

def getCart(message):
    global repository
    if message.text in 'Корзина 🛒':
        if user != 0:
            response = api('&chat_id=' + user.get('chat_id'), 'get_cart')
            status = response.get('status')
            if status == 200:
                repository.update({
                    'name': 'cart',
                    'data': response.get('data')
                })
                photo(response, user.get('chat_id'), 'cart')
                bot.send_message(chat_bot, 'Корзина товаров', reply_markup=cart())
            else:
                bot.send_message(chat_bot, 'Выберите товар.. корзина пуста')
        else:
            bot.send_message(chat_bot, 'Выберите товар.. корзина пуста')

def checkAuth():
    global user
    try:
        response = api('&chat_id=' + str(chat_bot), 'user')
        if response.get('status') == 200:
            user = response.get('data')
        else:
            user = 0
    except Exception as e:
        # bot.send_message(chat_bot, 'Пользователь не определен', reply_markup=seasson())
        user = 0


def rows(message):
    global method, results, category, repository
    try:
        query = '&category=' + category + '&search=' + search
        response = api(query, 'search')
        if response.get('status') == 200:
            repository.update({
                'name': 'rows',
                'data': response.get('data')
            })
            photo(response, chat_bot)
        else:
            if message.text == "☀ Летняя" or message.text == "♻ Всесезонная" or message.text == "❄ Зимняя":
                category = message.text
                text = "Вы выбрали " + category + " \r\n Введите ваш типоразмер по данному примеру 190/50 R13 \r\n где: 190 - ширина, 50 - профиль, R13 - Диаметр"
                msg = bot.send_message(chat_bot, text)
                bot.register_next_step_handler(msg, parameters_tire)
            else:
                msg = bot.send_message(chat_bot,
                                       'Ничего не найдено по данному запросу ' + category + ' и поисковой запрос ' + search + ' \r\nПопробуйте еще раз')
                bot.register_next_step_handler(msg, parameters_tire)
    except Exception as e:
        # bot.send_message(chat_bot, 'Ошибка в создании списка товаров')
        bot.send_message(chat_bot, e)



def parameters_tire(message):
    global operation
    filters(message.text)
    main_menu(message)
    # if message.text == '/start':
	   #  send_welcome(message)
    # elif message.text in "Новости 📰":
    #     try:
    #         # see next to CallBack_functions
    #         bot.send_message(message.chat.id, 'Какие новости вы хотите увидеть?', reply_markup=news_btn())

    #     except Exception as e:
    #         bot.send_message(chat_bot, 'error get news_btn')
    # elif message.text in "Настройки":
    #     try:
    #         if user != 0:
    #             bot.send_message(message.chat.id, 'Ваши персональные настройки \r ФИО: '+user.get('fullname')+'\r Номер телефона: '+ user.get('phone'), reply_markup=setting())
    #         else:
    #             operation = 'Register'
    #             get_fullname()
    #     except Exception as e:
    #         bot.send_message(chat_bot, 'error get setting')
    rows(message)


def get_fullname(message):
    global fullname
    fullname = message.text
    msg = bot.send_message(chat_bot, message.text + "\r\nВведи пожалуйста номер телефона")
    bot.register_next_step_handler(msg, get_phone)


def get_phone(message):
    global phone
    phone = message.text
    method = 'add_contact'
    query = '&fullname=' + fullname + '&phone=' + phone + "&chat_id=" + str(chat_bot)
    response = api(query, method)
    if response.get('status') == 403:
        bot.send_message(chat_bot, response.get('data'))
    elif response.get('status') == 200:
        if operation == 'normal':
            bot.send_message(chat_bot,
                                   'Ваш товар и контакты добавлены. ' + fullname + ' вы можете продолжить покупку, а для полного оформления перейдите в корзину')
            send_welcome(message)
        elif operation == 'fast':
            send_to_manager('Быстрая покупка', message)
        elif operation == 'call phone':
            send_to_manager('Обратный звонок', message)
        elif operation in 'Register':
            bot.send_message(message.chat.id, 'Спасибо за регистраию', reply_markup=seasson())

# when use callback_data in KeyButton
@bot.callback_query_handler(func=lambda message: True)
def callback_query(message):
    global currentProduct, method, operation, currentTotal
    try:
        if message.data == "корзина_добавить":

            operation = 'normal'
            msg = bot.send_message(chat_bot, "Выьерите кол-во:", reply_markup=totals())
            bot.register_next_step_handler(msg, echo_message)

        elif message.data == "звонок":
            currentTotal = ''
            if user != 0:

                send_to_manager('Обратный звонок', message)

            else:
                operation = 'call phone'
                msg = bot.send_message(chat_bot, 'Ведите ФИО')
                bot.register_next_step_handler(msg, get_fullname)

        elif message.data == "быстрая":

            operation = 'fast'
            msg = bot.send_message(chat_bot, "Выбрите кол-во", reply_markup=totals())
            bot.register_next_step_handler(msg, fast_buy)

        elif message.data in "change_fio":
            msg = bot.send_message(message.chat.id, "Введите новое ФИО")
            bot.register_next_step_handler(msg, change_fio)
        elif message.data in "change_phone":
            msg = bot.send_message(message.chat.id, "Введите новый Номер телефона")
            bot.register_next_step_handler(msg, change_phone)
        elif message.data in "news_week":
            news_week(message)
        elif message.data in "news_last":
            news_last(message)
        else:

            if repository.get('name') == 'rows':

                product = currentProduct = repository.get('data')[message.data]

                #this function done after click order a product
                # one_product(product, chat_bot, item)
                try:
                    one_product(product, chat_bot)
                except Exception as e:
                    bot.send_message(chat_bot, 'Ошибка при отрисовке данного товара')

            elif repository.get('name') == 'cart':

                id = message.data[1:]

                if message.data[:1] == 'd':

                    if del_cart(id, user.get('chat_id')).get('status') == 200:

                        getCart()

                    else:

                        bot.answer_callback_query(message.id, 'не удалось удалить, попробуйте повторить')

                elif message.data[:1] == 'c':

                    msg = bot.send_message(chat_bot, 'Напишите кол-во')
                    bot.register_next_step_handler(msg, change_total, id=id)

    except Exception as e:
        bot.send_message(chat_bot, 'Ошибка в Callback функции', reply_markup=seasson())


# any text out puted user
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global category, chat_bot, method, currentTotal, operation

    try:

        chat_bot = message.chat.id
        checkAuth()
        main_menu(message)
        if message.text in "Вернуться на главную":
            send_welcome(message)
        elif message.text in "Отправить заказ на оформление":
            try:
                bot.send_message(chat_bot, 'Ожидайте подтверждения заказа')
                response = api("&chat_id="+str(chat_bot),"order_buy")
                send_to_manager('Заказ', message, response.get('data'))
            except Exception as e:
                bot.send_message(chat_bot, 'отправка заказа на обработку оборвалась')
        # elif message.text == "☀ Летняя" or message.text == "♻ Всесезонная" or message.text == "❄ Зимняя":
        # elif message.text in "☀ Летняя ♻ Всесезонная ❄ Зимняя":

        #     category = message.text
        #     text = "Вы выбрали " + category + " \r\n Введите ваш типоразмер по данному примеру 190/50 R13 \r\n где: 190 - ширина, 50 - профиль, R13 - Диаметр"
        #     msg = bot.send_message(message.chat.id, text)
        #     bot.register_next_step_handler(msg, parameters_tire)

        # elif message.text in "Корзина 🛒":
        #     try:
        #         if user != 0:
        #             getCart()
        #         else:
        #             bot.send_message(chat_bot, 'Вы еще не делали покуп')
        #     except Exception as e:
        #         bot.send_message(chat_bot, 'error get cart')

        # elif message.text in "Новости 📰":
        #     try:
        #         # see next to CallBack_functions
        #         bot.send_message(message.chat.id, 'Какие новости вы хотите увидеть?', reply_markup=news_btn())

        #     except Exception as e:
        #         bot.send_message(chat_bot, 'error get news_btn')
        # elif message.text in "Настройки":
        #     try:
        #         if user != 0:
        #             bot.send_message(message.chat.id, 'Ваши персональные настройки \r ФИО: '+user.get('fullname')+'\r Номер телефона: '+ user.get('phone'), reply_markup=setting())
        #         else:
        #             operation = 'Register'
        #             get_fullname()

        #     except Exception as e:
        #         bot.send_message(chat_bot, 'error get setting')

        elif bool(re.match(r'^\d{1}|[1-5]', message.text)):

            currentTotal = message.text

            if operation == 'normal':
                try:
                    query = '&chat_id=' + str(chat_bot) + '&product=' + currentProduct.get(
                        'product_id') + "&total=" + currentTotal
                    response = api(query, 'add_cart')

                    if response.get('status') == 403:
                        # bot.send_message(chat_bot, response.get('data'), reply_markup=seasson())
                        bot.send_message(message.chat.id, 'не добавлено в корзину', reply_markup=seasson())
                    else:
                        name = user.get('fullname')
                        msg = bot.send_message(chat_bot,
                                               'Товар добавлен в корзину ' + name + "\r Вы можете перейти в корзину или продолжить поиск",
                                               reply_markup=seasson())
                except Exception as e:
                    msg = bot.send_message(chat_bot,
                                           "Введи контакты ФИО и номер телефона - в последующие разы вам не прийдется этот шаг проходить \r\n\r\nВведите ФИО ",
                                           reply_markup=seasson())
                    bot.register_next_step_handler(msg, get_fullname)

        else:
            bot.send_message(message.chat.id, 'Кнопка меню не работает')

    except Exception as e:

        bot.send_message(chat_bot, 'echo text error', reply_markup=seasson())


# bot.polling()


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)

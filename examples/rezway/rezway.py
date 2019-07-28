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

API_TOKEN = '724197308:AAEeHcxWTH-CGUxokIHZBYm-_5P2rrIHKpA'
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
            bot.send_message(chat_bot, user.get('fullname') + ' с Вами свяжеться менеждер')
            text = 'Telebot Api ' + button_name + ' \r\n Заказчик: ' + user.get(
                'fullname') + '\r\n телефон: ' + user.get('phone') + '\r\n Товар: ' + currentProduct.get('name')

            if currentTotal != '':
                text = text + '\r\n Кол-во ' + currentTotal

        bot.send_message('-374993145', text, reply_markup=seasson(), parse_mode='HTML')
        send_welcome(message)
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



def getCart():
    global repository
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
        emptyCart()

def emptyCart():
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
            bot.register_next_step_handler(message, parameters_tire)
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
    filters(message.text)
    if message.text == "Корзина":
        if user != 0:
            getCart()
    elif message.text == '/start'
        send_welcome(message)
    else:
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


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_bot
    chat_bot = message.chat.id
    text = "Предлагаем выбрать сезонность автомобильной шины"
    bot.send_message(message.chat.id, text, reply_markup=seasson())


# when use callback_data in KeyButton
@bot.callback_query_handler(func=lambda message: True)
def callback_query(message):
    global currentProduct, method, operation, currentTotal
    try:
        if message.data == "корзина_добавить":

            operation = 'normal'
            bot.send_message(chat_bot, "Выьерите кол-во:", reply_markup=totals())

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
    global category, chat_bot, method, currentTotal

    try:

        chat_bot = message.chat.id
        checkAuth()
        if message.text == "Вернуться на главную":
            send_welcome(message)
        elif message.text == "Отправить заказ на оформление":
            try:
                bot.send_message(chat_bot, 'Ожидайте подтверждения заказа')
                response = api("&chat_id="+str(chat_bot),"order_buy")
                send_to_manager('Заказ', message, response.get('data'))
            except Exception as e:
                bot.send_message(chat_bot, 'отправка заказа на обработку оборвалась')
        elif message.text == "☀ Летняя" or message.text == "♻ Всесезонная" or message.text == "❄ Зимняя":

            category = message.text
            text = "Вы выбрали " + category + " \r\n Введите ваш типоразмер по данному примеру 190/50 R13 \r\n где: 190 - ширина, 50 - профиль, R13 - Диаметр"
            msg = bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(msg, parameters_tire)

        elif message.text == "Корзина":

            try:

                if user != 0:

                    getCart()

                else:

                    bot.send_message(chat_bot, 'Вы еще не делали покуп')

            except Exception as e:
                bot.send_message(chat_bot, 'error get cart')

        elif bool(re.match(r'\d{1}', message.text)):

            currentTotal = message.text

            if operation == 'normal':
                query = '&chat_id=' + str(chat_bot) + '&product=' + currentProduct.get(
                    'product_id') + "&total=" + currentTotal
                response = api(query, 'add_cart')

                if response.get('status') == 403:
                    bot.send_message(chat_bot, response.get('data'), reply_markup=seasson())

            try:

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

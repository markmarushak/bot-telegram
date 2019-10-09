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


API_TOKEN = '798419976:AAEGP058AxX6pXBzHs88P7ETopD0dvqPXJ0'
bot = telebot.TeleBot(API_TOKEN)

host = "https://in-touch.ooo/api"
# api = host + '/index.php?route=api/product/'
# method = 'get'
key_chat = mesg = ""
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
        res = api('?chat_id='+str(message.chat.id), 'storeChat', message.chat.id)
        text = "Привет Менеджер, давай поработаем вместе"
        bot.send_message(message.chat.id, text, reply_markup=main())
    except Exception as e:
        bot.send_message(chat_bot, e)
    

def status(message, status):
	api('?chat_id='+str(message.chat.id)+'&status='+status, 'manager-status')

def send_message(message):
    api('?message='+message.text+'&manager_id='+str(message.chat.id), 'feedback', message.chat.id)
    # bot.send_message(message.chat.id, 'Сообщение отправлено')

# when use callback_data in KeyButton
@bot.callback_query_handler(func=lambda message: True)
def callback_query(message):
	pass

# any text out puted user
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global mesg
    if message.text in "Ушел":
        status(message, 'close')
    elif message.text in "Свободен":
        status(message, 'open')
    elif message.text == "Завершить":
        try:
            data = status(message, 'open')
            bot.send_message(message.chat.id, 'Вы свободны', reply_markup=main())
        except Exception as e:
            bot.send_message(message.chat.id, e)
    elif message.text == "Принять":
        try:
            data = status(message, 'close')
            bot.send_message(message.chat.id, 'Вы начали чат с клиентом ответте на заданный вопрос \r\n\r\n'+message.text, reply_markup=main())
        except Exception as e:
            bot.send_message(message.chat.id, e)
    elif message.text == "Заблокировать":
        bot.send_message(message.chat.id, 'Почему заблокирован клиент', reply_markup=main())
    else:
        try:
            send_message(message)
        except Exception as e:
            bot.send_message(message.chat.id, e)

bot.polling()


# while True:
#     try:
#         bot.polling()
#     except Exception:
#         time.sleep(15)

# -*- coding: utf-8 -*-
#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
from telebot import types
from telebot import util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
# from lib.test import *
from lib.keyboard import *

API_TOKEN = '633808414:AAGgQ3vSO6-7vdRj4YFnLTGuh1P302bmCuM'

bot = telebot.TeleBot(API_TOKEN)

chat_bot = ''

# parameters of the api

# main link api
api = 'http://rezway.loc/index.php?route=api/product/'
# method GET/POST/PUT/DELETE
method = 'get'
# query on example &category=Всесезонная резина&radius=265
_seasson = _width = _diameter = _profile = ''

# user parameters
cart = []
currentProduct = ''

# handler
def getProduct(id):
    query = '&product_id='+currentProduct
    request = requests.get(api+method+query)
    response = request.json()


def rows():
    global _seasson, _width, _diameter, _profile
    query = '&category='+_seasson+'&profile='+_profile+'&width='+_width+'&diameter='+_diameter
    request = requests.get(api+method+query)
    response = request.json()    
    if response.get('status') != 404:
        response = response.get('data')
        for i in response:
            bot.send_message(chat_bot, response[i].get('name'))
            bot.send_photo(
                chat_bot,
                photo="https://i2.rozetka.ua/goods/6155337/alloid_ni_3082p_images_6155337832.jpg",
                caption=response[i].get('name'),
                reply_markup=buy(response[i].get('product_id'))
            )
    else:
        bot.send_message(chat_bot, 'Ничего не найдено по данному запросу \r\n Сезонность: '+ _seasson+' \r\n Ширина: '+_width+' \r\n Профиль: '+_profile+' \r\n Диаметр: '+_diameter)

# test 
# 
@bot.message_handler(commands=['test_api'])
def test_api(message):
    global chat_bot, _seasson, _width, _diameter, _profile
    chat_bot = message.chat.id
    _seasson = 'Летняя резина'
    _width = '275'
    _profile = '40'
    _diameter = 'R19'
    rows()    

@bot.message_handler(commands=['test_api_bad'])
def bad_api(message):
    global chat_bot, _seasson, _width, _diameter, _profile
    chat_bot = message.chat.id
    _seasson = 'Летняя резина'
    _width = '285'
    _profile = '40'
    _diameter = 'R19'
    rows()    

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_bot
    chat_bot = message.chat.id
    text = "Рады вас приветсвовать в нашем Бот-приложенни от сайта Rezway.com.ua \U0001F602 \r\n Здесь вы найдете упрощенный вариант сайта для быстрого преобретения нужного товара \r\n\r\n Для начала работы выберите поиск товара и следуте простой инструкции "
    bot.send_message(message.chat.id, text, reply_markup=seasson())

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == "Поиск товара":
        text = "Выберите сезонность для вашего транспорта \U0001F68C \U0001F697 \U0001F699"
        bot.send_message(message.chat.id, text, reply_markup=seasson())
    else:
        bot.send_message(chat_bot, 'Кнопка меню не работает', reply_markup=seasson())

@bot.callback_query_handler(func=lambda message: True)
def callback_query(message):
    global query, currentProduct
    if message.data == 'Всесезонная резина' or message.data == 'Летняя резина' or message.data == 'Зимняя резина':
        query = query+'&category='+message.data
        msg = bot.send_message(chat_bot, 'Введите ширину резины например: "от 135 до 385" \r Минимальный интервал в 5 едениц например: "170, 175; 180, 185 и так далее" ')
        bot.register_next_step_handler(msg, filter_width)
        # return rows(message.data)
    else:
        currentProduct = message.data
        msg = bot.send_message(chat_bot, 'Вы выбрали вот такую резину - '+ currentProduct, reply_markup=reply_markup)
        bot.register_next_step_handler(msg, addToCart)

def filter_width(message):
    global query
    query = query+'&width='+message.text
    msg = bot.send_message(chat_bot, 'Введите профиль резины например: "25 - 80" \r Минимальный интервал в 5 едениц')
    bot.register_next_step_handler(msg, filter_profile)

def filter_profile(message):
    global query
    query = query+'&profile='+message.text
    msg = bot.send_message(chat_bot, 'Введите размер резина например: "R16, R22, R14C, R19.5"')
    bot.register_next_step_handler(msg, filter_diameter)

def filter_diameter(message):
    global query
    query = query+'&diameter='+message.text
    rows()

def addToCart(product_id):
	# bot.send_message(chat_bot, product_id)
    bot.send_message(chat_bot, product_id)

bot.polling()
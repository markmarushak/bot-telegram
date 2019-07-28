# -*- coding: utf-8 -*-
#!/usr/bin/python

import telebot
from telebot import types
from telebot import util
from telebot.types import *

def seasson():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add(
	    InlineKeyboardButton("☀ Летняя"),
	    InlineKeyboardButton("♻ Всесезонная"),
	    InlineKeyboardButton("❄ Зимняя"),
	    InlineKeyboardButton("Корзина")
    )
	markup.row_width = 1
	return markup

def buy(id):
	markup = InlineKeyboardMarkup()
	markup.add(
	    InlineKeyboardButton("Подробнее", callback_data=id))
	return markup

def order():
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(
	    InlineKeyboardButton("Добавить в карзину \U000027A1", callback_data="корзина_добавить"),
	    InlineKeyboardButton("Быстрая покупка ", callback_data="быстрая"),
	    InlineKeyboardButton("Обратный звонок \U0000260E", callback_data="звонок")
    )
	return markup

def totals():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add(
	    InlineKeyboardButton("1"),
	    InlineKeyboardButton("2"),
	    InlineKeyboardButton("4"),
	    InlineKeyboardButton("5"),
    )
	markup.row_width = 1
	return markup

def cart():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add(
	    InlineKeyboardButton("Вернуться на главную"),
	    InlineKeyboardButton("Отправить заказ на оформление"),
    )
	return markup

def cart_product(id):
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	markup.add(
	    InlineKeyboardButton("Удлить товар", callback_data="d"+id),
	    InlineKeyboardButton("Изменить кол-во", callback_data="c"+id)
    )
	return markup

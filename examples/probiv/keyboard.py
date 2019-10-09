# -*- coding: utf-8 -*-
#!/usr/bin/python

import telebot
from telebot import types
from telebot import util
from telebot.types import *

def main():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add(
	    InlineKeyboardButton("Ушел"),
	    InlineKeyboardButton("Свободен")
    )
	return markup

def open_chat(id):
	markup = InlineKeyboardMarkup()
	markup.add(
	    InlineKeyboardButton("Принять", callback_data=id),
	    InlineKeyboardButton("Заблокировать", callback_data=id))
	return markup

# Just example
def article_link(link):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(
	    InlineKeyboardButton("Открыть статью", url=link),
    )
	return markup
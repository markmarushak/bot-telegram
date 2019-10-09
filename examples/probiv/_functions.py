import re
import requests
import telebot
from keyboard import  *
# host = "https://in-touch.ooo/api"
host = "http://probiv.loc/api/"
# host = "http://rezway.loc"
# main link api
# method GET/POST/PUT/DELETE
# method = 'get'

API_TOKEN = '798419976:AAEGP058AxX6pXBzHs88P7ETopD0dvqPXJ0'

bot = telebot.TeleBot(API_TOKEN)

def api(query, method, chat_bot = 'null', req = 'get'):
    try:
        if req == 'get':
            request = requests.get(host + method + query)
            if chat_bot != 'null':
                bot.send_message(chat_bot, host + method + query)
            response = request.json()
            return response
        elif req == 'post':
            request = requests.post(host+method, query)
            bot.send_message(chat_bot, api_url + method + query)
            response = request.json()
            return response
    except Exception as e:
        bot.send_message(chat_bot, e)

def del_cart(id, chat_id):
    text = 'Загрузка '
    for i in range(6):
        text = text + '.'
        bot.send_message(chat_id, text)
    return api('&id='+id+'&chat_id='+chat_id, 'del_cart')

def photo(response, chat_bot, desc = 'null'):
    resources = response.get('data')
    for item in resources:
        if desc == 'cart':
            try:
                caption = "Номер товара: #"+ item+"\r\n<b>" + resources[item].get('name') + "</b>\r\n Описание: " + resources[item].get('description') + "\r\n <b>Цена: " + resources[item].get('price') + "</b>\r\n Кол-во:" + str(resources[item].get('total'))
                bot.send_photo(
                    chat_bot,
                    photo=img(resources[item].get('image')),
                    caption=caption,
                    parse_mode='HTML',
                    reply_markup=cart_product(item)
                 )
            except Exception as e:
                # bot.send_message(chat_bot, 'ошибка списка корзины')
                bot.send_message(chat_bot, e)
        elif desc != 'null':
            try:
                caption = "<b>" + resources[item].get('name') + "</b>\r\n Описание: " + resources[item].get('description') + "\r\n <b>Цена: " + resources[item].get('price') + "</b>"
                bot.send_photo(
                    chat_bot,
                    photo=img(resources[item].get('image')),
                    caption=caption,
                    parse_mode='HTML',
                    reply_markup=buy(item)
                )
            except Exception as e:
                bot.send_message(chat_bot, 'ошибка отрисовки списка поиска')
        else:
            try:
                bot.send_photo(
                    chat_bot,
                    photo=img(resources[item].get('image')),
                    caption="<b>" + resources[item].get('name') + "</b>\r\n<b>Цена: " + resources[item].get('price') + "</b>",
                    parse_mode='HTML',
                    reply_markup=buy(item)
                )
            except Exception as e:
                bot.send_message(chat_bot, 'ошибка отрисовки списка поиска')

def one_product(data, chat_bot):
    caption = "<b>" + data.get('name') + "</b>\r\n Описание: " + data.get('description') + "\r\n <b>Цена: " + data.get('price') + "</b>"
    bot.send_photo(
        chat_bot,
        photo=img(data.get('image')),
        caption=caption,
        parse_mode='HTML',
        reply_markup=order()
    )

def empty(value):
    try:
        value = float(value)
    except ValueError:
        pass
    return bool(value)


def article(resources, chat_bot, desc='null'):
    for item in resources:
        try:
            bot.send_photo(
                    chat_bot,
                    photo=img(resources[item].get('image')),
                    caption="<b>"+resources[item].get('name')+ "</b> \r\n"+resources[item].get('description'),
                    parse_mode='HTML',
                    reply_markup=article_link(link(resources[item].get('link')))
                    )
        except Exception as e:
            bot.send_message(chat_bot, e)

def img(path):
    img = path.replace("\/", "/");
    return host + "/image/" + img
    # return "https://i2.rozetka.ua/goods/6155337/alloid_ni_3082p_images_6155337832.jpg"

def link(path):
    link = path.replace("\/", "/");
    return host + link
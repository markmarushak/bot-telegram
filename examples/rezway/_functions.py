import re
import requests
import telebot
from keyboard import  *
host = "https://rezway.com.ua"
# host = "http://rezway.loc"
# main link api
api_url = host + '/index.php?route=api/product/'
# method GET/POST/PUT/DELETE
# method = 'get'

API_TOKEN = '724197308:AAEeHcxWTH-CGUxokIHZBYm-_5P2rrIHKpA'

bot = telebot.TeleBot(API_TOKEN)

def api(query, method, chat_bot = 'null'):
    try:
        request = requests.get(api_url + method + query)
        # bot.send_message(chat_bot, api_url + method + query)
        response = request.json()
        return response
    except Exception as e:
        bot.send_message(chat_bot, e)

def del_cart(id, chat_id):
    return api('&id='+id+'&chat_id='+chat_id, 'del_cart')

def photo(response, chat_bot, desc = 'null'):
    resources = response.get('data')
    for item in resources:
        if desc == 'cart':
            try:
                caption = "<b>" + resources[item].get('name') + "</b>\r\n Описание: " + resources[item].get('description') + "\r\n <b>Цена: " + resources[item].get('price') + "</b>\r\n Кол-во:" + str(resources[item].get('total'))
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


def img(path):
    img = path.replace("\/", "/");
    return host + "/image/" + img
    # return "https://i2.rozetka.ua/goods/6155337/alloid_ni_3082p_images_6155337832.jpg"

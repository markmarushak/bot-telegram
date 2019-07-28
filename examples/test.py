import telebot  # pip install pyTelegramBotApi

bot = telebot.TeleBot('724197308:AAEeHcxWTH-CGUxokIHZBYm-_5P2rrIHKpA')


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='CLick me', callback_data='add')
    markup.add(button)
    bot.send_message(chat_id=message.chat.id, text='Some text', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'add':
        bot.answer_callback_query(callback_query_id=call.id, text='Hello world')


if __name__ == '__main__':
    bot.polling()
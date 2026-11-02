import telebot
import os
from telebot import types
import datetime
import requests

bot =telebot.Telebot(os.environ.get('BOT_TOKEN'))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_time = types.InlineKeyboardButton('Узнать время', callback_data='get_time')
    btn_hello = types.InlineKeyboardButton('Сказать привет', callback_data='say_hello')
    btn_price = types.InlineKeyboardButton('Курс Биткоина 🪙', callback_data='get_price')
    markup.add(btn_time, btn_hello, btn_price)
    bot.reply_to(message, "Привет! Выбери действие на кнопках:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'get_time':
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        bot.send_message(call.message.chat.id, f"Сейчас {current_time}")
    elif call.data == 'say_hello':
        bot.send_message(call.message.chat.id, "И тебе привет, человек! 👋")
    elif call.data == 'get_price':
        bot.send_message(call.message.chat.id, "Секунду, запрашиваю курс... ⏳")
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
            data = response.json()
            price = data['bitcoin']['usd']
            bot.send_message(call.message.chat.id, f"Текущий курс Биткоина: ${price:,} 🚀")
        except:
            bot.send_message(call.message.chat.id, "Ошибка! Не могу получить курс.")

@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.reply_to(message, f"Сейчас {current_time}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

print("Бот запущен...")
bot.infinity_polling()

import telebot
import os
from telebot import types
import datetime
import requests
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
bot =telebot.TeleBot(os.environ.get('BOT_TOKEN'))
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

Thread(target=run_health_server, daemon=True).start()

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
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", headers=headers)
                data = response.json()
                price = float(data['price'])
                bot.send_message(call.message.chat.id, f"Текущий курс Биткоина: ${round(price, 2)} 🚀")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"Ошибка при получении курса: {e}")        
            

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

import os
import threading
from flask import Flask
import telebot

# Инициализация Flask-сервера для прохождения проверки порта на Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Запускаем Flask в фоновом потоке, чтобы Render видел открытый порт
threading.Thread(target=run_flask, daemon=True).start()

# --- Настройка вашего Телеграм-бота ---
# Вставьте ваш настоящий токен от BotFather в кавычки вместо "ВАШ_ТОКЕН_СЮДА"
bot = telebot.TeleBot("ВАШ_ТОКEN_СЮДА")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Бот успешно запущен на Render и работает 24/7! 🚀")

@bot.message_handler(content_types=['text'])
def send_echo(message):
    bot.send_message(message.chat.id, f"Вы написали: {message.text}")

# Запуск постоянного опроса Telegram
bot.polling(non_stop=True)

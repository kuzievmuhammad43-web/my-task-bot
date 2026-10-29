import os
import threading
from flask import Flask
import telebot

# Инициализация Flask для удовлетворения проверки Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Запуск Flask в отдельном потоке
threading.Thread(target=run_flask, daemon=True).start()

# --- Ваш бот ---
bot = telebot.TeleBot("ВАШ_ТОКЕН")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Бот успешно запущен на Render и работает 24/7!")

@bot.message_handler(content_types=['text'])
def send_echo(message):
    bot.send_message(message.chat.id, f"Вы написали: {message.text}")

bot.polling(non_stop=True)

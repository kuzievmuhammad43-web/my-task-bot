import telebot
from telebot import types

TOKEN = '9113581516:AAG2LcR7qp7dTSvZJ_kIX5CbgF8TTVjb7ns'
bot = telebot.TeleBot(TOKEN)

user_tasks = {}
user_links = {}
user_states = {}

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_tasks = types.KeyboardButton("📝 Мои задачи")
    btn_links = types.KeyboardButton("🔗 Сохраненные ссылки")
    btn_ai = types.KeyboardButton("🤖 Сократить текст")
    btn_help = types.KeyboardButton("❓ Инструкция")
    markup.row(btn_tasks, btn_links)
    markup.row(btn_ai, btn_help)
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    user_states[chat_id] = None
    welcome_text = (
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я твой личный супер-помощник.\n\n"
        "Выбери нужный раздел на клавиатуре ниже:"
    )
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_tasks:
        user_tasks[chat_id] = []
    if chat_id not in user_links:
        user_links[chat_id] = []

    if text == "📝 Мои задачи":
        user_states[chat_id] = None
        markup = types.InlineKeyboardMarkup()
        btn_add = types.InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")
        btn_clear = types.InlineKeyboardButton("🗑 Очистить всё", callback_data="clear_tasks")
        markup.add(btn_add, btn_clear)

        tasks = user_tasks[chat_id]
        if tasks:
            task_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
            bot.send_message(chat_id, f"📋 **Твои задачи:**\n\n{task_list}", parse_mode="Markdown", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Список задач пуст! Нажми кнопку ниже, чтобы добавить.", reply_markup=markup)

    elif text == "🔗 Сохраненные ссылки":
        user_states[chat_id] = None
        markup = types.InlineKeyboardMarkup()
        btn_add = types.InlineKeyboardButton("➕ Сохранить ссылку", callback_data="add_link")
        btn_clear = types.InlineKeyboardButton("🗑 Очистить ссылки", callback_data="clear_links")
        markup.add(btn_add, btn_clear)

        links = user_links[chat_id]
        if links:
            link_list = "\n".join([f"{i+1}. {l}" for i, l in enumerate(links)])
            bot.send_message(chat_id, f"🔗 **Твои ссылки:**\n\n{link_list}", parse_mode="Markdown", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Сохраненных ссылок нет. Нажми кнопку ниже, чтобы добавить.", reply_markup=markup)

    elif text == "🤖 Сократить текст":
        user_states[chat_id] = "waiting_for_text_to_summarize"
        bot.send_message(chat_id, "Пришли мне длинную статью или текст, а я выделю из него самое главное!")

    elif text == "❓ Инструкция":
        user_states[chat_id] = None
        info_text = (
            "⚙️ **Как пользоваться ботом:**\n\n"
            "• **Мои задачи:** Записывай дела и вычеркивай их по мере выполнения.\n"
            "• **Сохраненные ссылки:** Отправляй полезные статьи и сайты, чтобы не потерять.\n"
            "• **Сократить текст:** Отправь длинный текст, и бот составит его краткую выжимку."
        )
        bot.send_message(chat_id, info_text, parse_mode="Markdown")

    else:
        state = user_states.get(chat_id)
        if state == "waiting_for_task":
            user_tasks[chat_id].append(text)
            user_states[chat_id] = None
            bot.send_message(chat_id, f"✅ Задача «{text}» успешно добавлена!", reply_markup=get_main_keyboard())
        elif state == "waiting_for_link":
            user_links[chat_id].append(text)
            user_states[chat_id] = None
            bot.send_message(chat_id, "✅ Ссылка успешно сохранена!", reply_markup=get_main_keyboard())
        elif state == "waiting_for_text_to_summarize":
            user_states[chat_id] = None
            sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
            summary = ". ".join(sentences[:3]) + "." if len(sentences) >= 3 else text
            res = f"💡 **Главное из текста:**\n\n{summary}"
            bot.send_message(chat_id, res, parse_mode="Markdown", reply_markup=get_main_keyboard())
        else:
            bot.send_message(chat_id, "Воспользуйся кнопками меню ниже 👇", reply_markup=get_main_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    if call.data == "add_task":
        user_states[chat_id] = "waiting_for_task"
        bot.send_message(chat_id, "Напиши текст задачи и отправь мне:")
    elif call.data == "clear_tasks":
        user_tasks[chat_id] = []
        bot.send_message(chat_id, "🗑 Список задач очищен!")
    elif call.data == "add_link":
        user_states[chat_id] = "waiting_for_link"
        bot.send_message(chat_id, "Отправь мне ссылку:")
    elif call.data == "clear_links":
        user_links[chat_id] = []
        bot.send_message(chat_id, "🗑 Список ссылок очищен!")

print("Бот успешно запущен!")
bot.infinity_polling()
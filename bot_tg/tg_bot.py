import os
import time
import logging

import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

TG_TOKEN = os.getenv("TG_TOKEN")
ADMIN_ID = int(os.getenv("TG_ADMIN_ID", "0"))

if not TG_TOKEN:
    raise RuntimeError("TG_TOKEN не задан. Скопируйте .env.example в .env и заполните.")

bot = telebot.TeleBot(TG_TOKEN)


def get_user_info(user):
    """Универсальная функция для получения информации о пользователе."""
    username = f"@{user.username}" if user.username else ""
    return f"{username} (ID: {user.id}, Имя: {user.first_name})"


def send_welcome(chat_id, user):
    """Отправляет приветственное сообщение с меню."""
    welcome_text = (
        f"👋 Привет, *{user.first_name}*!\n\n"
        "Добро пожаловать в мою визитку!\n"
        "Выберите нужный раздел:"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛠 Услуги", callback_data="services"))
    markup.add(types.InlineKeyboardButton("⭐ Отзывы", callback_data="reviews"))
    markup.add(types.InlineKeyboardButton("📢 Телеграм канал", callback_data="TGK"))
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(commands=["start"])
def handle_start(message):
    send_welcome(message.chat.id, message.from_user)


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    except Exception as e:
        log.warning("Не удалось удалить сообщение: %s", e)

    if ADMIN_ID:
        try:
            bot.send_message(
                ADMIN_ID,
                f"Пользователь {get_user_info(call.from_user)} нажал кнопку: {call.data}",
                parse_mode="HTML",
            )
        except Exception as e:
            log.warning("Не удалось уведомить админа: %s", e)

    back_markup = types.InlineKeyboardMarkup()
    back_markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))

    if call.data == "services":
        bot.send_message(
            call.message.chat.id,
            """
🔧 *Раздел услуг*

1️⃣ 🤖 Написание ВК бота - от 500₽
→ Автоматизация сообществ ВКонтакте

2️⃣ 📩 Написание ТГ бота - от 1000₽
→ Полнофункциональные Telegram-боты

3️⃣ 💻 Создание ПК программы - По договоренности
→ Индивидуальные desktop-приложения

4️⃣ 🐍 Репетиторский курс Python
• С нуля - 800₽/урок
• Python PRO - 1500₽/урок

5️⃣ 📇 Создание визитки - от 2500₽
→ Бот-визитка с вашим контентом
""",
            parse_mode="Markdown",
            reply_markup=back_markup,
        )
    elif call.data == "reviews":
        bot.send_message(
            call.message.chat.id,
            "⭐ *Отзывы:* [перейти](https://t.me/+Yk0l7r1LmBo4NDEy)",
            parse_mode="Markdown",
            reply_markup=back_markup,
        )
    elif call.data == "TGK":
        bot.send_message(
            call.message.chat.id,
            "📢 *Мой телеграм канал:* [перейти](https://t.me/uapb169)",
            parse_mode="Markdown",
            reply_markup=back_markup,
        )
    elif call.data == "back":
        send_welcome(call.message.chat.id, call.from_user)


@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    if not ADMIN_ID:
        return
    try:
        bot.send_message(
            ADMIN_ID,
            f"Пользователь {get_user_info(message.from_user)} написал:\n\n"
            f"<code>{message.text}</code>",
            parse_mode="HTML",
        )
    except Exception as e:
        log.warning("Не удалось переслать сообщение админу: %s", e)


def run():
    """Запуск с ретраем вокруг polling, бот создаётся один раз."""
    attempt = 0
    while True:
        try:
            log.info("Бот запущен, ожидание сообщений...")
            bot.polling(none_stop=True, timeout=30, long_polling_timeout=30)
        except Exception as e:
            attempt += 1
            log.error("Ошибка polling №%s: %s", attempt, e)
            time.sleep(3)


if __name__ == "__main__":
    run()

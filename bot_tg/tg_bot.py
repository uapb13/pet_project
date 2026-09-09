import telebot
from telebot import types
import time
r = 1
while True:
    try:
        bot = telebot.TeleBot('токен')
        ADMIN_ID = 0

        def get_user_info(user):
            """Универсальная функция для получения информации о пользователе"""
            username = f"@{user.username}" if user.username else ""
            return f"{username} (ID: {user.id}, Имя: {user.first_name})"

        def send_welcome(chat_id, user):
            """Универсальная функция для отправки приветственного сообщения"""
            welcome_text = f"""
            👋 Привет, *{user.first_name}*! 

            Добро пожаловать в мою визитку! 
            Выберите нужный раздел:
            """
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🛠 Услуги", callback_data="services"))
            markup.add(types.InlineKeyboardButton("⭐ Отзывы", callback_data="reviews"))
            markup.add(types.InlineKeyboardButton("📢 Телеграм канал", callback_data="TGK"))
            
            bot.send_message(
                chat_id,
                welcome_text,
                parse_mode="Markdown",
                reply_markup=markup
            )

        @bot.message_handler(commands=['start'])
        def handle_start(message):
            send_welcome(message.chat.id, message.from_user)

        @bot.callback_query_handler(func=lambda call: True)
        def handle_inline_buttons(call):
            try:
                bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id
                )
            except Exception as e:
                print(f"Ошибка при удаления сообщения: {e}")

            # Отправляем админу информацию о действии
            bot.send_message(
                ADMIN_ID,
                f"Пользователь {get_user_info(call.from_user)} нажал кнопку: {call.data}",
                parse_mode="HTML"
            )

            if call.data == "services":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
                
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
        → Индивидуальные занятия с нуля
        • Python PRO - 1500₽/урок
        → Изучение Python на реальных задачах

        5️⃣ 📇 Создание визитки - от 2500₽
        → Бот-визитка с вашим контентом 
        """,
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            elif call.data == "reviews":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
                
                bot.send_message(
                    call.message.chat.id,
                    "⭐ *Отзывы:* [перейти](https://t.me/+Yk0l7r1LmBo4NDEy)",
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            elif call.data == "TGK":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))

                bot.send_message(
                    call.message.chat.id,
                    "📢 *Мой телеграм канал:* [перейти](https://t.me/uapb169)",
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            elif call.data == "back":
                send_welcome(call.message.chat.id, call.from_user)  # Используем call.from_user

        @bot.message_handler(func=lambda message: True)
        def forward_to_admin(message):
            bot.send_message(
                ADMIN_ID,
                f"Пользователь {get_user_info(message.from_user)} написал:\n\n<code>{message.text}</code>",
                parse_mode="HTML"
            )

        bot.polling(none_stop=True,
            timeout=30,  # Увеличиваем время ожидания
            long_polling_timeout=30 )
    except:
        r+=1
        print(f'Ошибка №{r}')
        time.sleep(3)
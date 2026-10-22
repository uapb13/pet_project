# 🐍 Pet Project — Telegram/VK боты и игра на Pygame

Набор моих pet-проектов на Python: Telegram-бот-визитка, VK-бот для управления
беседой (ролевая «армия») и аркадная игра на Pygame с таблицей рекордов.

Цель — практика работы с внешними API (Telegram Bot API, VK API),
SQLite, обработкой событий и графикой.

> ⚠️ Токены в репозитории не хранятся — замените их на свои (см. «Запуск»).

## 📦 Что внутри

| Папка | Проект | Стек |
|-------|--------|------|
| `bot_tg/` | Telegram-бот-визитка: услуги, отзывы, ссылка на канал, пересылка сообщений админу | Python, pyTelegramBotAPI |
| `vk_bot/` | VK-бот для беседы: должности, варны, муты, кики, заметки, структура «армии», генерация изображения со списком | Python, vk_api, Pillow, SQLite |
| `pyth/` | Игра «Rocket Wars»: меню, 8 уровней, режим выживания, рекорды | Python, Pygame, SQLite |

## 🚀 Быстрый старт

```bash
git clone https://github.com/uapb13/pet_project.git
cd pet_project
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows
pip install -r requirements.txt

import os
from dotenv import load_dotenv

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")
OWNER_ID = int(os.getenv("VK_OWNER_ID", "0"))
API_VERSION = "5.199"
DB_PATH = os.getenv("VK_DB_PATH", "bd_army.db")

if not VK_TOKEN:
    raise RuntimeError("VK_TOKEN не задан. Скопируйте .env.example в .env и заполните.")

RP_RANKS = [
    "Рядовой", "Ефрейтор", "Мл.Сержант", "Сержант", "Старшина", "Прапорщик",
    "Мл.Лейтенант", "Лейтенант", "Ст.Лейтенант", "Капитан", "Майор",
    "Подполковник", "Полковник", "Генерал-Майор", "Генерал-Лейтенант",
    "Генерал-Полковник", "Маршал",
]

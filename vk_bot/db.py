import sqlite3

from config import DB_PATH

con = sqlite3.connect(DB_PATH)
cursor = con.cursor()


def init_db():
    """Создаёт все таблицы, если их нет."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            должность TEXT NOT NULL,
            id_должность INTEGER NOT NULL,
            id_vk INTEGER NOT NULL UNIQUE,
            warn INTEGER DEFAULT 0,
            Komanders INTEGER DEFAULT 0,
            Rukovodstvo INTEGER DEFAULT 0,
            data TEXT DEFAULT '2067-01-01',
            salary TEXT DEFAULT '0',
            rp_rang TEXT DEFAULT 'Рядовой'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS size_beced (
            size_beced INTEGER NOT NULL,
            min_dolgnoct INTEGER NOT NULL,
            ignor TEXT,
            rykovodctvo TEXT,
            komabirs TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS setting_beced (
            num_beced INTEGER NOT NULL,
            hi_mes TEXT NOT NULL,
            bye_mes TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS structure_army (
            id_structure INTEGER PRIMARY KEY AUTOINCREMENT,
            name_structure TEXT NOT NULL,
            max_id_structure INTEGER NOT NULL,
            min_id_structure INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zametki_army (
            num_beced INTEGER NOT NULL,
            name_zametki1 TEXT NOT NULL, text_zametki1 TEXT NOT NULL,
            name_zametki2 TEXT NOT NULL, text_zametki2 TEXT NOT NULL,
            name_zametki3 TEXT NOT NULL, text_zametki3 TEXT NOT NULL,
            name_zametki4 TEXT NOT NULL, text_zametki4 TEXT NOT NULL,
            name_zametki5 TEXT NOT NULL, text_zametki5 TEXT NOT NULL,
            name_zametki6 TEXT NOT NULL, text_zametki6 TEXT NOT NULL,
            name_zametki7 TEXT NOT NULL, text_zametki7 TEXT NOT NULL,
            name_zametki8 TEXT NOT NULL, text_zametki8 TEXT NOT NULL,
            name_zametki9 TEXT NOT NULL, text_zametki9 TEXT NOT NULL,
            name_zametki10 TEXT NOT NULL, text_zametki10 TEXT NOT NULL
        )
    """)
    con.commit()


def close():
    con.commit()
    con.close()

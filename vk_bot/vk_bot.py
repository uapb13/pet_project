import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
import requests
import sqlite3
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import locale

con = sqlite3.connect("bd_army.db")
cursor = con.cursor()
import sqlite3

try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    pass

# В функции create_structures_image добавляем обработку текста
def draw_unicode_text(draw, position, text, font, fill):
    """
    Рисует текст с поддержкой Unicode
    """
    try:
        # Пробуем нарисовать как есть
        draw.text(position, text, fill=fill, font=font)
    except UnicodeEncodeError:
        # Если ошибка, пробуем конвертировать
        try:
            text_encoded = text.encode('utf-8', errors='ignore').decode('utf-8')
            draw.text(position, text_encoded, fill=fill, font=font)
        except:
            # Если совсем не получается, убираем проблемные символы
            text_clean = ''.join(c for c in text if ord(c) < 128)
            draw.text(position, text_clean, fill=fill, font=font)
# Использование employees id должность  id_vk warn Komanders Rukovodstvo data salary rp_rang
cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                должность TEXT NOT NULL,
                id_должность INTEGER NOT NULL,
                id_vk INTEGER NOT NULL UNIQUE
            )
        ''')
con.commit()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS size_beced (
                size_beced INTEGER NOT NULL,
                min_dolgnoct INTEGER NOT NULL,
                ignor TEXT,
                rykovodctvo TEXT,
                komabirs TEXT 
            )
        ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS setting_beced (
                num_beced INTEGER NOT NULL,
                hi_mes TEXT NOT NULL,
                bye_mes TEXT NOT NULL)
        ''')
con.commit()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS structure_army (
                id_structure INTEGER PRIMARY KEY AUTOINCREMENT,
                name_structure TEXT NOT NULL,
                max_id_structure INTEGER NOT NULL,
                min_id_structure INTEGER NOT NULL)
        ''')
con.commit()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS zametki_army (
                num_beced INTEGER NOT NULL,
                name_zametki1 TEXT NOT NULL,
                text_zametki1 TEXT NOT NULL,
                name_zametki2 TEXT NOT NULL,
                text_zametki2 TEXT NOT NULL,
                name_zametki3 TEXT NOT NULL,
                text_zametki3 TEXT NOT NULL,
                name_zametki4 TEXT NOT NULL,
                text_zametki4 TEXT NOT NULL,
                name_zametki5 TEXT NOT NULL,
                text_zametki5 TEXT NOT NULL,
                name_zametki6 TEXT NOT NULL,
                text_zametki6 TEXT NOT NULL,
                name_zametki7 TEXT NOT NULL,
                text_zametki7 TEXT NOT NULL,
                name_zametki8 TEXT NOT NULL,
                text_zametki8 TEXT NOT NULL,
                name_zametki9 TEXT NOT NULL,
                text_zametki9 TEXT NOT NULL,
                name_zametki10 TEXT NOT NULL,
                text_zametki10 TEXT NOT NULL
               
            )
        ''')
#1dfb3ea3f1453f!
#rp_rang

TOKEN = "токен"
vk_session = vk_api.VkApi(token=TOKEN,api_version='5.199')
vk = vk_session.get_api()
upload = VkUpload(vk_session)
longpoll = VkLongPoll(vk_session)
uapb_id = 206215526
muted_users = {}
rp_rang_list = ['Рядовой','Ефрейтор','Мл.Сержант','Сержант','Старшина','Прапорщик','Мл.Лейтенант','Лейтенант',
                'Ст.Лейтенант','Капитан','Майор','Подполковник','Полковник','Генерал-Майор',
                'Генерал-Лейтенант','Генерал-Полковник','Маршал',]


def get_conversation_peer_id(chat_id):
    """
    Преобразует ID чата в правильный формат для VK API
    """
    # Для бесед VK использует формат: 2000000000 + chat_id
    return 2000000000 + int(chat_id)

def mute_user_real(vk, user_id, duration_seconds,chat_id):

    try:
        peer_id = get_conversation_peer_id(chat_id)
        vk.messages.changeConversationMemberRestrictions(
            peer_id =peer_id,
            member_ids = [user_id],
            action='ro'
        )
        
        return True
        
    except Exception as e:
        send_chat(chat_id,e)
        return False

def unmute_user_real(vk, user_id, duration_seconds,chat_id):
    """
    Снятие мута
    """
    try:
        peer_id = get_conversation_peer_id(chat_id)
        
        vk.messages.changeConversationMemberRestrictions(
            peer_id=peer_id,
            member_ids=user_id,
            action='rw'
        )
        
        if peer_id in muted_users and user_id in muted_users[peer_id]:
            del muted_users[peer_id][user_id]
        return True
        
    except Exception as e:
        return False

def get_chat_title(peer_id):
    """
    Получает название беседы по peer_id
    
    peer_id = 2000000000 + chat_id для бесед
    или просто peer_id из события longpoll
    """
    peer_id = 2000000000+peer_id
    try:
        response = vk.messages.getConversationsById(
            peer_ids=peer_id,
            extended=1
        )
        
        # Название находится в items[0]['chat_settings']['title']
        title = response['items'][0]['chat_settings']['title']
        return title
    except Exception as e:
        return None
    
def send_forward_message(chat_id, message_text, original_message_id):
    """Отправить пересланное сообщение"""
    try:
        params = {
            'chat_id': chat_id,
            'message': message_text,
            'forward_messages': str(original_message_id),
            'random_id': 0
        }
        
        vk.messages.send(**params)
        return True
        
    except Exception as e:
        return False

def send_chat(id_chat, mes, mes_id = 0):
    if mes_id == 0:
        vk.messages.send(chat_id=id_chat,message=mes,random_id=0,disable_mentions=1)
    else:
        vk.messages.send(chat_id=id_chat,message=mes,random_id=0,disable_mentions=1,reply_to = mes_id)

def send_chat_ping(id_chat, mes,mes_id):
    vk.messages.send(chat_id=id_chat,message=mes,random_id=0,reply_to = mes_id)

def send_user(id_user, mes):
    vk.messages.send(user_id=id_user,message=mes,random_id=0)

def com_settings(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if user_id == uapb_id:
        for i in cursor.execute("SELECT * FROM size_beced"):
            send_chat(chat_id,f'''count beced - {i[0]}\n
id min - {i[1]}
ignor beced - {i[2]}
management - {i[3]}
commanders - {i[4]}''',mes_id)

def max_beced_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if user_id == uapb_id:
        for i in cursor.execute("SELECT * FROM size_beced"):
            cursor.execute('''
            UPDATE size_beced 
            SET size_beced = ?
            ''',(int(mes_ping[1]),))
            con.commit()
        send_chat(chat_id,f"✅ Теперь рассылка отправляетс в {mes_ping[1]}",mes_id)

def min_dg_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if user_id == uapb_id:
        for i in cursor.execute("SELECT * FROM size_beced"):
            cursor.execute('''
                        UPDATE size_beced 
                        SET min_dolgnoct = ?
                        ''',(int(mes_ping[1]),))
            con.commit()
        send_chat(chat_id,f"✅ Теперь минимальное значение для дж {mes_ping[1]}",mes_id)

def pin_mes_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    prov=1

    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности - айди вк - warn - командир - руководство
        if user_id == int(i[3]) and (i[5] or i[6]):
            prov = 0
            if reply_message:
                try:
                    vk_session.method("messages.pin", {
                        "peer_id": reply_message['peer_id'],
                        "message_id": reply_message['id']
                    })
                except:
                    send_chat(chat_id,'❌ Ошибка',mes_id)
                    break
            else:
                send_chat(chat_id,"❌ Для закрепа сообщения, нужно ответить на сообщение, которое ты хочешь заркепить",mes_id)
    if prov == 1:
        send_chat(chat_id,"❌ Попроси дядь с должностью повыше, закрепить сообщения",mes_id)

def number_bes_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    name_chat_maybe = get_chat_title(chat_id)
    send_chat(chat_id,f"✅ Number chat {chat_id}\nTitle chat:{name_chat_maybe}",mes_id)

def Rucovodctvo_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if "назн" == mes_ping[1] and user_id == uapb_id:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        cursor.execute('''
                UPDATE employees 
                SET Rukovodstvo = 1
                WHERE id_vk = ?
        ''', (target_id,))
        con.commit()
        send_chat(chat_id,f"✅ Новый Руководитель назначен ",mes_id)
    if "снять" == mes_ping[1] and user_id == uapb_id:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        cursor.execute('''
                UPDATE employees 
                SET Rukovodstvo = 0
                WHERE id_vk = ?
        ''', (target_id,))
        con.commit()
        send_chat(chat_id,f"✅ Руководитель снят ",mes_id)

def Komandos_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if "снять" == mes_ping[1] and user_id == uapb_id:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        cursor.execute('''
           UPDATE employees 
                SET Komanders = 0
                WHERE id_vk = ?
        ''', (target_id,))
        con.commit()
        send_chat(chat_id,f"✅ Командир снят ",mes_id)
    if "назн" == mes_ping[1] and user_id == 206215526:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        cursor.execute('''
             UPDATE employees 
                SET Komanders = 1
                WHERE id_vk = ?
        ''', (target_id,))
        con.commit()
        send_chat(chat_id,f"✅ Новый Командир назначен ",mes_id)
def setting_beced_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if "пуш" == mes_ping[1]:
        if user_id == uapb_id:
            for i in cursor.execute("SELECT * FROM size_beced"):
                cursor.execute('''
                    UPDATE size_beced 
                    SET ignor = ?
                ''',(str(i[2]).replace(f" {chat_id}", ''),))
                con.commit()
            send_chat(chat_id, "✅ В этой беседе теперь приходят пуши",mes_id)
        else: send_chat(chat_id, "❌ Попроси маршала",mes_id)
    if "игнор" == mes_ping[1]:
        if user_id == uapb_id:
            for i in cursor.execute("SELECT * FROM size_beced"):
                cursor.execute('''
                    UPDATE size_beced 
                    SET ignor = ?
                ''',(f"{i[2]} {chat_id}",))
                con.commit()
            send_chat(chat_id, "✅ В этой беседе больше не будут приходить пуши",mes_id)
        else: send_chat(chat_id, "❌ Попроси маршала",mes_id)
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if len(mes_ping)==2 and mes_ping[1]=='прив':
        prov_dg = 1

        for i in cursor.execute("SELECT * FROM setting_beced"):#num_beced, hi_mes, bye_mes
            if chat_id == int(i[0]):
                if reply_message:
                    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
                        if user_id == int(i[3]) and (i[5] or i[6]):
                            prov_dg=0
                            greeting_text = reply_message['text']
                            try:
                                cursor.execute('''
                                    UPDATE setting_beced 
                                    SET hi_mes = ?
                                    WHERE num_beced = ?
                                ''', (greeting_text, chat_id))
                                con.commit()
                                send_chat(chat_id,"✅ Приветсвие обновленно",mes_id)
                            except:
                                send_chat(chat_id,'❌ Ошибка',mes_id)
                                break
                    if prov_dg == 1:
                        send_chat(chat_id,"❌ Попроси дядь с должностью повыше, создать приветсвие",mes_id)
                else:
                    send_chat(chat_id,"❌ Для создания приветсвия, нужно ответить на сообщение, которое ты хочешь сделать привественным",mes_id)
    elif len(mes_ping)==2 and mes_ping[1] == 'пока':
        prov_dg = 1
        for i in cursor.execute("SELECT * FROM setting_beced"):#num_beced, hi_mes, bye_mes
            if chat_id == int(i[0]):
                if reply_message:
                    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
                        if user_id == int(i[3]) and (i[5]or i[6]):
                            prov_dg=0
                            greeting_text = reply_message['text']
                            try:
                                cursor.execute('''
                                    UPDATE setting_beced 
                                    SET bye_mes = ?
                                    WHERE num_beced = ?
                                ''', (greeting_text, chat_id))
                                con.commit()
                                send_chat(chat_id,"✅ Прощание обновленно",mes_id)
                            except:
                                send_chat(chat_id,'❌ Ошибка',mes_id)
                                break
                    if prov_dg == 1:
                        send_chat(chat_id,"❌ Попроси дядь с должностью повыше, создать прощание",mes_id)
                else:
                    send_chat(chat_id,"❌ Для создания прощания, нужно ответить на сообщение, которое ты хочешь сделать прощанием",mes_id)

def Nazn_dg_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
        if user_id == int(i[3]):
            if i[5] or i[6]:
                if int(i[2]) > int(mes_ping[2]):
                    dol = ''
                    dol = ' '.join(mes_ping[3:])
                    if "|" not in dol:
                        send_chat(chat_id,'❌ Вы забыли палочку "|", достаньте её из жопы, вставьте в вашу команду и попробуйте ещё раз',mes_id)
                        return
                    if len(dol[dol.find('|'):]) < 3:
                        send_chat(chat_id,'❌ После палки, вы должны написать никнейм солдата, пример:\n\n!назн @юзер <номер дж> <Название дж> | <никнейм>\n\nЖду.',mes_id)
                        return
                    target_id_str = mes_ping[1]
                    try:target_id = int(target_id_str[3:target_id_str.find('|')])
                    except:
                        send_chat(chat_id,'❌ Неправильный @юзер',mes_id)
                        return
                    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                    target_user = cursor.fetchone()
                    try:int(mes_ping[2])
                    except:
                        send_chat(chat_id,'❌ Неправильно указана цифра должности',mes_id)
                        return
                    if target_user:
                        if int(target_user[2]) > int(i[2]):
                            send_chat(chat_id,"❌ Не трожь дядь сверху, проклянут",mes_id)
                            return
                        cursor.execute('''
                            UPDATE employees 
                            SET должность = ?, id_должность = ? 
                            WHERE id_vk = ?
                        ''', (dol, int(mes_ping[2]), target_id))
                        con.commit()
                        send_chat(chat_id, f"✅ [id{mes_ping[1][3:12]}|Солдат] принят на должность {dol}",mes_id)
                        break
                    else:
                        cursor.execute('''
                            INSERT INTO employees (должность, id_должность,id_vk) 
                            VALUES (?, ?,?)
                            ''', (dol, int(mes_ping[2]), target_id))
                        con.commit()
                        send_chat(chat_id, f"✅ [id{mes_ping[1][3:12]}|Солдат] принят на должность {dol}\n\n(Это его первая запись)",mes_id)
                        break
                
                else:
                    send_chat(chat_id,f"❌ Нельзя выдавать роль, выше или равной ваше. Ваше значение {i[2]}",mes_id)
                    break
            else:
                send_chat(chat_id,'❌ Назначать моут только командиры, доблестные адепты армии.',mes_id)

def spisok_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if len(mes_ping) == 1:
        employees = cursor.execute("SELECT * FROM employees WHERE id_должность > 0 ORDER BY id_должность DESC").fetchall()
        user_ids = [str(i[3]) for i in employees if i[3] > 0]
        
        try:
            categories = {}
            #Вывод: [(1, 'бригада', '100,', 93)]
            stru_bd = cursor.execute("SELECT * FROM structure_army ORDER BY max_id_structure DESC").fetchall() 
            for i in stru_bd:
                categories[str(i[1])] = {'title':f'{str(i[1])}\n','members':[],"max":i[2],"min":i[3]}
            
            users_info = vk.users.get(user_ids=','.join(user_ids))
            users_dict = {str(user['id']): user for user in users_info}
            
            people_num = 0
            for i in employees:
                if i[3] > 0:
                    user_id = str(i[3])
                    if user_id in users_dict:
                        user = users_dict[user_id]
                        member_str = f"{i[2]}) [id{user_id}|{user['first_name']} {user['last_name']}] - {i[1]}\n"
                        people_num += 1
                        for strukture in stru_bd:
                            if i[2] >= int(strukture[3]):
                                categories[strukture[1]]['members'].append(member_str)
                                break
            
            # Формируем общий список
            spisok = 'Должностной список армии:\n\n'
            for category in categories.values():
                if category['members']:
                    spisok += f"{category['title']}({category['max']} - {category['min']})\n"
                    spisok += ''.join(category['members'])
                    spisok += f"Людей в структуре: {len(category['members'])}\n\n"
            
            spisok += f'\nКоличество людей в армии на должности: {people_num - len(categories["Остальной-состав"]["members"])}'
            
            # Разбиваем на части, если сообщение слишком длинное
            max_length = 4000  # Оставляем запас в 96 символов
            
            if len(spisok) <= max_length:
                send_chat(chat_id, spisok,mes_id)
            else:
                # Разбиваем на части
                parts = []
                current_part = ''
                
                for line in spisok.split('\n'):
                    if len(current_part) + len(line) + 1 <= max_length:
                        current_part += line + '\n'
                    else:
                        parts.append(current_part.strip())
                        current_part = line + '\n'
                
                if current_part:
                    parts.append(current_part.strip())
                
                # Отправляем частями
                for i, part in enumerate(parts, 1):
                    message = f"[Часть {i}/{len(parts)}]\n{part}"
                    send_chat(chat_id, message,mes_id)
                    
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            send_chat(chat_id, f"❌ Ошибка при получении списка: {e}\n\nПодробности:\n{error_details}",mes_id)
    if len(mes_ping) == 2 and mes_ping[1] == 'рп':
        rank_index = {rank: idx for idx, rank in enumerate(rp_rang_list)}

        # Получаем данные из БД (исключая Рядового)
        employees = cursor.execute("SELECT * FROM employees WHERE rp_rang != 'Рядовой'").fetchall()

        # Сортируем по рангу в обратном порядке (от высшего к низшему)
        sorted_employees = sorted(employees, key=lambda x: rank_index.get(x[9], 999), reverse=True)

        # Выводим результат
        
        itog_rp_list = 'РП звания:\n\n'
        n_rp_list = 1
        for employee in sorted_employees:
            target_nick_str = employee[1]
            target_nick = target_nick_str[target_nick_str.find('|')+1:]
            itog_rp_list+=f"{n_rp_list}) [id{employee[3]}|{target_nick}] - {employee[9]}\n"
            n_rp_list+=1
        send_chat(chat_id,itog_rp_list,mes_id)
def structure_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if user_id != uapb_id:
        send_chat(chat_id,'❌ Тебе с этим работать нельзя')
        return
    if mes_ping[1] == "список":
        stru_bd = cursor.execute("SELECT * FROM structure_army ORDER BY max_id_structure DESC").fetchall()
        spisok_fun_stru = '\n'.join([f"ID: {row[0]}, Название: {row[1]}, Max: {row[2]} Min: {row[3]}" for row in stru_bd])
        if spisok_fun_stru == '[]':
            send_chat(chat_id,'✅ Пусто')
        else:
            send_chat(chat_id,spisok_fun_stru)#Вывод: [(1, 'бригада', '100,', 93)]
    if mes_ping[1] == "добавить":
        if len(mes_ping)!= 5:
            send_chat(chat_id,"❌ !список добавить <Название> <макс> <мин>")
            return
        if not mes_ping[3].isdigit() and not mes_ping[4].isdigit():
            send_chat(chat_id,"❌ Последнии два аргумента должны быть числом")
            return
        cursor.execute('''
                         INSERT INTO structure_army (name_structure, max_id_structure, min_id_structure) 
                         VALUES (?, ?, ?)
        ''', (mes_ping[2], mes_ping[3],mes_ping[4],))
        con.commit()
        send_chat(chat_id,f'✅ Структура {mes_ping[2]} создана\n\nМаксимальная должность: {mes_ping[3]}\nМинимальная должность: {mes_ping[4]}')
        return
    
    if mes_ping[1] == "обновить":
        # Формат: !список обновить <id> <название> <макс> <мин>
        if len(mes_ping) != 6:
            send_chat(chat_id, "❌ !список обновить <ID> <Название> <макс> <мин>")
            return
        if not mes_ping[2].isdigit():
            send_chat(chat_id, "❌ ID должно быть числом")
            return

        if not mes_ping[4].isdigit() or not mes_ping[5].isdigit():
            send_chat(chat_id, "❌ Макс и мин должны быть числами")
            return
        structure_id = int(mes_ping[2])
        new_name = mes_ping[3]
        new_max = mes_ping[4]
        new_min = mes_ping[5]
        # Проверяем, существует ли запись с таким ID
        check = cursor.execute("SELECT * FROM structure_army WHERE id_structure = ?", (structure_id,)).fetchone()
        if not check:
            send_chat(chat_id, f"❌ Запись с ID {structure_id} не найдена")
            return
        cursor.execute('''
            UPDATE structure_army 
            SET name_structure = ?, max_id_structure = ?, min_id_structure = ?
            WHERE id_structure = ?
        ''', (new_name, new_max, new_min, structure_id))
        con.commit()
        send_chat(chat_id, f'✅ Структура обновлена:\n\nID: {structure_id}\nНазвание: {new_name}\nМакс: {new_max}\nМин: {new_min}')
        return
    if mes_ping[1] == "удалить":
        # Можно удалять по ID или по названию
        if len(mes_ping) != 3:
            send_chat(chat_id, "❌ !список удалить <ID или название>")
            return
        
        search_value = mes_ping[2]
        
        if search_value.isdigit():
            # Удаляем по ID
            structure_id = int(search_value)
            check = cursor.execute("SELECT * FROM structure_army WHERE id_structure = ?", (structure_id,)).fetchone()
            if not check:
                send_chat(chat_id, f"❌ Запись с ID {structure_id} не найдена")
                return
            
            cursor.execute("DELETE FROM structure_army WHERE id_structure = ?", (structure_id,))
            con.commit()
            send_chat(chat_id, f"✅ Запись с ID {structure_id} удалена")
        else:
            # Удаляем по названию (удаляет все совпадения, если есть дубликаты)
            check = cursor.execute("SELECT * FROM structure_army WHERE name_structure = ?", (search_value,)).fetchall()
            if not check:
                send_chat(chat_id, f"❌ Запись с названием '{search_value}' не найдена")
                return
            
            cursor.execute("DELETE FROM structure_army WHERE name_structure = ?", (search_value,))
            con.commit()
            send_chat(chat_id, f"✅ Удалено {len(check)} записей с названием '{search_value}'")
        return
    
        

    
def dg_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    proverka = 1
    target_id = user_id
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if reply_message and len(mes_ping)==1:
        target_id = reply_message['from_id']
    elif len(mes_ping)==2:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,)):#номер - должность - айди должности  - айди вк - warn
        if int(i[3]) == target_id and len(mes_ping)<=2:
            proverka-=1
            user_info = vk.users.get(user_ids=int(i[3]))
            first_name = user_info[0]['first_name']
            last_name = user_info[0]['last_name']
            send_chat(chat_id,f"[id{int(i[3])}|{first_name} {last_name}] - {i[1]} ({i[2]})",mes_id)
            break
    if proverka and len(mes_ping)<=2:
        send_chat(chat_id,f"❌ [id{target_id}|Боец] не зарегестрирован",mes_id)
def kick_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if reply_message:
        target_id = reply_message['from_id']
        if target_id != user_id:
            for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
                count_beced = int(i[0])
            for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
                if int(i[3])==user_id:
                    var_user_kick = i
                    if i[5] or i[6]:
                        cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                        target_user = cursor.fetchone()
                        if int(target_user[2])>=int(var_user_kick[2]):
                            send_chat(chat_id,"❌ Вы не можете искючить человека выше вас или равного вам",mes_id)
                            return
                        if len(mes_ping)==1:
                            try:
                                vk.messages.removeChatUser(chat_id=chat_id, user_id=target_id)
                            except:send_chat(chat_id,f"❌ [id{target_id}|Пользоватеь] не находится в чате",mes_id)
                        elif "!" == mes_ping[1]:
                            if i[6]:
                                shet = 0
                                for i in range(2,count_beced+1):#size_beced):
                                    try:
                                        vk.messages.removeChatUser(chat_id=i, user_id=target_id)
                                        shet+=1
                                    except:
                                        pass
                                send_chat(chat_id,f"✅ [id{target_id}|Пользоватеь] был исключен из {shet} чатов",mes_id)
                            else:
                                send_chat(chat_id,f"❌ Вы не сотрудник Бригады Армии",mes_id)
                    else:
                        send_chat(chat_id,f"❌ Вы не Руководство Армии",mes_id)
        else:
            send_chat(chat_id, "❌ Еблан?",mes_id)
    elif len(mes_ping) == 2:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            count_beced = int(i[0])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
            if int(i[3])==user_id:
                var_user_kick = i
                if i[5] or i[6]:
                    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                    target_user = cursor.fetchone()
                    if int(target_user[2])>=int(var_user_kick[2]):
                        send_chat(chat_id,"❌ Вы не можете искючить человека выше вас или равного вам",mes_id)
                        return
                    try:
                        vk.messages.removeChatUser(chat_id=chat_id, user_id=target_id)
                    except:send_chat(chat_id,f"❌ [id{target_id}|Пользоватеь] не находится в чате",mes_id)
                else:
                    send_chat(chat_id,f"❌ Вы не Руководство Армии",mes_id)
    elif len(mes_ping) == 3 and str(mes_ping[2]) == '!':
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            count_beced = int(i[0])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
            if int(i[3]) == user_id:
                var_user_kick = i
                if i[6]:
                    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                    target_user = cursor.fetchone()
                    if int(target_user[2])>=int(var_user_kick[2]):
                        send_chat(chat_id,"❌ Вы не можете искючить человека выше вас или равного вам",mes_id)
                        return
                    count_bec_kik=0
                    for j in range(2,count_beced+1):#size_beced):
                        try:
                            vk.messages.removeChatUser(chat_id=j, user_id=target_id)
                            count_bec_kik+=1
                        except:pass
                    send_chat(chat_id,f"✅ [id{target_id}|Пользоватеь] был исключен из {count_bec_kik} чатов",mes_id)
                else:
                        send_chat(chat_id,f"❌ Вы не сотрудник Бригады Армии",mes_id)
    else:
        send_chat(chat_id, "❌ Чет не кикается",mes_id)

def ping_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
        if user_id == int(i[3]):
            if i[5] or i[6]:
                send_chat_ping(chat_id, f'@all\n[id{user_id}|Автор]',mes_id)
            else:
                send_chat(chat_id, f"❌ Вы не являетесь Командиром Армии",mes_id)
            break

def push_uapb_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        size_beced = int(i[0])
    if user_id == uapb_id:
        original_text = message_text_orig
        push_index = original_text.lower().find('!пушь')
        if push_index != -1:
            send_mes = original_text[push_index + 5:].strip()
            if send_mes and send_mes[0] == ' ':
                send_mes = send_mes[1:]
        for i in range(size_beced):
            try:
                send_chat(i, f'{send_mes}')#\n[id{user_id}|Автор]
            except:pass
def push_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        no_beced = str(i[2])
        size_beced = int(i[0])
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
        if user_id == int(i[3]):
            if i[6]:
                original_text = message_text_orig
                send_mes = ''
                if "@all" in original_text or "@anal" in original_text:
                    send_mes = "@all"            
                for i in range(size_beced):
                    try:
                        if str(i) not in no_beced.split():
                            send_forward_message(i, send_mes,mes_id)
                    except:pass
            else:
                send_chat(chat_id,'❌ Вы не являетесь Руководством Армии',mes_id)
def ya_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if len(mes_ping)==1:
        send_chat(chat_id, f'✅ На месте\n[id{user_id}|Автор]',mes_id)

def set_bec_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if len(mes_ping)==2 and mes_ping[1]=='прив':
        prov_dg = 1
        for i in cursor.execute("SELECT * FROM setting_beced"):#num_beced, hi_mes, bye_mes
            if chat_id == int(i[0]):
                if reply_message:
                    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
                        if user_id == int(i[3]) and (i[5] or i[6]):
                            prov_dg=0
                            greeting_text = reply_message['text']
                            try:
                                cursor.execute('''
                                    UPDATE setting_beced 
                                    SET hi_mes = ?
                                    WHERE num_beced = ?
                                ''', (greeting_text, chat_id))
                                con.commit()
                                send_chat(chat_id,"✅ Приветсвие обновленно",mes_id)
                            except:
                                send_chat(chat_id,'❌ Ошибка',mes_id)
                                break
                    if prov_dg == 1:
                        send_chat(chat_id,"❌ Попроси дядь с должностью повыше, создать приветсвие",mes_id)
                else:
                    send_chat(chat_id,"❌ Для создания приветсвия, нужно ответить на сообщение, которое ты хочешь сделать привественным",mes_id)
    elif len(mes_ping)==2 and mes_ping[1] == 'пока':
        prov_dg = 1
        for i in cursor.execute("SELECT * FROM setting_beced"):#num_beced, hi_mes, bye_mes
            if chat_id == int(i[0]):
                if reply_message:
                    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
                        if user_id == int(i[3]) and (i[5] or i[6]):
                            prov_dg=0
                            greeting_text = reply_message['text']
                            try:
                                cursor.execute('''
                                    UPDATE setting_beced 
                                    SET bye_mes = ?
                                    WHERE num_beced = ?
                                ''', (greeting_text, chat_id))
                                con.commit()
                                send_chat(chat_id,"✅ Прощание обновленно",mes_id)
                            except:
                                send_chat(chat_id,'❌ Ошибка',mes_id)
                                break
                    if prov_dg == 1:
                        send_chat(chat_id,"❌ Попроси дядь с должностью повыше, создать прощание",mes_id)
                else:
                    send_chat(chat_id,"❌ Для создания прощания, нужно ответить на сообщение, которое ты хочешь сделать прощанием",mes_id)
                


def valid_user(user_id, event):
    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (user_id,))
    user = cursor.fetchone()
    now = datetime.now().isoformat()  # '2026-06-04T12:30:45.123456'
    time_now = now[:now.find('T')]
    if not user:
        cursor.execute('''
            INSERT INTO employees (должность, id_должность, id_vk,data, rp_rang) 
            VALUES (?, ?, ?, ?)
            ''', ('Рядовой', 0, user_id,time_now,'Рядовой',))
        con.commit()
def new_user_fun(event):
    if len(event.raw) > 6 and isinstance(event.raw[6], dict):
        try:
            chat_id = event.chat_id
        except:pass
        
        extra_data = event.raw[6]
        source_act = extra_data.get('source_act')
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ignor_bec = str(i[2])
        if source_act == 'chat_invite_user':
            for i in cursor.execute("SELECT * FROM setting_beced"):
                if chat_id == int(i[0]):
                    himes_fun = i[1]
            source_mid = extra_data.get('source_mid')
            if source_mid:
                if str(source_mid).startswith('-'):
                    try:
                        group_info = vk_session.method('groups.getById', {
                            'group_id': str(source_mid).replace('-', '')
                        })
                        if group_info:
                            group_name = group_info[0].get('name', 'Неизвестно')
                            send_chat(chat_id,f"Приглашен бот/группа: {group_name}")
                    except Exception as e:
                        pass
                else:
                    try:
                        user_info = vk_session.method('users.get', {
                            'user_ids': source_mid,
                            'fields': 'first_name,last_name'
                        })
                        if user_info and str(chat_id) not in ignor_bec.split():
                            first_name = user_info[0].get('first_name', '')
                            last_name = user_info[0].get('last_name', '')
                            full_name = f"{first_name} {last_name}"
                            send_chat(chat_id,f"[id{source_mid}|{full_name}]\n{himes_fun}")
                    except Exception as e:
                        pass
        if source_act == 'chat_kick_user':
            try:
                if str(chat_id) not in ignor_bec.split():
                    for i in cursor.execute("SELECT * FROM setting_beced"):
                        if chat_id == int(i[0]):
                            byemes_fun = i[2]
                            break
                    send_chat(chat_id,f"{byemes_fun}")
            except:pass

def zametka_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if mes_ping[1]=='добавить':
        size_beced = cursor.execute("SELECT * FROM size_beced").fetchall()#кол-во бесед - мин айди - игнор бесед - руководство - командиры.fetchall()  
        ruk = str(size_beced[0][3]).split()
        kom = str(size_beced[0][4]).split()
        employees = cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)).fetchall()#номер - должность - айди должности  - айди вк - warn - командир - руководство
        if not employees:
            send_chat(chat_id, '❌ Вы не найдены в базе данных сотрудников',mes_id)
            return
        if not (employees[0][5] or employees[0][6]):
            send_chat(chat_id,'❌ Создавать заметки сообщения, могут только Бригада и Командиры, тебе стоит дослужить до этого, щенок, прежде чем закреплять',mes_id)
            return
        if len(mes_ping) < 2:
            send_chat(chat_id,"❌ Дайте название заметки, сударь",mes_id)
            return
        name_zametki = ' '.join(mes_ping[2:])
        messages = vk.messages.getById(message_ids=mes_id)
        msg_data = messages['items'][0]
        reply_message = msg_data.get('reply_message')
        if not reply_message:
            send_chat(chat_id,"❌ Отвечать на сообщение я сам должен?",mes_id)
            return
        text_zametki = reply_message['text']
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        existing = cursor.fetchone()
        if existing:
            for j in range(1, 21, 2):  
                if existing[j] == name_zametki:
                    send_chat(chat_id,"❌ Такая заметка уже есть, заметочник фигов",mes_id)
                    return
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        zametki = cursor.fetchone()
        if zametki:
            for j in range(1, 21, 2): 
                if zametki[j] == 'чисто':
                    name_index = j
                    text_index = j + 1
                    
                    cursor.execute(f"""
                        UPDATE zametki_army 
                        SET name_zametki{(j+1)//2} = ?, text_zametki{(j+1)//2} = ?
                        WHERE num_beced = ?
                    """, (name_zametki, text_zametki, chat_id))
                    con.commit()
                    send_chat(chat_id,"✅ Заметка создана",mes_id)
                    return
            send_chat(chat_id,'❌ Максимум 10 заметок в этом чате',mes_id)

    elif mes_ping[1] == 'список':
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        zametki = cursor.fetchone()
        if not zametki:
            send_chat(chat_id,'❌ В этом чате заметок нет',mes_id)
            return
        zametki_list = []
        for j in range(1, 21, 2):
            if zametki[j] != 'чисто': 
                zametki_list.append(zametki[j])
        count_zametok = len(zametki_list)
        if count_zametok==0:
            send_chat(chat_id,'❌ В этом чате, заметок нет',mes_id)
            return
        else:
            message_text = f"📋 В этом чате [{count_zametok}/10] заметок:\n\n"
            index = 1
            for name in zametki_list:
                message_text += f"{index}) {name}\n"
                index+=1
            send_chat(chat_id,message_text,mes_id)

    elif mes_ping[1] == 'просмотр' or mes_ping[1] == 'показать':
        if len(mes_ping) < 3:
            send_chat(chat_id,"❌ Укажите номер заметки для просмотра",mes_id)
            return
        try:
            note_index = int(mes_ping[2])
        except ValueError:
            send_chat(chat_id,"❌ Номер заметки должен быть числом",mes_id)
            return
        if note_index < 1 or note_index > 10:
            send_chat(chat_id,"❌ Номер заметки должен быть от 1 до 10",mes_id)
            return
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        zametki = cursor.fetchone()
        if not zametki:
            send_chat(chat_id,"📋 В этом чате заметок нет",mes_id)
            return
        name_index = (note_index - 1) * 2 + 1  
        text_index = name_index + 1  
        
        name_zametki = zametki[name_index]
        text_zametki = zametki[text_index]
        if name_zametki == 'чисто':
            send_chat(chat_id,f"❌ Заметки под номером {note_index} не существует",mes_id)
            return
        message_text = f"📝 Заметка №{note_index}\n"
        message_text += f"📌 Название: {name_zametki}\n"
        message_text += f"📄 Текст:\n{text_zametki}"
        
        send_chat(chat_id, message_text,mes_id)
    
    elif mes_ping[1] == 'удалить':
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
            if int(i[3])==user_id:
                if not (i[5] or i[6]):
                    send_chat(chat_id,'❌ Удалять заметки сообщения, могут только Бригада и Командиры, тебе стоит дослужить до этого, щенок, прежде чем закреплять',mes_id)
                    return
        if len(mes_ping) < 3:
            send_chat(chat_id,"❌ Укажите номер заметки для удаления",mes_id)
            return
        try:
            note_index = int(mes_ping[2])
        except ValueError:
            send_chat(chat_id,"❌ Номер заметки должен быть числом",mes_id)
            return
        if note_index < 1 or note_index > 10:
            send_chat(chat_id,"❌ Номер заметки должен быть от 1 до 10",mes_id)
            return
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        zametki = cursor.fetchone()
        if not zametki:
            send_chat(chat_id,"📋 В этом чате заметок нет",mes_id)
            return
        name_index = (note_index - 1) * 2 + 1
        if zametki[name_index] == 'чисто':
            send_chat(chat_id,f"❌ Заметки под номером {note_index} не существует",mes_id)
            return
        name_zametki = zametki[name_index]
        cursor.execute(f"""
            UPDATE zametki_army 
            SET name_zametki{note_index} = ?, text_zametki{note_index} = ?
            WHERE num_beced = ?
        """, ('чисто', 'чисто', chat_id))
        con.commit()
        send_chat(chat_id,f'✅ Заметка "{name_zametki}" удалена',mes_id)
    if len(mes_ping) == 1:
        send_chat(chat_id,f'❌ И че заметка? Зачем ты тратишь мои нервы и силы попосту. Напиши "добавить/удалить/просмотр/список"',mes_id)

def mute_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if len(mes_ping) == 2:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
            if int(i[3])==user_id:
                if i[5] or i[6]:
                    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                    target_user = cursor.fetchone()
                    if int(target_user[2])>=int(i[2]):
                        if mute_user_real(vk, user_id, 60,chat_id):
                            send_chat(chat_id,f"❌ Кого ты пытаешся замутить, солага? Вот тебе мут попытку саботажа, напиши командиру, что бы размутил",mes_id)
                            name_chat_maybe = get_chat_title(chat_id)
                            try: send_user(user_id,f'Вы получили мут в чате "{name_chat_maybe}", сочуствую')
                            except: pass
                            return
                        else:
                            send_chat(chat_id,'❌ Временно не работает',mes_id)
                            return
                    else:
                        if mute_user_real(vk, target_id, 60,chat_id):
                            send_chat(chat_id,f"🔇 [id{target_id}|Пользователь] замучен",mes_id)
                            name_chat_maybe = get_chat_title(chat_id)
                            try: send_user(target_id,f'Вы получили мут в чате "{name_chat_maybe}", сочуствую')
                            except: pass
                            return
                        else:
                            send_chat(chat_id,'❌ Временно не работает',mes_id)
                            return
                else:
                    if mute_user_real(vk, user_id, 60,chat_id):
                        send_chat(chat_id,'❌ Кого ты пытаешся замутить, солага? Вот тебе мут попытку саботажа, напиши командиру, что бы размутил',mes_id)
                        return
                    return
    if len(mes_ping) == 1:
        messages = vk.messages.getById(message_ids=mes_id)
        msg_data = messages['items'][0]
        reply_message = msg_data.get('reply_message')
        if not reply_message:
            send_chat(chat_id,f'❌ Кого ты мутишь то? На сообщение ответь',mes_id)
            return
        target_id = reply_message['from_id']
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
            if int(i[3])==user_id:
                target_id = reply_message['from_id']
                if i[5] or i[6]:
                    if target_id == user_id:
                        send_chat(chat_id,"❌ Ты че, садист?",mes_id)
                        return
                    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                    target_user = cursor.fetchone()
                    if int(target_user[2])>=int(i[2]):
                        if mute_user_real(vk, user_id, 60,chat_id):
                            send_chat(chat_id,f"❌ Кого ты пытаешся замутить, солага? Вот тебе мут попытку саботажа, напиши командиру, что бы размутил",mes_id)
                            name_chat_maybe = get_chat_title(chat_id)
                            try: send_user(target_id,f'Вы получили мут в чате "{name_chat_maybe}", сочуствую')
                            except: pass
                            return
                        else:
                            send_chat(chat_id,'❌ Временно не работает',mes_id)
                            return
                    else:
                        if mute_user_real(vk, target_id, 60,chat_id):
                            send_chat(chat_id,f"🔇 [id{target_id}|Пользователь] замучен")
                            name_chat_maybe = get_chat_title(chat_id)
                            try: send_user(target_id,f'Вы получили мут в чате "{name_chat_maybe}", сочуствую')
                            except: pass
                            return
                        else:
                            send_chat(chat_id,'❌ Временно не работает',mes_id)
                            return
                else:
                    if mute_user_real(vk, user_id, 60,chat_id):
                        send_chat(chat_id,'❌ Кого ты пытаешся замутить, солага? Вот тебе мут попытку саботажа, напиши командиру, что бы размутил',mes_id)
                        return
                    return
def unmute_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if len(mes_ping) == 2:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
            if int(i[3])==user_id:
                if i[5] or i[6]:
                    if unmute_user_real(vk, target_id, 60,chat_id):
                        send_chat(chat_id,f"🔇 [id{target_id}|Пользователь] размучен ✅",mes_id)
                        return
                    else:
                        send_chat(chat_id,'❌ не размучен, к счастью',mes_id)
                        return
                else:
                    if mute_user_real(vk, user_id, 60,chat_id):
                        send_chat(chat_id,'❌ Кого ты пытаешся размутить, солага? Вот тебе мут попытку саботажа, напиши командиру, что бы размутил',mes_id)
                        return
                    return
    if len(mes_ping) == 1:
        messages = vk.messages.getById(message_ids=mes_id)
        msg_data = messages['items'][0]
        reply_message = msg_data.get('reply_message')
        if not reply_message:
            send_chat(chat_id,f'❌ Кого ты размутишь то? На сообщение ответь',mes_id)
            return
        target_id = reply_message['from_id']
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
            if int(i[3])==user_id:
                target_id = reply_message['from_id']
                if i[5] or i[6]:
                    if unmute_user_real(vk, target_id, 60,chat_id):
                        send_chat(chat_id,f"🔇 [id{target_id}|Пользователь] размучен",mes_id)
                        return
                    else:send_chat(chat_id,'❌ Временно не работает',mes_id)
                else:
                    if mute_user_real(vk, user_id, 60,chat_id):
                        send_chat(chat_id,'❌ Кого ты пытаешся размутить, солага? Вот тебе мут попытку саботажа, напиши командиру, что бы размутил',mes_id)
                        return
                    return
def comands_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if len(mes_ping)==1:
        send_chat(chat_id,"""Команды бота:
‼Общие команды:‼
!чат_н - Показать номер чата.
!список - Показать дж список армии.
!я - Проверка бота.
!комы - Показать доступные команды.
!дж - Показать свою должность в армии или другого солдата.
!варнлист - Показать список игроков с выгоыоврами
!инфо @юзер - Узнать информацию о солдате
!ник @юзер - Узнать ник по вк
!вк <ник> - Узнать вк по нику
                  
‼Команды командиров:‼
!пинг - Оповестить всю беседу.
                  
!закреп - Закрепить ответное сообщение.

!заметка (добавить "название"/удалить "номер заметки"/просмотр "номер заметки"/показать "номер заметки"/список) - Добавить заметку из ответного сообщения/ удалить заметку по её номеру /посмотреть заметку по её номеру.

!кик @юзер/!кик @юзер ! - Удалить человека из чата/Удалить из всех чатов армии.

!мут @юзер/!размут @юзер - мут/размут человека в чате

!назн @юзер <номер дж> <Название дж> | <Ник>- Добавление человека на дж.

!беседа (прив/пока) - Добавляет приветственное/прощальное сообщение  чата

!варн @юзер (+/-) - Выдача варна/снятие варна
                  
!снять @юзер - Очистить польностью данные об игрке(увольнение)

!дата @юзер - Назначить человеку дату вступления в армию
                  
!зп @юзер <Сумма> - Назначить человеку зарплату

‼Команды руководства:‼
!датад @юзер <2067-01-01> - Поменять дату начала службы Солдату по формату "Год-Месяц-День"
!пуш - Оповещение во все чаты
!кик @юзер ! - Удалить Солдата из всех чатов
                  
‼Недоступные команды:‼
!Настройки.
!Макс_бесед.
!мин_дж.
!рук.
!ком.
!пушь.
!беседа (пуш/игнор)
!структура
!назню""",mes_id)
def warnlist_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    g = ''
    num = 1
    employees = cursor.execute("SELECT * FROM employees WHERE warn > 0 ORDER BY warn DESC").fetchall() # номер - должность - айди должности  - айди вк - warn
    user_ids = [str(i[3]) for i in employees if i[3] > 0]
    users_info = vk.users.get(user_ids=','.join(user_ids))
    users_dict = {str(user['id']): user for user in users_info}
    for i in employees:
        if i[3] > 0:  
            user_id = str(i[3])
            if user_id in users_dict:
                user = users_dict[user_id]
                g += f"{num}) [id{user_id}|{user['first_name']} {user['last_name']}]({i[1][i[1].find('|')+2:]}) - {i[4]}\n"
                num+=1
    if num == 1:
        send_chat(chat_id,"✅ Варнлист пуст. Поведение солдат достойно похвалы.",mes_id)
    else:send_chat(chat_id,f'Хулиганы армии: \n\n{g}',mes_id)

def warn_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,))#номер - должность - айди должности  - айди вк - warn - командир - руководство
    employee = cursor.fetchone()
    if employee:
        if not (employee[5] or employee[6]):
            send_chat(chat_id,'❌ Работа с варнами лежит на плечах Командиров и Бригады, не трогай их команды, огузок.',mes_id)
            return
    if len(mes_ping)>3 or len(mes_ping)==1 :
        send_chat(chat_id,'❌ Неправильно прописана команда. \n\nВарн @юзер +/-',mes_id)
        return
    if len(mes_ping)==2:
        messages = vk.messages.getById(message_ids=mes_id)
        msg_data = messages['items'][0]
        reply_message = msg_data.get('reply_message')
        if not reply_message:
            send_chat(chat_id,"❌ Отвечать на сообщение я сам должен?",mes_id)
            return
        target_id = reply_message['from_id']
        if target_id == user_id:
            send_chat(chat_id,"❌ Ты че, садист?",mes_id)
            return
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк - warn
            if int(i[3])==target_id:
                num_warn = int(i[4])
                if mes_ping[1]=="+":
                    cursor.execute('''
                            UPDATE employees 
                            SET warn = ? 
                            WHERE id_vk = ?
                        ''', (num_warn+1, target_id))
                    con.commit()
                    send_chat(chat_id,f"✅ Варн выдан. Теперь у солдата [{num_warn+1}/3]",mes_id)
                elif mes_ping[1]=="-":
                    if num_warn > 0:
                        cursor.execute('''
                                UPDATE employees 
                                SET warn = ? 
                                WHERE id_vk = ?
                            ''', (num_warn-1, target_id))
                        con.commit()
                        send_chat(chat_id,f"✅ Варн снят. Теперь у солдата [{num_warn-1}/3]",mes_id)
                    else:send_chat(chat_id,"❌ Он не имеет варнов",mes_id)
                else:send_chat(chat_id,f"❌ И как мне реагировать на {mes_ping[1]}?",mes_id)
    elif len(mes_ping)== 3:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        if target_id == user_id:
            send_chat(chat_id,"❌ Ты че, садист?",mes_id)
            return
        try:
            int(target_id)
        except:
            send_chat(chat_id,'❌ Неправильный @юзер',mes_id)
            return
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк - warn
            if int(i[3])==target_id:
                num_warn = int(i[4])
                if mes_ping[2]=="+":
                    cursor.execute('''
                            UPDATE employees 
                            SET warn = ? 
                            WHERE id_vk = ?
                        ''', (num_warn+1, target_id))
                    con.commit()
                    send_chat(chat_id,f"✅ Варн выдан. Теперь у солдата [{num_warn+1}/3]",mes_id)
                elif mes_ping[2]=="-":
                    if num_warn > 0:
                        cursor.execute('''
                                UPDATE employees 
                                SET warn = ? 
                                WHERE id_vk = ?
                            ''', (num_warn-1, target_id))
                        con.commit()
                        send_chat(chat_id,f"✅ Варн снят. Теперь у солдата [{num_warn-1}/3]",mes_id)
                    else:send_chat(chat_id,"❌ Он не имеет варнов",mes_id)
                else:
                    send_chat(chat_id,f"❌ И как мне реагировать на {mes_ping[1]}?",mes_id)
        

def leave_dj_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство
        if user_id == int(i[3]):
            if i[5] or i[6]:
                if len(mes_ping) == 2:
                    target_id_str = mes_ping[1]
                    try:target_id = int(target_id_str[3:target_id_str.find('|')])
                    except:
                        send_chat(chat_id,'❌ Неправильный @юзер',mes_id)
                        return
                elif len(mes_ping) == 1:
                    messages = vk.messages.getById(message_ids=mes_id)
                    msg_data = messages['items'][0]
                    reply_message = msg_data.get('reply_message')
                    if reply_message:
                        target_id = reply_message['from_id']
                    else:
                        send_chat(chat_id,'❌ Ты шлюху снимаешь? Нормально ответь на сообщение человека, кого снять',mes_id)
                        return
                else:
                    send_chat(chat_id,'❌ Что-то не то',mes_id)
                    return
                cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                target_user = cursor.fetchone()
                if int(target_user[2])>=int(i[2]):
                    send_chat(chat_id,'❌ Вы не можете снять человека выше вас по должности',mes_id)
                    return
                if target_user:
                    target_rols = target_user[2]
                    cursor.execute('''
                    UPDATE employees 
                            SET Komanders = 0
                            WHERE id_vk = ?
                    ''', (target_id,))
                    con.commit()
                    cursor.execute('''
                            UPDATE employees 
                            SET Rukovodstvo = 0
                            WHERE id_vk = ?
                    ''', (target_id,))
                    con.commit()
                    cursor.execute('''
                    UPDATE employees 
                            SET data = "2067-01-01"
                            WHERE id_vk = ?
                    ''', (target_id,))
                    con.commit()
                    cursor.execute('''
                        UPDATE employees 
                        SET должность = ?, id_должность = ? , warn = ?
                            WHERE id_vk = ?
                    ''', ('Рядовой', 0,0, target_id))
                    con.commit()
                    send_chat(chat_id, f"✅ [id{target_id}|Солдат] снят",mes_id)
                    break
                else:
                    send_chat(chat_id, f"❌[id{target_id}|Солдат] не на должости ",mes_id)
                    break
                
            else:
                send_chat(chat_id,'❌ Снять могут ток командиры и Бригада.')
def uapb_Nazn_dg_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if user_id != uapb_id:
        return
    for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn
        if user_id == int(i[3]):
                    dol = ''
                    dol = ' '.join(mes_ping[3:])
                    if "|" not in dol:
                        send_chat(chat_id,'❌ Вы забыли палчку "|", достаньте её из жопы, вставьте в вашу команду и попробуйте ещё раз')
                        return
                    if len(dol[dol.find('|'):]) < 3:
                        send_chat(chat_id,'❌ После палки, вы должны написать никнейм солдата, пример:\n\n!назн @юзер <номер дж> <Название дж> | <никнейм>\n\nЖду.',mes_id)
                        return
                    target_id_str = mes_ping[1]
                    try:target_id = int(target_id_str[3:target_id_str.find('|')])
                    except:
                        send_chat(chat_id,'❌ Неправильный @юзер',mes_id)
                        return
                    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                    target_user = cursor.fetchone()
                    try:int(mes_ping[2])
                    except:
                        send_chat(chat_id,'❌ Неправмильно указана цифра должности',mes_id)
                        return
                    if target_user:
                        cursor.execute('''
                            UPDATE employees 
                            SET должность = ?, id_должность = ? 
                            WHERE id_vk = ?
                        ''', (dol, int(mes_ping[2]), target_id))
                        con.commit()
                        send_chat(chat_id, f"✅ [id{mes_ping[1][3:12]}|Солдат] принят на должность {dol}",mes_id)
                        break
                    else:
                        cursor.execute('''
                            INSERT INTO employees (должность, id_должность,id_vk) 
                            VALUES (?, ?,?)
                            ''', (dol, int(mes_ping[2]), target_id))
                        con.commit()
                        send_chat(chat_id, f"✅ [id{mes_ping[1][3:12]}|Солдат] принят на должность {dol}\n\n(Это его первая запись)",mes_id)
                        break
def Nickname_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if reply_message:
        target_id = reply_message["from_id"]
    else:
        if len(mes_ping)==1:
            for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):
                dol = i[1]
                send_chat(chat_id,dol[dol.find('|')+1:],mes_id)
                return
        try:
            target_id_str = mes_ping[1]
            target_id = int(target_id_str[3:target_id_str.find('|')])
        except:
            send_chat(chat_id,'❌ Неправильно указан юзер',mes_id)
            return
    for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк - warn
        if target_id == int(i[3]):
            dol = i[1]
            send_chat(chat_id,dol[dol.find('|')+1:],mes_id)

def poisk_vk_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    flag = 1
    try:
        poisk_nickname = mes_ping[1]
    except:
        send_chat(chat_id,'❌ Напиши ник',mes_id)
        return
    for i in cursor.execute("SELECT * FROM employees"):#номер - должность - айди должности  - айди вк - warn
        if poisk_nickname == i[1][i[1].find('|')+2:]:
            dol = i[1]
            send_chat(chat_id,f'[id{i[3]}|Ваш солдат]',mes_id)
            flag = 0
            break
    if flag:
        send_chat(chat_id,'❌ Он не армеец, либо неправильно указан ник',mes_id)

def data_fun(**kwargs):
    #{'user_id': 206215526, 'mes_ping': ['!я'], 'chat_id': 15, 'message_text_orig': '!я', 'mes_id': 278946}
    now = datetime.now().date()  # возвращает объект date
    time_now = str(now)
    mes_id = kwargs['mes_id']
    mes_ping = kwargs['mes_ping']
    user_id = kwargs['user_id']
    chat_id = kwargs['chat_id']
    for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство - дата - зп
        if user_id == int(i[3]):
            if not (i[5] or i[6]):
                send_chat(chat_id,'❌ Дату назначения имеют право устанавливать только Командиры и Руководство армии',mes_id)
                return
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if reply_message:
        target_id = reply_message["from_id"]
    else:
        try:
            target_id_str = mes_ping[1]
            target_id = int(target_id_str[3:target_id_str.find('|')])
        except:
            send_chat(chat_id,'❌ Неправильно указан юзер',mes_id)
            return
    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn- командир - руководство - дата - зп
    target_user = cursor.fetchone()
    if target_user:
        if target_user[7] != '2067-01-01':
            send_chat(chat_id,f'❌ Солдат уже на службе',mes_id)
            return
        cursor.execute('''
                    UPDATE employees 
                    SET data = ? 
                    WHERE id_vk = ?
        ''', (time_now, target_id))
        con.commit()
        send_chat(chat_id,f'✅ Готово, Солдат встал на службу: {time_now}',mes_id)
    else:
        send_chat(chat_id,f'❌ [id{target_id}|Человек] не состоит не должности в армии ',mes_id)

def rp_rang_fun(**kwargs):
    #{'user_id': 206215526, 'mes_ping': ['!я'], 'chat_id': 15, 'message_text_orig': '!я', 'mes_id': 278946}
    mes_id = kwargs['mes_id']
    mes_ping = kwargs['mes_ping']
    user_id = kwargs['user_id']
    chat_id = kwargs['chat_id']
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if reply_message and len(mes_ping)==1:
        target_id = reply_message["from_id"]
        for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство - дата - зп - рп_ранг
            if target_id == int(i[3]):
                valid_user = i
                send_chat(chat_id,f"РП звание бойца: {valid_user[9]}",mes_id)
    elif reply_message and len(mes_ping) == 2:
        target_id = reply_message["from_id"]
        if target_id == user_id:
            send_chat(chat_id,'❌ Ранг имеют право менять только другие Командиры и Руководство армии',mes_id)
            return
        for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство - дата - зп - рп_ранг
            if user_id == int(i[3]):
                valid_user = i
                if not (i[5] or i[6]):
                    send_chat(chat_id,'❌ Ранг имеют право менять только Командиры и Руководство армии',mes_id)
                    return
                else:
                    if mes_ping[1] not in rp_rang_list:
                        send_chat(chat_id,'❌ Пропишите ранг правильно, буква в букву, как он назван на сервере (без пробелов, пример: Мл.Сержант)',mes_id)
                        return
                    cursor.execute('''
                                    UPDATE employees 
                                    SET rp_rang = ? 
                                    WHERE id_vk = ?
                    ''', (mes_ping[1], target_id))
                    con.commit()
                    send_chat(chat_id,f'✅ РП Звание бойца изменено на {mes_ping[1]}',mes_id)
                    return
                        
        send_chat(chat_id,'❌ Изменить рп ранг: !ранг <Звание>\n\n(Для отвтеных команд)',mes_id)
        return
    elif len(mes_ping) == 1:
        print(1)
        for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство - дата - зп - рп_ранг
            if user_id == int(i[3]):
                send_chat(chat_id,f"Ваше РП звание бойца: {i[9]}",mes_id)
    elif len(mes_ping) == 2:
        try:
            target_id_str = mes_ping[1]
            target_id = int(target_id_str[3:target_id_str.find('|')])
        except:
            send_chat(chat_id,'❌ Неправильно указан юзер',mes_id)
            return
    elif len(mes_ping) == 3:
        try:
            target_id_str = mes_ping[1]
            target_id = int(target_id_str[3:target_id_str.find('|')])
        except:
            send_chat(chat_id,'❌ Неправильно указан юзер',mes_id)
            return
        if target_id == user_id:
            send_chat(chat_id,'❌ Ранг имеют право менять только другие Командиры и Руководство армии',mes_id)
            return
        for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство - дата - зп - рп_ранг
            if user_id == int(i[3]):
                valid_user = i
                if not (i[5] or i[6]):
                    send_chat(chat_id,'❌ РП звание имеют право менять только Командиры и Руководство армии',mes_id)
                    return
                else:
                    if mes_ping[2] not in rp_rang_list:
                        send_chat(chat_id,'❌ Пропишите ранг правильно, буква в букву, как он назван на сервере (без пробелов, пример: Мл.Сержант)',mes_id)
                        return
                    cursor.execute('''
                                    UPDATE employees 
                                    SET rp_rang = ? 
                                    WHERE id_vk = ?
                    ''', (mes_ping[2], target_id))
                    con.commit()
                    send_chat(chat_id,f'✅ РП Звание бойца изменено на {mes_ping[2]}',mes_id)
    else:
        send_chat(chat_id,f'❌ Работа с РП званием:\n\n!ранг @юзер - Посмотреть ранг\n\n!ранг @юзер <Звание> - Поменять звание',mes_id)
def info_sold_fun(**kwargs):
    #{'user_id': 206215526, 'mes_ping': ['!я'], 'chat_id': 15, 'message_text_orig': '!я', 'mes_id': 278946}
    try:
        mes_id = kwargs['mes_id']
        mes_ping = kwargs['mes_ping']
        user_id = kwargs['user_id']
        chat_id = kwargs['chat_id']
        messages = vk.messages.getById(message_ids=mes_id)
        msg_data = messages['items'][0]
        reply_message = msg_data.get('reply_message')
        if reply_message and len(mes_ping)==1:
            target_id = reply_message["from_id"]
        elif len(mes_ping)==1:
            target_id = user_id
        elif len(mes_ping)==2:
            try:
                target_id_str = mes_ping[1]
                target_id = int(target_id_str[3:target_id_str.find('|')])
            except:
                send_chat(chat_id,'❌ Неправильно указан юзер',mes_id)
                return
        cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn - командир - руководство - дата - зп
        target_user = cursor.fetchone()
        if target_user:
            if int(target_user[5]):
                role_sold = 'Командира'
            elif int(target_user[6]):
                role_sold = 'Руководителя'
            else:
                role_sold = 'Солдата'
            if target_user[7] != "2067-01-01":
                start_date = datetime.strptime(target_user[7], "%Y-%m-%d")
                today = datetime.now()
                months = (today.year - start_date.year) * 12 + (today.month - start_date.month)
                if today.day < start_date.day:
                    months -= 1
            else:months = 0
            koeff = 1+months*0.1
            if months == 1:
                mesac = 'месяц'
            elif months >1 and months < 5:
                mesac = 'месяца'
            else:mesac = 'месяцев'
            send_chat(chat_id,f'Информация нашего [id{target_id}|{role_sold}]:\n\nНик: {target_user[1][target_user[1].find("|")+1:]}\n-------------\nДолжность: {target_user[1][:target_user[1].find("|")]} ({target_user[2]})\n-------------\nВыговоры: {target_user[4]}/3\n-------------\nДата вступления на службу: {target_user[7]}\n-------------\nВыслуга {months} {mesac}\n-------------\nРП ранг: {target_user[9]}',mes_id)
    except Exception as e:
        send_chat(15,f'{e}\n\n{mes_ping}')
def datad_fun(**kwargs):
    #{'user_id': 206215526, 'mes_ping': ['!я'], 'chat_id': 15, 'message_text_orig': '!я', 'mes_id': 278946}
    mes_id = kwargs['mes_id']
    mes_ping = kwargs['mes_ping']
    user_id = kwargs['user_id']
    chat_id = kwargs['chat_id']
    for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn - командир - руководство - дата - зп
        if user_id == int(i[3]):
            valid_user = i
            if not (i[6]):
                send_chat(chat_id,'❌ Дату назначения имеют право изменять только Руководство армии',mes_id)
                return
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if reply_message and len(mes_ping)==2:
        target_id = reply_message["from_id"]
        time_need = mes_ping[1]
    else:
        try:
            target_id_str = mes_ping[1]
            target_id = int(target_id_str[3:target_id_str.find('|')])
            time_need = mes_ping[2]
        except:
            send_chat(chat_id,'❌ Неправильно указан юзер',mes_id)
            return
    proverka_time = time_need.split('-')
    if not (proverka_time[0].isdigit() and proverka_time[1].isdigit() and proverka_time[2].isdigit()):
        send_chat(chat_id, '❌ Неверный формат времени, верный:\n\n YYYY-MM-DD',mes_id)
    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn- командир - руководство - дата - зп
    target_user = cursor.fetchone()
    if target_user:
        if int(valid_user[2]) <= int(target_user[2]) and user_id!=uapb_id:
            send_chat(chat_id,f'❌ Запрщено менять дату назначения Солдатам, выше вас',mes_id)
            return
        cursor.execute('''
                    UPDATE employees 
                    SET data = ? 
                    WHERE id_vk = ?
        ''', (time_need, target_id))
        con.commit()
        send_chat(chat_id,f'✅ Готово, Солдат встал на службу: {time_need}',mes_id)
    else:
        send_chat(chat_id,f'❌ [id{target_id}|Человек] не состоит не должности в армии ',mes_id)

def create_structures_image(categories, output_path=None):
    """
    Создаёт изображение с таблицей структур и игроков в них.
    """
    # Настройки внешнего вида
    padding = 20
    cell_padding = 10
    header_height = 50
    row_height = 30
    font_size = 13
    header_font_size = 15
    
    # Определяем количество столбцов = количество структур
    structures = [name for name, data in categories.items() if data['members']]
    num_columns = len(structures)
    
    # Если структур нет, создаём простое сообщение
    if num_columns == 0:
        img = Image.new('RGB', (500, 200), color=(30, 30, 40))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        draw.text((20, 80), "Нет данных о структурах", fill=(255, 255, 255), font=font)
        return img
    
    # Определяем максимальное количество игроков в одной структуре
    max_members = max([len(data['members']) for data in categories.values() if data['members']], default=0)
    num_rows = max(1, max_members + 1)  # +1 для заголовка
    
    # Вычисляем размеры
    column_width = max(220, 350)
    img_width = num_columns * (column_width + padding) + padding
    img_height = num_rows * row_height + header_height + padding * 2 + 50  # +50 для статистики
    
    # Создаём изображение
    img = Image.new('RGB', (int(img_width), int(img_height)), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)
    
    # Загружаем шрифты
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        header_font = ImageFont.truetype("arial.ttf", header_font_size)
        small_font = ImageFont.truetype("arial.ttf", font_size - 2)
    except:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Рисуем заголовок
    draw.text((padding, 10), "📊 Структура армии", fill=(255, 255, 255), font=header_font)
    
    # Рисуем таблицу
    for col_idx, structure_name in enumerate(structures):
        data = categories[structure_name]
        members = data['members']
        
        x = padding + col_idx * (column_width + padding)
        y = header_height + padding
        
        # Заголовок структуры
        header_text = f"{structure_name}\n({data['max']} - {data['min']})"
        header_lines = header_text.split('\n')
        
        # Рисуем фон заголовка
        draw.rectangle([x, y, x + column_width, y + header_height], fill=(50, 50, 80))
        
        # Текст заголовка
        current_y = y + 5
        for line in header_lines:
            text_bbox = draw.textbbox((0, 0), line, font=header_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = x + (column_width - text_width) // 2
            draw.text((text_x, current_y), line, fill=(255, 255, 200), font=header_font)
            current_y += header_font_size + 3
        
        # Рисуем строки с игроками
        for row_idx, member_str in enumerate(members):
            row_y = y + header_height + row_idx * row_height
            
            # Цвет строки (чередование)
            color = (60, 60, 80) if row_idx % 2 == 0 else (45, 45, 65)
            draw.rectangle([x, row_y, x + column_width, row_y + row_height], 
                         fill=color, outline=(100, 100, 130), width=1)
            
            # Обрезаем длинные строки
            display_text = member_str.strip().replace('\n', ' ')
            # Убираем лишние пробелы
            display_text = ' '.join(display_text.split())
            
            # Если текст слишком длинный, обрезаем
            if len(display_text) > 45:
                display_text = display_text[:42] + '...'
            
            # Рисуем текст
            text_bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_width > column_width - cell_padding * 2:
                draw.text((x + cell_padding, row_y + 5), display_text, 
                         fill=(200, 200, 255), font=small_font)
            else:
                draw.text((x + cell_padding, row_y + 5), display_text, 
                         fill=(200, 200, 255), font=font)
    
    # Добавляем статистику внизу
    total_people = sum([len(data['members']) for data in categories.values() if data['members']])
    stats_y = y + header_height + max_members * row_height + padding
    draw.text((padding, stats_y), 
             f"📊 Всего людей на должностях: {total_people}", 
             fill=(150, 200, 150), font=font)
    
    if output_path:
        img.save(output_path)
        return img
    else:
        return img

def send_vk_photo(chat_id, image, mes_id=None):
    """
    Отправляет изображение в VK чат
    """
    try:
        # Сохраняем изображение в байты
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Получаем сервер для загрузки
        upload_url = vk.photos.getMessagesUploadServer()['upload_url']
        
        # Загружаем фото
        files = {'photo': ('structures.png', img_byte_arr, 'image/png')}
        response = requests.post(upload_url, files=files)
        
        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.status_code}")
        
        upload_data = response.json()
        
        # Сохраняем фото в сообщениях
        photo_data = vk.photos.saveMessagesPhoto(
            photo=upload_data.get('photo'),
            server=upload_data.get('server'),
            hash=upload_data.get('hash')
        )[0]
        
        # Создаём attachment
        attachment = f"photo{photo_data['owner_id']}_{photo_data['id']}"
        
        # Отправляем сообщение с фото
        vk.messages.send(
            chat_id=chat_id,
            attachment=attachment,
            random_id=0
        )
        return True
        
    except Exception as e:
        print(f"Error sending photo: {e}")
        return False

def spisok_fun1(user_id, mes_ping, chat_id, message_text_orig, mes_id):
    if len(mes_ping) == 1:
        employees = cursor.execute("SELECT * FROM employees WHERE id_должность > 0 ORDER BY id_должность DESC").fetchall()
        user_ids = [str(i[3]) for i in employees if i[3] > 0]
        
        try:
            categories = {}
            stru_bd = cursor.execute("SELECT * FROM structure_army ORDER BY max_id_structure DESC").fetchall() 
            for i in stru_bd:
                categories[str(i[1])] = {'title': f'{str(i[1])}\n', 'members': [], "max": i[2], "min": i[3]}
            
            users_info = vk.users.get(user_ids=','.join(user_ids))
            users_dict = {str(user['id']): user for user in users_info}
            
            people_num = 0
            for i in employees:
                if i[3] > 0:
                    user_id = str(i[3])
                    if user_id in users_dict:
                        user = users_dict[user_id]
                        member_str = f"{i[2]}) {user['first_name']} {user['last_name']} - {i[1]}"
                        people_num += 1
                        for strukture in stru_bd:
                            if i[2] >= int(strukture[3]):
                                categories[strukture[1]]['members'].append(member_str)
                                break
            
            # ---- СОЗДАНИЕ И ОТПРАВКА ИЗОБРАЖЕНИЯ ----
            try:
                # Создаём изображение
                img = create_structures_image(categories)
                
                # Отправляем изображение
                success = send_vk_photo(chat_id, img, mes_id)
                
                if success:
                    # Дополнительно отправляем текстовую статистику
                    stats_message = "📊 Статистика:\n"
                    stats_message += f"Всего на должностях: {people_num}\n\n"
                    for name, data in categories.items():
                        if data['members']:
                            stats_message += f"• {name}: {len(data['members'])} чел.\n"
                    send_chat(chat_id, stats_message, mes_id)
                else:
                    # Если не удалось отправить фото, отправляем текстом
                    send_chat(chat_id, "⚠️ Не удалось отправить изображение, отправляю текстом:", mes_id)
                    send_text_spisok(categories, people_num, chat_id, mes_id)
                    
            except Exception as img_error:
                print(f"Image error: {img_error}")
                # Отправляем текстом при ошибке
                send_chat(chat_id, f"⚠️ Ошибка создания изображения, отправляю текстом:", mes_id)
                send_text_spisok(categories, people_num, chat_id, mes_id)
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            send_chat(chat_id, f"❌ Ошибка при получении списка: {e}", mes_id)

def send_text_spisok(categories, people_num, chat_id, mes_id):
    """Отправляет текстовый список как запасной вариант"""
    spisok = 'Должностной список армии:\n\n'
    for category in categories.values():
        if category['members']:
            spisok += f"{category['title']}({category['max']} - {category['min']})\n"
            spisok += '\n'.join(category['members']) + '\n'
            spisok += f"Людей в структуре: {len(category['members'])}\n\n"
    
    spisok += f'\nКоличество людей в армии на должности: {people_num}'
    
    # Разбиваем на части, если сообщение слишком длинное
    max_length = 4000
    if len(spisok) <= max_length:
        send_chat(chat_id, spisok, mes_id)
    else:
        parts = []
        current_part = ''
        for line in spisok.split('\n'):
            if len(current_part) + len(line) + 1 <= max_length:
                current_part += line + '\n'
            else:
                parts.append(current_part.strip())
                current_part = line + '\n'
        if current_part:
            parts.append(current_part.strip())
        for i, part in enumerate(parts, 1):
            send_chat(chat_id, f"[Часть {i}/{len(parts)}]\n{part}", mes_id)
Commands_full = {
    '!пуш':push_fun,
    '!пушь':push_uapb_fun,
    '!кик':kick_fun,
    '!бан':kick_fun,
    '!закреп':pin_mes_fun,
    '!дж':dg_fun,
    '!роль':dg_fun,
    '!беседа':set_bec_fun,
    "!заметка":zametka_fun,
    "!мут":mute_fun,
    "!размут":unmute_fun,
    '!варн':warn_fun,
    "!варнлист":warnlist_fun,
    '!снять':leave_dj_fun,
    '!структура':structure_fun,
    '!ник':Nickname_fun,
    '!вк':poisk_vk_fun,
    '!настройки':com_settings,
    '!макс_бесед':max_beced_fun,
    '!мин_дж':min_dg_fun,
    "!чат_н":number_bes_fun,
    '!рук':Rucovodctvo_fun,
    '!ком':Komandos_fun,
    '!беседа':setting_beced_fun,
    '!назн':Nazn_dg_fun,
    '!список':spisok_fun,
    '!админы':spisok_fun,
    '!роли':spisok_fun,
    '!пинг':ping_fun,
    '!я':ya_fun,
    '!комы':comands_fun,
    '!команды':comands_fun,
    "!назню":uapb_Nazn_dg_fun,
    "!дата":data_fun,
    '!ранг':rp_rang_fun,
    '!инфо':info_sold_fun,
    "!датад":datad_fun
}
def main():
    print("Бот запущен. Ожидание сообщений...")
    for event in longpoll.listen():
        new_user_fun(event)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            chat_bool = 0
            try:
                chat_id = event.chat_id
                chat_bool = 1
            except: pass
            user_id = event.user_id
            message_text = event.text.lower()
            message_text_orig = event.text
            mes_id = event.message_id
            mes_ping = event.text.split()
            if len(message_text) !=0 and chat_bool:
                normalized_text = re.sub(r'^!\s+', '!', message_text_orig.strip()).split()
                valid_user(user_id,event) 
                try: Commands_full[normalized_text[0].lower()](user_id=user_id,mes_ping=normalized_text,chat_id=chat_id,message_text_orig=message_text_orig,mes_id=mes_id)
                except: pass
                # if "!добавить" == mes_ping[0]:
                #     vk.messages.addChatUser(chat_id=chat_id,user_id=int(mes_ping[1][3:mes_ping[1].find('|')]))
            if not chat_bool and "заявка" in message_text:
                send_forward_message(26,'#Заявка', event.message_id)
                send_user(user_id,"Заявка принята✅\n\nКомандир напишет вам в личные сообщения одобрена или не одобрена заявка, ожидайте")
            if not chat_bool and "жалоба" in message_text:
                send_forward_message(26,'#Жалоба', event.message_id)
                send_user(user_id,"Жалоба принята✅\n\nРуководство рассмотрит её и вынесит свой вердикт. Благодарим за отзывчивость.")
            
# egeg = ''
# for i in cursor.execute("SELECT должность, id_vk FROM employees"):
#     if '|' in i[0]:
#         target_id_str = i[0]
#         target_id = target_id_str[target_id_str.find('|'):]
#         egeg += f'[id{i[1]}|{target_id}]\n'
# send_chat(1,egeg)

if __name__ == "__main__":
    while True:
        try:
            main()
        except:
            print('------------------------------------Перезагрузка-----------------------------------------')
            time.sleep(1)
cursor.close()
con.close()

#Добавиь новую запись в бд
# cursor.execute('''
                #         INSERT INTO size_beced (size_beced, min_dolgnoct) 
                #         VALUES (?, ?)
                #     ''', (35, 90,))
                # con.commit()


#Добавить новый столбец
# cursor.execute('''
                #     ALTER TABLE size_beced 
                #     ADD COLUMN ignor TEXT DEFAULT \'\'
                # ''')
                # con.commit()

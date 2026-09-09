import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
import requests
from io import BytesIO
import random as rn
import sqlite3
import re

con = sqlite3.connect("bd_prav.db")
cursor = con.cursor()
import sqlite3

# Использование
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
# cursor.execute('''
# ALTER TABLE employees 
# ADD COLUMN warn INTEGER NOT NULL DEFAULT 0
# ''')
# con.commit()

TOKEN = "токен"
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
upload = VkUpload(vk_session)
longpoll = VkLongPoll(vk_session)
uapb_id = 206215526
romanovick_id = 403876899
muted_users = {}

def get_conversation_peer_id(chat_id):
    """
    Преобразует ID чата в правильный формат для VK API
    """
    # Для бесед VK использует формат: 2000000000 + chat_id
    return 2000000000 + int(chat_id)

def get_all_chat_members(peer_id):
    """Получает список ID всех пользователей в беседе."""
    try:
        # 1. Вызываем метод getConversationMembers
        # Параметр fields='profiles' позволяет получить имена, но пока нам нужны только ID.
        response = vk.messages.getConversationMembers(
            peer_id=peer_id,
            fields='profiles'  # Опционально: подтянуть данные профиля
        )
        
        # 2. Извлекаем ID участников
        members_list = []
        for item in response['items']:
            member_id = item['member_id']
            # Отсеиваем ботов и удаленные страницы (у них member_id < 0)
            if member_id > 0:
                members_list.append(member_id)
                
        return members_list
        
    except:
        return []

def mute_user_real(vk, user_id, duration_seconds,chat_id):

    try:
        peer_id = get_conversation_peer_id(chat_id)
        vk.messages.changeConversationMemberRestrictions(
            peer_id=peer_id,
            member_ids=[user_id],
            for_=duration_seconds,  # обратите внимание на for_ (с подчеркиванием)
            action='ro'  # ro - мут (read only)
        )
        
        # Для отслеживания в боте (опционально)
        unmute_time = time.time() + duration_seconds
        if peer_id not in muted_users:
            muted_users[peer_id] = {}
        muted_users[peer_id][user_id] = unmute_time
    
        return True
        
    except Exception as e:
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

def send_chat(id_chat, mes):
    vk.messages.send(chat_id=id_chat,message=mes,random_id=0,disable_mentions=1)

def send_chat_ping(id_chat, mes):
    vk.messages.send(chat_id=id_chat,message=mes,random_id=0)

def send_user(id_user, mes):
    vk.messages.send(user_id=id_user,message=mes,random_id=0)

def com_settings(user_id,mes_ping,chat_id):
    if user_id == uapb_id or romanovick_id == user_id:
        for i in cursor.execute("SELECT * FROM size_beced"):
            send_chat(chat_id,f'''count beced - {i[0]}\n
ignor beced - {i[2]}
management - {i[3]}
commanders - {i[4]}''')

def max_beced_fun(user_id,mes_ping,chat_id):
    if user_id == uapb_id or romanovick_id == user_id:
        for i in cursor.execute("SELECT * FROM size_beced"):
            cursor.execute('''
            UPDATE size_beced 
            SET size_beced = ?
            ''',(int(mes_ping[1]),))
            con.commit()
        send_chat(chat_id,f"Теперь рассылка отправляетс в {mes_ping[1]}")

def min_dg_fun(user_id,mes_ping,chat_id):
    if user_id == uapb_id or romanovick_id == user_id:
        for i in cursor.execute("SELECT * FROM size_beced"):
            cursor.execute('''
                        UPDATE size_beced 
                        SET min_dolgnoct = ?
                        ''',(int(mes_ping[1]),))
            con.commit()
        send_chat(chat_id,f"Теперь минимальное значение для дж {mes_ping[1]}")

def pin_mes_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    prov=1
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        ryk = i[3]
        kom = i[4]
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn
        if user_id == int(i[3]) and (str(i[2]) in ryk.split() or str(i[2]) in kom.split()):
            prov = 0
            if reply_message:
                try:
                    vk_session.method("messages.pin", {
                        "peer_id": reply_message['peer_id'],
                        "message_id": reply_message['id']
                    })
                except:
                    send_chat(chat_id,'❌ Ошибка')
                    break
            else:
                send_chat(chat_id,"❌ Для закрепа сообщения, нужно ответить на сообщение, которое ты хочешь заркепить, маленький хуесос")
    if prov == 1:
        send_chat(chat_id,"❌ Попроси дядь с должностью повыше, закрепить сообщения")

def number_bes_fun(user_id,mes_ping,chat_id):
    send_chat(chat_id,f"number chat {chat_id}")

def Rucovodctvo_fun(user_id,mes_ping,chat_id):
    if "назн" == mes_ping[1] and user_id == uapb_id or romanovick_id == user_id:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк
            if int(target_id) == int(i[3]):
                target_rols = str(i[2])
                break
        for i in cursor.execute("SELECT * FROM size_beced"):
            cursor.execute('''
                UPDATE size_beced 
                SET rykovodctvo = ?
            ''',(f"{i[3]} {target_rols}",))
            con.commit()
            break
        send_chat(chat_id,f"Новый Руководитель назначен ")
    if "снять" == mes_ping[1] and user_id == uapb_id or romanovick_id == user_id:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк
            if int(target_id) == int(i[3]):
                target_rols = str(i[2])
                break
        for i in cursor.execute("SELECT * FROM size_beced"):
            cursor.execute('''
                UPDATE size_beced 
                SET rykovodctvo = ?
            ''',(i[3].replace(f" {target_rols}",""),))
            con.commit()
            break
        send_chat(chat_id,f"Руководитель снят ")

def Komandos_fun(user_id,mes_ping,chat_id):
    if "снять" == mes_ping[1] and user_id == uapb_id or romanovick_id == user_id:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк
            if target_id == int(i[3]):
                target_rols = str(i[2])
                break
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            cursor.execute('''
                UPDATE size_beced 
                SET komabirs = ?
            ''',(i[4].replace(f" {target_rols}",""),))
            con.commit()
            break
        send_chat(chat_id,f"Админ снят ")
    if "назн" == mes_ping[1] and user_id ==  uapb_id or romanovick_id == user_id:
        target_id_str = mes_ping[2]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(target_id,)):#номер - должность - айди должности  - айди вк
            if target_id == int(i[3]):
                target_rols = str(i[2])
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            cursor.execute('''
                UPDATE size_beced 
                SET komabirs = ?
            ''',(f"{i[4]} {target_rols}",))
            con.commit()
            break
        send_chat(chat_id,f"Новый Админ назначен ")
def setting_beced_fun(user_id,mes_ping,chat_id):
    
        if "пуш" == mes_ping[1]:
            if user_id == uapb_id or romanovick_id == user_id:
                for i in cursor.execute("SELECT * FROM size_beced"):
                    cursor.execute('''
                        UPDATE size_beced 
                        SET ignor = ?
                    ''',(str(i[2]).replace(f" {chat_id}", ''),))
                    con.commit()
                send_chat(chat_id, "В этой беседе теперь приходят пуши")
            else: send_chat(chat_id, "Попроси Президента")
        if "игнор" == mes_ping[1]:
            if user_id == uapb_id or romanovick_id == user_id:
                for i in cursor.execute("SELECT * FROM size_beced"):
                    cursor.execute('''
                        UPDATE size_beced 
                        SET ignor = ?
                    ''',(f"{i[2]} {chat_id}",))
                    con.commit()
                send_chat(chat_id, "В этой беседе больше не будут приходить пуши")
            else: send_chat(chat_id, "Попроси Президента")

def Nazn_dg_fun(user_id,mes_ping,chat_id):
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        ruk = str(i[3]).split()
        kom = str(i[4]).split()
    for i in cursor.execute("SELECT * FROM employees  WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn
        if user_id == int(i[3]):
            if str(i[2]) in ruk or str(i[2]) in kom:
                if int(i[2]) > int(mes_ping[2]):
                    dol = ''
                    dol = ' '.join(mes_ping[3:])
                    target_id_str = mes_ping[1]
                    try:target_id = int(target_id_str[3:target_id_str.find('|')])
                    except:
                        send_chat(chat_id,'❌ Неправильный @юзер')
                        return
                    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (target_id,))#номер - должность - айди должности  - айди вк - warn
                    target_user = cursor.fetchone()
                    try:int(mes_ping[2])
                    except:
                        send_chat(chat_id,'❌ Неправмильно указана цифра должности')
                        return
                    if target_user:
                        cursor.execute('''
                            UPDATE employees 
                            SET должность = ?, id_должность = ? 
                            WHERE id_vk = ?
                        ''', (dol, int(mes_ping[2]), target_id))
                        con.commit()
                        send_chat(chat_id, f"[id{mes_ping[1][3:12]}|Сотрудник] принят на должность {dol}✅")
                        break
                    else:
                        cursor.execute('''
                            INSERT INTO employees (должность, id_должность,id_vk) 
                            VALUES (?, ?,?)
                            ''', (dol, int(mes_ping[2]), target_id))
                        con.commit()
                        send_chat(chat_id, f"[id{mes_ping[1][3:12]}|Сотрудник] принят на должность {dol}✅ \n\n(Это его первая запись)")
                        break
                
                else:
                    send_chat(chat_id,f"❌ Нельзя выдавать роль, выше или равной ваше. Ваше значение {i[2]}")
                    break
            else:
                send_chat(chat_id,'❌ Назначать моут только админы, доблестные адепты правительства.')

def spisok_fun(user_id,mes_ping,chat_id):
    employees = cursor.execute("SELECT * FROM employees WHERE id_должность > 0 ORDER BY id_должность DESC").fetchall()  #номер - должность - айди должности  - айди вк - warn
    user_ids = [str(i[3]) for i in employees if i[3] > 0]
    try:
        categories = {
            'Pravit': {'title': '=====Правительство======\n', 'members': []},
            'zakon_vla': {'title': '\n====Законодательная власть=====\n', 'members': []},
            'FOIV': {'title': '\n========Федеральные орагны испольнительной власти=======\n', 'members': []},
            'ROIV': {'title': '\n========Региональнные орагны испольнительной власти========\n', 'members': []},
            'SV': {'title': '\n========Судебная Власть=======\n', 'members': []},
            'Advokatu': {'title': '\n=Адвокатска палата=\n', 'members': []},
            'ostalnoe': {'title': '\n=Остальной состав/Прочие роли=\n', 'members': []}
        }
        users_info = vk.users.get(user_ids=','.join(user_ids))
        users_dict = {str(user['id']): user for user in users_info}
        spisok = 'Должностной список Правительства:\n\n' 
        people_num = 0
        for i in employees:
            if i[3] > 0: 
                user_id = str(i[3])
                if user_id in users_dict:
                    user = users_dict[user_id]
                    member_str = f"{i[2]}) [id{user_id}|{user['first_name']} {user['last_name']}] - {i[1]}\n"
                    people_num+=1
                if i[2] > 100:  # Бригада (95-100)
                    categories['Pravit']['members'].append(member_str)
                elif i[2] > 80:  # Командиры
                    categories['zakon_vla']['members'].append(member_str)
                elif i[2] > 60:  # ДШБ (85-93)
                    categories['FOIV']['members'].append(member_str)
                elif i[2] > 40:  # ВП (61-84)
                    categories['ROIV']['members'].append(member_str)
                elif i[2] > 20:  # РСН (41-60)
                    categories['SV']['members'].append(member_str)
                elif i[2] > 10:  # РСН (41-60)
                    categories['Advokatu']['members'].append(member_str)
                else:  # Остальной состав (31 и ниже)
                    categories['ostalnoe']['members'].append(member_str)
        for category in categories.values():
            if category['members']:  # Проверяем, есть ли люди в категории
                spisok += category['title']
                spisok += ''.join(category['members'])
                spisok += f"Людей в отделе: {len(category['members'])}\n"
        spisok+=f'\nКоличество людей в правительстве на должности: {people_num-len(categories["ostalnoe"]["members"])}'  
        send_chat(chat_id, spisok)
    except Exception as e:
        send_chat(chat_id, f"Ошибка при получении списка: {e}")

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
        if int(i[3]) == target_id:
            proverka-=1
            user_info = vk.users.get(user_ids=int(i[3]))
            first_name = user_info[0]['first_name']
            last_name = user_info[0]['last_name']
            send_chat(chat_id,f"[id{int(i[3])}|{first_name} {last_name}] - {i[1]} ({i[2]})")
            break
    if proverka:
        send_chat(chat_id,f"[id{target_id}|Сотрудник] не зарегестрирован")
def kick_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if reply_message:
        target_id = reply_message['from_id']
        if target_id != user_id:
            for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
                ruk = str(i[3])
                count_beced = int(i[0])
            for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
                if int(i[3])==user_id:
                    if str(i[2]) in ruk.split():
                        if len(mes_ping)==1:
                            try:
                                vk.messages.removeChatUser(chat_id=chat_id, user_id=target_id)
                            except:send_chat(chat_id,f"[id{target_id}|Пользоватеь] не находится в чате")
                        elif "!" == mes_ping[1]:
                            shet = 0
                            for i in range(count_beced+1):#size_beced):
                                try:
                                    vk.messages.removeChatUser(chat_id=i, user_id=target_id)
                                    shet+=1
                                except:
                                    pass
                            send_chat(chat_id,f"[id{target_id}|Пользоватеь] был исключен из {shet} чатов")
                    else:
                        send_chat(chat_id,f"❌ Вы не сотрудник Руководства правительства")
        else:
            send_chat(chat_id, "❌ Еблан?")
    elif len(mes_ping) == 2:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ruk = str(i[3])
            count_beced = int(i[0])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
            if int(i[3])==user_id:
                if str(i[2]) in ruk.split():
                    try:
                        vk.messages.removeChatUser(chat_id=chat_id, user_id=target_id)
                    except:send_chat(chat_id,f"[id{target_id}|Пользоватеь] не находится в чате")
                else:
                        send_chat(chat_id,f"❌ Вы не сотрудник Руководства правительства")
    elif len(mes_ping) == 3 and str(mes_ping[2]) == '!':
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ruk = str(i[3])
            count_beced = int(i[0])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
            if int(i[3]) == user_id:
                if str(i[2]) in ruk.split():
                    count_bec_kik=0
                    for j in range(count_beced+1):#size_beced):
                        try:
                            vk.messages.removeChatUser(chat_id=j, user_id=target_id)
                            count_bec_kik+=1
                        except:pass
                    send_chat(chat_id,f"[id{target_id}|Пользоватеь] был исключен из {count_bec_kik} чатов")
                else:
                        send_chat(chat_id,f"❌ Вы не сотрудник Руководства правительства")
    else:
        send_chat(chat_id, "Чет не кикается")

def ping_fun(user_id,mes_ping,chat_id):
    for j in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        ruk = str(j[3])
        kom = str(j[4])
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
        if user_id == int(i[3]):
            if str(i[2]) in ruk.split() or str(i[2]) in kom.split():
                send_chat_ping(chat_id, f'@all\n[id{user_id}|Автор]')
            else:
                send_chat(chat_id, f"Вы не являетесь админом правительства")
            break

def push_uapb_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        size_beced = int(i[0])
    if user_id == uapb_id or romanovick_id == user_id:
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
        ruk = str(i[3])
        no_beced = str(i[2])
        size_beced = int(i[0])
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
        if user_id == int(i[3]):
            if str(i[2]) in ruk.split():
                original_text = message_text_orig
                send_mes = ''
                if "@all" in original_text:
                    send_mes = "@all"            
                for i in range(size_beced):
                    try:
                        if str(i) not in no_beced.split():
                            send_forward_message(i, send_mes, mes_id)
                    except:pass
            else:
                send_chat(chat_id,'Вы не являетесь Руководством правительства')
def ya_fun(user_id,mes_ping,chat_id):
    if len(mes_ping)==1:
        send_chat(chat_id, f'На месте\n[id{user_id}|Автор]')

def set_bec_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    messages = vk.messages.getById(message_ids=mes_id)
    msg_data = messages['items'][0]
    reply_message = msg_data.get('reply_message')
    if len(mes_ping)==2 and mes_ping[1]=='прив':
        prov_dg = 1
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ryk = i[3]
            kom = i[4]
        for i in cursor.execute("SELECT * FROM setting_beced"):#num_beced, hi_mes, bye_mes
            if chat_id == int(i[0]):
                if reply_message:
                    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
                        if user_id == int(i[3]) and (str(i[2]) in ryk.split() or str(i[2]) in kom.split()):
                            prov_dg=0
                            greeting_text = reply_message['text']
                            try:
                                cursor.execute('''
                                    UPDATE setting_beced 
                                    SET hi_mes = ?
                                    WHERE num_beced = ?
                                ''', (greeting_text, chat_id))
                                con.commit()
                                send_chat(chat_id,"Приветсвие обновленно")
                            except:
                                send_chat(chat_id,'Ошибка')
                                break
                    if prov_dg == 1:
                        send_chat(chat_id,"Попроси дядь с должностью повыше, создать приветсвие")
                else:
                    send_chat(chat_id,"Для создания приветсвия, нужно ответить на сообщение, которое ты хочешь сделать привественным, маленький хуесос")
    elif mes_ping[1] == 'пока':
        prov_dg = 1
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ryk = i[3]
            kom = i[4]
        for i in cursor.execute("SELECT * FROM setting_beced"):#num_beced, hi_mes, bye_mes
            if chat_id == int(i[0]):
                if reply_message:
                    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
                        if user_id == int(i[3]) and (str(i[2]) in ryk.split() or str(i[2]) in kom.split()):
                            prov_dg=0
                            greeting_text = reply_message['text']
                            try:
                                cursor.execute('''
                                    UPDATE setting_beced 
                                    SET bye_mes = ?
                                    WHERE num_beced = ?
                                ''', (greeting_text, chat_id))
                                con.commit()
                                send_chat(chat_id,"Прощание обновленно")
                            except:
                                send_chat(chat_id,'Ошибка')
                                break
                    if prov_dg == 1:
                        send_chat(chat_id,"Попроси дядь с должностью повыше, создать прощание")
                else:
                    send_chat(chat_id,"Для создания прощания, нужно ответить на сообщение, которое ты хочешь сделать прощанием, маленький хуесос")
                


def valid_user(user_id, event):
    cursor.execute("SELECT * FROM employees WHERE id_vk = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute('''
            INSERT INTO employees (должность, id_должность, id_vk,warn) 
            VALUES (?, ?, ?,?)
            ''', ('Сотрудник правительства', 0, user_id,0))
        con.commit()
def new_user_fun(event):
    if len(event.raw) > 6 and isinstance(event.raw[6], dict):
        try:
            chat_id = event.chat_id
        except:pass
        extra_data = event.raw[6]
        source_act = extra_data.get('source_act')
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
                        if user_info:
                            first_name = user_info[0].get('first_name', '')
                            last_name = user_info[0].get('last_name', '')
                            full_name = f"{first_name} {last_name}"
                            send_chat(chat_id,f"[id{source_mid}|{full_name}]\n{himes_fun}")
                    except Exception as e:
                        pass
        if source_act == 'chat_kick_user':
            try:
                for i in cursor.execute("SELECT * FROM setting_beced"):
                    if chat_id == int(i[0]):
                        byemes_fun = i[2]
                send_chat(chat_id,f"{byemes_fun}")
            except:pass

def zametka_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if mes_ping[1]=='добавить':
        size_beced = cursor.execute("SELECT * FROM size_beced").fetchall()#кол-во бесед - мин айди - игнор бесед - руководство - командиры.fetchall()  
        ruk = str(size_beced[0][3]).split()
        kom = str(size_beced[0][4]).split()
        employees = cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)).fetchall()#номер - должность - айди должности  - айди вк.fetchall()
        if not employees:
            send_chat(chat_id, 'Вы не найдены в базе данных сотрудников')
            return
        if not (str(employees[0][2]) in kom or str(employees[0][2]) in ruk):
            send_chat(chat_id,'Создавать заметки сообщения, могут только Руководство и админы тебе стоит заслужить это, щенок, прежде чем закреплять')
            return
        if len(mes_ping) < 2:
            send_chat(chat_id,"Дайте название заметки, сударь")
            return
        name_zametki = ' '.join(mes_ping[2:])
        messages = vk.messages.getById(message_ids=mes_id)
        msg_data = messages['items'][0]
        reply_message = msg_data.get('reply_message')
        if not reply_message:
            send_chat(chat_id,"Отвечать на сообщение я сам должен?")
            return
        text_zametki = reply_message['text']
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        existing = cursor.fetchone()
        if existing:
            for j in range(1, 21, 2):  
                if existing[j] == name_zametki:
                    send_chat(chat_id,"Такая заметка уже есть, заметочник фигов")
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
                    send_chat(chat_id,"Заметка создана")
                    return
            send_chat(chat_id,'Максимум 10 заметок в этом чате')

    elif mes_ping[1] == 'список':
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        zametki = cursor.fetchone()
        if not zametki:
            send_chat(chat_id,'В этом чате заметок нет')
            return
        zametki_list = []
        for j in range(1, 21, 2):
            if zametki[j] != 'чисто': 
                zametki_list.append(zametki[j])
        count_zametok = len(zametki_list)
        if count_zametok==0:
            send_chat(chat_id,'В этом чате, заметок нет')
            return
        else:
            message_text = f"📋 В этом чате [{count_zametok}/10] заметок:\n\n"
            index = 1
            for name in zametki_list:
                message_text += f"{index}) {name}\n"
                index+=1
            send_chat(chat_id,message_text)

    elif mes_ping[1] == 'просмотр' or mes_ping[1] == 'показать':
        if len(mes_ping) < 3:
            send_chat(chat_id,"❌ Укажите номер заметки для просмотра")
            return
        try:
            note_index = int(mes_ping[2])
        except ValueError:
            send_chat(chat_id,"❌ Номер заметки должен быть числом")
            return
        if note_index < 1 or note_index > 10:
            send_chat(chat_id,"❌ Номер заметки должен быть от 1 до 10")
            return
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        zametki = cursor.fetchone()
        if not zametki:
            send_chat(chat_id,"📋 В этом чате заметок нет")
            return
        name_index = (note_index - 1) * 2 + 1  
        text_index = name_index + 1  
        
        name_zametki = zametki[name_index]
        text_zametki = zametki[text_index]
        if name_zametki == 'чисто':
            send_chat(chat_id,f"❌ Заметки под номером {note_index} не существует")
            return
        message_text = f"📝 Заметка №{note_index}\n"
        message_text += f"📌 Название: {name_zametki}\n"
        message_text += f"📄 Текст:\n{text_zametki}"
        
        send_chat(chat_id, message_text)
    
    elif mes_ping[1] == 'удалить':
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ruk = str(i[3]).split()
            kom = str(i[4]).split()
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
            if int(i[3])==user_id:
                if not (str(i[2]) in kom or str(i[2]) in ruk):
                    send_chat(chat_id,'Удалять заметки сообщения, могут только Руководство и админы тебе стоит заслужить это, щенок, прежде чем закреплять')
                    return
        if len(mes_ping) < 3:
            send_chat(chat_id,"❌ Укажите номер заметки для удаления")
            return
        try:
            note_index = int(mes_ping[2])
        except ValueError:
            send_chat(chat_id,"❌ Номер заметки должен быть числом")
            return
        if note_index < 1 or note_index > 10:
            send_chat(chat_id,"❌ Номер заметки должен быть от 1 до 10")
            return
        cursor.execute("SELECT * FROM zametki_army WHERE num_beced = ?", (chat_id,))
        zametki = cursor.fetchone()
        if not zametki:
            send_chat(chat_id,"📋 В этом чате заметок нет")
            return
        name_index = (note_index - 1) * 2 + 1
        if zametki[name_index] == 'чисто':
            send_chat(chat_id,f"❌ Заметки под номером {note_index} не существует")
            return
        name_zametki = zametki[name_index]
        cursor.execute(f"""
            UPDATE zametki_army 
            SET name_zametki{note_index} = ?, text_zametki{note_index} = ?
            WHERE num_beced = ?
        """, ('чисто', 'чисто', chat_id))
        con.commit()
        send_chat(chat_id,f'✅ Заметка "{name_zametki}" удалена')
    if len(mes_ping) == 1:
        send_chat(chat_id,f'И че заметка? Зачем ты тратишь мои нервы и силы попосту. Напиши "добавить/удалить/просмотр/список"')

def mute_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if len(mes_ping) == 2:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ruk = str(i[3]).split()
            kom = str(i[4]).split()
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
            if int(i[3])==user_id:
                if str(i[2]) in kom or str(i[2]) in ruk:
                    if mute_user_real(vk, target_id, 60,chat_id):
                        send_chat(chat_id,f"🔇 [id{target_id}|Пользователь] замучен")
                        return
                    else:send_chat(chat_id,'не замучен, лох')
                else:
                    if mute_user_real(vk, user_id, 60,chat_id):
                        send_chat(chat_id,'Кого ты пытаешся замутить, солага? Вот тебе мут попытку саботажа, напиши Руководству, что бы размутил')
                    return

def unmute_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    if len(mes_ping) == 2:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ruk = str(i[3])
            kom = str(i[4])
        for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк
            if int(i[3])==user_id:
                if str(i[2]) in kom or str(i[2]) in ruk:
                    if unmute_user_real(vk, target_id, 60,chat_id):
                        send_chat(chat_id,f"🔇 [id{target_id}|Пользователь] размучен ✅")
                        return
                    else:send_chat(chat_id,'не размучен, лох')
                else:
                    if mute_user_real(vk, target_id, 60,chat_id):
                        send_chat(chat_id,'Кого ты пытаешся размутить, солага? Вот тебе мут попытку саботажа, напиши Руководству, что бы размутил')
                    return
def comands_fun(user_id,mes_ping,chat_id):
    if len(mes_ping)==1:
        send_chat(chat_id,"""Команды бота:
‼Общие команды:‼
!чат_н - Показать номер чата.
!список - Показать дж список Правитиельства.
!я - Проверка бота.
!комы - Показать доступные команды.
!дж - Показать свою должность в Правитиельстве или другого сотрудника.

‼Команды админов:‼
!пинг - Оповестить всю беседу.
!закреп - Закрепить ответное сообщение.

!заметка (добавить "название"/удалить "номер заметки"/просмотр "номер заметки"/показать "номер заметки"/список) - Добавить заметку из ответного сообщения/ удалить заметку по её номеру /посмотреть заметку по её номеру.

!кик @юзер/!кик @юзер ! - Удалить человека из чата/Удалить из всех чатов правительства.

!мут @юзер/!размут @юзер - мут/размут человека в чате

!назн @юзер <номер дж> <Название дж> - Добавление человека на дж.

!беседа (прив/пока) - Добавляет приветственное/прощальное сообщение  чата

!варн @юзер (+/-) - Выдача варна/снятие варна

‼Недоступные команды:‼
!Настройки.
!Макс_бесед.
!мин_дж.
!рук.
!ком.
!пушь.
!беседа (пуш/игнор)""")
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
                g += f"{num}) [id{user_id}|{user['first_name']} {user['last_name']}] - {i[4]}\n"
                num+=1
    if num == 1:
        send_chat(chat_id,"Варнлист пуст. Поведение сотрудников достойно похвалы.")
    else:send_chat(chat_id,f'Хулиганы правительства: \n\n{g}')

def warn_fun(user_id,mes_ping,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
            ruk = str(i[3])
            kom = str(i[4])
    cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,))#номер - должность - айди должности  - айди вк - warn
    employee = cursor.fetchone()
    if employee:
        if not (str(employee[2]) in kom or str(employee[2]) in ruk):
            send_chat(chat_id,'❌ Работа с варнами лежит на плечах Руководства и админов, не трогай их команды, огузок.')
            return
    if len(mes_ping)>3 or len(mes_ping)==1 :
        send_chat(chat_id,'❌ Неправильно прописана команда. \n\nВарн @юзер +/-')
        return
    if len(mes_ping)==2:
        messages = vk.messages.getById(message_ids=mes_id)
        msg_data = messages['items'][0]
        reply_message = msg_data.get('reply_message')
        if not reply_message:
            send_chat(chat_id,"❌ Отвечать на сообщение я сам должен?")
            return
        target_id = reply_message['from_id']
        if target_id == user_id:
            send_chat(chat_id,"❌ Ты че, садист?")
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
                    send_chat(chat_id,f"✅ Варн выдан. Теперь у сотрудника [{num_warn+1}/3]")
                elif mes_ping[1]=="-":
                    if num_warn > 0:
                        cursor.execute('''
                                UPDATE employees 
                                SET warn = ? 
                                WHERE id_vk = ?
                            ''', (num_warn-1, target_id))
                        con.commit()
                        send_chat(chat_id,f"✅ Варн снят. Теперь у сотрудника [{num_warn-1}/3]")
                    else:send_chat(chat_id,"❌ Он не имеет варнов")
                else:send_chat(chat_id,f"❌ И как мне реагировать на {mes_ping[1]}?")
    elif len(mes_ping)== 3:
        target_id_str = mes_ping[1]
        target_id = int(target_id_str[3:target_id_str.find('|')])
        if target_id == user_id:
            send_chat(chat_id,"❌ Ты че, садист?")
            return
        try:
            int(target_id)
        except:
            send_chat(chat_id,'❌ Неправильный @юзер')
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
                    send_chat(chat_id,f"✅ Варн выдан. Теперь у сотрудника [{num_warn+1}/3]")
                elif mes_ping[2]=="-":
                    if num_warn > 0:
                        cursor.execute('''
                                UPDATE employees 
                                SET warn = ? 
                                WHERE id_vk = ?
                            ''', (num_warn-1, target_id))
                        con.commit()
                        send_chat(chat_id,f"✅ Варн снят. Теперь у сотрудника [{num_warn-1}/3]")
                    else:send_chat(chat_id,"❌ Он не имеет варнов")
                else:
                    send_chat(chat_id,f"❌ И как мне реагировать на {mes_ping[1]}?")
def mute_all_fun(user_id,normalized_text,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        ruk = str(i[3]).split()
        kom = str(i[4]).split()
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn
        if int(i[3])==user_id:
            if str(i[2]) in ruk:
                peer_id = 2000000000 +chat_id
                members_var = get_all_chat_members(peer_id)
                for mute_meb in members_var:
                    try:mute_user_real(vk, mute_meb, 60,chat_id)
                    except:pass
                send_chat(chat_id,'Всех замутил Босс!')
            else:
                send_chat(chat_id,'Вы не Руководство правительства')
def unmute_all_fun(user_id,normalized_text,chat_id,message_text_orig,mes_id):
    for i in cursor.execute("SELECT * FROM size_beced"):#кол-во бесед - мин айди - игнор бесед - руководство - командиры
        ruk = str(i[3]).split()
        kom = str(i[4]).split()
    for i in cursor.execute("SELECT * FROM employees WHERE id_vk = ?",(user_id,)):#номер - должность - айди должности  - айди вк - warn
        if int(i[3])==user_id:
            if str(i[2]) in ruk:
                peer_id = 2000000000 +chat_id
                members_var = get_all_chat_members(peer_id)
                for mute_meb in members_var:
                    try:unmute_user_real(vk, mute_meb, 60,chat_id)
                    except:pass
                send_chat(chat_id,'К сожалению всех размутил Босс!')
            else:
                send_chat(chat_id,'Вы не Руководство правительства')
                
Commands_first_world = {'!настройки':com_settings,'!макс_бесед':max_beced_fun,
'!мин_дж':min_dg_fun,"!чат_н":number_bes_fun,'!рук':Rucovodctvo_fun,'!адм':Komandos_fun,
'!беседа':setting_beced_fun,'!назн':Nazn_dg_fun,'!список':spisok_fun,'!пинг':ping_fun,
'!я':ya_fun,'!комы':comands_fun,'!команды':comands_fun, '!роли':spisok_fun}

Commands_full = {'!пуш':push_fun,'!пушь':push_uapb_fun,'!кик':kick_fun,'!бан':kick_fun,'!закреп':pin_mes_fun,
'!дж':dg_fun,'!роль':dg_fun,'!беседа':set_bec_fun, "!заметка":zametka_fun,"!мут":mute_fun,"!размут":unmute_fun,
'!варн':warn_fun,"!варнлист":warnlist_fun,'!тишина':mute_all_fun,'!громко':unmute_all_fun}
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
                try:Commands_first_world[normalized_text[0].lower()](user_id,normalized_text,chat_id)
                except: pass   
                try: Commands_full[normalized_text[0].lower()](user_id,normalized_text,chat_id,message_text_orig,mes_id)
                except: pass
            if not chat_bool and "заявка" in message_text:
                send_forward_message(3,'#Заявка', event.message_id)
                send_user(user_id,"Заявка принята✅\n\nСотрудник правительства напишет вам в личные сообщения одобрена или не одобрена заявка, ожидайте")
            if not chat_bool and "жалоба" in message_text:
                send_forward_message(3,'#Жалоба', event.message_id)
                send_user(user_id,"Жалоба принята✅\n\nСотрудник правительства рассмотрит её и вынесит свой вердикт. Благодарим за отзывчивость.")
                
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
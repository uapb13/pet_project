# import pygame as py
# import random
# py.init()
# screen = py.display.set_mode((0, 0), py.RESIZABLE) #Создаем игру размером с экрана игрока
# bg_img = py.image.load('kosmos-fon-89.jpg')
# bg_img = py.transform.scale(bg_img, (screen.get_size())) #Игра
# bg_menu = py.image.load('bc.jpg')
# bg_menu = py.transform.scale(bg_menu, (screen.get_size())) #Меню
# bg_lose = py.image.load('lose.jpg')                                      #Устанавливаем все нужные фоны 
# bg_lose = py.transform.scale(bg_lose, (screen.get_size())) #Поражение
# bg_win = py.image.load('win.png')
# bg_win = py.transform.scale(bg_win, (screen.get_size())) # Победа
# py.display.set_caption('Space Invaders') #Установка заголовка игры
# clock = py.time.Clock() #Установка частоты кадров
# FPS = 180
# light_img = [py.image.load('Light0.png'),py.image.load('Light1.png'),py.image.load('Light2.png'),py.image.load('Light3.png'),py.image.load('Light4.png'),py.image.load('Light5.png'),py.image.load('Light6.png'),py.image.load('Light7.png'),py.image.load('Light8.png'),py.image.load('Light9.png'),py.image.load('Light10.png'),]

# pos_y = screen.get_size()[1]
# pos_x = screen.get_size()[0] #Сразу считаем скок ху, что бы потом не нагружать игру

# kittenimage = py.image.load('Rocket.png')
# rockimage = py.image.load('Meteorit.png') # Открываем все нужные нам спрайты
# poderok = py.image.load('podarok.png')

# schet = 0 #Счёт игрока
# podik = 0 #Шанс удачи получить подарок
# podrik = 1 #Поймал ли игрок подарок или нет
# mouse_counter = 0
# need_draw = False

# class Podarok(py.sprite.Sprite):
#     def __init__(self):
#         super(Podarok, self).__init__()
#         self.image = py.transform.scale(poderok, (100, 100)) #Все тоже самое для Подарка
#         self.rect = self.image.get_rect()
#         self.speed = round(random.uniform(2.8, 4.8),1)
#         self.rect.x = random.randint(0, pos_x)
#         self.rect.y = -150
            
#     def update(self):
#         global podik
#         if podik >=95: #Проверка получился ли шанс
#             self.rect.y +=self.speed
#             if self.rect.y>pos_y:
#                 self.rect.x = random.randint(0, pos_x-100)
#                 self.rect.y = -150
#                 self.speed = random.uniform(2.8, 4.8) #Создание и отправление подарка
#                 podik = 0 #Сброс шанса

#     hits_p = 1#py.sprite.spritecollide(cat, podarki, False)
#     #if py.sprite.spritecollideany(cat, podarki): #Проверка столкновения игрока с подарком
#     if hits_p:
#         for i in hits_p:
#             i.kill() #Удалить српайт, что бы метеорит не стал слишком мелким
#         podrik += 1 
#         podik = 0 


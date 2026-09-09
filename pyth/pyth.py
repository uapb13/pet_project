import pygame as py
import random
import time
import webbrowser
import datetime
import sqlite3
import traceback
py.init()
#image_path = '/data/data/uapb13.test.uapb13/files/app'
con = sqlite3.connect('baze.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS score_surv(id INTEGER PRIMARY KEY, data TEXT, score TEXT, time TEXT)')


screen = py.display.set_mode((0, 0), py.RESIZABLE) #Создаем игру размером с экрана игрока (py.FULLSCREEN)(py.RESIZABLE)
bg_img = py.image.load('pyth/kosmos-fon-89.jpg')
bg_img = py.transform.scale(bg_img, (screen.get_size())) #Игра
bg_menu = py.image.load('pyth/bc.jpg')
bg_menu = py.transform.scale(bg_menu, (screen.get_size())) #Меню
bg_lose = py.image.load('pyth/lose.jpg')                                      #Устанавливаем все нужные фоны 
bg_lose = py.transform.scale(bg_lose, (screen.get_size())) #Поражение
bg_win = py.image.load('pyth/win.png')
bg_win = py.transform.scale(bg_win, (screen.get_size())) # Победа
py.display.set_caption('pyth/Rocket Wars') #Установка заголовка игры
clock = py.time.Clock() #Установка частоты кадров
FPS = 150
light_img = [py.image.load('pyth/Light0.png'),py.image.load('pyth/Light1.png'),py.image.load('pyth/Light2.png'),
             py.image.load('pyth/Light3.png'),py.image.load('pyth/Light4.png'),py.image.load('pyth/Light5.png'),
             py.image.load('pyth/Light6.png'),py.image.load('pyth/Light7.png'),py.image.load('pyth/Light8.png'),
             py.image.load('pyth/Light9.png'),py.image.load('pyth/Light10.png'),]

pos_y = screen.get_size()[1]
pos_x = screen.get_size()[0]    #Сразу считаем скок ху, что бы потом не нагружать игру
print(pos_x,pos_y)

kittenimage = py.image.load('pyth/Rocket.png')
rockimage = [py.image.load('pyth/metior_1.png'),py.image.load('pyth/metior_1.png'),py.image.load('pyth/metior_2.png'),py.image.load('pyth/metior_3.png')] # Открываем все нужные нам спрайты
NLO_image = [py.image.load('pyth/NLO.png'),py.image.load('pyth/NLO.png'),py.image.load('pyth/NLO.png'),py.image.load('pyth/NLO.png')]

schet = 0 #Счёт игрока
mouse_counter = 0
need_draw = False
speed_rocks = 1.0 # коэф скорости метиоров

licenzia_1  ='Играя в эту игру, вы подверждаете, что'
licenzia_2 = 'если ваш корабль сломается, вы не будете переживать'
licenzia_3 = 'за его жизнь'

try:
    class Cat(py.sprite.Sprite):
        def __init__(self,w,h):
            super(Cat, self).__init__()
            self.image = py.transform.scale(kittenimage, (w,h)) #Ставим картинку и размеры персонажу
            self.rect = self.image.get_rect() #Получаем эти самые размеры для столкновений 
            self.rect.x = procent(pos_x,50)
            self.rect.y = procent(pos_y,80)  #Место расположение спрайта

        def update(self):
            self.speedx = 0
            keystate = py.key.get_pressed()   #Движение спрайта
            if keystate[py.K_a] and self.rect[0]-1>-1:
                self.speedx -= 5
            if keystate[py.K_d] and self.rect[0]+1<pos_x-100:
                self.speedx += 5
            self.rect.right+= self.speedx

    class Rock(py.sprite.Sprite):
        def __init__(self,speed_st,speed_end,w,h,cartinka):
            super(Rock, self).__init__()
            self.cartinka = cartinka
            self.number_img = random.randint(1,3)
            self.w = w
            self.h = h
            self.metior_timer = datetime.datetime.now()
            self.image = py.transform.scale(cartinka[self.number_img], (w, h))  #Все тоже самое, что с игроком
            self.rect = self.image.get_rect()
            self.speed_st = speed_st
            self.speed_end = speed_end
            self.speed = round(random.uniform(speed_st, speed_end),1)
            self.rect.x = random.randint(0, pos_x)
            self.rect.y = -150
            
        def update(self):  # Движение метеоритов 
            global schet,speed_rocks
            self.rect.y +=self.speed
            #print_text(f'{float(str(datetime.datetime.now()-self.metior_timer)[5:10])}',procent(pos_x,90),procent(pos_y,5),font_color=(0,255,0))
            if float(str(datetime.datetime.now()-self.metior_timer)[5:10])>=0.3:
                self.image = py.transform.scale(self.cartinka[self.number_img], (self.w, self.h))
                self.metior_timer = datetime.datetime.now()
                if self.number_img == 3:
                    self.number_img = 0
                self.number_img +=1
            if self.rect.y>pos_y:
                self.rect.x = random.randint(0, pos_x-100)
                self.rect.y = -150
                self.speed = round(random.uniform(self.speed_st, self.speed_end),1)*speed_rocks
                schet+=1 #Счетчик
      
    class Button_rect():
        def __init__(self, width, height):
            self.width = width
            self.height = height
            #self.inactive_color = (13,162,50)
            self.active_color = (23,204,50)
            self.draw_effects = False
            self.clr_effects = False
            self.rect_h = 10
            self.rect_w = width
        
        def draw(self,x,y,mes,action=None):
            mouse = py.mouse.get_pos() #(100,123)
            click = py.mouse.get_pressed()
            if x<mouse[0]<x+self.width and y<mouse[1]<y+self.height:
                if click[0]==1:
                    pass  #Потом можно звук добавить
                    if action is not None:
                        action()
                        end_lvl()

            self.draw_beat_rect(mouse[0],mouse[1],x,y)
            print_text(mes=mes,x=x+10,y=y+10,font_size=int((self.width+self.height)//6))

        def draw_beat_rect(self,ms_x,ms_y,x,y):
            if x <= ms_x <= x+self.width and y <= ms_y <= y+self.height:
                self.draw_effects = True

            if self.draw_effects:
                if ms_x < x or ms_x > x + self.width or ms_y < y or ms_y > y + self.height:
                    self.draw_effects = False
                    self.clr_effects = True

                if self.rect_h < self.height:
                    self.rect_h += (self.height-10)/40

            if self.clr_effects and not self.draw_effects:
                if self.rect_h >10:
                    self.rect_h -= (self.height-10)/40
                else:
                    self.clr_effects = False
            draw_y = y + self.height-self.rect_h
            py.draw.rect(screen,self.active_color, (x, draw_y,self.rect_w,self.rect_h))

    def procent(num,proc):#procent(100,30)
        get = (num/100)*proc
        return get
    
    def tip_quit():
        con.commit()
        con.close()
        py.quit()
        quit()

    def anti_show():
        show = False
        return show
    
    def utube():
        webbrowser.open('https://www.youtube.com/channel/UCaIm7MkIwg2vZmbesuX1ZXA', new=0)

    def score_table():
        number = 1
        number_score = 15
        len_text_table = 36
        print_text('Дата        Счёт    Время раунда',procent(pos_x,35),procent(pos_y,10),font_color=(0,255,0))
        for i in cur.execute(f'SELECT data,score,time FROM score_surv ORDER BY score DESC'):
            print_text(f'{number}   {i[0]}',procent(pos_x,30),procent(pos_y,number_score),font_color=(0,255,0))
            number+=1
            number_score +=5
            if number == 10:
                break
        number = 1
        number_score = 15
        for i in cur.execute(f'SELECT data,score,time FROM score_surv ORDER BY score DESC'):
            print_text(f'{i[1]}',procent(pos_x,45),procent(pos_y,number_score),font_color=(0,255,0))
            number+=1
            number_score +=5
            if number == 10:
                break
        number = 1
        number_score = 15
        for i in cur.execute(f'SELECT data,score,time FROM score_surv ORDER BY score DESC'):
            print_text(f'{i[2]}',procent(pos_x,53),procent(pos_y,number_score),font_color=(0,255,0))
            number+=1
            number_score +=5
            if number == 10:
                break

    def show_menu(): #Меню для игрока
        show = True             #ширина кнопки    #Высота кнопки
        start_btn = Button_rect(procent(pos_x,13),procent(pos_y,6)) #Кнопки старта и выхода из игры
        quit_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        utube_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lucuha_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        record_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        while show:
            for e in py.event.get():
                if e.type == py.QUIT:
                    tip_quit()
            screen.blit(bg_menu,(0,0))
            start_btn.draw(procent(pos_x,42),procent(pos_y,31),'Старт',vubor_lvl)
            utube_btn.draw(procent(pos_x,42),procent(pos_y,41),'Ютуб',utube)   #Обычное меню для игрока
            lucuha_btn.draw(procent(pos_x,42),procent(pos_y,51),'Лицензия',licuha)
            record_btn.draw(procent(pos_x,42),procent(pos_y,61),'Рекорды',record_surv)
            quit_btn.draw(procent(pos_x,42),procent(pos_y,71),'Выход',tip_quit)
            print_text('@uapb13',procent(pos_x,2),procent(pos_y,5),font_color=(0,255,0))
            draw_ms()
            py.display.update()
            clock.tick(FPS)

    def record_surv():
        #global licenzia_1,licenzia_2,licenzia_3
        show = True
        back_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        while show:
            screen.blit(bg_menu,(0,0))
            score_table()
            print_text('@uapb13',procent(pos_x,2),procent(pos_y,5),font_color=(0,255,0))
            back_btn.draw(procent(pos_x,42),procent(pos_y,90),'Назад',show_menu)
            py.display.update()
            draw_ms()
            clock.tick(FPS)
            for e in py.event.get():
                if e.type == py.QUIT:
                    tip_quit()

    def licuha():
        global licenzia_1,licenzia_2,licenzia_3
        show = True
        back_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        while show:
            screen.blit(bg_menu,(0,0))
            print_text(licenzia_1,procent(pos_x,35),procent(pos_y,31),font_color=(0,255,0))
            print_text(licenzia_2,procent(pos_x,35),procent(pos_y,35),font_color=(0,255,0))
            print_text(licenzia_3,procent(pos_x,35),procent(pos_y,39),font_color=(0,255,0))
            print_text('@uapb13',procent(pos_x,2),procent(pos_y,5),font_color=(0,255,0))
            back_btn.draw(procent(pos_x,42),procent(pos_y,90),'Назад',show_menu)
            py.display.update()
            draw_ms()
            clock.tick(FPS)
            for e in py.event.get():
                if e.type == py.QUIT:
                    tip_quit()

    def vubor_lvl():
        time.sleep(0.1)
        show = True
        lvl1_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lvl2_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lvl3_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lvl4_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lvl5_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lvl6_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lvl7_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        lvl8_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        beck_lvl_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        back_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        while show:
            for e in py.event.get():               #Меню выбора уровня
                if e.type == py.QUIT:
                    tip_quit()
            screen.blit(bg_menu,(0,0))
            lvl1_btn.draw(procent(pos_x,20),procent(pos_y,20),'1 Уровень',lvl_1)
            lvl2_btn.draw(procent(pos_x,35),procent(pos_y,20),'2 Уровень',lvl_2)
            lvl3_btn.draw(procent(pos_x,50),procent(pos_y,20),'3 Уровень',lvl_3)
            lvl4_btn.draw(procent(pos_x,65),procent(pos_y,20),'4 Уровень',lvl_4)
            lvl5_btn.draw(procent(pos_x,20),procent(pos_y,35),'5 Уровень',lvl_5)
            lvl6_btn.draw(procent(pos_x,35),procent(pos_y,35),'6 Уровень',lvl_6)
            lvl7_btn.draw(procent(pos_x,50),procent(pos_y,35),'7 Уровень',lvl_7)
            lvl8_btn.draw(procent(pos_x,65),procent(pos_y,35),'8 Уровень',lvl_8)
            beck_lvl_btn.draw(procent(pos_x,80),procent(pos_y,80),'Выживание',besk_lvl)
            back_btn.draw(procent(pos_x,42),procent(pos_y,90),'Назад',show_menu)
            print_text('@uapb13',procent(pos_x,2),procent(pos_y,5),font_color=(0,255,0))
            draw_ms()
            py.display.update()
            clock.tick(FPS)
                    
    def print_text(mes,x,y,font_color=(0,0,0),font_type=None,font_size=int(procent((pos_x+pos_y)//3,5))): #Создание текста
        font_type = py.font.Font(font_type,font_size)
        text = font_type.render(mes,True,font_color)
        screen.blit(text,(x,y))
        
    cat_size = (int((pos_x+pos_y)//35))
    cat = Cat(cat_size,cat_size*1.5)
    rocks = py.sprite.Group()
    all_sprites = py.sprite.Group()
    player = py.sprite.Group()
    NLOs = py.sprite.Group()
    player.add(cat)
    all_sprites.add(cat)

    def NLO_sprite(num,size):
        for i in range(num):
            r = Rock(1.0, 3.0,size,size,NLO_image) #Минимальная,Максимальная скорость. Размеры, картинка
            NLOs.add(r)
            all_sprites.add(r)

    def sprite_lvl(num,size,difictal):
        for i in range(num):
            r = Rock(2.0, 7.0,int(size//2),size,rockimage) #Минимальная,Максимальная скорость. Размеры, картинка
            rocks.add(r)
            all_sprites.add(r)
        if difictal > 0:
            NLO_sprite(num//10,size*2)
        

    def end_lvl():
        global schet
        for helof in rocks:
            helof.kill()
        for helof in NLOs:
            helof.kill()
        cat.rect.x = pos_x / 2

    def nastroiki_lvl(nachalo=(int((pos_x+pos_y)//25)),num_sprite=5,pobeda=25,play_w=1,besk=False,difictal = 0):
        global schet,speed_rocks
        timer = datetime.datetime.now() #начало уровня
        timer_speed = datetime.datetime.now() #Ускорение метеоров
        timer_acceleration = 10 # Через сколько секунд, будет ускорение
        back_btn = Button_rect(procent(pos_x,13),procent(pos_y,6))
        bg_y = 0 #С помощью него будет двигаться фон
        score_num = 1 #Нужно записать рекорд или нет
        r = True #Услвия игры
        schet = 0 #Счет очков
        play = play_w #Усливие проиграл, выйграл или играет ещё игрок
        nachalo = nachalo #Размер метиорита 
        proverka = 0 #Что бы остановилось время выйгрыша
        speed_rocks = 1.0

        end_lvl()
        rocks.remove()
        all_sprites.remove() #Очистить все старые спрайты
        sprite_lvl(num_sprite,nachalo,difictal) #Создаем новые спрайты для каждого уровня по разному

        while r:#                            Группа спрайтов   
            #                           спрайт    |    Что делать
            hits = py.sprite.spritecollide(cat, rocks, False) #Проверка столкновения игрока с метиоритом
            hits_NLO = py.sprite.spritecollide(cat, NLOs, False) #Проверка столкновения игрока с НЛО
            if hits or hits_NLO:
                play = 2
                timer_end = datetime.datetime.now()
                end_lvl()

            if schet >= pobeda: #Счет очков игрока
                play = 3
                if proverka == 0:
                    timer_win = datetime.datetime.now()
                proverka+=1
                
            if play == 1 and besk == False:
                screen.blit(bg_img, (0, bg_y))
                screen.blit(bg_img, (0, bg_y-pos_y))

                bg_y+=1
                if bg_y >= pos_y: #Движение фона
                    bg_y=0

                back_btn.draw(procent(pos_x,5),procent(pos_y,90),'Назад',show_menu)
                all_sprites.update() #Всё отрисовываем
                all_sprites.draw(screen)
                print_text(f'Ваш счет: {schet}',procent(pos_x,5),procent(pos_y,6),font_color=(255,0,0))
                print_text(f'Для победы: {pobeda}',procent(pos_x,5),procent(pos_y,10),font_color=(255,0,0)) #Двигаем фон и отписываем счетчик очков игрока 
                print_text(f'Время: {str(datetime.datetime.now()-timer)[:7]}',procent(pos_x,5),procent(pos_y,14),font_color=(255,0,0))
            if play == 1 and besk == True:
                screen.blit(bg_img, (0, bg_y))
                screen.blit(bg_img, (0, bg_y-pos_y))

                if int(str(datetime.datetime.now()-timer_speed)[5:7])>=timer_acceleration:
                    speed_rocks += 0.1
                    timer_speed = datetime.datetime.now()
                bg_y+=1
                if bg_y >= pos_y: #Движение фона
                    bg_y=0

                back_btn.draw(procent(pos_x,5),procent(pos_y,90),'Назад',show_menu)
                all_sprites.update() #Всё отрисовываем
                all_sprites.draw(screen)
                print_text(f'Ваш счет: {schet}',procent(pos_x,5),procent(pos_y,6),font_color=(255,0,0)) 
                print_text(f'Время: {str(datetime.datetime.now()-timer)[:7]}',procent(pos_x,5),procent(pos_y,10),font_color=(255,0,0))
                print_text(f'Скорость метеоров: {round(speed_rocks,1)}',procent(pos_x,5),procent(pos_y,14),font_color=(255,0,0))
                print_text(f'Ускорение через: {timer_acceleration-int(str(datetime.datetime.now()-timer_speed)[5:7])} секунд',procent(pos_x,5),procent(pos_y,18),font_color=(255,0,0))

            elif play == 2 and besk == True: #Поражение
                score = schet
                if score_num == 1:
                    print(str(timer_end-timer)[:7])
                    cur.execute(f'INSERT INTO score_surv (data,score,time) VALUES (?,?,?)',(str(datetime.datetime.now())[0:11], score, str(timer_end-timer)[:7]))
                    con.commit()
                    score_num+=1
                screen.blit(bg_lose,(0,0))
                if str(timer_end-timer)[:5]=="0:00:":
                    print_text(f'Вы продержались: {str(timer_end-timer)[5:7]} Секунд',procent(pos_x,38),procent(pos_y,6),font_color=(255,0,0))
                else:
                    print_text(f'Вы продержались: {str(timer_end-timer)[2:7]} Минут',procent(pos_x,38),procent(pos_y,6),font_color=(255,0,0))
                print_text(f'Ваш счёт: {score} очков',procent(pos_x,38),procent(pos_y,10),font_color=(255,0,0))
                back_btn.draw(procent(pos_x,42),procent(pos_y,90),'Назад',show_menu)

            elif play == 2 and besk == False: #Поражение
                score = schet
                screen.blit(bg_lose,(0,0))
                if str(timer_end-timer)[:5]=="0:00:":
                    print_text(f'Вы продержались: {str(timer_end-timer)[5:7]} Секунд',procent(pos_x,38),procent(pos_y,6),font_color=(255,0,0))
                else:
                    print_text(f'Вы продержались: {str(timer_end-timer)[2:7]} Минут',procent(pos_x,38),procent(pos_y,6),font_color=(255,0,0))
                print_text(f'Ваш счёт: {score} очков',procent(pos_x,38),procent(pos_y,10),font_color=(255,0,0))
                back_btn.draw(procent(pos_x,42),procent(pos_y,90),'Назад',show_menu)

            elif play == 3: #Победа
                score = schet
                screen.fill((255,255,255))
                screen.blit(bg_win,(0,0))
                if str(timer_win-timer)[:5]=="0:00:":
                    print_text(f'Вы выйграли за: {str(timer_win-timer)[5:7]} Секунд',procent(pos_x,38),procent(pos_y,6),font_color=(255,0,0))
                else:
                    print_text(f'Вы выйграли за: {str(timer_win-timer)[2:7]} Минут',procent(pos_x,38),procent(pos_y,6),font_color=(255,0,0))
                print_text(f'Ваш счёт: {score} очков',procent(pos_x,38),procent(pos_y,10),font_color=(255,0,0))
                back_btn.draw(procent(pos_x,42),procent(pos_y,90),'Назад',show_menu)
        
            draw_ms()
            py.display.update()
            clock.tick(FPS)

            for e in py.event.get(): #Ещё одна кнопка
                if e.type == py.QUIT:
                    r = False
                    tip_quit()
    def draw_ms():
        global mouse_counter,need_draw
        mouse = py.mouse.get_pos()
        click = py.mouse.get_pressed()
        mouse_size = [10,12,16,20,28,34,40,48,54,58]

        if click[0] or click[1]:
            need_draw = True
        if need_draw:
            draw_x = mouse[0]-mouse_size[mouse_counter]//2
            draw_y = mouse[1]-mouse_size[mouse_counter]//2
            screen.blit(light_img[mouse_counter],(draw_x,draw_y))
            mouse_counter+=1
            if mouse_counter == 10:
                mouse_counter = 0
                need_draw = False

    def lvl_1():
        nastroiki_lvl() #Создание 1 уровня

    def lvl_2():
        nastroiki_lvl(num_sprite=10,pobeda=50,play_w=1) #Создание 2 уровня
    
    def lvl_3():
        nastroiki_lvl(num_sprite=15,pobeda=75,play_w=1) #Создание 3 уровня

    def lvl_4():
        nastroiki_lvl(num_sprite=20,pobeda=75,play_w=1) #Создание 3 уровня
    
    def lvl_5():
        nastroiki_lvl(num_sprite=10,pobeda=55,play_w=1,difictal=1) #Создание 1 уровня

    def lvl_6():
        nastroiki_lvl(num_sprite=15,pobeda=70,play_w=1,difictal=1) #Создание 2 уровня
    
    def lvl_7():
        nastroiki_lvl(num_sprite=20,pobeda=95,play_w=1,difictal=1) #Создание 3 уровня
        
    def lvl_8():
        nastroiki_lvl(num_sprite=30,pobeda=100,play_w=1,difictal=1) #Создание 3 уровня

    def besk_lvl():
        nastroiki_lvl(num_sprite=15,pobeda=999999999,play_w=1,besk=True)

    show_menu()
    tip_quit()
    
except Exception:
    #pass
    traceback.print_exc()
    #time.sleep(50)
    input()
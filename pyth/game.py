import pygame as py
import random
py.init()#импортирование файлов


wind=py.display.set_mode((0,0),py.RESIZABLE)
ser=True
backround=py.image.load('pyth/kosmos-fon-89.jpg')
backround=py.transform.scale(backround,wind.get_size())
player1=py.image.load('pyth/Rocket.png')
vrag1=[py.image.load('pyth/metior_1.png'),py.image.load('pyth/metior_1.png'),py.image.load('pyth/metior_1.png')]
vrag2=py.image.load('pyth/metior_1.png')
clock=py.time.Clock()
count=0
FPS=120#НАЧАЛЬНАЯ РАСТАНОВКА
pos_x=wind.get_size()[0]
pos_y=wind.get_size()[1]


class Player(py.sprite.Sprite):
    def __init__(self,x,y,w,z,player1):
        super(Player,self).__init__()
        self.image=py.transform.scale(player1,(w,z))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def update(self):
        speed_roc=15                            
        self.speedx=0
        self.speedy=0
        keystate= py.key.get_pressed()
        if keystate[py.K_w]:
            self.speedy-=speed_roc
        if keystate[py.K_s]:
            self.speedy+=speed_roc
        if keystate[py.K_d]:
            self.speedx+=speed_roc
        if keystate[py.K_a]:
            self.speedx-=speed_roc
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy

class Vrag(py.sprite.Sprite):
    def __init__(self,x,y,w,z,vrag_class,lvl,speed_max_class,speed_mini_class):
        super(Vrag,self).__init__()
        self.carting_vrag_class=vrag_class
        self.number_img=random.randint(1,2)
        self.w=w
        self.z=z
        self.image=py.transform.scale(self.carting_vrag_class[self.number_img],(self.w,self.z))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.start_y=y
        self.speed_vrag=random.randint(speed_max_class,speed_mini_class)
        self.lvl=lvl

    
    def update(self):
        global count
        self.image=py.transform.scale(self.carting_vrag_class[self.number_img],(self.w,self.z))
        self.rect.y+=self.speed_vrag
        if self.number_img==2:
            self.number_img=0
        self.number_img+=1
        if self.rect.y>pos_y:
            self.rect.y=self.start_y
            self.rect.x=random.randint(0,pos_x)
            count+=self.lvl


class button_rect():
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.active_color=(0,250,0)


    def draw(self,x,y,mes,action=None):
        mouse=py.mouse.get_pos()
        click=py.mouse.get_pressed()
        if x<mouse[0]<x+self.width and y<mouse[1]<y+self.height:
            if click[0]==1:
                if action is not None:
                    action()

        py.draw.rect(wind,self.active_color, (x, y,self.width,self.height))
        print_text(mes=mes,x=x+10,y=y+10,font_size=int((self.width+self.height)//6))



player=Player(350,650,150,150,player1)
sprite=py.sprite.Group()
vrag_group=py.sprite.Group()
sprite.add(player)
def ctpoka(count=1,cor_x_1=0,cor_x_2=pos_x,cor_y=0,width=100,heigth=100,cartinka=vrag1,speed_max=10,speed_mini=1,lvl_def=1):
    for i in range(count):
        vrag=Vrag(random.randint(cor_x_1,cor_x_2),cor_y,width,heigth,cartinka,lvl_def,speed_mini,speed_max)
        sprite.add(vrag)
        vrag_group.add(vrag)


ctpoka(count=10,speed_max=5)
#ctpoka(width=500,heigth=500,cartinka=vrag2,lvl_def=5)
ctpoka(count=10,heigth=75,speed_mini=1,lvl_def=2)

def print_text(mes,x,y,font_color=(0,0,0),font_type=None,font_size=100):#создание текста
    font_type = py.font.Font(font_type,font_size)
    text=font_type.render(mes,True,font_color)
    wind.blit(text,(x,y))

def end_game():
    py.quit()

def menu():
    show = True
    quit_btn=button_rect(100,50)
    start = button_rect(100,50)
    while show:
        wind.blit(backround,(0,0))#цыкыл игры
        start.draw(250,700,'старт',play)
        quit_btn.draw(50,700,'выход',end_game)

def play():
    ser = True
    quit_btn=button_rect(100,50)
    while ser:
        wind.blit(backround,(0,0))#цыкыл игры
        sprite.draw(wind)
        sprite.update()
        quit_btn.draw(50,700,'выход',end_game)
        print_text(f'счет {count}',100,100,font_color=(0,255,0))
        py.display.update()
        hit=py.sprite.spritecollide(player,vrag_group,False)
        #if hit:
        #    ser=False
        if count>=10000000000:
            ser=False
        for event in py.event.get():
            if event.type==py.QUIT:
                ser=False#проверка на закрытие
        clock.tick(FPS)
menu()
py.quit()#закрытие


#
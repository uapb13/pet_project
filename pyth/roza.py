import turtle

# Функция для рисования огня
def draw_fire():
    turtle.color("orange")
    turtle.begin_fill()
    turtle.left(90)
    turtle.forward(100)
    turtle.right(90)
    turtle.circle(50, 180)
    turtle.right(90)
    turtle.forward(100)
    turtle.right(90)
    turtle.circle(50, 180)
    turtle.end_fill()

# Функция для рисования лепестка розы
def draw_petal():
    turtle.color("red")
    turtle.begin_fill()
    turtle.circle(100, 60)
    turtle.left(120)
    turtle.circle(100, 60)
    turtle.end_fill()

# Функция для рисования стебля
def draw_stem():
    turtle.color("green")
    turtle.right(90)
    turtle.forward(200)

# Настройка окна
turtle.bgcolor("black")
turtle.speed(10)

# Рисуем огонь
turtle.penup()
turtle.goto(-50, -100)
turtle.pendown()
draw_fire()

# Рисуем розу
turtle.penup()
turtle.goto(0, 0)
turtle.pendown()
for _ in range(6):
    draw_petal()
    turtle.left(60)

# Рисуем стебель
turtle.penup()
turtle.goto(0, 0)
turtle.pendown()
draw_stem()

# Завершение рисования
turtle.hideturtle()
turtle.done()
#Б02-010 Артаева Рожков Садыков
from random import randint
import numpy as np
#Имеется игровое поле 600 на 600
class Platform():
    def __init__(self):
        #Платформа создается снизу в центре экрана в виде маленького черного прямоугольника
        self.x0 = 300
        self.y0 = 550
        self.v = 5
        self.width = 60
        self.height = 15
        
        rect(screen, (0,0,0), (self.x0-self.width/2, self.y0-self.height/2, self.width, self.height)) #рисование картинки платформы
        platform = pygame.Rect(self.x0-self.width/2, self.y0-self.height/2, self.width, self.height) #физичная платформа
        self.lives = 3

    def move(self, dir):
        if dir == "left" and self.x0 >= 30:
            self.x0 -= self.v
        if dir == "right" and self.x0 <= 570:
            self.x0 += self.v

    pass



class Ball():
    def __init__(self):
        # Шары создаются в нижней половине экрана автоматически со временем (повышающаяся сложность)
        # или после смерти старого шара (шар умирает = вылетает снизу экрана (игрок не смог его отбить))
        # Координата появления случайная, скорость направлена вверх,
        # но в самое первое перемещение будет заменена
        self.x = 3 * Platform.x0//4
        self.y = Platform.y0 + Platform.height//2
        self.v = 50
        self.vx = 0
        self.vy = 50
        self.radius = 10 #радиус шарика
        circle(screen, (0,0,0), (self.x, self.y), self.radius) #рисую круг
       
        self.innersquareradius = 7  #Внутри круга сделал квадрат поменьше, innercircleradius это длина половины стороны квадратика
        
        innersquare = pygame.Rect(self.x-self.innersquareradius, self.y-self.innersquareradius, 2*self.innersquareradius, 2*self.innersquareradius)  #Создал физичный квадратик

    def move(self, platform):
        x = platform.x0
        y = platform.y0
        w = platform.width
        h = platform.height
        if self.x <= 0 or self.x >=600:
            self.x = 599
            self.vx = -self.vx
        if innersquare.colliderect(Platform): """ нужныйобьект.colliderect(обьект с которым проверяется столкновение) - проверяет наслоение двух прямоугольников) """
            self.vy *= -1
        #if (x - w/2 <= self.x <= x + w/2
        #        and self.y <= y + h//2):
        #    alpha = int(self.v * np.atan(w/(2 * x) * np.tan(np.pi/9)))
        #   self.vx = self.v * np.cos(alpha)
        #    self.vy = self.v * np.sin(alpha)
        self.x += self.vx
        self.y += self.vy

        pass


class Targets():
    def __init__(self):
        self.height = 15
        self.width = 30
        pass

    def create_bricks(self):
        brick_list = [pygame.Rect(6 + 36 * i, 20 + 20 * j, 30, 15) for i in range(15) for j in range(5)] #создание физичных прямоугольников
        color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(15) for j in range(5)] #случайный цвет
class Bonuses():
    def __init__(self):
        pass


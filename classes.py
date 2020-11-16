#Б02-010 Артаева Рожков Садыков
from random import randint
#Имеется игровое поле 600 на 600
class Platform():
    def __init__(self):
        #Платформа создается снизу в центре экрана в виде маленького черного прямоугольника
        self.x0 = 300
        self.y0 = 550
        self.width = 60
        self.height = 15
        rect(screen, (0,0,0), self.x0-self.width/2, self.y0-self.height/2, self.width, self.height,)
        self.lives = 3

            
class Balls():
    def __init__(self):
        #Шары создаются в нижней половине экарана автоматически со временем (повышающаяся сложность) или после смерти старого шара (шар умирает = вылетает снизу экрана (игрок не смог его отбить))
        #Координата появления случайная, скорость направлена случайно вверх
        self.x0=randint(0, 600)
        self.y0=randint(350, 500)
        self.vx=randint(-5, 5)
        self.vy=randint(1, 5)
        
        pass
        
class Targets():
    def __init__(self):
        self.height = 15
        self.width = 30
        pass
    
    def create_bricks():
        a = [48, 84, 120, 156, 192,	228, 264, 300, 336, 372, 408, 444, 480, 516, 552
             48, 84, 120, 156, 192,	228, 264, 300, 336, 372, 408, 444, 480, 516, 552
             48, 84, 120, 156, 192,	228, 264, 300, 336, 372, 408, 444, 480, 516, 552
             48, 84, 120, 156, 192,	228, 264, 300, 336, 372, 408, 444, 480, 516, 552
             48, 84, 120, 156, 192,	228, 264, 300, 336, 372, 408, 444, 480, 516, 552]
        for i in range(0, 75):
            rect(screen, (0,0,0), a[i]-self.width/2, 20+(i//15)*20-self.height/2, self.width, self.height)
        
class Bonuses():
    def __init__(self):
        pass
            

# Б02-010 Артаева Рожков Садыков
from random import *
import numpy as np
import pygame
from pygame.draw import *
from playsound import *

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
LILAC = (182, 102, 210)
AMBER = (255, 191, 0)
VINOUS = (113, 25, 25)
RED_CORAL = (255, 127, 80)
BLUE_STEEL = (80, 127, 255)
LIME = (204, 255, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (93, 150, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, BLACK, WHITE, MAGENTA, CYAN, LILAC, AMBER, RED_CORAL, DARK_GREEN, BLUE_STEEL, LIME]


class Platform:
    def __init__(self):
        # Платформа создается снизу в центре экрана в виде маленького черного прямоугольника
        self.x = 400
        self.y = 630
        self.v = 10
        self.width = 80
        self.height = 20
        # физичная платформа
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        self.lives = 3

    def move(self, direction: str):
        if direction == "left" and self.x > self.width / 2:
            self.x -= self.v
        if direction == "right" and self.x < 800 - self.width / 2:
            self.x += self.v
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, screen):
        platformimage = pygame.image.load("./images/platform.png")
        platformimage = pygame.transform.scale(platformimage, [round(self.width), round(self.height)])
        screen.blit(platformimage, (self.x - self.width // 2, self.y - self.height // 2))


class Ball:
    def __init__(self):
        # Шары создаются в нижней половине экрана автоматически со временем (повышающаяся сложность)
        # или после смерти старого шара (шар умирает = вылетает снизу экрана (игрок не смог его отбить))
        # Координата появления случайная, скорость направлена вверх,
        # но в самое первое перемещение будет заменена
        self.x = 530
        self.y = 666
        self.vx = 0
        self.vy = -10
        self.v = (self.vx ** 2 + self.vy ** 2) ** 0.5
        self.radius = 9  # радиус шарика

        self.position_on_platform = random() - 0.5
        self.on_platform = True
        # Внутри круга сделал квадрат поменьше, inner_square_radius - это длина половины стороны квадратика
        self.inner_square_radius = self.radius / 2 ** 0.5
        # Создал физичный квадратик
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def move_freely(self, platform):
        x = platform.x
        w = platform.width
        if self.x + self.vx < self.radius or self.x + self.vx > 800 - self.radius:
            self.vx = -self.vx
            playsound("./sounds/sfx_wall_hitted.wav", False)
        if self.y + self.vy < 70 + self.radius:
            playsound("./sounds/sfx_wall_hitted.wav", False)
            self.vy = -self.vy
        if self.inner_square.colliderect(platform.physical_obj):
            # нужныйобъект.colliderect(обьект с которым проверяется столкновение)
            # проверяет наслоение двух прямоугольников
            alpha = np.arctan(2 * (self.x - x) / w * np.tan(7 * np.pi / 18))
            self.vx = round(self.v * np.sin(alpha))
            self.vy = - round(self.v * np.cos(alpha))
        self.x += self.vx
        self.y += self.vy
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def move_on_platform(self, platform):
        self.x = platform.x + self.position_on_platform * (platform.width - self.radius)
        self.y = platform.y - platform.height / 2 - self.radius
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def draw(self, screen):
        ballimage = pygame.image.load("./images/Ball.png")
        ballimage = pygame.transform.scale(ballimage, [18, 18])
        screen.blit(ballimage, (self.x - self.inner_square_radius, self.y - self.inner_square_radius))


# Функция детальной проверки коллизии и отражения мяча
def detect_collision(obj1, obj2):
    dx, dy = obj1.vx / obj1.v, obj1.vy / obj1.v  # функция находит единичный вектор скорости мяча
    # Проверка перекрытия прямоугольников мяча и кирпича слева, справа, сверху и снизу кирпича соответственно
    # в зависимости от направления скорости
    if dx > 0:
        delta_x = obj1.inner_square.right - obj2.left
    else:
        delta_x = obj2.right - obj1.inner_square.left
    if dy > 0:
        delta_y = obj1.inner_square.bottom - obj2.top
    else:
        delta_y = obj2.bottom - obj1.inner_square.top
    # Отражение скоростей
    if abs(delta_x - delta_y) < 3:
        obj1.vx *= -1
        obj1.vy *= -1

    elif delta_x > delta_y:
        obj1.vy *= -1
    elif delta_y > delta_x:
        obj1.vx *= -1


class Targets:
    def __init__(self, level_map: str):
        self.gifted_bricks_list = []
        self.height = 33
        self.width = 72
        self.horizontal_number = 11
        self.vertical_number = 4
        self.brick_list = []
        self.color_list = []
        with open(level_map, 'r') as file:
            level_map = file.read().split('\n')
            level_map = level_map[:len(level_map) - 1]
            for i in range(len(level_map)):
                level_map[i] = level_map[i][1:len(level_map[i]) - 2]
                level_map[i] = level_map[i].split(') (')
                for j in range(len(level_map[i])):
                    level_map[i][j] = level_map[i][j].split()
                    for h in range(len(level_map[i][j])):
                        level_map[i][j][h] = int(level_map[i][j][h])
                    if level_map[i][j][0] != 0:
                        self.brick_list.append(pygame.Rect(7 + 72 * j, 87 + 33 * i, self.width, self.height))
                        self.color_list.append(COLORS[level_map[i][j][1]])
        """self.color_list = [choice(COLORS) for i in
                           range(len(self.brick_list))]  # случайный цвет"""

    def draw_bricks(self, screen):
        surf1 = pygame.image.load("./images/frame.png")
        surf1 = pygame.transform.scale(surf1, (self.width, self.height))
        for i in range(len(self.brick_list)):
            rect(screen, self.color_list[i], self.brick_list[i])
            screen.blit(surf1, self.brick_list[i])
        #FIXME     
        surf2 = pygame.image.load("./images/explosivebricks.png")
        surf2 = pygame.transform.scale(surf2, (self.width, self.height))
        for k in range(len(self.gifted_explosive_bricks_list)):
            screen.blit(surf2, self.brick_list[i])
        
        

    def move(self):
        self.vertical_number += 1
        for j in range(len(self.brick_list)):
            self.brick_list[j].move_ip(0, 33)
        for i in range(self.horizontal_number):
            self.brick_list.insert(0, pygame.Rect(7 + 72 * i, 87,
                                                  self.width, self.height))
            self.color_list.insert(0, choice(COLORS))

    def gift_bricks(self):
        for i in range(len(self.brick_list)):
            a = randint(1, 7)
            if a == 1:
                self.gifted_bricks_list.append(i)
                
    #дает некоторым кирпичам возможность взорваться            
    def gift_explosive_bricks(self):
        self.gifted_explosive_bricks_list = []
        for i in range(len(self.brick_list)):
            a = randint(1, 7)
            if a == 1:
                self.gifted_explosive_bricks_list.append(i)


class Menu:
    def __init__(self):
        self.button = [pygame.Rect(250, 100 + 100 * i, 300, 70) for i in range(3)]
        self.click = [False, False, False]

    def action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(3):
                if self.button[i].collidepoint(pygame.mouse.get_pos()):
                    playsound("./sounds/sfx_button_clicked.wav", False)
                    self.click[i] = True

    def draw(self, screen, type: str):
        frame = pygame.image.load("./images/frame.png")
        frame = pygame.transform.scale(frame, (300, 70))
        button_1 = pygame.Surface((300, 70))
        button_2 = pygame.Surface((300, 70))
        button_3 = pygame.Surface((300, 70))
        if type == "start":
            button_1 = pygame.image.load("images/button_arcade.png")
            button_2 = pygame.image.load("images/button_endless.png")
            button_3 = pygame.image.load("images/button_exit.png")
        elif type == "level":
            button_1 = pygame.image.load("images/button_level1.png")
            button_2 = pygame.image.load("images/button_level2.png")
            button_3 = pygame.image.load("images/button_level3.png")
        elif type == "pause":
            button_1 = pygame.image.load("images/button_continue.png")
            button_2 = pygame.image.load("images/button_restart.png")
            button_3 = pygame.image.load("images/button_exit.png")
        elif type == "end":
            button_1 = pygame.image.load("images/button_yetuseless.png")
            button_2 = pygame.image.load("images/button_restart.png")
            button_3 = pygame.image.load("images/button_exit.png")
        button_1 = pygame.transform.scale(button_1, (300, 70))
        button_2 = pygame.transform.scale(button_2, (300, 70))
        button_3 = pygame.transform.scale(button_3, (300, 70))
        if not type == "end":
            button_1.blit(frame, (0, 0))
        button_2.blit(frame, (0, 0))
        button_3.blit(frame, (0, 0))
        screen.blit(button_1, (250, 100))
        screen.blit(button_2, (250, 200))
        screen.blit(button_3, (250, 300))


if __name__ == "__main__":
    print("This module is not for direct call!")

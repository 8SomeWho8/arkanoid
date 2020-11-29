# Б02-010 Артаева Рожков Садыков
from random import *
import numpy as np
import pygame
from pygame.draw import *

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
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, LILAC, AMBER, VINOUS, RED_CORAL, BLUE_STEEL, LIME]


class Platform:
    def __init__(self):
        # Платформа создается снизу в центре экрана в виде маленького черного прямоугольника
        self.x = 300
        self.y = 550
        self.v = 5
        self.width = 60
        self.height = 15
        # физичная платформа
        self.physical_obj = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.lives = 3

    def move(self, direction: str, screen):
        if direction == "left" and self.x >= 30:
            self.x -= self.v
        if direction == "right" and self.x <= 570:
            self.x += self.v
        # отрисовка картинки платформы
        self.physical_obj = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        rect(screen, BLACK, self.physical_obj)


class Ball:
    def __init__(self):
        # Шары создаются в нижней половине экрана автоматически со временем (повышающаяся сложность)
        # или после смерти старого шара (шар умирает = вылетает снизу экрана (игрок не смог его отбить))
        # Координата появления случайная, скорость направлена вверх,
        # но в самое первое перемещение будет заменена
        self.x = -10
        self.y = -10
        self.v = 50
        self.vx = 0
        self.vy = 50
        self.radius = 10  # радиус шарика

        self.inner_square_radius = 7  # Внутри круга сделал квадрат поменьше, innersquareradius это длина половины стороны квадратика

        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)  # Создал физичный квадратик

    def move(self, platform, screen):
        x = platform.x
        y = platform.y
        w = platform.width
        h = platform.height
        if self.x <= 0 or self.x >= 600:
            self.x = 599  # ???
            self.vx = -self.vx
        if self.inner_square.colliderect(platform.physical_obj):
            # нужныйобъект.colliderect(обьект с которым проверяется столкновение)
            # проверяет наслоение двух прямоугольников
            alpha = int(self.v * np.atan(w/(2 * x) * np.tan(np.pi/9)))
            self.vx = self.v * np.cos(alpha)
            self.vy = - self.v * np.sin(alpha)
        self.x += self.vx
        self.y += self.vy
        circle(screen, BLACK, (self.x, self.y), self.radius)  # рисую круг


class Targets:
    def __init__(self):
        self.height = 15
        self.width = 30
        self.horizontal_number = 15
        self.vertical_number = 5

    def create_bricks(self, screen):
        brick_list = [pygame.Rect(6 + 36 * i, 20 + 20 * j, 30, 15) for i in range(self.horizontal_number)
                      for j in range(self.vertical_number)]  # создание физичных прямоугольников
        color_list = [choice(COLORS) for i in range(self.horizontal_number * self.vertical_number)]  # случайный цвет
        for i in range(self.horizontal_number * self.vertical_number):
            rect(screen, color_list[i], brick_list[i])

class Bonuses:
    def __init__(self):
        pass


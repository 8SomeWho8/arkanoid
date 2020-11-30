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
        self.x = 100
        self.y = 550
        self.v = 10
        self.width = 60
        self.height = 15
        # физичная платформа
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        self.lives = 3

    def move(self, direction: str):
        if direction == "left" and self.x >= 30:
            self.x -= self.v
        if direction == "right" and self.x <= 570:
            self.x += self.v
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, screen):
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        rect(screen, BLACK, self.physical_obj)


class Ball:
    def __init__(self):
        # Шары создаются в нижней половине экрана автоматически со временем (повышающаяся сложность)
        # или после смерти старого шара (шар умирает = вылетает снизу экрана (игрок не смог его отбить))
        # Координата появления случайная, скорость направлена вверх,
        # но в самое первое перемещение будет заменена
        self.x = 300
        self.y = 500
        self.v = 10
        self.vx = 6
        self.vy = -8
        self.radius = 7  # радиус шарика

        # Внутри круга сделал квадрат поменьше, inner_square_radius - это длина половины стороны квадратика
        self.inner_square_radius = self.radius / 2**0.5

        # Создал физичный квадратик
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def move(self, platform):
        x = platform.x
        w = platform.width
        if self.x <= 0 or self.x >= 600:
            self.vx = -self.vx
        if self.y <= 0:
            self.vy = -self.vy
        if self.inner_square.colliderect(platform.physical_obj):
            # нужныйобъект.colliderect(обьект с которым проверяется столкновение)
            # проверяет наслоение двух прямоугольников
            alpha = np.arctan(2*(self.x - x) / w * np.tan(7*np.pi/18))
            self.vx = round(self.v * np.sin(alpha))
            self.vy = - round(self.v * np.cos(alpha))
        self.x += self.vx
        self.y += self.vy
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def draw(self, screen):
        circle(screen, BLACK, (round(self.x), round(self.y)), self.radius)


class Targets:
    def __init__(self):
        self.height = 15
        self.width = 30
        self.horizontal_number = 16
        self.vertical_number = 5
        self.brick_list = [pygame.Rect(6 + 36 * i, 20 + 20 * j, self.width, self.height) for i in range(self.horizontal_number)
                           for j in range(self.vertical_number)]  # создание физичных прямоугольников
        self.color_list = [choice(COLORS) for i in range(self.horizontal_number * self.vertical_number)]  # случайный цвет

    def draw_bricks(self, screen):
        for i in range(self.horizontal_number * self.vertical_number):
            rect(screen, self.color_list[i], self.brick_list[i])


class Bonuses:
    def __init__(self):
        pass


if __name__ == "__main__":
    print("This module is not for direct call!")
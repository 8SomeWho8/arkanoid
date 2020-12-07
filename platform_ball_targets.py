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
        self.x = 400
        self.y = 730
        self.v = 10
        self.width = 80
        self.height = 20
        # физичная платформа
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        self.lives = 3

    def move(self, direction: str):
        if direction == "left" and self.x > 40:
            self.x -= self.v
        if direction == "right" and self.x < 760:
            self.x += self.v
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, screen):
        rect(screen, BLACK, self.physical_obj)


class Ball:
    def __init__(self):
        # Шары создаются в нижней половине экрана автоматически со временем (повышающаяся сложность)
        # или после смерти старого шара (шар умирает = вылетает снизу экрана (игрок не смог его отбить))
        # Координата появления случайная, скорость направлена вверх,
        # но в самое первое перемещение будет заменена
        self.x = 530
        self.y = 666
        self.v = 10
        self.vx = 0
        self.vy = -10
        self.radius = 9  # радиус шарика

        self.on_platform = True

        # Внутри круга сделал квадрат поменьше, inner_square_radius - это длина половины стороны квадратика
        self.inner_square_radius = self.radius / 2**0.5

        # Создал физичный квадратик
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def move_freely(self, platform):
        x = platform.x
        w = platform.width
        if self.x <= 0 or self.x >= 800:
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

    def move_on_platform(self, platform, position_on_platform: float):
        self.x = platform.x + position_on_platform*platform.width
        self.y = platform.y - platform.height/2 - self.radius
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def draw(self, screen):
        circle(screen, BLACK, (round(self.x), round(self.y)), self.radius)


# Функция детальной проверки коллизии и отражения мяча
def detect_collision(obj1, obj2):
    dx, dy = obj1.vx/obj1.v, obj1.vy/obj1.v  # функция находит единичный вектор скорости мяча
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
    if delta_x > delta_y:
        obj1.vy *= -1
    elif delta_y > delta_x:
        obj1.vx *= -1


class Targets:
    def __init__(self):
        self.height = 20
        self.width = 40
        self.horizontal_number = 16
        self.vertical_number = 5
        self.brick_list = [pygame.Rect(8 + 48 * i, 27 + 27 * j, self.width, self.height) for i in range(self.horizontal_number)
                           for j in range(self.vertical_number)]  # создание физичных прямоугольников
        self.color_list = [choice(COLORS) for i in range(self.horizontal_number * self.vertical_number)]  # случайный цвет

    def draw_bricks(self, screen):
        for i in range(len(self.brick_list)):
            rect(screen, self.color_list[i], self.brick_list[i])

    def move(self):
        self.vertical_number += 1
        for i in range(self.horizontal_number):
            for i in range(len(self.brick_list)):
                self.brick_list[i].move_ip(0, 20)
            self.brick_list.insert(0, pygame.Rect(8 + 48 * i, 27 + 27 * (self.vertical_number - 1),
                                                  self.width, self.height))
            self.color_list.insert(0, choice(COLORS))


if __name__ == "__main__":
    print("This module is not for direct call!")

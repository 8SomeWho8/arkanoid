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
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, LILAC, AMBER, RED_CORAL, BLUE_STEEL, LIME]


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
        platformimage = pygame.image.load("platform.png")
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

        self.on_platform = False
        # Внутри круга сделал квадрат поменьше, inner_square_radius - это длина половины стороны квадратика
        self.inner_square_radius = self.radius / 2 ** 0.5
        # Создал физичный квадратик
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def move_freely(self, platform):
        x = platform.x
        w = platform.width
        if self.x + self.vx < 0 or self.x + self.vx > 800:
            self.vx = -self.vx
        if self.y + self.vy < 50:
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

    def move_on_platform(self, platform, position_on_platform: float):
        self.x = platform.x + position_on_platform * platform.width
        self.y = platform.y - platform.height / 2 - self.radius
        self.inner_square = pygame.Rect(self.x - self.inner_square_radius, self.y - self.inner_square_radius,
                                        2 * self.inner_square_radius, 2 * self.inner_square_radius)

    def draw(self, screen):
        ballimage = pygame.image.load("ball.png")
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
    if delta_x > delta_y:
        obj1.vy *= -1
    elif delta_y > delta_x:
        obj1.vx *= -1


class Targets:
    def __init__(self):
        self.height = 26
        self.width = 66
        self.horizontal_number = 11
        self.vertical_number = 4
        self.brick_list = [pygame.Rect(8 + 72 * i, 87 + 33 * j, self.width, self.height) for i in
                           range(self.horizontal_number)
                           for j in range(self.vertical_number)]  # создание физичных прямоугольников
        self.color_list = [choice(COLORS) for i in
                           range(self.horizontal_number * self.vertical_number)]  # случайный цвет

    def draw_bricks(self, screen):
        surf1 = pygame.image.load("frame.png")
        surf1 = pygame.transform.scale(surf1, (self.width, self.height))
        for i in range(len(self.brick_list)):
            rect(screen, self.color_list[i], self.brick_list[i])
            screen.blit(surf1, self.brick_list[i])

    def move(self):
        self.vertical_number += 1
        for i in range(self.horizontal_number):
            for j in range(len(self.brick_list)):
                self.brick_list[j].move_ip(0, 20)
            self.brick_list.insert(0, pygame.Rect(8 + 48 * i, 27 + 27 * (self.vertical_number - 1),
                                                  self.width, self.height))
            self.color_list.insert(0, choice(COLORS))

    def gift_bricks(self):
        self.gifted_bricks_list = []
        for i in range(len(self.brick_list)):
            a = randint(1, 10)
            if a == 10:
                self.gifted_bricks_list.append(i)




class Menu:
    def __init__(self):
        self.button = [pygame.Rect(250, 100 + 100 * i, 300, 80) for i in range(3)]
        self.click = [False, False, False]

    def action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(3):
                if self.button[i].collidepoint(pygame.mouse.get_pos()):
                    self.click[i] = True

    def draw_start_menu(self, screen):
        frame = pygame.image.load("frame.png")
        frame = pygame.transform.scale(frame, (300, 80))
        arcade_button = pygame.image.load("arcade.png")
        endless_button = pygame.image.load("endless.png")
        exit_button = pygame.image.load("exit.png")
        arcade_button.blit(frame, (0, 0))
        endless_button.blit(frame, (0, 0))
        exit_button.blit(frame, (0, 0))
        screen.blit(arcade_button, (250, 100))
        screen.blit(endless_button, (250, 200))
        screen.blit(exit_button, (250, 300))

    def draw_pause_menu(self, screen):
        frame = pygame.image.load("frame.png")
        frame = pygame.transform.scale(frame, (300, 80))
        continue_button = pygame.image.load("continue.png")
        restart_button = pygame.image.load("restart.png")
        exit_button = pygame.image.load("exit.png")
        continue_button.blit(frame, (0, 0))
        restart_button.blit(frame, (0, 0))
        exit_button.blit(frame, (0, 0))
        screen.blit(continue_button, (250, 100))
        screen.blit(restart_button, (250, 200))
        screen.blit(exit_button, (250, 300))

    def draw_end_menu(self, screen):
        frame = pygame.image.load("frame.png")
        frame = pygame.transform.scale(frame, (300, 80))
        restart_button = pygame.image.load("restart.png")
        exit_button = pygame.image.load("exit.png")
        restart_button.blit(frame, (0, 0))
        exit_button.blit(frame, (0, 0))
        rect(screen, RED_CORAL, (250, 100, 300, 80))
        screen.blit(restart_button, (250, 200))
        screen.blit(exit_button, (250, 300))

if __name__ == "__main__":
    print("This module is not for direct call!")

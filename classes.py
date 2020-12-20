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
    '''
    Платформа, имеет координаты, скорость, ширину и высоту, картинку, и объект класса Rect,
    помогающий в обработке столкновений.
    Может быть подвинута и нарисована.
    '''
    def __init__(self):
        self.x = 400
        self.y = 630
        self.v = 10
        self.width = 80
        self.height = 20
        self.image = pygame.image.load("./images/platform.png")
        # физичная платформа
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        self.lives = 3

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.x > self.width / 2:
            self.x -= self.v
        if key[pygame.K_RIGHT] and self.x < 800 - self.width / 2:
            self.x += self.v
        self.physical_obj = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self, screen):
        self.image = pygame.transform.scale(self.image, [round(self.width), round(self.height)])
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))


class Ball:
    '''
    Шар, имеет координаты, скорости, радиус, картинку, объект класса Rect,
    помогающий в обработке столкновений, случайную позицию появления на платформе.

    Может двигаться с платформой, двигаться самостоятельно и быть нарисованным.
    '''
    def __init__(self):
        self.x = 530
        self.y = 666
        self.vx = 0
        self.vy = -10
        self.v = (self.vx ** 2 + self.vy ** 2) ** 0.5
        self.radius = 9  # радиус шарика
        self.position_on_platform = random() - 0.5
        self.on_platform = True
        self.image = pygame.image.load("./images/Ball.png")
        # внутри круга физичный квадратик
        self.inner_square_radius = self.radius / 2 ** 0.5
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
        self.image = pygame.transform.scale(self.image, [18, 18])
        screen.blit(self.image, (self.x - self.inner_square_radius, self.y - self.inner_square_radius))


# функция детальной проверки коллизии и отражения мяча
def detect_collision(ball, Rect):
    dx, dy = ball.vx / ball.v, ball.vy / ball.v  # функция находит единичный вектор скорости мяча
    # проверка перекрытия прямоугольников мяча и кирпича слева, справа, сверху и снизу кирпича соответственно
    # в зависимости от направления скорости
    if dx > 0:
        delta_x = ball.inner_square.right - Rect.left
    else:
        delta_x = Rect.right - ball.inner_square.left
    if dy > 0:
        delta_y = ball.inner_square.bottom - Rect.top
    else:
        delta_y = Rect.bottom - ball.inner_square.top
    # отражение скоростей
    if abs(delta_x - delta_y) < 5:
        ball.vx *= -1
        ball.vy *= -1
    elif delta_x > delta_y:
        ball.vy *= -1
    elif delta_y > delta_x:
        ball.vx *= -1


class Targets:
    '''
    Цели, имеет количество кирпичей по координатам, размеры одного кирпича,
    массив со всеми существующими в момент игры кирпичами, массив с цветами этих кирпичей,
    массив одаренных бонусами кирпичей, картинку рамки.

    Можно подвинуть(в бесконечном режиме), нарисовать и одарить некоторые из кирпичей бонусами.
    '''
    def __init__(self, level_map: str):
        self.gifted_bricks_list = []
        self.height = 33
        self.width = 72
        self.horizontal_number = 11
        self.vertical_number = 4
        self.brick_list = []
        self.color_list = []
        self.frame = pygame.image.load("./images/frame.png")
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

    def draw_bricks(self, screen):
        self.frame = pygame.transform.scale(self.frame, (self.width, self.height))
        for i in range(len(self.brick_list)):
            rect(screen, self.color_list[i], self.brick_list[i])
            screen.blit(self.frame, self.brick_list[i])

    def move(self):
        self.vertical_number += 1
        for j in range(len(self.brick_list)):
            self.brick_list[j].move_ip(0, 33)
        for i in range(self.horizontal_number):
            self.brick_list.insert(0, pygame.Rect(7 + 72 * i, 87,
                                                  self.width, self.height))
            self.color_list.insert(0, choice(COLORS))
            
    # прячет в некоторых кирпичах бонусы
    def gift_bricks(self):
        for i in range(len(self.brick_list)):
            a = randint(1, 7)
            if a == 1:
                self.gifted_bricks_list.append(i)


class Menu:
    '''
    Меню имеют три кнопки и три переменные, означающие нажатие на соответствующую кнопку,
    картинки всех кнопок.

    Можно нажать на него и нарисовать(в трёх вариантах: старт, аркада, пауза, конец).
    '''
    def __init__(self):
        self.button = [pygame.Rect(250, 100 + 100 * i, 300, 70) for i in range(3)]
        self.click = [False, False, False]
        self.frame = pygame.image.load("./images/frame.png")
        self.button_arcade = pygame.image.load("images/button_arcade.png")
        self.button_endless = pygame.image.load("images/button_endless.png")
        self.button_exit = pygame.image.load("images/button_exit.png")
        self.button_level1 = pygame.image.load("images/button_level1.png")
        self.button_level2 = pygame.image.load("images/button_level2.png")
        self.button_level3 = pygame.image.load("images/button_level3.png")
        self.button_continue = pygame.image.load("images/button_continue.png")
        self.button_restart = pygame.image.load("images/button_restart.png")
        self.button_yetuseless = pygame.image.load("images/button_yetuseless.png")

    def action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(3):
                if self.button[i].collidepoint(pygame.mouse.get_pos()):
                    playsound("./sounds/sfx_button_clicked.wav", False)
                    self.click[i] = True

    def draw(self, screen, type: str):
        self.frame = pygame.transform.scale(self.frame, (300, 70))
        button_1 = pygame.Surface((300, 70))
        button_2 = pygame.Surface((300, 70))
        button_3 = pygame.Surface((300, 70))
        if type == "start":
            button_1 = self.button_arcade
            button_2 = self.button_endless
            button_3 = self.button_exit
        elif type == "level":
            button_1 = self.button_level1
            button_2 = self.button_level2
            button_3 = self.button_level3
        elif type == "pause":
            button_1 = self.button_continue
            button_2 = self.button_restart
            button_3 = self.button_exit
        elif type == "end":
            button_1 = self.button_yetuseless
            button_2 = self.button_restart
            button_3 = self.button_exit
        button_1 = pygame.transform.scale(button_1, (300, 70))
        button_2 = pygame.transform.scale(button_2, (300, 70))
        button_3 = pygame.transform.scale(button_3, (300, 70))
        if not type == "end":
            button_1.blit(self.frame, (0, 0))
        button_2.blit(self.frame, (0, 0))
        button_3.blit(self.frame, (0, 0))
        screen.blit(button_1, (250, 100))
        screen.blit(button_2, (250, 200))
        screen.blit(button_3, (250, 300))


def rating(score, screen):
    # анимированное окно ввода ника
    w = 800
    h = 700
    button_width = 300
    button_height = 95
    font = pygame.font.Font("Thintel.ttf", 50)
    input_box = pygame.Rect(int((w - button_width) /2) + 15, int(h / 2 - 10), int(button_width - 15), 45)
    color_inactive = (100, 100, 100)
    color_active = (0, 0, 0)
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        with open('currentnickname.txt', 'a') as f:
                            print(text, file=f)
                            done = True
                            finished = True
                            break
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        surf192 = pygame.Surface((800, 700))
        surf192.fill(WHITE)
        surf192.set_alpha(3)
        screen.blit(surf192, (0,0))
        rect(screen, BLACK, (int((w - button_width) / 2) - 1, int((h - button_height) / 2) - 1, button_width + 2,
                             button_height + 2))
        rect(screen, (124, 240, 246), (int((w - button_width) / 2), int((h - button_height) / 2), button_width,
                                       button_height))
        name_text = font.render('Enter your name ', True, (20, 20, 20))
        screen.blit(name_text, (int((w - button_width) / 2) + 12, int((h - button_height) / 2) + 3))
        txt_surface = font.render(text, True, color)
        width = button_width - 30
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    # передача ника во вспомогательный файл с рейтингом
    nickbase = open('currentnickname.txt', 'r')
    s = nickbase.readline()
    k = s.rstrip()
    nickbase.close()
    nickname = k

    # затирание вспомогательного файла
    yuio = open('currentnickname.txt', 'w')
    yuio.close()

    # сохранение 5 лучших игроков
    top5_r = open('top5.txt', 'r')
    s = top5_r.readlines() # Saving the state of top5.txt file
    top5_r.close()
    top5_w = open('top5.txt', 'w')
    if len(s) == 0:  # If top5.txt is empty writing a new result
        print('1. ' + nickname + ' ' + str(score), file=top5_w)
    else:
        list_of_scores = []
        for i in range(len(s)):  # Reading scores from the file to create list of scores of all 5 players
            score_r = s[i][len(s[i]) - 2]
            j = len(s[i]) - 3
            while s[i][j] != ' ':
                score_r += s[i][j]
                j -= 1
            list_of_scores.append(int(score_r[::-1]))
        if score >= list_of_scores[0]:  # If player has achieved top 1 result number of a player "above" him is -1
            i_sup = -1
        else:  # Finding the supremum for player's score in list_of_scores
            i_sup = 0
            for i in range(len(list_of_scores)):
                if score < list_of_scores[i]:
                    i_sup = i
        for i in range(len(s)):  # Deleting old positions for every player in top 5, for example "4. "
            s[i] = s[i][3 + i // 5:]
        s.insert(i_sup + 1, nickname + ' ' + str(score) + '\n')  # Adding player's result to top5 massive
        for i in range(len(s)):  # Adding new positions for every player in top5
            s[i] = str(i + 1) + '. ' + s[i]
        # Writing top 5(or less) players in the file
        if len(s) > 5:
            top5_w.writelines(s[:len(s) - 1])
        else:
            top5_w.writelines(s)
    top5_w.close()


if __name__ == "__main__":
    print("This module is not for direct call!")

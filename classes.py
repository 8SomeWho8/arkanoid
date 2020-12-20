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
        self.image = pygame.image.load("./images/Ball.png")
        self.position_on_platform = random() - 0.5
        self.on_platform = True
        # внутри круга сделал квадрат поменьше, inner_square_radius - это длина половины стороны квадратика
        self.inner_square_radius = self.radius / 2 ** 0.5
        # создал физичный квадратик
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
        self.image = pygame.transform.scale(self.image, [2 * self.radius, 2 * self.radius])
        screen.blit(self.image, (self.x - self.inner_square_radius, self.y - self.inner_square_radius))


# функция детальной проверки коллизии и отражения мяча
def detect_collision(obj1, obj2):
    dx, dy = obj1.vx / obj1.v, obj1.v / obj1.v  # функция находит единичный вектор скорости мяча
    # проверка перекрытия прямоугольников мяча и кирпича слева, справа, сверху и снизу кирпича соответственно
    # в зависимости от направления скорости
    if dx > 0:
        delta_x = obj1.inner_square.right - obj2.left
    else:
        delta_x = obj2.right - obj1.inner_square.left
    if dy > 0:
        delta_y = obj1.inner_square.bottom - obj2.top
    else:
        delta_y = obj2.bottom - obj1.inner_square.top
    # отражение скоростей
    if abs(delta_x - delta_y) < 3:
        obj1.vx *= -1
        obj1.v *= -1

    elif delta_x > delta_y:
        obj1.v *= -1
    elif delta_y > delta_x:
        obj1.vx *= -1


class Targets:
    '''
    Цели имеют количество по вертикали, по горизонтали, размеры одного кирпича,
    массив всех кирпичей, массив цветов всех кирпичей, картинку рамки, картинку взрывного кирпича,
    Можно подвинуть (в бесконечном режиме), нарисовать, одарить бонусами и одарить взрывоопасностью.
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
        self.exp_brick = pygame.image.load("./images/explosivebricks.png")
        self.gifted_explosive_bricks_list = []
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
                        self.color_list.append(COLORS[int(level_map[i][j][1])])

    def draw_bricks(self, screen):
        self.frame = pygame.transform.scale(self.frame, (self.width, self.height))
        self.exp_brick = pygame.transform.scale(self.exp_brick, (self.width, self.height))
        for i in range(len(self.brick_list)):
            rect(screen, self.color_list[i], self.brick_list[i])
            screen.blit(self.frame, self.brick_list[i])
        #FIXME
        for k in range(len(self.gifted_explosive_bricks_list)):
            screen.blit(self.exp_brick, self.brick_list[k])
        
    def move(self):
        self.vertical_number += 1
        for j in range(len(self.brick_list)):
            self.brick_list[j].move_ip(0, 33)
        for i in range(self.horizontal_number):
            self.brick_list.insert(0, pygame.Rect(7 + 72 * i, 87,
                                                  self.width, self.height))
            self.color_list.insert(0, choice(COLORS))

    # прячет в некоторыч кирпичах бонусы
    def gift_bricks(self):
        for i in range(len(self.brick_list)):
            a = randint(1, 7)
            if a == 1:
                self.gifted_bricks_list.append(i)
                
    # дает некоторым кирпичам возможность взорваться
    def gift_explosive_bricks(self):
        for i in range(len(self.brick_list)):
            a = randint(1, 7)
            if a == 1:
                self.gifted_explosive_bricks_list.append(i)


class Menu:
    '''
    Меню имеют три кнопки и три переменные, означающие нажатие на соответствующую кнопку.
    Можно нажать на него и нарисовать(в трёх вариантах: старт, аркада, пауза, конец).
    '''
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


class Bonus:
    '''
    родительский класс всех бонусов, созданный для описания общих для всех бонусов
    функций: движения и рисования.
    Каждый бонус имеет кооррдинаты, скорости, ширину и высоту, тип и объект класса Rect, помогающий
    в описании столкновений.
    '''
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.v = 3
        self.width = 32
        self.height = 32
        self.type = "Bonus"
        self.physical_obj = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)

    def move(self):
        self.y += self.v
        self.physical_obj = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)

    def draw(self, screen):
        bonusimage = pygame.image.load("./images/" + self.type + ".png")
        bonusimage = pygame.transform.scale(bonusimage, [32, 32])
        screen.blit(bonusimage, (self.x - self.width / 2, self.y - self.height / 2))


class SpeedBonus(Bonus):
    def __init__(self, x, y):
        self.type = "SpeedBonus"
        Bonus.__init__(self, x, y)
        self.additional_speed = 5

    def boost(self, platform: Platform, balls):
        platform.v += self.additional_speed
        return 0


class WidthBonus(Bonus):
    def __init__(self, x, y):
        self.type = "WidthBonus"
        Bonus.__init__(self, x, y)
        self.width_multiplier = 1.5

    def boost(self, platform: Platform, balls):
        platform.width *= self.width_multiplier
        platform.physical_obj = pygame.Rect(platform.x - platform.width // 2, platform.y - platform.height // 2,
                                            platform.width, platform.height)
        return 1


class SlowDownBonus(Bonus):
    def __init__(self, x, y):
        self.type = "SlowDownBonus"
        Bonus.__init__(self, x, y)
        self.slow_multiplier = 1.5

    def boost(self, platform, balls):
        for ball in balls:
            ball.v /= self.slow_multiplier
            ball.vx /= self.slow_multiplier
            ball.v /= self.slow_multiplier
            return 2


class LifeBonus(Bonus):
    def __init__(self, x, y):
        self.type = "LifeBonus"
        Bonus.__init__(self, x, y)
        self.health_boost = 1

    def boost(self, platform, balls):
        platform.lives += self.health_boost


class AntiBonus:
    # нужны для удобной деактивации эффекта бонусов
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vy = 1
        self.vx = 0
        self.width = 30
        self.height = 30
        self.physical_obj = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2,
                                        self.width, self.height)

        self.timer = 600

    def move(self):
        self.y += self.vy

    def draw(self, screen):
        antibonusimage = pygame.image.load("./images/heart.png")
        antibonusimage = pygame.transform.scale(antibonusimage, [30, 30])
        screen.blit(antibonusimage, (self.x, self.y))


class SpeedAntiBonus(AntiBonus):
    def __init__(self, x, y):
        AntiBonus.__init__(self, x, y)
        self.additional_speed = 5

    def boost(self, platform: Platform, balls):
        platform.v -= self.additional_speed


class WidthAntiBonus(AntiBonus):
    def __init__(self, x, y):
        AntiBonus.__init__(self, x, y)
        self.width_multiplier = 1.5

    def boost(self, platform: Platform, balls):
        platform.width /= self.width_multiplier


class SlowDownAntiBonus(AntiBonus):
    def __init__(self, x, y):
        AntiBonus.__init__(self, x, y)
        self.slow_multiplier = 1.5

    def boost(self, platform, balls):
        for ball in balls:
            ball.v *= self.slow_multiplier
            ball.vx *= self.slow_multiplier
            ball.v *= self.slow_multiplier


def trigger_bonus(x, y, list_of_bonuses, t):
    if t == 1 or t == 2 or t == 3 or t == 4:
        list_of_bonuses.append(SpeedBonus(x, y))
    elif t == 5 or t == 6 or t == 7 or t == 8:
        list_of_bonuses.append(WidthBonus(x, y))
    elif t == 9 or t == 10 or t == 11 or t == 12:
        list_of_bonuses.append(SlowDownBonus(x, y))
    elif t == 13:
        list_of_bonuses.append(LifeBonus(x, y))


def trigger_antibonus(x, y, list_of_antibonuses, p):
    if p == 0:
        list_of_antibonuses.append(SpeedAntiBonus(x, y))
    elif p == 1:
        list_of_antibonuses.append(WidthAntiBonus(x, y))
    elif p == 2:
        list_of_antibonuses.append(SlowDownAntiBonus(x, y))
    elif p == 3:
        pass


# на кадр увеличивает радиус шара, почти равносильно взрыву
def trigger_explosion(x, y, obj8):
    obj8.radius *= 10


def rating(score, screen):
    # анимированное окно ввода ника
    w = 800
    h = 800
    button_width = 300
    button_height = 100
    font = pygame.font.Font('Thintel.ttf', 50)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(int((w - button_width) / 2) + 15, int(h / 2 - 10), int(button_width - 15), 50)
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
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((0, 0, 0))
        rect(screen, (255, 218, 158),
             (int((w - button_width) / 2), int((h - button_height) / 2), button_width, button_height))
        name_text = font.render('Enter your name ', True, (99, 128, 255))
        screen.blit(name_text, (int((w - button_width) / 2) + 11, int((h - button_height) / 2) + 3))
        txt_surface = font.render(text, True, color)
        width = button_width - 30
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)

    # передача ника во вспомогательный файл с рейтингом
    nickbase = open('currentnickname.txt', 'r')
    s = nickbase.readline()
    k = s.rstrip()
    nickbase.close()
    nickname = k

    # затирание вспомогательного файла
    yuio = open('currentnickname.txt', 'w')
    yuio.close()

    # сохранение 10 лучших игроков
    top10_r = open('top10.txt', 'r')
    s = top10_r.readlines()  # сохранение исходного состояние файла с рейтингом
    top10_r.close()
    top10_w = open('top10.txt', 'w')
    if len(s) == 0:  # если файл с рейтингом пуст6 то сразу пишет новый результат
        print('1. ' + nickname + ' ' + str(score), file=top10_w)
    else:
        list_of_scores = []
        for i in range(len(s)):
            score_r = s[i][len(s[i]) - 2]
            j = len(s[i]) - 3
            while s[i][j] != ' ':
                score_r += s[i][j]
                j -= 1
            list_of_scores.append(int(score_r[::-1]))
        if score >= list_of_scores[0]:  # if player has achieved top 1 result number of a player "above" him is -1
            i_sup = -1
        else:  # finding the supremum for player's score in list_of_scores
            i_sup = 0
            for i in range(len(list_of_scores)):
                if score < list_of_scores[i]:
                    i_sup = i
        for i in range(len(s)):  # deleting old positions for every player in top 10, for example "4. "
            s[i] = s[i][3 + i // 10:]
        s.insert(i_sup + 1, nickname + ' ' + str(score) + '\n')  # adding player's result to top10 massive
        for i in range(len(s)):  # adding new positions for every player in top 10
            s[i] = str(i + 1) + '. ' + s[i]
        # writing top 10(or less) players in the file
        if len(s) > 10:
            top10_w.writelines(s[:len(s) - 1])
        else:
            top10_w.writelines(s)
    top10_w.close()


if __name__ == "__main__":
    print("This module is not for direct call!")

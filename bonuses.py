from classes import *
import pygame


class Bonus:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vy = 3
        self.vx = 0
        self.width = 32
        self.height = 32
        self.physical_obj = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

        self.timer = 600

    def move(self):
        self.y += self.vy
        self.physical_obj = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

    def draw(self, screen):
        bonusimage = pygame.image.load("./images/" + self.type + ".png")
        bonusimage = pygame.transform.scale(bonusimage, [32, 32])
        screen.blit(bonusimage, (self.x - self.width/2, self.y - self.height/2))


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
            ball.vy /= self.slow_multiplier
            return 2


class LifeBonus(Bonus):
    def __init__(self, x, y):
        self.type = "LifeBonus"
        Bonus.__init__(self, x, y)
        self.health_boost = 1

    def boost(self, platform, balls):
        platform.lives += self.health_boost


class AntiBonus: #нужны для удобной деактивации эффекта бонусов
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
            ball.vy *= self.slow_multiplier


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
    
    
#На кадр увеличивает ралиус шара, почти равносильно взрыву
def trigger_explosion(x, y, obj8):
    obj8.radius *= 10
    



if __name__ == "__main__":
    print("This module is not for direct call!")


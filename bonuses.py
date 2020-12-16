from platform_ball_targets import *
import pygame


class Bonus:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vy = 3
        self.vx = 0
        self.width = 30
        self.height = 30
        self.physical_obj = pygame.Rect(self.x - self.width/2, self.y - self.height/2,
                                        self.width, self.height)
        
        self.timer = 600

    def move(self):
        self.y += self.vy
        

   
    def collision_with_platform(self, platform: Platform):
        if self.physical_obj.colliderect(platform.physical_obj):
            return True
        else:
            return False
        
    def draw(self, screen):
        bonusimage = pygame.image.load("ball.png")
        bonusimage = pygame.transform.scale(bonusimage, [30, 30])
        screen.blit(bonusimage, (self.x, self.y))
        


class SpeedBonus(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.additional_speed = 5

    def boost(self, platform: Platform, balls):
        platform.v += self.additional_speed
        return 0


class WidthBonus(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.width_multiplier = 1.5

    def boost(self, platform: Platform, balls):
        platform.width *= self.width_multiplier
        
        return 1


class SlowDownBonus(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.slow_multiplier = 1.5

    def boost(self, platform, balls):
        for ball in balls:
            ball.v /= self.slow_multiplier
            ball.vx /= self.slow_multiplier
            ball.vy /= self.slow_multiplier
            return 2
                
                


class AntiBonus:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vy = 1
        self.vx = 0
        self.width = 30
        self.height = 30
        self.physical_obj = pygame.Rect(self.x - self.width/2, self.y - self.height/2,
                                        self.width, self.height)
        
        self.timer = 600

    def move(self):
        self.y += self.vy
        

   
    def collision_with_platform(self, platform: Platform):
        if self.physical_obj.colliderect(platform.physical_obj):
            return True
        else:
            return False
        
    def draw(self, screen):
        antibonusimage = pygame.image.load("heart.png")
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
        Bonus.__init__(self, x, y)
        self.slow_multiplier = 1.5

    def boost(self, platform, balls):
        for ball in balls:
            ball.v *= self.slow_multiplier
            ball.vx *= self.slow_multiplier
            ball.vy *= self.slow_multiplier
            
            
            
            
            
def trigger_bonus(x, y, l, t):
    if t == 1:
        l.append(SpeedBonus(x, y))
    elif t == 2:
        l.append(WidthBonus(x, y))
    elif t == 3:
        l.append(SlowDownBonus(x, y))


def trigger_antibonus(x, y, b, p):
    if p == 0:
        b.append(SpeedAntiBonus(x, y))
    elif p == 1:
        b.append(WidthAntiBonus(x, y))
    elif p == 2:
        b.append(SlowDownAntiBonus(x, y))

    pass


if __name__ == "__main__":
    print("This module is not for direct call!")

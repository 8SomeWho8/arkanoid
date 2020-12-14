from platform_ball_targets import *
import pygame


class Bonus:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vy = 3
        self.vx = 0
        self.width = 20
        self.height = 20
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
        bonusimage = pygame.transform.scale(bonusimage, [20, 20])
        screen.blit(bonusimage, (self.x, self.y))
        


class SpeedBonus(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.additional_speed = 5

    def boost(self, platform: Platform, balls):
        platform.v += self.additional_speed


class WidthBonus(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.width_multiplier = 1.5

    def boost(self, platform: Platform, balls):
        platform.width *= self.width_multiplier


class SlowDownBonus(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.slow_multiplier = 1.5

    def boost(self, platform, balls):
        for ball in balls:
            ball.v /= self.slow_multiplier
            ball.vx /= self.slow_multiplier
            ball.vy /= self.slow_multiplier
                
                
def trigger_bonus(x, y, l):
    a = randint(1,3)
    if a == 1:
        l.append(SpeedBonus(x, y))
    elif a == 2:
        l.append(WidthBonus(x, y))
    elif a == 3:
        l.append(SlowDownBonus(x, y))

    pass


if __name__ == "__main__":
    print("This module is not for direct call!")


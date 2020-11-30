from classes import *
import pygame


class Bonus:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vy = 5
        self.vx = 0
        self.width = 20
        self.height = 10
        self.physical_obj = pygame.Rect(self.x - self.width/2, self.y - self.height/2,
                                        self.width, self.height)

    def move(self):
        self.y -= self.vy
        self.physical_obj = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2,
                                        self.width, self.height)

    def collision_with_platform(self, platform: Platform):
        if self.physical_obj.colliderect(platform.physical_obj):
            return True
        else:
            return False


class SpeedBonus(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.additional_speed = 5

    def collision_with_platform(self, platform: Platform):
        collided = Bonus.collision_with_platform(self, platform)
        if collided:
            platform.v += self.additional_speed


if __name__ == "__main__":
    print("This module is not for direct call!")

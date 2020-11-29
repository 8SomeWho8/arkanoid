import pygame
from pygame.draw import *
from classes import *
pygame.init()

FPS = 60
screen = pygame.display.set_mode((600, 600))
WHITE = (255, 255, 255)


class GameManager:
    def __init__(self):
        global screen

    def main_loop(self, screen):
        clock = pygame.time.Clock()
        game_over = False

        platform = Platform()
        ball_1 = Ball()
        balls = [ball_1]
        targets = Targets()

        while not game_over:
            clock.tick(FPS)
            screen.fill(WHITE)
            for ball in balls:
                ball.move(platform, screen)
            targets.create_bricks(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        platform.move("left", screen)
                    elif event.key == pygame.K_RIGHT:
                        platform.move("right", screen)
            pygame.display.update()


gm = GameManager()
gm.main_loop(screen)

import pygame
from pygame.draw import *
from classes import *

FPS = 60

WHITE = (255, 255, 255)

class GameManager:
    def __init__(self):
        pass

    def main_loop(self, screen):
        clock = pygame.time.Clock()
        game_over = False

        platform = Platform()
        ball = Balls()

        while not game_over:
            clock.Tick(FPS)
            screen.fill(WHITE)
            ball.move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        platform.move("left")
                    elif event.key == pygame.K_RIGHT:
                        platform.move("right")



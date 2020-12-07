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
        platform.draw(screen)
        ball_1 = Ball()
        balls = [ball_1]
        targets = Targets()
        k = 0
        surf = pygame.image.load("gold.jpg")
        screen.blit (surf, (100, 200))
        while not game_over:
            clock.tick(FPS)
            screen.fill(WHITE)
            screen.blit(surf, (0, 0))
            for ball in balls:
                ball.move(platform)
            
            # метод collidelist() находит индекс кирпича с которым столкнулся мяч, или -1 если столкновения не было
            hit_index = ball_1.inner_square.collidelist(targets.brick_list) # hit_index=главный_обьект.collidelist(обьект, с которым проверяется столкновение)
            if hit_index != -1:
                k += 1
                hit_rect = targets.brick_list.pop(hit_index) # находим по индексу нужный кирпич и одновременно удаляем его из списка
                detect_collision(ball_1, hit_rect) # функция для отражения мяча от кирпича
                hit_color = targets.color_list.pop(hit_index) # аналогично с цветом кирпича
                detect_collision(ball_1, hit_rect) # функция для отражения мяча от кирпича
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    pygame.quit()
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                platform.move("left")
            if key[pygame.K_RIGHT]:
                platform.move("right")
            targets.draw_bricks(screen)
            for ball in balls:
                ball.draw(screen)
            platform.draw(screen)
            score = pygame.font.Font('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 15).render('Score:'+str(k), True, RED_CORAL)
            screen.blit(score, (500, 500))
            pygame.display.update()


gm = GameManager()
gm.main_loop(screen)

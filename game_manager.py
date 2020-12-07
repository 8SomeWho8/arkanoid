import pygame
from pygame.draw import *
from platform_ball_targets import *

pygame.init()
FPS = 60
screen = pygame.display.set_mode((800, 800))
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
        targets.gift_bricks()
        surf = pygame.image.load("fon.jpg")
        surf = pygame.transform.scale(surf, [800, 800])

        while not game_over:
            clock.tick(FPS)
            screen.fill(WHITE)
            screen.blit(surf, (0, 0))

            # метод collidelist() находит индекс кирпича с которым столкнулся мяч, или -1 если столкновения не было
            hit_index = ball_1.inner_square.collidelist(
                targets.brick_list)  # hit_index=главный_обьект.collidelist(обьект, с которым проверяется столкновение)
            if hit_index != -1:

                for i in range(len(targets.gifted_bricks_list)):  # поиск мертвого кирпича в списке одаренных
                    if hit_index == targets.gifted_bricks_list[i]:
                        trigger_bonus(ball_1.x,
                                      ball_1.y)  # запускается функция появления и дальнейшей жизни бонуса, а также передается примерное место смерти кирпича (не придумал как запросить координаты мертвого кирпича, решил взять координату шарика, она не сильно отличается)

                k += 1
                hit_rect = targets.brick_list.pop(
                    hit_index)  # находим по индексу нужный кирпич и одновременно удаляем его из списка
                detect_collision(ball_1, hit_rect)  # функция для отражения мяча от кирпича
                hit_color = targets.color_list.pop(hit_index)  # аналогично с цветом кирпича
                detect_collision(ball_1, hit_rect)  # функция для отражения мяча от кирпича
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for ball in balls:
                            ball.on_platform = False
                            alpha = np.arctan(2 * (ball.x - platform.x) / platform.width * np.tan(7 * np.pi / 18))
                            ball.vx = round(ball.v * np.sin(alpha))
                            ball.vy = - round(ball.v * np.cos(alpha))

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                platform.move("left")
            if key[pygame.K_RIGHT]:
                platform.move("right")
            for ball in balls:
                if ball.on_platform:
                    ball.move_on_platform(platform, -0.5)
                else:
                    ball.move_freely(platform)
            targets.draw_bricks(screen)
            for ball in balls:
                ball.draw(screen)
            platform.draw(screen)
            score = pygame.font.SysFont('arial', 20).render('Score:' + str(k), True, RED_CORAL)
            screen.blit(score, (700, 700))
            pygame.display.update()


gm = GameManager()
gm.main_loop(screen)

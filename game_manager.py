import pygame
from pygame.draw import *
from platform_ball_targets import *
from bonuses import *

pygame.init()
FPS = 60
screen = pygame.display.set_mode((800, 700))
WHITE = (255, 255, 255)


class GameManager:
    def __init__(self):
        global screen

    def main_loop(self, screen):
        clock = pygame.time.Clock()
        game_over = False
        game_restart = False
        game_pause = False
        game_exit = False
        menu = Menu()
        platform = Platform()
        platform.draw(screen)
        ball_1 = Ball()
        balls = [ball_1]
        bonuses = []
        antibonuses = []
        targets = Targets()
        score = 0
        targets.gift_bricks()
        background = pygame.image.load("desert.png")
        background = pygame.transform.scale(background, [800, 700])

        while not game_over and not game_restart:
            while not game_pause and not game_over:
                clock.tick(FPS)
                screen.blit(background, (0, 0))

                # метод collidelist() находит индекс кирпича с которым столкнулся мяч, или -1 если столкновения не было
                hit_index = ball_1.inner_square.collidelist(
                    targets.brick_list)  # hit_index=главный_обьект.collidelist(обьект, с которым проверяется столкновение)
                if hit_index != -1:

                    for i in range(len(targets.gifted_bricks_list)):  # поиск мертвого кирпича в списке одаренных
                        if hit_index == targets.gifted_bricks_list[i]:
                            m = randint(1, 3)
                            trigger_bonus(ball_1.x,
                                          ball_1.y,
                                          bonuses,
                                          m)  # запускается функция появления и дальнейшей жизни бонуса, а также передается примерное место смерти кирпича (не придумал как запросить координаты мертвого кирпича, решил взять координату шарика, она не сильно отличается)

                    score += 1
                    hit_rect = targets.brick_list.pop(
                        hit_index)  # находим по индексу нужный кирпич и одновременно удаляем его из списка
                    detect_collision(ball_1, hit_rect)  # функция для отражения мяча от кирпича
                    hit_color = targets.color_list.pop(hit_index)  # аналогично с цветом кирпича
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            for ball in balls:
                                if ball.on_platform:
                                    alpha = np.arctan(2 * (ball.x - platform.x) / platform.width * np.tan(7 * np.pi / 18))
                                    ball.vx = round(ball.v * np.sin(alpha))
                                    ball.vy = - round(ball.v * np.cos(alpha))
                                    ball.on_platform = False
                        if event.key == pygame.K_ESCAPE:
                            game_pause = True

                key = pygame.key.get_pressed()

                if key[pygame.K_LEFT]:
                    platform.move("left")       
                if key[pygame.K_RIGHT]:
                    platform.move("right")

                for bonus in bonuses:
                    if bonus.physical_obj.colliderect(platform.physical_obj):
                        trigger_antibonus(0, 0, antibonuses, bonus.boost(platform, balls)) 
                        bonuses.remove(bonus)
                        
                    else:
                        bonus.move()
                        
                    if bonus.y > 850  and len(bonuses) > 1:
                        bonuses.remove(bonus)

                for bonus in bonuses:
                    bonus.draw(screen)
                    
                    
                for antibonus in antibonuses:
                    if (antibonus.y + antibonus.height) > platform.y:
                        
                        antibonus.boost(platform, balls)
                        antibonuses.remove(antibonus)
                    else:
                        antibonus.move()

                for ball in balls:
                    if ball.on_platform:
                        ball.move_on_platform(platform, -0.25)
                    else:
                        ball.move_freely(platform)
                    if platform.lives > 1 and ball.y > 800 + ball.radius and len(balls) == 1:
                        platform.lives -= 1
                        ball.on_platform = True
                    elif ball.y > 800 + ball.radius and len(balls) > 1:
                        balls.remove(ball)
                    elif platform.lives == 1 and ball.y > 800 + ball.radius and len(balls) == 1:
                        game_over = True

                targets.draw_bricks(screen)

                for ball in balls:
                    ball.draw(screen)

                platform.draw(screen)
                heartimage = pygame.image.load("heart.png")
                heartimage = pygame.transform.scale(heartimage, [30, 30])
                for i in range(0, platform.lives):
                    screen.blit(heartimage, (50 + 40 * i, 20))

                score_text = pygame.font.SysFont('arial', 30).render('Score:' + str(score), True, BLACK)
                screen.blit(score_text, (650, 20))

                # if platform.lives == 0:

                pygame.display.update()
            while game_pause:
                screen.blit(background, (0, 0))
                menu.draw_pause_menu(screen)
                pygame.display.update()
                for event in pygame.event.get():
                    menu.action(event)
                if menu.click[0] == True:
                    game_pause = False
                    menu.click[0] = False
                elif menu.click[1] == True:
                    game_pause = False
                    game_restart = True
                    menu.click[1] = False
                elif menu.click[2] == True:
                    game_over = True
                    menu.click[2] = False
                    pygame.quit()

        while game_over:
            clock.tick(FPS)
            game_over_background = pygame.image.load('game_over.png')
            game_over_background = pygame.transform.scale(game_over_background, [800, 700])
            screen.blit(game_over_background, (0, 0))
            menu.draw_end_menu(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    pygame.quit()
                else:
                    menu.action(event)
                if menu.click[0] == True:
                    pygame.quit()
                elif menu.click[1] == True:
                    game_restart = True
                    game_over = False
                    menu.click[1] = False
                elif menu.click[2] == True:
                    game_over = True
                    pygame.quit()

        while game_restart:
            self.main_loop(screen)
            game_restart = False

        # while not game_exit:
        #     game_over_background = pygame.image.load('game_over.png')
        #     game_over_background = pygame.transform.scale(game_over_background, [800, 700])
        #     screen.blit(game_over_background, (0, 0))
        #     pygame.display.update()
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             game_exit = True
        #             pygame.quit()


gm = GameManager()
gm.main_loop(screen)

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
        game_win = False
        game_restart = False
        game_pause = False
        game_arcade = False
        game_endless = False
        game_end = False
        menu = Menu()
        platform = Platform()
        ball_1 = Ball()
        balls = [ball_1]
        bonuses = []
        antibonuses = []
        score = 0
        time = 0
        level_map = "./levels/endless.txt"
        back_score = pygame.Surface((800, 70))
        back_score.fill((255, 255, 255))
        background = pygame.image.load("./images/endless_ground.png")
        background = pygame.transform.scale(background, [800, 630])
        game_start_background = pygame.image.load("./images/game_start.png")
        game_start_background = pygame.transform.scale(game_start_background, [800, 700])
        game_level_background = pygame.image.load("./images/game_level.png")
        game_level_background = pygame.transform.scale(game_level_background, [800, 700])
        heart_image = pygame.image.load("./images/heart.png")
        heart_image = pygame.transform.scale(heart_image, [30, 30])

        while not game_arcade and not game_endless and not game_end:
            screen.blit(game_start_background, (0, 0))
            menu.draw(screen, "start")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                else:
                    menu.action(event)
                if menu.click[0]:
                    game_arcade = True
                    menu.click[0] = False
                elif menu.click[1]:
                    game_endless = True
                    menu.click[1] = False
                elif menu.click[2]:
                    menu.click[2] = False
                    game_end = True

        while game_arcade and not game_end:
            screen.blit(game_level_background, (0, 0))
            menu.draw(screen, "level")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                else:
                    menu.action(event)
                if menu.click[0]:
                    level_map = "./levels/level1.txt"
                    background = pygame.image.load("./images/level1_ground.png")
                    game_arcade = False
                    menu.click[0] = False
                elif menu.click[1]:
                    level_map = "./levels/level2.txt"
                    background = pygame.image.load("./images/level2_ground.png")
                    game_arcade = False
                    menu.click[1] = False
                elif menu.click[2]:
                    level_map = "./levels/level3.txt"
                    background = pygame.image.load("./images/level3_ground.png")
                    game_arcade = False
                    menu.click[2] = False

        while not game_over and not game_restart and not game_win and not game_end:
            targets = Targets(level_map)
            targets.gift_bricks()
            while not game_pause and not game_over and not game_end:
                clock.tick(FPS)
                screen.blit(back_score, (0, 0))
                screen.blit(background, (0, 70))
                time += 1
                # метод collidelist() находит индекс кирпича с которым столкнулся мяч, или -1 если столкновения не было
                # hit_index=главный_обьект.collidelist(обьект, с которым проверяется столкновение)
                hit_index = ball_1.inner_square.collidelist(targets.brick_list)
                if hit_index != -1:
                    for i in range(len(targets.gifted_bricks_list)):  # поиск мертвого кирпича в списке одаренных
                        if hit_index == targets.gifted_bricks_list[i]:
                            m = randint(1, 13)
                            # запускается функция появления и дальнейшей жизни бонуса на месте смерти кирпича
                            trigger_bonus(targets.brick_list[targets.gifted_bricks_list[i]].center[0],
                                          targets.brick_list[targets.gifted_bricks_list[i]].center[1], bonuses, m)

                    score += 1
                    # находим по индексу нужный кирпич и одновременно удаляем его из списка
                    hit_rect = targets.brick_list.pop(hit_index)
                    detect_collision(ball_1, hit_rect)  # функция для отражения мяча от кирпича
                    targets.color_list.pop(hit_index)  # аналогично с цветом кирпича
                if len(targets.brick_list) == 0:
                    game_win = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_end = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            for ball in balls:
                                if ball.on_platform:
                                    alpha = np.arctan(
                                        2 * (ball.x - platform.x) / platform.width * np.tan(7 * np.pi / 18))
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

                    if bonus.y > 850:
                        bonuses.remove(bonus)

                for antibonus in antibonuses:
                    if (antibonus.y + antibonus.height) > platform.y:
                        antibonus.boost(platform, balls)
                        antibonuses.remove(antibonus)
                    else:
                        antibonus.move()

                for ball in balls:
                    if ball.on_platform:
                        ball.move_on_platform(platform)
                    else:
                        ball.move_freely(platform)
                    if platform.lives > 1 and ball.y > 800 + ball.radius and len(balls) == 1:
                        platform.lives -= 1
                        ball.on_platform = True
                        ball.position_on_platform = random() - 0.5
                    elif ball.y > 800 + ball.radius and len(balls) > 1:
                        balls.remove(ball)
                    elif platform.lives == 1 and ball.y > 800 + ball.radius and len(balls) == 1:
                        playsound("./sounds/sfx_game_over.wav", False)
                        game_over = True

                if game_endless and not game_over:
                    if time == 900:
                        time = 0
                        targets.move()
                        targets.gift_bricks()
                    for i in range(len(targets.brick_list)):
                        if targets.brick_list[i].bottom > 630:
                            game_over = True

                targets.draw_bricks(screen)

                for bonus in bonuses:
                    bonus.draw(screen)

                for ball in balls:
                    ball.draw(screen)

                platform.draw(screen)
                for i in range(0, platform.lives):
                    screen.blit(heart_image, (50 + 40 * i, 20))

                score_text = pygame.font.Font('Thintel.ttf', 50).render('Score: ' + str(score), True, BLACK)
                screen.blit(score_text, (650, 10))

                pygame.display.update()
            while game_pause and not game_end:
                screen.blit(game_start_background, (0, 0))
                menu.draw(screen, "pause")
                pygame.display.update()
                for event in pygame.event.get():
                    menu.action(event)
                if menu.click[0]:
                    game_pause = False
                    menu.click[0] = False
                elif menu.click[1]:
                    game_pause = False
                    game_restart = True
                    menu.click[1] = False
                elif menu.click[2]:
                    menu.click[2] = False
                    game_end = True

        while (game_over or game_win) and not game_end:
            game_end_background = pygame.Surface((800, 700))
            if game_over:
                game_end_background = pygame.image.load("./images/game_over.png")
            elif game_win:
                game_end_background = pygame.image.load("./images/game_win.png")
            game_end_background = pygame.transform.scale(game_end_background, [800, 700])
            screen.blit(game_end_background, (0, 0))
            menu.draw(screen, "end")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                else:
                    menu.action(event)
                if menu.click[1]:
                    game_restart = True
                    game_over = False
                    menu.click[1] = False
                elif menu.click[2]:
                    game_end = True

        while game_restart and not game_end:
            game_restart = False
            self.main_loop(screen)

        pygame.quit()


if __name__ == "__main__":
    gm = GameManager()
    gm.main_loop(screen)

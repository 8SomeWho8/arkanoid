from bonuses import *
pygame.init()
FPS = 60
screen = pygame.display.set_mode((800, 700))


def main_loop(screen):
    pygame.mixer.music.load("./sounds/menu_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    clock = pygame.time.Clock()

    # переменные - флажки состояния игры
    game_over = False
    game_win = False
    game_restart = False
    game_pause = False
    game_arcade = False
    game_endless = False
    game_end = False
    game_choose = False
    game_rating = False

    # объявление главных объектов игры
    menu = Menu()
    platform = Platform()
    ball = Ball()
    bonuses = []
    antibonuses = []
    score = 0
    time = 0
    level_map = "./levels/endless.txt"

    # создание всех нужных картинок для отрисовки игры
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

    # цикл, описывающий работу главного меню
    while not game_arcade and not game_endless and not game_end:
        screen.blit(game_start_background, (0, 0))
        menu.draw(screen, "start")
        name_text = pygame.font.Font('Thintel.ttf', 70).render('B R I C K  S T A R S', True, BLACK)
        screen.blit(name_text, (250, 30))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = True
            else:
                menu.action(event)
            if menu.click[0]:
                game_arcade = True
                game_choose = True
                menu.click[0] = False
            elif menu.click[1]:
                game_endless = True
                menu.click[1] = False
            elif menu.click[2]:
                menu.click[2] = False
                game_end = True

    # цикл, описывающий работу меню выбора уровня в аркадном режиме
    while game_arcade and not game_end and game_choose:
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
                game_choose = False
                menu.click[0] = False
            elif menu.click[1]:
                level_map = "./levels/level2.txt"
                background = pygame.image.load("./images/level2_ground.png")
                game_choose = False
                menu.click[1] = False
            elif menu.click[2]:
                level_map = "./levels/level3.txt"
                background = pygame.image.load("./images/level3_ground.png")
                game_choose = False
                menu.click[2] = False

    # главный процесс -- движение и взаимодействие всех объектов
    if not game_over and not game_restart and not game_win and not game_end:
        pygame.mixer.music.pause()
    while not game_over and not game_restart and not game_win and not game_end:
        targets = Targets(level_map)
        targets.gift_bricks()
        while not game_pause and not game_over and not game_end and not game_win:
            clock.tick(FPS)
            screen.blit(back_score, (0, 0))
            screen.blit(background, (0, 70))
            time += 1
            # метод collidelist() находит индекс кирпича с которым столкнулся мяч, или -1 если столкновения не было
            # hit_index=главный_обьект.collidelist(обьект, с которым проверяется столкновение)
            hit_index = ball.inner_square.collidelist(targets.brick_list)
            if hit_index != -1:
                playsound("./sounds/sfx_brick_destroyed.wav", False)
                for i in range(len(targets.gifted_bricks_list)):  # поиск мертвого кирпича в списке одаренных
                    if hit_index == targets.gifted_bricks_list[i]:
                        m = randint(1, 13)
                        # запускается функция появления и дальнейшей жизни бонуса на месте смерти кирпича
                        trigger_bonus(targets.brick_list[targets.gifted_bricks_list[i]].center[0],
                                      targets.brick_list[targets.gifted_bricks_list[i]].center[1], bonuses, m)
                score += 1
                # находим по индексу нужный кирпич и одновременно удаляем его из списка
                hit_rect = targets.brick_list.pop(hit_index)
                detect_collision(ball, hit_rect)  # функция для отражения мяча от кирпича
                targets.color_list.pop(hit_index)  # аналогично с цветом кирпича

            # проверка, не выиграна ли еще игра :)
            if len(targets.brick_list) == 0:
                game_win = True

            # обработка событий клавиатуры: нажатие выхода, пробела и escape
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if ball.on_platform:
                            ball.move_freely(platform)
                            ball.on_platform = False
                    if event.key == pygame.K_ESCAPE:
                        game_pause = True

            platform.move()

            # работа с бонусами
            for bonus in bonuses:
                if bonus.physical_obj.colliderect(platform.physical_obj):
                    trigger_antibonus(0, 0, antibonuses, bonus.boost(platform, ball))
                    playsound("./sounds/sfx_powerup_got.wav", False)
                    bonuses.remove(bonus)
                else:
                    bonus.move()
                if bonus.y > 850:
                    bonuses.remove(bonus)
            for antibonus in antibonuses:
                if (antibonus.y + antibonus.height) > platform.y:
                    antibonus.boost(platform, ball)
                    antibonuses.remove(antibonus)
                else:
                    antibonus.move()

            if ball.on_platform:
                ball.move_on_platform(platform)
            else:
                ball.move_freely(platform)

            if platform.lives > 1 and ball.y > 800 + ball.radius:
                platform.lives -= 1
                ball.on_platform = True
                ball.position_on_platform = random() - 0.5
            elif platform.lives == 1 and ball.y > 800 + ball.radius:
                playsound("./sounds/sfx_game_over.wav", False)
                game_over = True

            # движение целей в бесконечном режиме игры
            if game_endless and not game_over:
                if time == 900:
                    time = 0
                    targets.move()
                    targets.gift_bricks()
                for i in range(len(targets.brick_list)):
                    if targets.brick_list[i].bottom > 630:
                        game_over = True

            # рисование
            targets.draw_bricks(screen)
            for bonus in bonuses:
                bonus.draw(screen)
            ball.draw(screen)
            platform.draw(screen)
            for i in range(0, platform.lives):
                screen.blit(heart_image, (50 + 40 * i, 20))
            score_text = pygame.font.Font('Thintel.ttf', 50).render('Score: ' + str(score), True, BLACK)
            screen.blit(score_text, (650, 10))
            pygame.display.update()

        # цикл, описывающий работу паузы
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

    # работа с рейтингом
    if game_endless and game_over:
        rating(score, screen)

    # цикл, описывающий работу конечного меню
    while (game_over or game_win) and not game_end:
        game_end_background = pygame.Surface((800, 700))
        if game_over:
            game_end_background = pygame.image.load("./images/game_over.png")
        elif game_win:
            game_end_background = pygame.image.load("./images/game_win.png")
        game_end_background = pygame.transform.scale(game_end_background, [800, 700])
        screen.blit(game_end_background, (0, 0))
        if game_arcade:
            menu.draw(screen, "end_arcade")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                else:
                    menu.action(event)
                if menu.click[1]:
                    game_restart = True
                    game_over = False
                    game_win = False
                    menu.click[1] = False
                elif menu.click[2]:
                    game_end = True
        if game_endless:
            menu.draw(screen, "end_endless")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                else:
                    menu.action(event)
                if menu.click[0]:
                    game_rating = True
                    menu.click[0] = False
                elif menu.click[1]:
                    game_restart = True
                    game_over = False
                    menu.click[1] = False
                elif menu.click[2]:
                    game_end = True

        while game_rating and not game_restart and not game_end:
            rating_background = pygame.image.load("images/ground_rating.png")
            top5_r = open('top5.txt', 'r')
            s = top5_r.readlines()  # Saving the state of top5.txt file
            top5_r.close()
            screen.blit(rating_background, (0, 0))
            for i in range(len(s)):
                rating_text = pygame.font.Font('Thintel.ttf', 50).render(s[i], True, BLACK)
                screen.blit(rating_text, (150, 86 + 88 * i))
            rating_text = pygame.font.Font('Thintel.ttf', 50).render('press space to restart', True, BLACK)
            screen.blit(rating_text, (150, 541))
            pygame.display.update()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_restart = True
            pygame.display.update()


    # в случае рестарта запуск новой игры
    while game_restart and not game_end:
        game_restart = False
        main_loop(screen)
    pygame.quit()


if __name__ == "__main__":
    main_loop(screen)

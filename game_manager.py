from bonuses import *
pygame.init()
FPS = 60
screen = pygame.display.set_mode((800, 700))
WHITE = (255, 255, 255)
class GameManager:
    def __init__(self):
        global screen
    def main_loop(self, screen):
        pygame.mixer.music.load("./sounds/menu_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
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
        if not game_over and not game_restart and not game_win and not game_end:
            pygame.mixer.music.pause()
        while not game_over and not game_restart and not game_win and not game_end:
            targets = Targets(level_map)
            targets.gift_bricks()
            while not game_pause and not game_over and not game_end:
                ball_1.radius = 9 #нужно, чтобы по прошествии кадра размер шарика обратно уменьшался
                clock.tick(FPS)
                screen.blit(back_score, (0, 0))
                screen.blit(background, (0, 70))
                time += 1
                # метод collidelist() находит индекс кирпича с которым столкнулся мяч, или -1 если столкновения не было
                # hit_index=главный_обьект.collidelist(обьект, с которым проверяется столкновение)
                hit_index = ball_1.inner_square.collidelist(targets.brick_list)
                if hit_index != -1:
                    playsound("./sounds/sfx_brick_destroyed.wav", False)
                    for i in range(len(targets.gifted_bricks_list)):  # поиск мертвого кирпича в списке одаренных
                        if hit_index == targets.gifted_bricks_list[i]:
                            m = randint(1, 13)
                            # запускается функция появления и дальнейшей жизни бонуса на месте смерти кирпича
                            trigger_bonus(targets.brick_list[targets.gifted_bricks_list[i]].center[0],
                                          targets.brick_list[targets.gifted_bricks_list[i]].center[1], bonuses, m)

                    #Проверка на взрывоопасность        
                    for k in range(len(targets.gifted_explosive_bricks_list)):
                        if hit_index == targets.gifted_explosive_bricks_list[k]:
                            trigger_explosion(ball_1.x, ball_1.y, ball)
                            print('booom') #для отладки



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
                        playsound("./sounds/sfx_powerup_got.wav", False)
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


        if game_endless and game_over:

            #Анимированное окно ввода ника
            w = 800
            h = 800
            button_width = 300
            button_height = 100
            font = pygame.font.Font(None, 50)
            clock = pygame.time.Clock()
            input_box = pygame.Rect(int((w - button_width) /2) + 15, int(h / 2 - 10), int(button_width - 15), 50)
            color_inactive = (100, 100, 100)
            color_active = (0, 0, 0)
            color = color_inactive
            active = False
            text = ''
            done = False

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            active = not active
                        else:
                            active = False
                        color = color_active if active else color_inactive
                    if event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:
                                with open('currentnickname.txt', 'a') as f:
                                    print(text, file=f)
                                    done = True
                                    finished = True
                                    break
                                    return
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            else:
                                text += event.unicode

                screen.fill((0, 0, 0))
                rect(screen, (255,218,158), (int((w - button_width) / 2), int((h - button_height) / 2), button_width, button_height))
                name_text = font.render('Enter your name ', 1, (99, 128, 255))
                screen.blit(name_text, (int((w - button_width) / 2) + 11, int((h - button_height) / 2) + 3))
                txt_surface = font.render(text, True, color)
                width = button_width - 30
                input_box.w = width
                screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                pygame.draw.rect(screen, color, input_box, 2)
                pygame.display.flip()
                clock.tick(30)

            #Передача ника во вспомогательный файл с рейтингом
            nickbase = open('currentnickname.txt', 'r')
            s = nickbase.readline()
            k = s.rstrip()
            nickbase.close()
            nickname = k

            #затирание вспомогательного файла
            yuio = open('currentnickname.txt', 'w')
            yuio.close()


            # Сохранение 10 лучших игроков
            top10_r = open('top10.txt', 'r')
            s = top10_r.readlines() # Saving the state of top10.txt file
            top10_r.close()
            top10_w = open('top10.txt', 'w')
            if len(s) == 0:  # If top10.txt is empty writing a new result
                print('1. ' + nickname + ' ' + str(score), file=top10_w)
            else:
                list_of_scores = []
                for i in range(len(s)):  # Reading scores from the file to create list of scores of all 10 players
                    score_r = s[i][len(s[i]) - 2]
                    j = len(s[i]) - 3
                    while s[i][j] != ' ':
                        score_r += s[i][j]
                        j -= 1
                    list_of_scores.append(int(score_r[::-1]))
                if score >= list_of_scores[0]:  # If player has achieved top 1 result number of a player "above" him is -1
                    i_sup = -1
                else:  # Finding the supremum for player's score in list_of_scores
                    i_sup = 0
                    for i in range(len(list_of_scores)):
                        if score < list_of_scores[i]:
                            i_sup = i
                for i in range(len(s)):  # Deleting old positions for every player in top 10, for example "4. "
                    s[i] = s[i][3 + i // 10:]
                s.insert(i_sup + 1, nickname + ' ' + str(score) + '\n')  # Adding player's result to top10 massive
                for i in range(len(s)):  # Adding new positions for every player in top 10
                    s[i] = str(i + 1) + '. ' + s[i]
                # Writing top 10(or less) players in the file
                if len(s) > 10:
                    top10_w.writelines(s[:len(s) - 1])
                else:
                    top10_w.writelines(s)
            top10_w.close()

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

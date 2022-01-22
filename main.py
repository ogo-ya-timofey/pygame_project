from pygame import *
import pygame
import sys
import os
from levels import Level, hitlist, coinlist
i = 0
j = 0
current_level_no = 0
coins_counter = 0
walkRight = ['data/pygame_right_1.png',
'data/pygame_right_2.png', 'data/pygame_right_3.png',
'data/pygame_right_4.png', 'data/pygame_right_5.png',
'data/pygame_right_6.png']

walkLeft = ['data/pygame_left_1.png',
'data/pygame_left_2.png', 'data/pygame_left_3.png',
'data/pygame_left_4.png', 'data/pygame_left_5.png',
'data/pygame_left_6.png']
BACKGROUND_COLOR = "#000000"
FPS = 60
size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Трамп меняет профессию')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/pygame_idle.png')
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0

    def update(self):
        global coins_counter
        global starty, startx
        global current_level_no
        global i
        global j
        self.calc_grav()
        self.rect.x += self.change_x
        if j == 2:
            if self.change_x == -9 and i <= 5:
                self.image = pygame.image.load(walkLeft[i])
                i += 1
            elif i > 5:
                i = 0
            elif self.change_x == 9 and i <= 5:
                self.image = pygame.image.load(walkRight[i])
                i += 1
            j = 0
        else:
            j += 1
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
            if block in hitlist:
                time.wait(100)
                self.rect.x = 0
                self.rect.y = 720 - 71
        coin_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, False)
        for coin in coin_hit_list:
            if coin in coinlist and coins_counter < 5:
                coins_counter += 1
                self.level.coin_list.remove(coin)

        # Передвигаемся вверх/вниз
        self.rect.y += self.change_y
        if self.rect.x >= SCREEN_WIDTH - 9 * 10 and current_level_no < 4:
            current_level_no += 1
            startx = 0
            starty = 720 - 71
            main()
        elif self.rect.x >= SCREEN_WIDTH - 9 * 10 and current_level_no == 4:
            final_screen()
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            if block in hitlist:
                time.wait(500)
                self.rect.x = 0
                self.rect.y = 720 - 71
            self.change_y = 0



    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -13

    def go_left(self, speedboost):
        if not speedboost:
            self.change_x = -9

    def go_right(self, speedboost):
        if not speedboost:
            self.change_x = 9

    def stop(self):
        global current_level_no
        self.change_x = 0
        self.image = pygame.image.load('data/pygame_idle.png')


class Static_coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/coin3.png')
        self.rect = self.image.get_rect()


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/arrow.png')
        self.rect = self.image.get_rect()

    def move(self, updown):
        if updown == 'down':
            self.rect.y += 40
        elif updown == 'up':
            self.rect.y -= 40



def terminate():
    pygame.quit()
    sys.exit()


def final_screen_win_text():
    global out
    size = width, height = 1080, 720
    screen = pygame.display.set_mode((width, height), 0, 0)
    pygame.display.set_caption("Путешествие Дональда")
    intro_text = ["Дональд остался очень доволен тем,",
                  "что вы собрали все монеты",
                  f"и сделали это за {out}!",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "Нажмите любую клавишу для выхода в главное меню"
                  ]
    suptiters = ["Над проектом работали:",
                 "Писанко Александр  и  Тимофей Маркин"]
    fon = pygame.transform.scale(pygame.image.load('data/final_win_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/font1.otf', 45)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font('data/font1.otf', 30)
    text_coord = 630
    for sup in suptiters:
        string_rendered = font.render(sup, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def final_screen_lose_text():
    size = width, height = 1080, 720
    screen = pygame.display.set_mode((width, height), 0, 0)
    pygame.display.set_caption("Путешествие Дональда")
    intro_text = ["                         Дональд расстроен!",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  f"К сожалению, вы собрали только {coins_counter} монет из 5.",
                  "Возвращайтесь в главное меню и попробуйте снова!",
                  "Для выхода в главное меню нажмите любую клавишу."]
    fon = pygame.transform.scale(pygame.image.load('data/final_lose_fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/font1.otf', 45)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def final_screen():
    global starty, startx
    global current_level_no
    size = width, height = 1080, 720
    pygame.display.set_mode(size)
    pygame.display.set_caption("Путешествие Дональда")
    if coins_counter == 5:
        final_screen_win_text()
    else:
        final_screen_lose_text()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
                main()
            pygame.display.flip()
            clock.tick(FPS)
    current_level_no = 0
    startx, starty = 0, 0



def start_screen_text():
    size = width, height = 1080, 720
    screen = pygame.display.set_mode((width, height), 0, 0)
    pygame.display.set_caption("Путешествие Дональда")
    intro_text = [
                  "Ваша задача - пройти 5 локаций и помочь Дональду собрать 5 монеток.",
                  "Вы можете проходить игру на время и соревноваться с друзьями.",
                  "Управление:",
                  "'Стрелки вправо и влево' - движение",
                  "'Пробел' - прыжок",
                  "'S' - сохранение",
                  "'R' - возврат в главное меню",
                  "     Новая игра",
                  "     Загрузить сохранение",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "                                   Для продолжения нажмите 'SPACE'"]

    fon = pygame.transform.scale(pygame.image.load('data/fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/font1.otf', 45)
    text_coord = 50
    string_rendered = font.render("ПУТЕШЕСТВИЕ ДОНАЛЬДА", 1, pygame.Color('white'))
    screen.blit(string_rendered, (330, 0))
    font = pygame.font.Font('data/font1.otf', 30)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)






def start_screen():
    global starty, startx
    global current_level_no
    global coins_counter
    global size
    screen = pygame.display.set_mode(size)
    start_screen_text()
    current_level_no = 0
    clock = pygame.time.Clock()
    arrow = Arrow()
    arrow.rect.x = 10
    arrow.rect.y = 340
    arrow_sprite_list = pygame.sprite.Group()
    arrow_sprite_list.add(arrow)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and arrow.rect.y < 340 + 40:
                    start_screen_text()
                    arrow.move('down')
                if event.key == pygame.K_UP and arrow.rect.y > 340:
                    start_screen_text()
                    arrow.move('up')
                if event.key == K_SPACE and arrow.rect.y == 340:
                    startx = 0
                    starty = 720
                    current_level_no = 0
                    coins_counter = 0
                    return
                if event.key == K_SPACE and arrow.rect.y == 340 + 40:
                    with open('data/Сохранение.txt', encoding="utf-8") as f:
                        data = f.readlines()
                        startx = int(data[0])
                        starty = int(data[1])
                        current_level_no = int(data[2])
                        coins_counter = int(data[3])
                    f.close()
                    return

        arrow_sprite_list.draw(screen)
        arrow_sprite_list.update()
        pygame.display.flip()
        clock.tick(FPS)



start_screen()
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720



def main():
    global starty
    global startx
    global screen
    global out
    pygame.init()
    os.environ['Sp_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
    pygame.display.set_caption("Путешествие Дональда")
    player = Player()
    static_coin = Static_coin()
    level_list = []
    level_list.append(Level(player, 1, "jungle"))
    level_list.append(Level(player, 2, "cave"))
    level_list.append(Level(player, 3, "ice"))
    level_list.append(Level(player, 4, "night"))
    level_list.append(Level(player, 5, "forest"))
    global current_level_no
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    static_coin.rect.x = 0
    static_coin.rect.y = 0
    player.level = current_level
    player.rect.x = startx
    player.rect.y = starty - player.rect.height
    active_sprite_list.add(player)
    active_sprite_list.add(static_coin)
    done = False
    clock = pygame.time.Clock()
    while not done:
        font = pygame.font.Font('data/etna-free-font.otf', 45)
        string_rendered = font.render(f': {coins_counter}', True, pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left(False)
                if event.key == pygame.K_RIGHT:
                    player.go_right(False)
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_r:
                    start_screen()
                    main()
                if event.key == pygame.K_s:
                    f = open("data/Сохранение.txt", 'w')
                    f.write(str(player.rect.x))
                    f.write('\n')
                    f.write(str(player.rect.y))
                    f.write('\n')
                    f.write(str(current_level_no))
                    f.write('\n')
                    f.write(str(coins_counter))
                    f.close()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        ticks = pygame.time.get_ticks()
        millis = ticks % 1000
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        screen.blit(string_rendered, (45, 0))
        pygame.display.flip()
        active_sprite_list.update()
        current_level.update()
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        if player.rect.left < 0:
            player.rect.left = 0
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(45)
        pygame.display.flip()
    pygame.quit()
main()
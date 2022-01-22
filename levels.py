import pygame
pygame.init()
hitlist = []
coinlist = []
coinanim = ['data/coin1.png',
            'data/coin2.png',
            'data/coin3.png', 'data/coin4.png', 'data/coin5.png',
            'data/coin6.png', 'data/coin7.png', 'data/coin8.png',
            'data/coin9.png', 'data/coin10.png']

i1 = 0


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(coinanim[0])
        self.rect = self.image.get_rect()

    def update(self):
        global i1
        if i1 <= 9:
            self.image = pygame.image.load(coinanim[i1])
            i1 += 1
        elif i1 > 9:
            i1 = 0


class Block(pygame.sprite.Sprite):
    def __init__(self, material):
        super().__init__()
        self.image = pygame.image.load(f'data/block_{material}.png')
        self.rect = self.image.get_rect()


class Platform(pygame.sprite.Sprite):
    def __init__(self, material):
        super().__init__()
        self.image = pygame.image.load(f'data/platform_{material}.png')
        self.rect = self.image.get_rect()


class Wood(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f'data/wood.png')
        self.rect = self.image.get_rect()


class BlockDie(Platform):
    def __init__(self, rotation, material):
        Platform.__init__(self, material)
        if rotation == '^':
            self.image = pygame.image.load(f"data/dieBlock_up_{material}.png")
        if rotation == 'v':
            self.image = pygame.image.load(f"data/dieBlock_down_{material}.png")
        if rotation == '<':
            self.image = pygame.image.load(f"data/dieBlock_left_{material}.png")
        if rotation == '>':
            self.image = pygame.image.load(f"data/dieBlock_right_{material}.png")


class Level(object):
    def __init__(self, player, level_num, texture):
        global hitlist
        global coinlist
        self.level_num = level_num
        self.platform_list = pygame.sprite.Group()
        self.blockdie_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.player = player
        level = []
        levelFile = open(f'levels/{level_num}.txt')
        line = " "
        while line[0] != "/":
            line = levelFile.readline()
            if line[0] == "[":
                while line[0] != "]":
                    line = levelFile.readline()
                    if line[0] != "]":
                        endLine = line.find("|")
                        level.append(line[0: endLine])
        x = y = 0
        for row in level:
            for col in row:
                if col == "@":
                    coinblock = Coin()
                    coinblock.rect.x = x
                    coinblock.rect.y = y
                    coinblock.player = self.player
                    self.coin_list.add(coinblock)
                    coinlist.append(coinblock)
                if col == ".":
                    block = Block(texture)
                    block.rect.x = x
                    block.rect.y = y
                    block.player = self.player
                    self.platform_list.add(block)
                if col == "-":
                    block = Platform(texture)
                    block.rect.x = x
                    block.rect.y = y
                    block.player = self.player
                    self.platform_list.add(block)
                if col == "w":
                    block = Wood()
                    block.rect.x = x
                    block.rect.y = y
                    block.player = self.player
                    self.platform_list.add(block)
                if col == "^" or col == 'v' or col == '<' or col == '>':
                    blockdie = BlockDie(col, texture)
                    blockdie.rect.x = x
                    blockdie.rect.y = y
                    blockdie.player = self.player
                    self.platform_list.add(blockdie)
                    hitlist.append(blockdie)
                x += 40
            y += 40
            x = 0

    def update(self):
        self.platform_list.update()
        self.coin_list.update()

    def draw(self, screen):
        bg = pygame.image.load(f'data/bg{self.level_num}.jpg')
        screen.blit(bg, (0, 0))
        self.platform_list.draw(screen)
        self.coin_list.draw(screen)
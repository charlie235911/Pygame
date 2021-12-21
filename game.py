import pygame
import random
import os

FPS = 120

WIDTH = 990
HEIGHT = 660

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 148, 255)

#遊戲初始化 and 創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("水母香菇猜猜看遊戲")
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("img", "背景.png")).convert()
player_img = pygame.image.load(os.path.join("img", "手.png")).convert()
jellyfish_img = pygame.image.load(os.path.join("img", "水母.png")).convert()
mushroom_img = pygame.image.load(os.path.join("img", "香菇.png")).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (196,195))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 900 
        self.rect.y = 500

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += 2
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= 2
        if key_pressed[pygame.K_UP]:
            self.rect.y -= 2
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += 2
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Jellyfish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(jellyfish_img, (180,150))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, 600)
        self.speedx = random.randrange(-2,2)
        self.speedy = random.randrange(-2,2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.speedx == 0 and self.speedy == 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, 600)
            self.speedx = random.randrange(-2,2)
            self.speedy = random.randrange(-2,2)
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, 600)
            self.speedx = random.randrange(-2,2)
            self.speedy = random.randrange(-2,2)
        if self.rect.bottom < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, 600)
            self.speedx = random.randrange(-2,2)
            self.speedy = random.randrange(-2,2)
        if self.rect.right > WIDTH + self.rect.width:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, 600)
            self.speedx = random.randrange(-2,2)
            self.speedy = random.randrange(-2,2)
        if self.rect.left < 0 - self.rect.width:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, 600)
            self.speedx = random.randrange(-2,2)
            self.speedy = random.randrange(-2,2)
        
class Mushroom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mushroom_img, (61,64))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-1,1)
        self.speedy = random.randrange(1,3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-2,2)
            self.speedy = random.randrange(2,4)

all_sprites = pygame.sprite.Group()
mushroom = pygame.sprite.Group()
jellyfish = pygame.sprite.Group()
player = pygame.sprite.Group()
for i in range(8):
    m = Mushroom()
    all_sprites.add(m)
    mushroom.add(m)
for i in range(5):
    j = Jellyfish()
    all_sprites.add(j)
    jellyfish.add(j)
p = Player()
all_sprites.add(p)
player.add(p)


#遊戲迴圈
running = True
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #更新遊戲
    all_sprites.update()
    catches = pygame.sprite.groupcollide(mushroom, player, True, True)
    for catch in catches:
        j = Jellyfish()
        all_sprites.add(j)
        jellyfish.add(j)

    #畫面顯示
    screen.fill(BLUE)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()
#sprite
from warnings import WarningMessage
import pygame
import random 
import os

FPS=60
WIDTH=500
HEIGHT=600

BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)

#遊戲初始化 創視窗
pygame.init()#初始
screen=pygame.display.set_mode((WIDTH,HEIGHT))#視窗
pygame.display.set_caption("水母香菇遊戲")
clock=pygame.time.Clock()#迴圈更新頻率

#載入圖片
backgrond_img=pygame.image.load(os.path.join("img","seabackground.png")).convert()
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
mushroom_img=pygame.image.load(os.path.join("img","mushroom.png")).convert()
jellyfish_img=pygame.image.load(os.path.join("img","jellyfish.png")).convert()

#載入音樂
catch_sound=pygame.mixer.Sound(os.path.join("sound","catch.mp3"))
catch_sound.set_volume(0.1)
allday_sound=pygame.mixer.Sound(os.path.join("sound","allday.mp3"))
allday_sound.set_volume(0.5)
pygame.mixer.music.load(os.path.join("sound","cookbgm.mp3"))
pygame.mixer.music.set_volume(0.2)


font_name = os.path.join("font.ttf")
def draw_text(surf,text,size,x,y):
    font =pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,BLACK)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def draw_start():
    screen.blit(backgrond_img, (0,0))
    draw_text(screen, '不要拔水母我只要香菇!', 40, WIDTH/2, HEIGHT/4)
    draw_text(screen, '上下左右鍵 移動 手 空白鍵抓取', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(68,68)) 
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius =self.rect.width/2
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.center=(WIDTH/2,HEIGHT/2)
        self.rect.bottom=HEIGHT-10
        self.speedx = 8
    def update(self):
        key_pressed =pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x +=self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -=self.speedx
        if key_pressed[pygame.K_DOWN]:
            self.rect.y +=self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -=self.speedx
        
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.bottom>HEIGHT:
            self.rect.bottom=HEIGHT
        if self.rect.top<0:
            self.rect.top=0
    def catch(self):
        x=1
class Mushroom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(mushroom_img,(40,40)) 
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius =self.rect.width/2
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy =random.randrange(2,4)
        self.speedx =random.randrange(-4,4)
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>HEIGHT or self.rect.right>WIDTH or self.rect.left<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedy =random.randrange(2,4)
            self.speedx =random.randrange(-4,4)

class Jellyfish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(jellyfish_img,(40,40)) 
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius =self.rect.width/2
        # pygame.draw.circle(self.image,YELLOW,self.rect.center,self.radius)
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy =random.randrange(2,10)
        self.speedx =random.randrange(-4,4)
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>HEIGHT or self.rect.right>WIDTH or self.rect.left<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedy =random.randrange(2,10)
            self.speedx =random.randrange(-4,4)
all_sprite=pygame.sprite.Group()
mushrooms=pygame.sprite.Group()
jellyfishs=pygame.sprite.Group()
player=Player()
all_sprite.add(player)
for i in range(12):
    jellyfish=Jellyfish()
    all_sprite.add(jellyfish)
    jellyfishs.add(jellyfish)
for i in range(8):
    mushroom=Mushroom()
    all_sprite.add(mushroom)
    mushrooms.add(mushroom)   
score =0
jnum10=0
time=0
pygame.mixer.music.play(-1)
def ends(score,jnum10,time):
    if score>=500:
        wait = True
        while wait:
            clock.tick(FPS)
            # 取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(backgrond_img, (0,0))
            draw_text(screen, '挑戰成功!!!', 64, WIDTH/2, HEIGHT/4)
            draw_text(screen, f'水母: {jnum10}', 22, WIDTH/2, HEIGHT/2)
            draw_text(screen, f'分數: {int(score)}', 18, WIDTH/2, HEIGHT*5/8)
            draw_text(screen, f'花費時間: {int(time)}', 18, WIDTH/2, HEIGHT*3/4)
            pygame.display.update()
def endf(score,jnum10,time):
    if score<500:
        pygame.mixer.music.load(os.path.join("sound","end.mp3"))
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(1)
        wait = True
        while wait:
            clock.tick(FPS)
            # 取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(pygame.transform.scale(jellyfish_img,(WIDTH,HEIGHT)), (0,0))
            draw_text(screen, '挑戰失敗...', 64, WIDTH/2, HEIGHT/4)
            draw_text(screen, f'水母: {jnum10}', 22, WIDTH/2, HEIGHT/2)
            draw_text(screen, f'分數: {int(score)}', 18, WIDTH/2, HEIGHT*5/8)
            draw_text(screen, f'花費時間: {int(time)}', 18, WIDTH/2, HEIGHT*3/4)
            pygame.display.update()

draw_start()
# 遊戲迴圈
running = True
while running:
    clock.tick(FPS)
    catchsm=0
    catchsj=0
    # 取得輸入
    for event in pygame.event.get():#同時發生的所有事件
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # player.catch()
                m =pygame.sprite.spritecollide(player,mushrooms,True,pygame.sprite.collide_circle)
                for i in m:
                    catchsm+=1
                j =pygame.sprite.spritecollide(player,jellyfishs,True,pygame.sprite.collide_circle)
                for i in j:
                    catchsj+=1

    # 更新遊戲
    all_sprite.update()
    # hits =pygame.sprite.groupcollide(rocks,bullets,True,False)
    # catchsm =pygame.sprite.spritecollide(player,mushrooms,True,pygame.sprite.collide_circle)
    # catchsj =pygame.sprite.spritecollide(player,jellyfishs,True,pygame.sprite.collide_circle)
    for catchm in range(catchsm):
        score+=10
        mushroom=Mushroom()
        all_sprite.add(mushroom)
        mushrooms.add(mushroom)
        catch_sound.play()
    for catchj in range(catchsj):
        jnum10+=1
        jellyfish=Jellyfish()
        all_sprite.add(jellyfish)
        jellyfishs.add(jellyfish)
        allday_sound.play()
    if time>=100 or jnum10>=10:
        running=False
    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(backgrond_img,(0,0))
    all_sprite.draw(screen)
    draw_text(screen,f'score: {str(score)} /500',18,WIDTH/2,10)
    draw_text(screen,f'jellyfish: {str(jnum10)} /10',18,WIDTH*27/32,10)
    time+=1/60
    draw_text(screen,f'time: {int(time)} /100',18,WIDTH*5/32,10)
    pygame.display.update()
ends(score,jnum10,time)
endf(score,jnum10,time)

pygame.quit()
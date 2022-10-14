import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
vec = pygame.math.Vector2 # 2 for 2 dimensional

FPS = 60
FramePerSec = pygame.time.Clock()

HEIGHT1 = 640
WIDTH = 360

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60 

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
SPEED = 5
SCORE = 0

###would be used if added text 
# font = pygame.font.SysFont("Verdana", 60)  
# font_small = pygame.font.SysFont("Verdana", 20)
# game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("bg_5.png") #defines background as the image being used as the background

#window size, background color before the photo and the title
DISPLAYSURF = pygame.display.set_mode((360,640))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Player(pygame.sprite.Sprite): #flappy bird
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flappy_bird_5.png") #defines self.image as the flappybird photo
        self.rect = self.image.get_rect()
        self.rect.center = (100,320) #starting position
        self.jumping = False
        self.pos = vec((60,360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    

    def move(self): #defines move
        self.acc = vec(0,0.1) #gravity
    
    #commands so the bird will be able to move plus gravity will work
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
             
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos


    def jump(self): #defines jump 
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.top > 0:  #lets you move up and down with arrows #used before gravity and space bar
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -25)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)
        if self.rect.top > 0:              #if space bar is pressed and you are still on screen make you jump
            if pressed_keys[K_SPACE]:
                self.vel.y = -5
        

        
class Obstacles(pygame.sprite.Sprite):  #code to have incoming obstacles #doesn't work currently
    
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT-10)) 
        self.speed = random.randint(-1,1)
        self.moving = True
        self.point = True

    def move(self):
        self.acc = vec(3,0)
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed < 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH


P1 = Player() #defines P1 as the Player Class
O1 = Obstacles() #defines O1 as the Obstacles Class

O1.surf = pygame.Surface((WIDTH, 20))  #obstacle dimenstions / display
O1.surf.fill(GREEN)
O1.rect = O1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

all_sprites = pygame.sprite.Group() #defines all_sprites and adds P1
all_sprites.add(P1)
#all_sprites.add(O1)

INC_SPEED = pygame.USEREVENT + 1       #time to run the game
pygame.time.set_timer(INC_SPEED, 1000)


while True: #game loop
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background,(0,0))  #constantly putting the background up
    
    for entity in all_sprites:    #has flappy bird move
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        P1.jump()
        #O1.move()


    if P1.rect.top < -50 or P1.rect.top > HEIGHT1: #if flappybird hits the top or bottom of the screen game over
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            DISPLAYSURF.fill(RED)
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()

    pygame.display.update() #keeps the game loop running
    FramePerSec.tick(FPS)
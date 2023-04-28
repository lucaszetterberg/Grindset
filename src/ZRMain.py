import pygame 
import random
import os
import sys

pygame.init()



## Global constants
global gameSpeed, obstacles
x_pos_bg = 0
y_pos_bg = 380
points = 0
font = pygame.font.Font('freesansbold.ttf', 20)
gameSpeed = 15
black = (0,0,0)
white = (200,200,200)

CLOUD = pygame.image.load(os.path.join("src", "Cloud.png"))
BG = pygame.image.load(os.path.join("src", "Track.png"))


SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1200
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("images", "ZigmaRun1.png")), pygame.image.load(os.path.join("images", "ZigmaRun2.png"))]
JUMPING = pygame.image.load(os.path.join("images", "ZigmaJump.png"))
SLIDING = [pygame.image.load(os.path.join("images", "ZigmaSlide.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("images", "LargeCactus1.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("images", "LargeCactus1.png"))]

pygame.display.set_caption("Zigma runner")
fps = 60 
font = pygame.font.Font("freesansbold.ttf",16)
obstacles = []

class Player:
    PLAYER_X = 80
    PLAYER_Y = 310
    PLAYER_Y_SLIDE = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.slide_img = SLIDING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.player_slide = False
        self.player_run = True
        self.player_jump = False

        self.step_index = 0
        self.image = self.run_img[0]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.PLAYER_X
        self.player_rect.y = self.PLAYER_Y
        self.jump_vel = self.JUMP_VEL

    def update(self, keyboardInput):
        if self.player_slide:
            self.slide()
        if self.player_run:
            self.run()
        if self.player_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

        if keyboardInput[pygame.K_UP] or keyboardInput[pygame.K_SPACE] and not self.player_jump:
            self.player_slide = False
            self.player_run = False
            self.player_jump = True
        elif keyboardInput[pygame.K_DOWN] and not self.player_jump:
            self.player_slide = True
            self.player_run = False
            self.player_jump = False
        elif not (self.player_jump or keyboardInput[pygame.K_DOWN]):
            self.player_slide = False
            self.player_run = True
            self.player_jump = False

    def slide(self):
        self.image = self.slide_img[0]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.PLAYER_X
        self.player_rect.y = self.PLAYER_Y_SLIDE
        self.step_index += 1
        
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.PLAYER_X
        self.player_rect.y = self.PLAYER_Y
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.player_jump:
            self.player_rect.y -= int(self.jump_vel * 4)
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.player_jump = False
            self.jump_vel = self.JUMP_VEL


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.player_rect.x, self.player_rect.y))
    
class Obstacle:
    def __init__(self, image, type):
        self.image
        self.type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        
    def update(self):
        self.rect.x -= gameSpeed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, ZRMain):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 325
        
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.image = image
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 300

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= gameSpeed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(3800, 3800)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

def menu():
    title_font = pygame.font.Font('freesansbold.ttf', 50)
    menu_font = pygame.font.Font('freesansbold.ttf', 30)

    title_text = title_font.render('Zigma Runner', True, white)
    title_rect = title_text.get_rect()
    title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    start_text = menu_font.render('Press SPACE to start', True, white)
    start_rect = start_text.get_rect()
    start_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    quit_text = menu_font.render('Press Q to quit', True, white)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(start_text, start_rect)
        SCREEN.blit(quit_text, quit_rect)
        pygame.display.update()


def draw_background():
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    x_pos_bg -= gameSpeed


def score():
    global points, gameSpeed
    points += 1
    if points % 100  == 0:
        gameSpeed += 1

    text = font.render("Points: " + str(points), True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (1100, 40)
    SCREEN.blit(text, textRect)

    
          
def main():
    # Show the menu and wait for user input

    menu()
    global gameSpeed, x_pos_bg, y_pos_bg, points
    cloud = Cloud()
    death_count = 0
    
    ## Makes timer, sets gameRunning to true (if gameRunning is false the game will not run)
    timer = pygame.time.Clock()

    player = Player()
    GAMERUNNING = True
    

    
    ## Main game loop, can be viewed as what is happening in each frame
    
    while GAMERUNNING:
        timer.tick(fps)
        SCREEN.fill((white))
        draw_background()
        cloud.draw(SCREEN)
        cloud.update()
        score()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                GAMERUNNING = False

        keyboardInput = pygame.key.get_pressed()
        
        if len(obstacles) == 0:
            obstacles.append(LargeCactus(LARGE_CACTUS))
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.player_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                GAMERUNNING = False


        player.draw(SCREEN)
        player.update(keyboardInput)
        
        pygame.display.flip()
    
    pygame.quit()
    
main()

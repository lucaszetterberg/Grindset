import pygame 
import random
from PIL import Image
##from Player import Player

pygame.init()

screenWidth = 1200
screenHeight = 700
player_x = 100
player_y = 580
deltaY = 0
deltaX = 0
gravity = 1

black = (0,0,0)
white = (235,235,235)

screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Zigma runner")
background = black
fps = 60 
font = pygame.font.Font("freesansbold.ttf",16)
timer = pygame.time.Clock()

##image = Image.open(background)

gameRunning = True

while gameRunning:
    timer.tick(fps)
    screen.fill(background)
    floor = pygame.draw.rect(screen, white, [0, 600, screenWidth, 5])
    player = pygame.draw.rect(screen, white, [player_x, player_y, 20, 20])
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and deltaY == 0:
                deltaY = 20
    
    if deltaY > 0 or player_y < 580:
        player_y -= deltaY
        deltaY -= gravity
    
    if player_y > 580:
        player_y = 580
    
    if player_y == 580 and deltaY < 0:
        deltaY = 0
    
    pygame.display.flip()
pygame.quit()
import pygame
import os

os.system("cls")
pygame.init()

width = 1500
height= 800

screen = pygame.display.set_mode((width, height))

mainLoop = True
clock = pygame.time.Clock()

while mainLoop:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False
                pygame.quit()
                
    clock.tick(60)
    pygame.display.update()


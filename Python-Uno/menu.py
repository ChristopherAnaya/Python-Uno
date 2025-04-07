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

    background_image = pygame.image.load(r"art\menu.jpg").convert_alpha()
    background_image = pygame.transform.scale(background_image, (width, height))
    screen.blit(background_image, (0,0))
    clock.tick(60)
    pygame.display.update()


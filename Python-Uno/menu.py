import pygame
import os

os.system("cls")
pygame.init()

width = 1500
height= 800

screen = pygame.display.set_mode((width, height))

mainLoop = True
clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, lenght, height, color, transparency = 255, hover_color = None):
        rect_surface = pygame.Surface((lenght, height)) 
        rect_surface.set_alpha(transparency)
        rect_surface.fill(color)
        self.rect = rect_surface.get_rect(topleft=(x, y))
        self.rect_surface = rect_surface
        self.hover_color = hover_color
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(self.rect_surface, (self.x, self.y))

    def hover(self, status):
        if self.hover != None:
            self.rect_surface.fill(self.color if not status else self.hover_color)
            if status:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

def first():
    big_font = pygame.font.SysFont("roboto", 60)
    small_font = pygame.font.SysFont("roboto", 30)

    search = pygame.image.load(rf"art\Magnifying_glass.png").convert_alpha()
    search = pygame.transform.scale(search, (150, 150))

    search_text = big_font.render("Search", 1, (240, 240, 240))
    search_text_2 = small_font.render("Find Avaible Games", 1, (220, 220, 220))
    search_text_3 = small_font.render("On Your Network", 1, (220, 220, 220))

    create = pygame.image.load(rf"art\plus.png").convert_alpha()
    create = pygame.transform.scale(create, (150, 150))

    create_text = big_font.render("Create", 1, (240, 240, 240))
    create_text_2 = small_font.render("Create A New Game", 1, (220, 220, 220))
    create_text_3 = small_font.render("On Your Network", 1, (220, 220, 220))

    screen.blit(search, (500, 225))
    screen.blit(search_text, (425 + (300 - search_text.get_width()) // 2, 450))
    screen.blit(search_text_2, (425 + (300 - search_text_2.get_width()) // 2, 500))
    screen.blit(search_text_3, (425 + (300 - search_text_3.get_width()) // 2, 525))

    screen.blit(create, (850, 225))
    screen.blit(create_text, (775 + (300 - create_text.get_width()) // 2, 450))
    screen.blit(create_text_2, (775 + (300 - create_text_2.get_width()) // 2, 500))
    screen.blit(create_text_3, (775 + (300 - create_text_3.get_width()) // 2, 525))

def create():
    background = Button(350, 100, 800, 400, (60,60,60), 200)
    background.draw()

    button_font = pygame.font.SysFont("roboto", 70)

    cancel = button_font.render("Cancel", 1, (240, 240, 240))
    default = button_font.render("Default", 1, (240, 240, 240))
    create = button_font.render("Create", 1, (240, 240, 240))


    screen.blit(cancel, (350 + (250 - cancel.get_width()) / 2, 510 + (75 - cancel.get_height()) / 2))
    screen.blit(default, (625 + (250 - default.get_width()) / 2, 510 + (75 - default.get_height()) / 2))
    screen.blit(create, (900 + (250 - create.get_width()) / 2, 510 + (75 - create.get_height()) / 2))

def menu(mode = None):
    if mode == "create":
        return mode, [["first", Button(350, 510, 250, 75, (30,30,30), 220, (50, 50, 50))], ["default", Button(625, 510, 250, 75, (30,30,30), 220, (50, 50, 50))], ["make", Button(900, 510, 250, 75, (30,30,30), 220, (50, 50, 50))]]
    else:
        return mode, [["search", Button(425, 150, 300, 500, (70,70,70), 200, (90, 90, 90))], ["create", Button(775, 150, 300, 500, (70,70,70), 200, (90, 90, 90))]]
    
def extras(mode = None):
    if mode == "create":
        create()
    else:
        first()

mode, rects = menu()
while mainLoop:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in rects:
                if x[1].rect.collidepoint(event.pos):
                    mode, rects = menu(x[0])

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for x in rects:
        x = x[1]
        x.hover(x.rect.collidepoint(mouse_x, mouse_y))

    background_image = pygame.image.load(r"art\menu.jpg").convert_alpha()
    background_image = pygame.transform.scale(background_image, (width, height))

    screen.blit(background_image, (0,0))
    
    for x in rects:
        x = x[1]
        x.draw()

    extras(mode)
    clock.tick(60)
    pygame.display.update()


import pygame

card_height = 100
card_width = 60

def load_sprite(x, y):
    cards_sheet = pygame.image.load(r"art/cards_spritesheet.png").convert_alpha()
    sprite = pygame.Surface((60, 100), pygame.SRCALPHA)  
    sprite.blit(cards_sheet, (0, 0), (x, y, card_width, card_height)) 
    return sprite

def load_image(filename):
    return pygame.image.load(rf"art\{filename}").convert_alpha()
    
def sprites():

    
    cards_sprites = {
    "yellow_0":load_sprite(0,0),
    "yellow_1":load_sprite(60,0),
    "yellow_2":load_sprite(120,0),
    "yellow_3":load_sprite(180,0),
    "yellow_4":load_sprite(240,0),
    "yellow_5":load_sprite(300,0),
    "yellow_6":load_sprite(360,0),
    "yellow_7":load_sprite(420,0),
    "yellow_8":load_sprite(480,0),
    "yellow_9":load_sprite(540,0),
    "yellow_block":load_sprite(600,0),
    "yellow_reverse":load_sprite(660,0),
    "yellow_plus2":load_sprite(720,0),
    "green_0":load_sprite(0,100),
    "green_1":load_sprite(60,100),
    "green_2":load_sprite(120,100),
    "green_3":load_sprite(180,100),
    "green_4":load_sprite(240,100),
    "green_5":load_sprite(300,100),
    "green_6":load_sprite(360,100),
    "green_7":load_sprite(420,100),
    "green_8":load_sprite(480,100),
    "green_9":load_sprite(540,100),
    "green_block":load_sprite(600,100),
    "green_reverse":load_sprite(660,100),
    "green_plus2":load_sprite(720,100),
    "red_0":load_sprite(0,200),
    "red_1":load_sprite(60,200),
    "red_2":load_sprite(120,200),
    "red_3":load_sprite(180,200),
    "red_4":load_sprite(240,200),
    "red_5":load_sprite(300,200),
    "red_6":load_sprite(360,200),
    "red_7":load_sprite(420,200),
    "red_8":load_sprite(480,200),
    "red_9":load_sprite(540,200),
    "red_block":load_sprite(600,200),
    "red_reverse":load_sprite(660,200),
    "red_plus2":load_sprite(720,200),
    "blue_0":load_sprite(0,300),
    "blue_1":load_sprite(60,300),
    "blue_2":load_sprite(120,300),
    "blue_3":load_sprite(180,300),
    "blue_4":load_sprite(240,300),
    "blue_5":load_sprite(300,300),
    "blue_6":load_sprite(360,300),
    "blue_7":load_sprite(420,300),
    "blue_8":load_sprite(480,300),
    "blue_9":load_sprite(540,300),
    "blue_block":load_sprite(600,300),
    "blue_reverse":load_sprite(660,300),
    "blue_plus2":load_sprite(720,300),
    "wild_change":load_sprite(780,0),
    "wild_plus4":load_sprite(780,100),
    "wild_switch":load_sprite(780, 200),
    "wild_swap":load_sprite(780,300),
    "back":load_sprite(840,0)
    }

    return cards_sprites
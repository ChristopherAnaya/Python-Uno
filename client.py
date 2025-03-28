from network import Network
from sprites import *
import pygame
import os


#python client.py




os.system("cls")
pygame.init()

width = 1500
height= 800

screen = pygame.display.set_mode((width, height))

cards_sprites = sprites()

back_card_image = pygame.transform.scale(cards_sprites["back"], (card_width, card_height))

current_hovering = None

def player_hands(game, n):
    global current_rects
    current_rects = []

    counter = 0
    num = len(game.player_hands[f"player{n.p}"])

    start_x = (width - (num * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5))) / 2

    if num % 2 == 0:
        rotations = ([i for i in range(-num // 2, 0)] + [i for i in range(1, num // 2 + 1)])[::-1]
    else:
        rotations = [i for i in range(-num // 2 + 1, num // 2 + 1)][::-1]

    for i, card in enumerate(game.player_hands[f"player{n.p}"]):
        
        card_image = pygame.transform.scale(cards_sprites[card], (card_width * 1.5, card_height * 1.5))
        rotated_image = pygame.transform.rotate(card_image, rotations[counter])
        
        
        rect = rotated_image.get_rect(topleft=(start_x + counter * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5), 
                                               600 + abs(rotations[counter])))
        screen.blit(rotated_image, rect.topleft)

        
        mask = pygame.mask.from_surface(rotated_image)
        current_rects.append((i, rect, mask))
        counter += 1

"""    draw_p = (n.p + 1) % 5
    if draw_p == 0:
        draw_p = 1
    start_y = (height - (len(game.player_hands[f"player{draw_p}"]) * card_width + (len(game.player_hands[f"player{draw_p}"]) - 1) * 10)) / 2
    counter = 0
    for card in game.player_hands[f"player{draw_p}"]:
        rotated_image = pygame.transform.rotate(cards_sprites["back"], 90)
        rect = rotated_image.get_rect(topleft=(card_width * 2, start_y + (card_width + 10) * counter))
        screen.blit(rotated_image, rect.topleft)
        counter += 1

    draw_p = (draw_p + 1) % 5
    if draw_p == 0:
        draw_p = 1
    start_x = (width - (len(game.player_hands[f"player{n.p}"]) * card_width + (len(game.player_hands[f"player{n.p}"]) - 1) * 10)) / 2
    counter = 0
    for card in game.player_hands[f"player{draw_p}"]:
        rotated_image = pygame.transform.rotate(cards_sprites["back"], 180)
        rect = rotated_image.get_rect(topleft=(start_x + counter * (card_width + 10), 100))
        screen.blit(rotated_image, rect.topleft)
        counter += 1
    
    draw_p = (draw_p + 1) % 5
    if draw_p == 0:
        draw_p = 1
    start_y = (height - (len(game.player_hands[f"player{draw_p}"]) * card_width + (len(game.player_hands[f"player{draw_p}"]) - 1) * 10)) / 2
    counter = 0
    for card in game.player_hands[f"player{draw_p}"]:
        rotated_image = pygame.transform.rotate(cards_sprites["back"], 270)
        rect = rotated_image.get_rect(topleft=(width - card_width * 2 - card_height, start_y + (card_width + 10) * counter))
        screen.blit(rotated_image, rect.topleft)
        counter += 1"""


def redraw(n, game):
    
    screen.fill((128,128,128))

    if not(game.ready):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting For More Players...", 1, (255,0,0))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

    else:
        global draw_rect

        player_hands(game, n)

        for x in game.played_cards:
            card_image = pygame.transform.rotate(cards_sprites[x[0]], x[1])
            rotated_rect = card_image.get_rect(center=((width - card_width) / 2 + x[2], 400 + x[3]))
            screen.blit(card_image, rotated_rect.topleft)

        for i in range(len(game.current_deck) if len(game.current_deck) <= 5 else 5):  
            offset = i * 2 
            screen.blit(back_card_image, ((width - card_width) / 2 * 1.5 - offset, 400 - offset)) 

        draw_rect = cards_sprites["back"].get_rect(topleft=((width - card_width) / 2 * 1.5 - offset, 400 - offset))

        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(f"It Is Players {game.current_player} Turn And You Are {n.p}", 1, (0,0,0))
        screen.blit(text, (width/2 - text.get_width()/2, 0))

def main():
    global increase, current_hovering
    
    mainLoop = True
    clock = pygame.time.Clock()
    try:
        n = Network()
        print("Connected To Server")
        print(f"Joined As Player {n.p}\nWaiting For Connection")
    except:
        print("An Error Ocurred The Server May Not Be Online")
        mainLoop = False
        pygame.quit()

    first_time = True

    while mainLoop:
        try:
            game = n.send("get")
        except:
            mainLoop = False
            print("Connection Interrupted\nReturning To Menu\n")
            break
        
        if first_time:
            first_time = False
            increase = [0] * len(game.player_hands[f"player{n.p}"])
            print(increase)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False
                pygame.quit()
            if game.ready:
                
                clicked = None
                if event.type == pygame.MOUSEBUTTONDOWN and game.current_player == n.p:
                    for index, rect, mask in current_rects:
                        local_mouse_pos = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                        if rect.collidepoint(event.pos) and mask.get_at(local_mouse_pos):
                            clicked = index

                        if draw_rect.collidepoint(event.pos):
                            clicked = "Draw"

                if clicked != None:
                    if clicked == "Draw":
                        game = n.send("draw")
                        increase.append(0)
                    else:
                        if game.player_hands[f"player{n.p}"][clicked] in game.valid_cards:
                            game = n.send(game.player_hands[f"player{n.p}"][clicked])
                            del increase[clicked]

                
                current_hovering = None
                
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                hovering = None
                if event.type == pygame.MOUSEMOTION and game.current_player == n.p:
                    for index, rect, mask in current_rects:
                        local_mouse_pos = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                        if rect.collidepoint(event.pos) and mask.get_at(local_mouse_pos):
                            hovering = index

                        if draw_rect.collidepoint(event.pos):
                            hovering = "Draw"

                if hovering != None:
                    if hovering == "Draw":
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        if game.player_hands[f"player{n.p}"][hovering] in game.valid_cards:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            current_hovering = hovering
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        
        

        if current_hovering != None:
            increase[current_hovering] += 1
        for i, x in enumerate(increase):
            if x != 0:
                if i != current_hovering:
                    increase[i] -= 1
                    
        print(increase)
                

        redraw(n, game)
        
        clock.tick(60)
        pygame.display.update()
        

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill((128,128,128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to play", 1, (0,0,0))
        screen.blit(text, (width / 2 - text.get_width()/2, height / 2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main() 

while True:
    menu_screen()


#python client.py
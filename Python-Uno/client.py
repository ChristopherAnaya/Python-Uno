from network import Network
from sprites import *
import pygame
import os
import time


#python client.py




os.system("cls")
pygame.init()

width = 1500
height= 800

screen = pygame.display.set_mode((width, height))

cards_sprites = sprites()

back_card_image = pygame.transform.scale(cards_sprites["back"], (card_width * 1.5, card_height * 1.5))

current_hovering = None

drawing = False
draw_frame = 0
draw_cords = [0,0]
masks = []

def player_hands(game, n):
    global current_rects, draw_frame, draw_cords, drawing
    current_rects = []
    num = len(game.player_hands[f"player{n.p}"])
    start_x = (width - (num * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5))) / 2

    
    hand = game.player_hands[f"player{n.p}"]
    if drawing:
        draw_image = pygame.transform.scale(cards_sprites[hand[-1]], (card_width * 1.5, card_height * 1.5))
        draw_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
        draw_cords = [int(((start_x + (num-1) * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5)) - ((width - card_width * 1.5) / 2 * 1.2 )) / 60 * draw_frame), int( 275 / 60 * draw_frame)]
        del hand[-1]
        draw_frame += 3
    

    for i, card in enumerate(hand):
        
        card_image = pygame.transform.scale(cards_sprites[card], (card_width * 1.5, card_height * 1.5))
        
        if n.p != game.current_player:
            card_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
        rect = card_image.get_rect(topleft=(start_x + i * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5), 
                                               600 - increase[i]))
        
        screen.blit(card_image, rect.topleft)

        mask = pygame.mask.from_surface(card_image)
        current_rects.append((i, rect, mask))

    if drawing:
        screen.blit(draw_image, ((width - card_width * 1.5) / 2 * 1.2 + draw_cords[0], 325 + draw_cords[1])) 

        if draw_frame == 60:
                drawing = False
                draw_frame = 0
                draw_cords = [0,0]

    draw_p = (n.p + 1) % 5
    if draw_p == 0:
        draw_p = 1

    num = len(game.player_hands[f"player{draw_p}"])

    start_y = (height - (num * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5))) / 2

    for i, card in enumerate(game.player_hands[f"player{draw_p}"]):
        
        card_image = pygame.transform.scale(cards_sprites["back"], (card_width * 1.5, card_height * 1.5))
        rotated_image = pygame.transform.rotate(card_image, 270)
        
        rect = rotated_image.get_rect(topleft=(card_height * .5, start_y + i * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5)))
        screen.blit(rotated_image, rect.topleft)

    draw_p = (draw_p+ 1) % 5
    if draw_p == 0:
        draw_p = 1

    num = len(game.player_hands[f"player{draw_p}"])

    start_x = (width - (num * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5))) / 2

    for i, card in enumerate(game.player_hands[f"player{draw_p}"]):
        
        card_image = pygame.transform.scale(cards_sprites["back"], (card_width * 1.5, card_height * 1.5))
        rotated_image = pygame.transform.rotate(card_image, 180)
        
        rect = rotated_image.get_rect(topleft=(start_x + i * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5), 
                                               100))
        screen.blit(rotated_image, rect.topleft)

    draw_p = (draw_p + 1) % 5
    if draw_p == 0:
        draw_p = 1

    num = len(game.player_hands[f"player{draw_p}"])

    start_y = (height - (num * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5))) / 2
    for i, card in enumerate(game.player_hands[f"player{draw_p}"]):
        
        card_image = pygame.transform.scale(cards_sprites["back"], (card_width * 1.5, card_height * 1.5))
        rotated_image = pygame.transform.rotate(card_image, 90)
        
        rect = rotated_image.get_rect(topleft=(width - card_height * 1.5 - card_height * .5, start_y + i * (card_width - ((num // 2 - (1 if num // 2 != 0 else 0))) * 5)))
        screen.blit(rotated_image, rect.topleft)


def redraw(n, game):
    if 0 in [len(x) for x in list(game.player_hands.values())]:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(f"You Win!", 1, (0,0,0)) if [len(x) for x in list(game.player_hands.values())][n.p-1] == 0 else font.render(f"Player {[len(x) for x in list(game.player_hands.values())].index(0) + 1} Wins.", 1, (0,0,0))
        pygame.draw.rect(screen, (100, 100, 100), ((width - text.get_width()) // 2 - 20, (height - text.get_height()) // 2 - 20, text.get_width() + 40, text.get_height() + 40))
        screen.blit(text, ((width - text.get_width()) // 2, (height - text.get_height()) // 2))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
    
    else:
        screen.fill((128,128,128))
        if not(game.ready):
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Waiting For More Players...", 1, (255,0,0))
            screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

        else:
            global draw_rect, masks

            for x in game.played_cards:
                card_image = pygame.transform.scale(cards_sprites[x[0]], (card_width * 1.5, card_height * 1.5))
                card_image = pygame.transform.rotate(card_image, x[1])
                rotated_rect = card_image.get_rect(center=((width - card_width) / 2 + x[2], 400 + x[3]))
                screen.blit(card_image, rotated_rect.topleft)

            screen.blit(back_card_image, ((width - card_width * 1.5) / 2 * 1.2 , 325)) 

            draw_rect = back_card_image.get_rect(topleft=((width - card_width * 1.5) / 2 * 1.2 , 325))

            font = pygame.font.SysFont("comicsans", 40)
            first_text = font.render(f"It Is Players {game.current_player} Turn And You Are {n.p}", 1, (0,0,0))
            screen.blit(first_text, (width/2 - first_text.get_width()/1.5, 0))
            second_text = font.render(f"Seconds left:{round(30.00 - game.time_left, 2)}", 1, (0,0,0))
            screen.blit(second_text, (width/2 - first_text.get_width()/2 + first_text.get_width(), 0))

            player_hands(game, n)

            if game.pause:
                rect = pygame.Surface((150, 150), pygame.SRCALPHA)
                rect.fill((100, 100, 100))
                rect = pygame.transform.rotate(rect, 45)
                pos = rect.get_rect(center=(width//2, height//2))
                screen.blit(rect, pos.topleft)



                
                masks = []
                blue_rect = pygame.Surface((50, 50), pygame.SRCALPHA)
                blue_rect.fill((0,0,255))
                blue_rect = pygame.transform.rotate(blue_rect, 45)
                blue_pos = blue_rect.get_rect(center=(width//2, height//2 - 50))
                screen.blit(blue_rect, blue_pos.topleft)

                red_rect = pygame.Surface((50, 50), pygame.SRCALPHA)
                red_rect.fill((255, 0, 0))
                red_rect = pygame.transform.rotate(red_rect, 45)
                red_pos = red_rect.get_rect(center=(width//2 + 50, height//2))
                screen.blit(red_rect, red_pos.topleft)

                green_rect = pygame.Surface((50, 50), pygame.SRCALPHA)
                green_rect.fill((0, 255, 0))
                green_rect = pygame.transform.rotate(green_rect, 45)
                green_pos = green_rect.get_rect(center=(width//2 - 50, height//2))
                screen.blit(green_rect, green_pos.topleft)

                yellow_rect = pygame.Surface((50, 50), pygame.SRCALPHA)
                yellow_rect.fill((255, 255, 0))
                yellow_rect = pygame.transform.rotate(yellow_rect, 45)
                yellow_pos = yellow_rect.get_rect(center=(width//2, height//2 + 50))
                screen.blit(yellow_rect, yellow_pos.topleft)

                mask = pygame.mask.from_surface(blue_rect)
                masks.append([blue_pos, mask])
                mask = pygame.mask.from_surface(red_rect)
                masks.append([red_pos, mask])
                mask = pygame.mask.from_surface(green_rect)
                masks.append([green_pos, mask])
                mask = pygame.mask.from_surface(yellow_rect)
                masks.append([yellow_pos, mask])

def main():
    global increase, current_hovering, drawing, masks
    
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False
                pygame.quit()
            if game.ready:
                clicked = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.current_player == n.p:
                        for index, rect, mask in current_rects:
                            local_mouse_pos = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                            if rect.collidepoint(event.pos) and mask.get_at(local_mouse_pos):
                                clicked = index

                        if draw_rect.collidepoint(event.pos):
                            clicked = "Draw"
                            drawing = True

                        if game.pause:
                            for i, (rect, mask) in enumerate(masks):
                                local_mouse_pos = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                                if rect.collidepoint(event.pos) and mask.get_at(local_mouse_pos):
                                    game = n.send(["blue", "red", "green", "yellow"][i])

                if clicked != None and not game.pause:
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
                    if not game.pause:
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

        
        if len(increase) != len(game.player_hands[f"player{n.p}"]):
            for x in range(len(game.player_hands[f"player{n.p}"]) - len(increase)):
                increase.append(0)

        if current_hovering != None:
            if increase[current_hovering] < 50:
                increase[current_hovering] += 5
        for i, x in enumerate(increase):
            if x != 0:
                if i != current_hovering:
                    increase[i] -= 5
                

        redraw(n, game)
        clock.tick(60)
        pygame.display.update()

switch = "te"

while True:
    if switch == "t":
        import menu
    else:
        main()
#python client.py
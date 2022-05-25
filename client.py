import pygame
import math
from pygame_textinput import TextInputVisualizer, TextInputManager
from sys import exit
from network import Network
from interface import redrawWindow, redrawMenu, font
from game import findPos

pygame.init()

class Button:
    def __init__(self, name, x, y, width, height):
        self.name = name    
        self.x = x  
        self.y = y  
        self.width = width  
        self.height = height    
        self.rect = pygame.Rect(x, y, self.width, self.height) 


width = 1280   
height = 720    
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slave")
icon = pygame.image.load("pictures/Icon.png").convert_alpha()
pygame.display.set_icon(icon)

buttons = [Button("Play", 1020, 370, 116, 50), Button("Pass", 1150, 370, 116, 50), Button("Send", 1150, 370, 116, 50),

Button("Start", 579, 480, 122, 50), Button("Quit", 579, 550, 122, 50), Button("Back", 1070, 600, 122, 50)]


def updateHand(game, player):
    hand = game.findPlayerHand(player)
    for index in range(len(hand)):
        if index == len(hand) - 1:
            hand[index].rect = pygame.Rect(90*index, 540, hand[index].width, hand[index].height)
        else:
            hand[index].rect = pygame.Rect(90*index, 540, hand[index].width - 35, hand[index].height)
    return hand

def pickACard(game, card, chosenCard):
    pick = len(chosenCard)
    if card in chosenCard:
        chosenCard.remove(card)
    elif pick == 0:
        chosenCard.append(card)
    elif game.state == 2:
        if pick == 1:
            chosenCard.append(card)
    elif game.state == 3:
        chosenCard.clear()
        chosenCard.append(card)
    elif 1 <= pick <= 3:
        if card.value == chosenCard[-1].value:
            chosenCard.append(card)
        else:
            chosenCard.clear()
            chosenCard.append(card)
    chosenCard.sort()

def checkPlay(game, chosenCard):
    type = len(game.currentCard)    
    play = len(chosenCard)
    if play == 0:
        return False
    elif game.first:
        if chosenCard[0].rank == 1:
            return True
        return False
    elif type == 0:
        return True
    elif type == play:
        return chosenCard[-1] > game.currentCard[-1]
    elif play - type == 2:
        return True
    else:
        return False

def checkPass(game):
    if not game.currentCard:
        return False
    return True

def checkSend(game, chosenCard):
    send = len(chosenCard)
    if game.state == 2:
        if send == 2:
            if send == 2:
                return True
            return False
    elif game.state == 3:
        if send == 1:
            return True
        return False

def updateAction(game, chosenCard, action):
    if game.state == 1 or game.state == 4:
        action[0] = checkPlay(game, chosenCard)
        action[1] = checkPass(game)
    elif game.state == 2 or game.state == 3:
        action[2] = checkSend(game, chosenCard)


def menu():
    scene = 0   
    running = True  
    clock = pygame.time.Clock() 
    manager = TextInputManager(validator = lambda input: len(input) <= 7)
    name = TextInputVisualizer(manager = manager, font_object = font)  
    pygame.key.set_repeat(500, 50)

    while running:
        clock.tick(60) 
        redrawMenu(buttons, screen)
        events = pygame.event.get()
        name.update(events)
        screen.blit(name.surface, (640, 400))

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons[3].rect.collidepoint(pos):
                    if name.value:
                        running = False
                        scene = 1

                elif buttons[4].rect.collidepoint(pos):
                    running = False
                    scene = 2

                elif buttons[5].rect.collidepoint(pos):
                    running = False
                    pygame.quit()
                    exit()

        pygame.display.update()
  
    if scene == 1:
        main(name.value)




#------------------------------- main game function ----------------#
def main(name):
    scene = 0   
    running = True  
    timestart = True    
    sec = 20    
    clock = pygame.time.Clock() 
    chosenCard = [] 
    action = [False, False, False] 

    try:
        n = Network()
        player = int(n.getPlayer())
        game = n.send(name)
        playerPos = findPos(player)
    except:
        running = False
        scene = 1

    while running:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            running = False
            scene = 1
            break

        if player == game.turn:
            updateAction(game, chosenCard, action)

            if timestart:
                start = pygame.time.get_ticks()
                sec = 20
                timestart = False
            elif sec > 0:
                timediff = pygame.time.get_ticks() - start
                sec = 20 - math.floor((timediff%60000)/1000)

            else:
                if game.state == 1 or game.state == 4:
                    chosenCard.clear()
                    if game.currentCard:
                        game = n.send("pass")
                    else:
                        hand = game.findPlayerHand(player)
                        chosenCard.append(hand[0])
                        game = n.send(chosenCard)
                        chosenCard.clear()
                elif game.state == 2:
                    hand = game.findPlayerHand(player)
                    chosenCard.append(hand[0])
                    chosenCard.append(hand[1])
                    game = n.send(chosenCard)
                    chosenCard.clear()
                elif game.state == 3:
                    hand = game.findPlayerHand(player)
                    chosenCard.append(hand[0])
                    game = n.send(chosenCard)
                    chosenCard.clear()
                timestart = True

        redrawWindow(game, player, playerPos, chosenCard, action, buttons, sec, screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if game.state == 5:
                running = False
        
            if player == game.turn:
                hand = updateHand(game, player)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if game.state == 1 or game.state == 4:
                        if buttons[0].rect.collidepoint(pos):
                            if action[0]:
                                game = n.send(chosenCard)
                                chosenCard.clear()
                                timestart = True

                        elif buttons[1].rect.collidepoint(pos):
                            if action[1]:
                                game = n.send("pass")
                                chosenCard.clear()
                                timestart = True

                    elif game.state == 2 or game.state == 3:
                        if buttons[2].rect.collidepoint(pos):
                            if action[2]:
                                game = n.send(chosenCard)
                                chosenCard.clear()
                                timestart = True
                                
                    for card in hand:
                        if card.rect.collidepoint(pos):
                            pickACard(game, card, chosenCard)

    if scene == 1:
        menu()


menu()
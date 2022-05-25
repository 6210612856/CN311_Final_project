import pygame

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)

def image(obj, type):
    if type == "card":
        path =  "pictures/card/" + str(obj) + ".png"
    elif type == "object":
        path =  "pictures/object/" + str(obj) + ".png"
    elif type == "bg":
        path =  "pictures/bg/" + str(obj) + ".png"
    return pygame.image.load(path).convert_alpha()


def text(obj):
    return font.render(str(obj), 1, (0, 0, 0))


def showPos(game, loop, screen):
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (20, 320))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (180, 370))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (920, 40))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (1080, 90))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (470, 40))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (630, 90))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (20, 40))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (180, 90))
    if len(game.players) == 4:
        screen.blit(text(game.players[loop[0] - 1]), (140, 320))
        screen.blit(text(game.players[loop[1] - 1]), (1040, 40))
        screen.blit(text(game.players[loop[2] - 1]), (590, 40))
        screen.blit(text(game.players[loop[3] - 1]), (140, 40))


def showHand(game, player, chosenCard, screen):
    hand = game.findPlayerHand(player)
    for index in range(len(hand)):
        screen.blit(pygame.transform.scale(image(hand[index], "card"), (hand[index].width, hand[index].height)), (90*(index), 540))
        if hand[index] in chosenCard:
            screen.blit(pygame.transform.scale(image("Arrow", "object"), (100, 100)), (90*(index), 440))
    if player == 1:
        screen.blit(text(len(game.p1hand)), (140, 370))
        screen.blit(text(len(game.p2hand)), (1040, 90))
        screen.blit(text(len(game.p3hand)), (590, 90))
        screen.blit(text(len(game.p4hand)), (140, 90))
    elif player == 2:
        screen.blit(text(len(game.p2hand)), (140, 370))
        screen.blit(text(len(game.p3hand)), (1040, 90))
        screen.blit(text(len(game.p4hand)), (590, 90))
        screen.blit(text(len(game.p1hand)), (140, 90))
    elif player == 3:
        screen.blit(text(len(game.p3hand)), (140, 370))
        screen.blit(text(len(game.p4hand)), (1040, 90))
        screen.blit(text(len(game.p1hand)), (590, 90))
        screen.blit(text(len(game.p2hand)), (140, 90))
    elif player == 4:
        screen.blit(text(len(game.p4hand)), (140, 370))
        screen.blit(text(len(game.p1hand)), (1040, 90))
        screen.blit(text(len(game.p2hand)), (590, 90))
        screen.blit(text(len(game.p3hand)), (140, 90))


def showCurrentTurn(game, screen):
    if len(game.players) == 4:
        name = game.players[game.turn - 1]
        turn = name + "'s turn"
        screen.blit(text(turn), (100, 200))

    loop = image("Loop", "object")
    if game.loop == 0:
        loop = pygame.transform.flip(loop, True, False)
    screen.blit(pygame.transform.scale(loop, (50, 50)), (20, 200))

    cards = game.currentCard
    for index in range(len(cards)):
        screen.blit(pygame.transform.scale(image(cards[index], "card"), (cards[index].width, cards[index].height)), (520 + 90*(index), 240))

def showStatus(game, loop, screen):
    for player in loop:
        pos = loop.index(player)

        if player == game.turn:
            if pos == 0:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (20, 320))
            elif pos == 1:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (920, 40))
            elif pos == 2:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (470, 40))
            elif pos == 3:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (20, 40))

        elif player not in game.inplay:
            if player not in game.inround:
                if len(game.win2) >= 2:

                    if game.win1[0] != game.win2[0]:
                        if player == game.win2[1]:
                            if pos == 0:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (20, 330))
                            elif pos == 1:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (920, 50))
                            elif pos == 2:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (470, 50))
                            elif pos == 3:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (20, 50))
                        else:
                            if pos == 0:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 330))
                            elif pos == 1:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (920, 50))
                            elif pos == 2:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (470, 50))
                            elif pos == 3:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 50))

                    else:
                        if pos == 0:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 330))
                        elif pos == 1:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (920, 50))
                        elif pos == 2:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (470, 50))
                        elif pos == 3:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 50))

                else:
                    if pos == 0:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 330))
                    elif pos == 1:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (920, 50))
                    elif pos == 2:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (470, 50))
                    elif pos == 3:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 50))
            
            else:
                if pos == 0:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (20, 330))
                elif pos == 1:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (920, 50))
                elif pos == 2:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (470, 50))
                elif pos == 3:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (20, 50))


def showRole(game, loop, screen):
    role = ["King", "Queen", "People", "Slave"]
    for index in range(len(game.win1)):
        pos = loop.index(game.win1[index])
        if pos == 0:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (45, 290))
        elif pos == 1:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (945, 10))
        elif pos == 2:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (495, 10))
        elif pos == 3:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (45, 10))


def showPlay(game, player, action, buttons, sec, screen):
    if player == game.turn:

        screen.blit(text(sec), (1150, 300))
        screen.blit(pygame.transform.scale(image("Hourglass", "object"), (30, 30)), (1190, 310))

        if game.state == 2 or game.state == 3:
            if game.state == 2:
                screen.blit(text("Choose 2 cards to send to Slave!"), (490, 310))
            elif game.state == 3:
                screen.blit(text("Choose 1 card to send to People!"), (490, 310))
            if action[2]:
                screen.blit(pygame.transform.scale(image(buttons[2].name, "object"), (buttons[2].width, buttons[2].height)), (buttons[2].x, buttons[2].y))

        else:
            if game.first:
                screen.blit(text("You must play Three of Clubs!"), (490, 310))
            if action[0]:
                screen.blit(pygame.transform.scale(image(buttons[0].name, "object"), (buttons[0].width, buttons[0].height)), (buttons[0].x, buttons[0].y))
            if action[1]:
                screen.blit(pygame.transform.scale(image(buttons[1].name, "object"), (buttons[1].width, buttons[1].height)), (buttons[1].x, buttons[1].y))



def redrawWindow(game, player, loop, chosenCard, action, buttons, sec, screen):
    screen.fill((0, 100, 0))

    if game.state == 0:
        redrawWaiting(game, screen)
    else:
        showPos(game, loop, screen)
        showHand(game, player, chosenCard, screen)
        showCurrentTurn(game, screen)
        showStatus(game, loop, screen)
        showRole(game, loop, screen)
        showPlay(game, player, action, buttons, sec, screen)
        pygame.display.update()


def redrawMenu(buttons, screen):
    screen.blit(pygame.transform.scale(image("slavewonder", "bg"), (1280, 720)), (0, 0))
    screen.blit(text("Enter your name: "), (380, 400))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(630, 400, 250, 50))
    screen.blit(pygame.transform.scale(image(buttons[3].name, "object"), (buttons[3].width, buttons[3].height)), (buttons[3].x, buttons[3].y))
    screen.blit(pygame.transform.scale(image(buttons[4].name, "object"), (buttons[4].width, buttons[4].height)), (buttons[4].x, buttons[4].y))
    screen.blit(pygame.transform.scale(image(buttons[5].name, "object"), (buttons[5].width, buttons[5].height)), (buttons[5].x, buttons[5].y))

def redrawWaiting(game, screen):
    screen.blit(pygame.transform.scale(image("Waiting", "bg"), (1280, 720)), (0, 0))
    waittext = "Waiting for player (" + str(len(game.players)) + "/4)"
    screen.blit(text(waittext), (490, 345))
    pygame.display.update()


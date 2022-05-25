import random

class Game:
    def __init__(self, id):
        self.id = id    
        self.players = []   

        self.state = 0
        self.first = True   
        self.turn = 0   
        self.loop = 0  
        self.currentCard = []  
        self.p1hand = []    
        self.p2hand = []    
        self.p3hand = []    
        self.p4hand = []   
        self.inplay = [1, 2, 3, 4]  
        self.inround = [1, 2, 3, 4] 
        self.keepLoop = False   
        self.win1 = []  
        self.win2 = []  
        self.score = [0, 0, 0, 0]  

  
    def updateState(self):
        self.state += 1

        #start round 1
        if self.state == 1:
            print("Game state: ", self.state)
            print("Start round 1!")
            dealCards(self)
            self.findFirstPlayer()

        #prepare to start round 2, King have to send any 2 cards to slave
        elif self.state == 2:
            print("Round 1 score: ", self.win1)
            print("Round 1 end ;w;")
            print("Game state: ", self.state)
            print("Prepare to start round 2...")

            #reset parameters for round 2
            self.inplay = [1, 2, 3, 4]
            self.inround = [1, 2, 3, 4]
            dealCards(self)

            print("Slave send their 2 highest card to King")
            print("King have to send any 2 cards to Slave")
            self.turn = self.win1[0]

        #after king sent cards, Queen have to send any card to people
        elif self.state == 3:
            print("Game state: ", self.state)
            print("People send their highest card to Queen")
            print("Queen have to send any card to People")
            self.turn = self.win1[1]

        #start round 2
        elif self.state == 4:
            print("Game state: ", self.state)
            print("Start round 2!!")
            self.findFirstPlayer()

        #end game
        elif self.state == 5:
            print("Game state: ", self.state)
            print("Game end!!")
            print("Win in round 1", self.win1)
            print("Win in round 2", self.win2)

            #calculate score
            point = 2
            for player in self.win1:
                if point == 0:
                    point -= 1
                self.score[player - 1] += point
                point -= 1
            
            point = 2
            #if there is an overthrow, King got 0 point
            if self.win1[0] != self.win2[0]:
                for player in self.win2:
                    if point == 0:
                        point -= 1
                    if player == self.win1[0]:
                        self.score[player - 1] = 0
                    else:
                        self.score[player - 1] += point
                        point -= 1
            #if not, calculate normally
            else:
                for player in self.win2:
                    if point == 0:
                        point -= 1
                    self.score[player - 1] += point
                    point -= 1

            print("Score of each player: ", self.score)

        else:
            print("Game state: ", self.state)
            print("Game end!!!")


    def drow(self, deck):
        self.p1hand.append(deck.deal())
        self.p2hand.append(deck.deal())
        self.p3hand.append(deck.deal())
        self.p4hand.append(deck.deal())


    def sortHand(self):
        self.p1hand.sort()
        self.p2hand.sort()
        self.p3hand.sort()
        self.p4hand.sort()


    def findPlayerHand(self, player):
        if player == 1:
            return self.p1hand
        elif player == 2:
            return self.p2hand
        elif player == 3:
            return self.p3hand
        elif player == 4:
            return self.p4hand
        print("Can't find player: ", player)
        return None


    def findFirstPlayer(self):

        if self.state == 1:
            if self.p1hand[0].rank == 1:
                self.turn = 1
            elif self.p2hand[0].rank == 1:
                self.turn = 2
            elif self.p3hand[0].rank == 1:
                self.turn = 3
            elif self.p4hand[0].rank == 1:
                self.turn = 4
            else:
                print("Can't find three of clubs.")


        elif self.state == 4:
            slave = self.win1[3]
            king = self.win1[0]
            queen = self.win1[1]


            if slave == 1:
                if king == 4:
                    self.loop = 0
                elif king == 3 and queen == 4:
                    self.loop = 0
            elif slave - king == 1:
                self.loop = 0
            elif abs(slave - king) == 2 and slave - queen == 1:
                self.loop = 0
            else:
                self.loop = 1

            self.turn = slave

    def updateTurn(self, playCard, player):
        self.moveTurn(player)

        if self.first:
            self.first = False

        if playCard:
            for card in playCard:
                self.findPlayerHand(player).remove(card)
            self.currentCard = playCard

            if self.keepLoop:
                self.keepLoop = False

                if len(self.inplay) == 1:
                    self.currentCard.clear()
                    self.inplay = self.inround.copy()

                    if not self.findPlayerHand(player):
                        self.moveTurn(player)
            self.checkWin(player)


        else:
            self.inplay.remove(player)


            if self.keepLoop:
              
                if len(self.inplay) == 0:
                    if self.loop == 0:
                        self.loop = 1
                    else:
                        self.loop = 0
                    self.keepLoop = False
                    self.currentCard.clear()
                    self.inplay = self.inround.copy()
                    self.turn = player
                    print("Reverse loop to: ", self.loop)

          
            else:

                if len(self.inplay) == 1:
                    self.turn = self.inplay[0]
                    self.currentCard.clear()
                    self.inplay = self.inround.copy()

        print("Keep loop: ", self.keepLoop)
        print("Current turn: ", self.turn)
        print("Remaining player in play: ", self.inplay)
        print("Remaining player in round: ", self.inround)

    def moveTurn(self, player):
        turn = self.inplay.index(player)

        if self.loop == 0:
            if player == self.inplay[-1]:
                self.turn = self.inplay[0]
            else:
                self.turn = self.inplay[turn + 1]
        else:
            if player == self.inplay[0]:
                self.turn = self.inplay[-1]
            else:
                self.turn = self.inplay[turn - 1]


    def checkWin(self, player):

        if not self.findPlayerHand(player):
            self.inplay.remove(player)
            self.inround.remove(player)

            if self.state == 1:
                self.win1.append(player)

                if len(self.inround) == 1:
                    self.win1.append(self.inround[0])
                    self.findPlayerHand(self.inround[0]).clear()
                    self.currentCard.clear()
                    self.updateState()
                else:
                    self.keepLoop = True

            #if win in round 2
            if self.state == 4:
                if not self.win2:
                    self.win2.append(player)

                    if player != self.win1[0]:

                        if self.turn == self.win1[0]:                   
                            self.moveTurn(self.win1[0])
                        self.inplay.remove(self.win1[0])
                        self.inround.remove(self.win1[0])
                        self.win2.append(self.win1[0])
                        self.findPlayerHand(self.win1[0]).clear()

                elif len(self.inround) == 1:
                    self.win2.append(player)
                    self.win2.append(self.inround[0])
                    self.findPlayerHand(self.inround[0]).clear()
                    self.currentCard.clear()
                    self.updateState()

                else:
                    self.win2.append(player)
                    self.keepLoop = True

    def tradeCard(self, sendCard):
        print("Trade card...")

        if self.state == 2:
            slave = self.win1[3]
            king = self.win1[0]
            
            self.findPlayerHand(king).append(self.findPlayerHand(slave).pop(-1))
            self.findPlayerHand(king).append(self.findPlayerHand(slave).pop(-1))

            for card in sendCard:
                self.findPlayerHand(king).remove(card)
                self.findPlayerHand(slave).append(card)

            self.sortHand()
            self.updateState()

        elif self.state == 3:
            people = self.win1[2]
            queen = self.win1[1]

            self.findPlayerHand(queen).append(self.findPlayerHand(people).pop(-1))

            for card in sendCard:
                self.findPlayerHand(queen).remove(card)
                self.findPlayerHand(people).append(card)

            self.sortHand()
            self.updateState()

class Card( object ):
    def __init__(self, value, suit, rank):
        self.value = value  
        self.suit = suit    
        self.rank = rank    
        self.width = 125    
        self.height = 180   
        self.rect = None    

    def __repr__(self):
        return str(self.value) + " of " + str(self.suit)

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        if self.rank != other.rank:
            return False
        return True

class Deck( list ):
    def __init__(self):
        suits = {"Clubs":1, "Diamonds":2, "Hearts":3, "Spades":4}
        values = {"Three":1, "Four":2, "Five":3, "Six":4, "Seven":5, "Eight":6, "Nine":7, "Ten":8,
        "Jack":9, "Queen":10, "King":11 ,"Ace":12, "Two":13 }
        rank = 1

        for value in values:
            for suit in suits:
                self.append(Card(value, suit, rank))
                rank += 1

    def deal(self):
        return self.pop()




def dealCards(game):
    deck = Deck()                   
    random.shuffle(deck)            
    while deck:                     
        game.drow(deck)
    game.sortHand()             

def findPos(player):
        if player == 1:
            return [1, 2, 3, 4]
        elif player == 2:
            return [2, 3, 4, 1]
        elif player == 3:
            return [3, 4, 1, 2]
        elif player == 4:
            return [4, 1, 2, 3]
        print("Can't find player: ", player)
        return None
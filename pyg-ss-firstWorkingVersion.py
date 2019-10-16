#!/usr/bin/python3

import pygame, time, cards,random

pygame.init()
pygame.mixer.quit()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Swap and Slide')
clock = pygame.time.Clock()

black = (0,0,0)
lgreen = (20,255,95)
white = (255,255,255)
grey = (215,215,215)
red = (255,0,0)
cardWidth = 75
cardHeight = 107
columns = {1:205,2:305,3:405,4:505}
rows = {1:50,2:180,3:310,4:440}
chosenCards = []

userExit = False
easyMode = False
rulesPage = 0
gs = 'menu' #gs used for tracking gamestate "rules1"/rules2/menu/gamephase/secretwinnerscreen?:P

def readRules(rulesFile):
    with open(rulesFile,'r') as f:
        linesList=[]
        for line in f:
            linesList.append(line.strip())
        return linesList
rules1 = readRules('rules.txt')
rules2 = readRules('rules2.txt')

rulesPages=[rules1,rules2]
#cardPositions = cards.cardPos(200,50, cardWidth, cardHeight)

class Clickable:
    def __init__(self, fontsize, text, align, color, x, y, w, h):
        self.text=text
        self.fontsize=fontsize
        self.color=color
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.textSurf = pygame.font.SysFont("comicsansms", self.fontsize).render(self.text, True, self.color)
        self.textRect = self.textSurf.get_rect()
        self.tSWidth = self.textSurf.get_width()

        if align=="centre":
            self.textRect.center = ((self.x+(self.w/2)), self.y+(self.h/2))
        elif align=="left":
            self.textRect.center = ((self.x+(self.tSWidth/2)), self.y+(self.h/2))

        #check collision with this object with
        #   objName.textRect.collidepoint(x,y) OR ((x,y)) OR (event.pos)

    def blitRect(self):
        self.rect = pygame.draw.rect(gameDisplay,white,(self.x, self.y, self.w, self.h))
        self.rect2 = pygame.draw.rect(gameDisplay,grey,(self.x+3, self.y+3, self.w-6, self.h-6),1)

    def blitText(self):
        gameDisplay.blit(self.textSurf, self.textRect)

    def blitRT(self):
        self.blitRect()
        self.blitText()

    def doJob(self):
        #using global variables to track game settings, there could be a better way
        global userExit
        global easyMode
        global rulesPage
        global gs
        if self.text=="Beginner Mode":
            easyMode=True
            gs="game"
        elif self.text=="Expert Mode":
            easyMode=False
            gs="game"
        elif self.text=="Rules":
            showRules=True
            gs="rules"
        elif self.text=="Continue":
            rulesPage=1
        elif self.text=="Menu":
            rulesPage=0
            gs="menu"
            startGame()
        elif self.text=="Quit":
            userExit = True

#hoverCheck checks if the mouse position is 'colliding' with a given 'thing' 
#  in my case we're saying instances of my Clickable class are things
def hoverCheck(things, ePos):
    hoveredThings = []
    for i in things:
        if i.rect.collidepoint(ePos)==1:
            hoveredThings.append(i)
    return hoveredThings

#when a click happens on an object, this funciton tells the object to do its job obj.doJob() :)
def clickCheck(objectList):
    clickedHoveredThings=[]
    if pygame.mouse.get_pressed()[0]==1:
        clickedHoveredThings = hoverCheck(objectList,event.pos)
        if len(clickedHoveredThings)==1:
            clickedObject = clickedHoveredThings[0].doJob()
            return clickedObject
    else:
        return "No good clickcheck"

# #when a click happens on an object, this funciton tells the object to do its job obj.doJob() :)
def cardClickCheck(allCards):
    clickedHoveredThings=[]
    #if mouse1 pressed..
    if pygame.mouse.get_pressed()[0]==1:
        clickedHoveredThings = hoverCheck(allCards,event.pos)
        if len(clickedHoveredThings)==1:
            return clickedHoveredThings[0]
    else:
        pass

headingText = Clickable(45,"Swap & Slide","centre",black,350,10,150,80)
sbButton = Clickable(25,"Beginner Mode","centre",black,350,140,150,80)
seButton = Clickable(25,"Expert Mode","centre",black,350,240,150,80)
rulesButton = Clickable(25,"Rules","centre",black,350,340,150,80)
quitButton = Clickable(25,"Quit","centre",black,350,440,150,80)
continueButton = Clickable(25,"Continue","centre",black,620,240,150,80)
menuButton = Clickable(25,"Menu","centre",black,620,340,150,80)

def findCard(position): # position given is a list, format is [column,row]
    for i in newCard:
        if i.position_col == position[0] and i.position_row == position[1]:
            return i
    return 'E!'

class Card:
    def __init__(self, suit, value, position_col, position_row):
        self.suit = suit
        self.value = value
        self.position_col = position_col
        self.position_row = position_row
        self.selected = False

    def suit_name(self):
        suits_dict = {1: '♥', 2: '♦', 3: '♣', 4: '♠'} # doesn't work in PyCharm
        #suits_dict = {1: chr(3), 2: chr(4), 3: chr(5), 4: chr(6)} # doesn't work in PyCharm
        #suits_dict = {1: 'H', 2: 'D', 3: 'C', 4: 'S'}
        return suits_dict[self.suit]

    def value_name(self):
        values_dict = {1: 'A', 2: 'K', 3: 'Q', 4: 'J'}
        return values_dict[self.value]

    def __str__(self):
        return str(self.value_name()) + str(self.suit_name())

    def position(self):
        return [self.position_col, self.position_row]

    def render(self):
        self.surf = cards.cardImages[self.suit-1][self.value-1]
        self.rect = gameDisplay.blit(self.surf, (columns[self.position_col], rows[self.position_row]))

    def select(self):
        self.glowSurf = pygame.Surface((cardWidth, cardHeight))
        self.glowSurf.set_alpha(128)
        self.glowSurf.fill(red)
        self.glowRect = gameDisplay.blit(self.glowSurf, (columns[self.position_col], rows[self.position_row]))
        self.selected = True
            
    def deselect(self):
        self.selected = False

    def validate_neighbours(self, test): # this function is poop
        if test[0] > 4:
            pass
        elif test[0] < 1:
            pass
        elif test[1] > 4:
            pass
        elif test[1] < 1:
            pass
        else:
            return test

    def neighbours(self):
        temp_list = [
            self.validate_neighbours([self.position_col + 1, self.position_row]),
            self.validate_neighbours([self.position_col - 1, self.position_row]),
            self.validate_neighbours([self.position_col, self.position_row + 1]),
            self.validate_neighbours([self.position_col, self.position_row - 1]),
        ]
        new_list = []
        for i in temp_list:
            if i is not None:
                new_list.append(i)
                #new_list.append(findCard(i))
                #print(findCard(i))
        return new_list

def pcn(list):
    templist=[]
    for i in list:
        templist.append(str(i))
    return templist # for printing card names of cards in newCard list

def findCard(position): # position given is a list, format is [column,row]
    for i in newCard:
        if i.position_col == position[0] and i.position_row == position[1]:
            return i
    return 'E!'


def startGame():
    global moves
    moves = 0
    global newCard
    newCard = []
    global chosenCards
    chosenCards = []
    global dm
    if easyMode:
        dm = 'b'
    else:
        dm = 'e'
    positions = []
    for l in range(1, 5):
        for k in range(1, 5):
            positions.append([k, l])  # all positions are unique, [1,1]...[4,4]
            newCard.append(Card(suit=k, value=l, position_col=1, position_row=1))
    global finishedPosition
    finishedPosition = [[1, 1], [1, 2], [1, 3], [1, 4], [2, 1], [2, 2], [2, 3], [2, 4], [3, 1], [3, 2], [3, 3], [3, 4], [4, 1], [4, 2], [4, 3], [4, 4]]
    testPositions = [[1, 1], [1, 2], [1, 3], [1, 4], [2, 1], [2, 2], [2, 3], [2, 4], [3, 1], [3, 2], [3, 3], [3, 4], [4, 1], [4, 2], [4, 3], [4, 4]]
    #DONT THINK I NEED OR USE THIS TESTPOSITIONS LIST
    random.shuffle(positions)
    # for each card put it in a assign it's position from the (shuffed or not shuffled) list of positions
    counter = 0
    for card in newCard:
        card.position_row = positions[counter][1]
        card.position_col = positions[counter][0]
        counter += 1

def handleEvents():
    global event
    global userExit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            userExit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gs=='game':
                try:
                    clickedCard = cardClickCheck(newCard)
                    cardChoiceValidator(clickedCard)
                except:
                    pass
                try:
                    clickCheck([menuButton])
                except:
                    print("problem with cardClickCheck")

            if gs!='game':
                try:
                    clickCheck([sbButton,seButton,rulesButton,quitButton])
                except:
                    pass

def drawBoard():
    for card in newCard:
        card.render()
        # if card.selected:
            #card.select()
    for card in chosenCards:
        #pygame.draw.rect(gameDisplay, black, (x-3, y-3, cardWidth+6, cardHeight+6),1)
        pygame.draw.rect(gameDisplay, white, (columns[card.position_col]-3, rows[card.position_row]-3, cardWidth+6, cardHeight+6),2)
        card.select()

# GAME LOGIC FUNCTIONS
# GAME LOGIC FUNCTIONS
# GAME LOGIC FUNCTIONS

def usedSimilarFeature(chosenCards):
    if chosenCards[-2].suit == chosenCards[-1].suit:
        return True
    elif chosenCards[-2].value == chosenCards[-1].value:
        return True
    else:
        return False

def wouldMoveWithNeighborsUseSimilarFeature(card):
    cardNeighbours = card.neighbours()
    results = []
    for neighbour in cardNeighbours:
        results.append(usedSimilarFeature([card, findCard(neighbour)]))
        #print('does', card, 'swapping with', findCard(neighbour), "use a similar feature? ", results[-1])
    return results

def usfIsForced(card):
    results = wouldMoveWithNeighborsUseSimilarFeature(card)
    if True in results:
        if False in results:
            return False
        else:
            # print(card, 'is forced to use similar feature when SLIDing with a neighbour.')
            return 'usfForced'

    if False in results:
        if True in results:
            return False
        else:
            # print(card, "can't use a similar feature SLIDing with a neighbour")
            return 'cantUsf'
    return False

def validateSwap(chosenCards):
    if chosenCards[-2] == chosenCards[-1]:
        print('You cant swap or slide a card with itself.')
        return False
    else:
        global usf
        usf = usedSimilarFeature(chosenCards)
        return True

def validateSlide(chosenCards):
    #if validateSwap(chosenCards):
        #return False
    if chosenCards[-2] == chosenCards[-1]:
        print('You cant swap or slide a card with itself.')
        return False

    # TEST IF NOT SLIDING WITH A NEIGHBOR

    if not chosenCards[-2].position() in chosenCards[-1].neighbours():
        print(chosenCards[-1], 'is not one of', chosenCards[-2], "'s neighbors.")
        return False

    usf2 = False
    if chosenCards[-2].suit == chosenCards[-1].suit or chosenCards[-2].value == chosenCards[-1].value:
        usf2 = True
    # usf is a global, true if used sim feature in SWAP
    # usf2 is true if used sim feature in SLIDE
    # if they're both true or both false we have problems, so long as theyre different its a valid choice.
    if usf != usf2:
        return True
    else:
        return False

def swapOrSlidePhase():
    if moves % 1 == 0:
        return 'swap'
    elif moves % 1 == 0.5:
        return 'slide'
    else:
        return 'ERROR!'

def switchCards(chosenCards):
    # how this works... (a, b) = (b, a)
    # in the pygame version chosenCards always has 2 elements
    (chosenCards[0].position_row, chosenCards[1].position_row) = (chosenCards[1].position_row, chosenCards[0].position_row)
    (chosenCards[0].position_col, chosenCards[1].position_col) = (chosenCards[1].position_col, chosenCards[0].position_col)
    global moves
    moves += 0.5
    print("DEBUG: Turn: " + str(moves))
    gameFinished()

def cardChoiceValidator(clickedCard):
    global chosenCards
    
    if moves % 1 == 0: 
        #SWAPPHASE
        if len(chosenCards)==0:
            clickedCard.select()
            chosenCards.append(clickedCard)
            print("DEBUG: added {} to chosenCards".format(str(clickedCard)))
        if len(chosenCards)==1:
            if clickedCard in chosenCards:
                print("RuleError: can't swap a card with itself")
                pass
            else:
                #VALID usf etc
                clickedCard.select()
                chosenCards.append(clickedCard)
                print("DEBUG: added {} to chosenCards".format(str(clickedCard)))
    elif moves % 1 == 0.5: 
        #SLIDEPHASE
        if len(chosenCards)==2:
            if clickedCard not in chosenCards:
                print("RuleError: must choose from one of cards in swap phase")
            else:
                print("3rd cards choice complex validation check...")
                print("DEBUG: clickedcard.. neughbours, clickedcarDSS")
                print(clickedCard)
                print(clickedCard.neighbours())
                print(pcn(chosenCards))
                valid = True
                if usf and usfIsForced(clickedCard)=='usfForced':
                    print('RuleError: ', str(clickedCard), 'has no valid neighbours to swap with, choose the other card.')
                    valid = False
                    print(clickedCard.neighbours())

                if usf==False and usfIsForced(clickedCard)=='cantUsf':
                    print('RuleError: ', clickedCard, 'has no valid neighbours to swap with, choose the other card.')
                    valid = False
                    print(clickedCard.neighbours())

                print("DEBUG: find out about VALID 3rd choice...")
                print(valid)

                if valid:
                    #VALID usf etc
                    clickedCard.select()
                    chosenCards.append(clickedCard)
                    print("DEBUG: added {} to chosenCards".format(str(clickedCard)))
                else:
                    pass

                
        if len(chosenCards)==3:
            if clickedCard in chosenCards:
                pass
            else:
                clickedCard.select()
                chosenCards.append(clickedCard)
                print("DEBUG: added {} to chosenCards".format(str(clickedCard)))
        print("DEBUG: clickedCard: {} chosenCards: {} moves: {}".format(clickedCard, pcn(chosenCards), moves))
        pass

def gameFinished():
    currentPosition = []
    for card in newCard:
        currentPosition.append([card.position_row, card.position_col])
    if currentPosition == finishedPosition:
        if swapOrSlidePhase()=='swap':
            print("EASY MODE WON. game pack-up code needed.")
            gs = "menu"
            startGame()
            return True
        elif swapOrSlidePhase()=='slide' and easyMode:
            print("EXPERT MODE WON. game pack-up code needed.")
            gs = "menu"
            startGame()
            return True
    else:
        return False

def progressTurn(chosenCards):
    global gs
    if swapOrSlidePhase()=='swap':
        if len(chosenCards)==2:
            if validateSwap(chosenCards):
                switchCards(chosenCards)
            else:
                chosenCards.pop()
                return chosenCards
    if swapOrSlidePhase()=='slide':
        if len(chosenCards)==4:
            if validateSlide(chosenCards):
                switchCards(chosenCards[2:])
                #for card in chosenCards:
                    #card.deselect()
                return chosenCards
            else:
                chosenCards.pop()
                return chosenCards
    



# this doesnt require user interaction
# this just sets up everything like defining cards and 
startGame()

# MAIN GAME LOOP
while not userExit:

    handleEvents()

    #BACKGROUND, THIS COMES FIRST
    gameDisplay.fill(lgreen)

    #DECIDE WHAT TO DRAW: menu,rules,the actual game
    if gs=='game':

        def guideItemGen():
            valuesGuideA = Clickable(32,"A","left",black,160,100,1,1)
            valuesGuideA.blitText()
            valuesGuideK = Clickable(32,"K","left",black,160,230,1,1)
            valuesGuideK.blitText()
            valuesGuideQ = Clickable(32,"Q","left",black,160,360,1,1)
            valuesGuideQ.blitText()
            valuesGuideJ = Clickable(32,"J","left",black,160,490,1,1)
            valuesGuideJ.blitText()
            suitsGuideH =  Clickable(32,"H","left",black,235,30,1,1)
            suitsGuideH.blitText()
            suitsGuideD =  Clickable(32,"D","left",black,335,30,1,1)
            suitsGuideD.blitText()
            suitsGuideC =  Clickable(32,"C","left",black,435,30,1,1)
            suitsGuideC.blitText()
            suitsGuideS =  Clickable(32,"S","left",black,535,30,1,1)
            suitsGuideS.blitText()
        guideItemGen()

        drawScore = Clickable(25,"Turns: " + str(moves),"left",black,5,80,50,30)
        drawScore.blitText()
        menuButton.blitRT()

        #this blits cards and card.selected glow 
        drawBoard()

        #game and turn progression logic goes here:

        progressTurn(chosenCards)
        if len(chosenCards)==4:
            print("Removing all cards from chosenCards..")
            chosenCards = []
        # if progressTurn()==True:
        #     for card in chosenCards:
        #         card.deselect()
        #     chosenCards=[]

    elif gs=='rules':
        headingText.blitText()
        rulesLines = []
        yOffset = 0
        for line in rulesPages[rulesPage]:
            rulesLines.append(Clickable(22,line,"left",black,50,50+yOffset,150,80))
            yOffset+=25
        for i in rulesLines:
            i.blitText()
        if rulesPage==0:
            continueButton.blitRT()
            clickCheck([continueButton])
        else:
            menuButton.blitRT()
            clickCheck([menuButton])

    elif gs=='menu':
        headingText.blitText()
        sbButton.blitRT()
        seButton.blitRT()
        rulesButton.blitRT()
        quitButton.blitRT()
        #maybe should turn this into a function
        #  it only cares about left mouse button
        clickCheck([sbButton,seButton,rulesButton,quitButton])

    pygame.display.update()

    #this SLEEP is just so i can read console output without it flying past too fast...
    #maybe a sleep here can prevent picking up clicks on items which appear at the same coords
    #time.sleep(0.1)

    clock.tick(60)
    #time.sleep(0.5)

pygame.quit()
quit()




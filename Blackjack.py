import random
import names
import math
import msvcrt
def ordinal(n) : #used to write 1st, 2nd, 3rd,... of the number n
    if n%10 == 1:
        return str(n)+'st'
    elif n%10 == 2:
        return str(n)+'nd'
    elif n%10 == 3:
        return str(n)+'rd'
    else:
        return str(n)+'th'
def printMiddle(message, string='-'): #print the message at the middle of the screen
    emptySpace = 210 - len(message) - 2 #the length of a full screen is 210 characters
    if emptySpace%2 != 0:
        print(string*(int(emptySpace/2)+1), end=' ')
    else:
        print(string*int(emptySpace/2), end=' ')
    print(message, end=' ')
    print(string*int(emptySpace/2))
def botNamer(nOfBot): #return a list of random names with length of nOfBot
    botNames = []
    for i in range(nOfBot):
        name = names.get_first_name()
        while name in botNames: #filter for repeated names
            name = names.get_first_name() 
        botNames.append(name)
    return botNames
def continuePlay(string): #return a bool by asking input of yes or no
    userInput = input(string+ 'Type yes or no: ')
    userInput = userInput.lower()
    while userInput not in ['yes', 'no']:
        userInput = input('[Errors] Type yes or no: ')
        userInput = userInput.lower()
    return userInput == 'yes'
def initDeck(): #initialize a deck of 52 cards
    spades = ['S'+str(x) for x in range(2,11)]
    spades += ['SJ','SQ','SK','SA']
    hearts = ['H'+str(x) for x in range(2,11)]
    hearts += ['HJ','HQ','HK','HA']
    clubs = ['C'+str(x) for x in range(2,11)]
    clubs += ['CJ','CQ','CK','CA']
    diamonds = ['D'+str(x) for x in range(2,11)]
    diamonds += ['DJ','DQ','DK','DA']
    deck = spades + hearts + clubs + diamonds
    return deck
def initStack(nOfPlayers): #initialize a stack composing of the number of players
    stack = []
    for i in range(nOfPlayers):
        stack += initDeck()
    random.shuffle(stack)
    return stack
def symbolCard(card): #return the string of the card symbol
    symbol = {"D":"♦", "C":"♣", "H":"♥", "S":"♠"}
    return card[1:] + symbol[card[0]] #the first index codes the symbol, the rest codes the value
def nameCard(card): #return the string of the card name
    typeOfCard  = {'S':'Spades','H':'Heart', 'C':'Club', 'D':'Diamond'}
    valueOfCard = {'A':'Ace','2':'Two','3':'Three','4':'Four','5':'Five','6':'Six','7':'Seven','8':'Eight','9':'Nine','10':'Ten','J':'Jack','Q':'Queen','K':'King'}
    return valueOfCard[card[1:]] + ' of ' + typeOfCard[card[0]]
def drawCard(stack): #draw a card from the deck, return type: string
    cardDrawn = stack.pop(0)
    return cardDrawn
def draw2Cards(stack): #draw 2 cards from the deck, return type: list of strings
    cardDrawn = stack[0:2]
    del stack[0:2]
    return cardDrawn
def valueCard(card, name = None, score = None): #return value of the card
    if card[1:] == 'A': #The card is an Ace
        if name != None: #The deciding player is a bot
            return botAce(card, name, score) #pass the decision to the function below
        else: #The deciding player is a human
            value = int(input('[Ace!] Please select a value for your ' + nameCard(card) + ' (1/11): '))
            while value not in [1,11]:
                value = int(input('Enter 1 or 11: '))
            return value
    elif card[1:] in ('10','J','Q','K'):
        return 10
    return int(card[1:]) #not any special case
def botAce(card, name, score): #help the bot decide to choose 11 or 1 when it receives an Ace
    if score <= 10:
        print('[Ace!] Bot', name, 'chose 11 for its ' + nameCard(card))
        return 11
    else:
        print('[Ace!] Bot', name, 'chose 1 for its ' + nameCard(card))
        return 1
def initPlayers(botLevels): #intialize the list of players, botLevels is a dict passed by the main game function
    players = [] #initialize the return list
    nOfBot = input('[Bot] Please enter the number of bots: ')
    while not nOfBot.isdigit():
        nOfBot = input('[Errors] Please enter an interger: ')
    nOfBot = int(nOfBot)
    if nOfBot != 0:
        printMiddle('Choose your bot!') 
        print('1 - Dummy Dumb Dumb - Me do randomthing')
        print('2 - Dummy That Follows Command - Me do as you wish') #the player can choose the setting of this bot
        print('3 - Fixed player - Me play kinda okay')
        print('4 - Destroyer of humans - Me smort')
        print('--Enter 1 or 2 or 3 or 4--')
        botNames = botNamer(nOfBot)
        for i in range(0, nOfBot): 
            players.append(botNames[i])
            lvl = input('[Bot][Level] Choose your ' + ordinal(i+1) + ' bot: ') 
            while lvl not in ['1','2','3','4']:
                lvl = input('[Errors] Please enter a valid value: ')
            lvl = int(lvl)
            if lvl == 2: #ask for the setting 
                setting = input('[Bot][Setting] Choose a setting for this bot (0: Never draw, 1: Random, 2: Always draw): ')
                while setting not in ['0','1','2']:
                    setting = input('[Errors] Please enter a valid value')
                if setting == '0':
                    lvl = 0
                elif setting == '1':
                    lvl = 1
                elif setting == '2':
                    lvl = 2
            botLevels[botNames[i]] = lvl
    printMiddle('Player initialisation') 
    nOfPlayer = input('[Player] Please enter the number of players: ')
    while not str.isdigit(nOfPlayer):
        nOfPlayer = input('[Errors] Plase enter an interger: ')
    while nOfPlayer == '1' and len(players) == 0: #if there is no bot, there must be at least 2 players
        nOfPlayer = input('[Errors][Really man?] You can not play alone!: ')
    nOfPlayer = int(nOfPlayer)
    for i in range(1, nOfPlayer+1):
        currentName = input('[Player][Naming] Enter the name of the '+ordinal(i)+' player: ')
        while (currentName in players) or (currentName == ''): #filter repeated names and empty strings
            currentName = input('[Errors] Please choose a different name: ')
        players.append(currentName)
    return players
def initScores(players): #intialize the scores
    scores = {}
    for name in players:
        scores[name] = 0
    return scores
def winner(scores): #decide an unique winner with the current scores dictionary
    winningScore = -1
    for i in scores:
        if scores[i] == 21: #blackjack
            return i
        elif (scores[i] < 21) and (21 - scores[i] < 21- winningScore):
                winningScore = scores[i] #this player's score is closer to 21 than any other player
                winningKey = i
    return winningKey
def gameOver(scores, inPlay): #decide whether the game has ended or not
    if len(inPlay) == 0: #all player has stopped or gone bust
        return True
    elif 21 in scores.values(): #a player got blackjack
        return True
    elif len(inPlay) == 1 and inPlay[0] == winner(scores): #only 1 person in play left and he/she has the winning score
        return True                                        #prevent dumb people from making game with no winner
    else: #the game is not over
        return False
def firstTurn(stack, players, playerCards, inPlay, botLevels): #first turn of the game
    printMiddle('Drawing Turn')
    scores = initScores(players)
    for name in players: 
        draw = draw2Cards(stack) 
        if name not in botLevels: #the player is a human
            print('[Draw]', name, 'drew', symbolCard(draw[0]), 'and', symbolCard(draw[1]))
            for card in draw:
                scores[name] += valueCard(card)
                playerCards[name].append(card)
        else:
            print('[Draw] Bot', name, 'drew', symbolCard(draw[0]), 'and', symbolCard(draw[1]))
            for card in draw:
                scores[name] += valueCard(card, name, scores[name])
                playerCards[name].append(card)
        if scores[name] == 21: #if the player got an instant blackjack
            return {'Blackjack':name} 
        elif scores[name] > 21: #only trigger if the player is dumb enough to choose 11 for both of his/her 2 Aces
            print('You are out of this round!')
            inPlay.remove(name)
    return scores
def printInfo(turnNum, name, playerCards, scores): #used to write the current player's info at the start of the turn
    printMiddle('This is turn number - ' + str(turnNum) + ' - of: ' + name, '*')
    print('[Card]', end=' ')
    for i in playerCards[name]: #loop and print all the card of the current player
        print(symbolCard(i), end= ' ')
    print()
    print('[Total]', scores[name])
def playerTurn(stack, scores, inPlay, name, turnNum, playerCards): #a human's playing turn
    printInfo(turnNum, name, playerCards, scores)
    if continuePlay('Do you want to draw more card? '): #player decided to draw
        cardDrawn = drawCard(stack)
        scores[name] += valueCard(cardDrawn)
        playerCards[name].append(cardDrawn)
        print('You have drawn the', nameCard(cardDrawn), 'your new total is', scores[name])
        if scores[name] > 21: #bust
            print('You have lost')
            inPlay.remove(name)
        elif scores[name] == 21: #blackjack
            print('Blackjack! for player:', name)
            inPlay.clear() #immediately end the game
    else: #player decided to stop
        inPlay.remove(name)
def botNeverDraw(): #the bot that never draws
    return False
def botRandom(): #the bot that returns random bools
    return bool(random.randint(0,1))
def botAlwaysDraw(): #the bot that always draws
    return True
def botFixed(score): #the bot that chooses to draw based on its score
    if score in range(15):
        return True
    else:
        return False
def botSmart(scores, name): #the bot that is somewhat smart
    if name != winner(scores): #the bot does not have the winning score
        return True #after this the bot now has the winning score <=> the largest
    elif scores[name] <= 12:  #the bot score is too low
        return True #after this the bot has a score strictly higher than 11
    else: 
        return False
def botTurn(stack, scores, inPlay, name, turnNum, playerCards, botLevels): #a bot's playing turn
    printInfo(turnNum, name, playerCards, scores)
    if botLevels[name] == 0:
        drawDecision = botNeverDraw() #give the decision to draw the corresponding function
    elif botLevels[name] == 1:
        drawDecision = botRandom()
    elif botLevels[name] == 2:
        drawDecision = botAlwaysDraw()
    elif botLevels[name] == 3:
        drawDecision = botFixed(scores[name])
    else:
        drawDecision = botSmart(scores, name)
    if drawDecision: #bot decided to draw
        print('Bot', name, 'has decided to continue to draw')
        cardDrawn = drawCard(stack)
        scores[name] += valueCard(cardDrawn, name, scores[name]) 
        playerCards[name].append(cardDrawn)
        print('Bot', name, 'has drawn the', nameCard(cardDrawn), 'its new total is', scores[name])
        if scores[name] > 21: #bust
            print('Bot', name, 'has lost')
            inPlay.remove(name)
        elif scores[name] == 21: #blackjack
            print('Blackjack! for bot', name)
            inPlay.clear() #immediately end the game
    else: #bot decided to stop
        print('Bot', name, 'has decided to stop drawing')
        inPlay.remove(name)
def gameTurn(stack, scores, inPlay, turnNum, playerCards, botLevels): #call the function playerTurn or botTurn for all player in play
    for name in scores:
        if name in inPlay and not gameOver(scores, inPlay): 
            if name not in botLevels:
                playerTurn(stack, scores, inPlay, name, turnNum, playerCards)
            else: 
                botTurn(stack, scores, inPlay, name, turnNum, playerCards, botLevels)
def completeGame(stack, scores, inPlay, victories, playerCards, botLevels): #call the function gameTurn until the game is over
    turnNum = 1
    while not gameOver(scores, inPlay):
        printMiddle(ordinal(turnNum)+' turn')
        gameTurn(stack, scores, inPlay, turnNum, playerCards, botLevels)
        turnNum += 1
    WINNER = winner(scores) #get the winner from the function
    victories[WINNER] += 1
    printMiddle('The winner is ' + WINNER)
def botBet(bank, scores, name, lvl): #help the bots make their bets
    if lvl == 0: #the bot that never draws also never bets more than 1
        return 1
    elif lvl == 1: #the bot who draws at random, bets at random
        return random.randint(1,bank[name])
    elif lvl == 2: #the bot who always draws, always bets all his bank
        return bank[name]
    elif lvl == 3: #the bot who is fixed, always bets 20 percents of his bank no matter what
        return math.ceil(bank[name]/5)
    else: #the smart bot
        if name == winner(scores): #this bot has the winning score
            if scores[name] == 20: #this bot has a winning score and the score is really high
                bet = bank[name] * 80/100 
            elif scores[name] == 19:
                bet = bank[name] * 60/100
            elif scores[name] == 18:
                bet = bank[name] * 30/100
            elif scores[name] == 17:
                bet = bank[name] * 20/100
            else:
                bet = bank[name] * 10/100
        else: #this bot does not have the winning score
            if scores[winner(scores)] in [18,19,20]: #the winning score is really high
                bet = bank[name] * 1/100
            elif scores[winner(scores)] in [15,16,17]: #the winning score is kind of high
                bet = bank[name] * 5/100
            else:
                bet = bank[name] * 10/100
        return math.ceil(bet)
def getBets(bank, haveMoney, scores, botLevels): #initialize the bets of all the players
    printMiddle('Place your bet')
    bets = {}
    for name in haveMoney:
        if name not in botLevels:
            print('[Bets]', name + "'s turn to place his/her bet")
            print('[Bets] Your current bank is', bank[name], 'kopecs')
            amount = input('[Bets] Please enter your amount of bet: ')
            while not (amount.isdigit()) or (amount == '0') or (int(amount) > bank[name]):
                amount = input('[Errors] Please enter a positive interger smaller than your amount of kopecs: ')
            amount = int(amount)
            bets[name] = amount
            print()
        else: 
            print('[Bets] Bot', name + "'s turn to place his/her bet")
            print('[Bets] Its current bank is', bank[name], 'kopecs')
            amount = botBet(bank, scores, name, botLevels[name])
            bets[name] = amount
            print('[Bets] Bot', name, 'chose to gamble', amount, 'kopecs')
            print()
    return bets
def noBet(): #the game without bet
    #set up the game
    printMiddle('Blackjack No Bet', '+')
    botLevels = {}
    players = initPlayers(botLevels)
    victories = {}
    for name in players:
        victories[name] = 0
    #call the game until the user wants to stop
    replay = True
    while replay:
        playerCards = {}
        inPlay = []
        for name in players:
            playerCards[name] = []
            inPlay.append(name)
        stack = initStack(len(players))
        scores = firstTurn(stack, players, playerCards, inPlay, botLevels)
        if len(scores) == 1:
            printMiddle('[Straight Blackjack!!!] Winner is', scores['Blackjack'])
            victories[scores['Blackjack']] += 1 #add 1 victory to the winner's count
        else:
            completeGame(stack, scores, inPlay, victories, playerCards,botLevels)
        replay = continuePlay('[Replay] Do you want to play another game? ')
    #the game has ended
    for name in victories:
        print('Player', name, 'won', victories[name], 'games!')
    #ask whether the user wants to go to the menu or leave for good
    gotoMenu = continuePlay('Yes - Menu /// No - Exit program: ')
    if gotoMenu:
        menu()
    else:
        printMiddle('Thanks for playing!', '+')
def withBet(): #the game with bet
    #set up the game
    printMiddle('Blackjack With Bet', '+')
    botLevels = {}
    haveMoney = initPlayers(botLevels)
    bank = {}
    victories = {}
    for name in haveMoney:
        victories[name] = 0
        bank[name] = 100 #intialize the bank of each player to 100 kopecs
    #call the game until the user wants to stop
    replay = True
    while replay:
        #setup the round for all player in haveMoney list
        playerCards = {}
        inPlay = []
        for name in haveMoney: 
            playerCards[name] = []
            inPlay.append(name)
        stack = initStack(len(haveMoney)) 
        #start the round
        scores = firstTurn(stack, haveMoney, playerCards, inPlay, botLevels)
        if len(scores) == 1: #straight blackjack
            printMiddle('Straight Blackjack!!! Winner is ' + scores['Blackjack'])
            printMiddle('20 free kopecs for ' + scores['Blackjack'])
            bank[scores['Blackjack']] += 20
            victories[scores['Blackjack']] += 1 #add 1 victory to the winner's count
        else: 
            bets = getBets(bank, haveMoney, scores, botLevels)
            completeGame(stack, scores, inPlay, victories, playerCards, botLevels)
            WINNER = winner(scores)
            #redistribute money
            for name in haveMoney:
                if name != WINNER:
                    bank[name] -= bets[name] #remove the amount of bet from their bank
                else:
                    bank[name] += bets[name]*2 #give the winner 2 times his/her bet
            print('[Bank] The current bank is:', bank)
            #update haveMoney list
            for name in bets: #loop through the bets dict to avoid bug
                if bank[name] == 0: 
                    print('[Removed] Player', name, 'has no money left!')
                    haveMoney.remove(name) #remove the player who has no money left
        #the round has ended
        if len(haveMoney) != 1: 
            replay = continuePlay('[Replay] Do you want to play another game? ') #offer a replay
        else:
            printMiddle('[Congratulation] The last standing player is ' + haveMoney[0]) #only 1 person left
            replay = False
    #the game has ended
    for name in victories:
        print('Player', name, 'won', victories[name], 'games!')
    #ask whether the user wants to go to the menu or leave for good
    gotoMenu = continuePlay('Yes - Menu /// No - Exit program: ')
    if gotoMenu:
        menu()
    else:
        printMiddle('Thanks for playing!', '+')
def menu(): #the menu of the game
    printMiddle('Blackjack', '+')
    print('[Gamemode] 1 - Blackjack No Bet')
    print('[Gamemode] 2 - Blackjack With Bet')
    game = input('[Gamemode] Please choose a gamemode (1/2): ')
    while game not in ['1','2']:
        game = input('[Errors] Please enter a valid value: ')
    if game == '1':
        noBet()
    else:
        withBet()    
    msvcrt.getch() #prevent the program from closing immediately after it ends
menu()

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
blackjack = simplegui.load_image("http://s1.postimg.org/l5i83ycm7/blackjack_fondo.jpg")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []        

    def __str__(self):
        ans = ""
        for i in range(len(self.hand)):
            ans += self.hand[i].get_suit() + self.hand[i].get_rank() + " "
        return "hand contains " + ans              

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        value = 0
        aces = 0
        for i in range(len(self.hand)):
            value += VALUES[self.hand[i].get_rank()]
            if self.hand[i].get_rank() == 'A':
                aces += 1
        if 0 < aces < 3 and value + 10 < 22:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand)):
            pos[0] = 50 + i*75
            self.hand[i].draw(canvas, pos) 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(s, r) for r in RANKS for s in SUITS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        ans = ""
        for i in range(len(self.deck)):
            ans += self.deck[i].get_suit() + self.deck[i].get_rank() + " "
        return "Deck contains " + ans 

def win():
    global outcome, in_play, score    
    outcome = "You win! New deal?"
    in_play = False
    score += 1
    
def loose():
    global outcome, in_play, score
    outcome = "You loose. New deal?"
    in_play = False
    score += -1
    
#define event handlers for buttons
def deal():
    global outcome, in_play, myDeck, playerHand, dealerHand
    if in_play:
        loose()
    else:
        myDeck = Deck()
        playerHand = Hand()
        dealerHand = Hand()
        myDeck.shuffle()
        for i in range(2):
            playerHand.add_card(myDeck.deal_card())
            dealerHand.add_card(myDeck.deal_card())
        in_play = True
        outcome = "Hit or stand?"

def hit():
    if in_play:
        playerHand.add_card(myDeck.deal_card())
        if playerHand.get_value() > 21:
            loose()
    
def stand():
    if in_play:
        if playerHand.get_value() > 21:
            loose()
        else:
            while dealerHand.get_value() < 17:
                dealerHand.add_card(myDeck.deal_card())
        if dealerHand.get_value() > 21:
            win()
        elif playerHand.get_value() <= dealerHand.get_value():
            loose()
        else:
            win()

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_image(blackjack, [320, 225], [640, 450], [320, 225], [640, 450] )
    playerHand.draw(canvas, [40, 275])
    dealerHand.draw(canvas, [40, 75])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [86, 123], CARD_BACK_SIZE)
    canvas.draw_text(outcome, [48, 51], 30, "Black")
    canvas.draw_text(outcome, [50, 50], 30, "Yellow")
    canvas.draw_text("Score: "+str(score), [500, 50], 30, "Yellow")

# initialization frame
frame = simplegui.create_frame("Blackjack", 640, 450)
#frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
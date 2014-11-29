# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
TABLE_SIZE = [600, 600]


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

    def draw(self, canvas, pos, draw_back):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        
        if draw_back:
            canvas.draw_image(
                              card_back,
                              CARD_BACK_CENTER,
                              CARD_BACK_SIZE,
                              [pos[0] + CARD_CENTER[0],
                               pos[1] + CARD_CENTER[1]],
                              CARD_SIZE)
        else:
            canvas.draw_image(
                              card_images,
                              card_loc,
                              CARD_SIZE,
                              [pos[0] + CARD_CENTER[0],
                               pos[1] + CARD_CENTER[1]],
                              CARD_SIZE)


class Hand:
    """ Dealer's or Player's hand to deal with cards """
    def __init__(self):
        self.card_list = []

    def __str__(self):
        return 'Hand contains ' + ' '.join([str(card) for card in self.card_list])

    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        hand_value = 0
        has_ace = False
        
        for card in self.card_list:
            hand_value += VALUES[card.rank]
            
            if card.get_rank() == 'A':
                has_ace = True
        
        if has_ace and hand_value + 10 <= 21:
            hand_value += 10
        
        return hand_value
        
    def draw(self, canvas, pos, hide_first):
       
        for card in self.card_list:
            if self.card_list.index(card) == 0 and hide_first:
                draw_back = True
            else:
                draw_back = False
                
            card.draw(canvas,
                      [pos[0] + self.card_list.index(card) * CARD_SIZE[0],
                      pos[1]],
                      draw_back)


class Deck:
    """ A deck of cards """
    def __init__(self):
        self.card_list = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.card_list.append(Card(suit, rank))

    def __str__(self):
        return 'Deck contains ' + ' '.join([str(card) for card in self.card_list])

    def shuffle(self):
        random.shuffle(self.card_list)

    def deal_card(self):
        return self.card_list.pop()


def deal():
    """ Deal button handler """
    global deck, dealer_hand, player_hand, outcome, outcome_expl, in_play, score
    
    outcome = "Hit or stand?"
    outcome_expl = ""
    if in_play:
        outcome = "You have busted"
        outcome_expl = "You've asked to deal in the middle of the round."
        score -= 1
    else:
        in_play = True
    
    deck = Deck()
    deck.shuffle()
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())


def hit():
    """ Hit button handler """
    global in_play, score, outcome, outcome_expl
    
    if in_play:
        player_hand.add_card(deck.deal_card())
    
        if player_hand.get_value() > 21:
            score -= 1
            outcome = "You have busted, new deal?"
            outcome_expl = "Player's got " + str(player_hand.get_value())
            in_play = False


def stand():
    """ Stand button handler """
    global in_play, score, outcome, outcome_expl
    
    if in_play:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(deck.deal_card())
        
        if (dealer_hand.get_value() <= 21 and
            dealer_hand.get_value() >= player_hand.get_value()):
            score -= 1
            outcome = "Dealer's won, new deal?"
        else:
            score += 1
            outcome = "Player's won, new deal?"
        
        in_play = False
        outcome_expl = ("Dealer's " + str(dealer_hand.get_value()) +
                        " vs Player's " + str(player_hand.get_value()))


def draw(canvas):
    """ Draw handler """
    
    # Player's side in a slightly different background
    canvas.draw_polygon(
                        [(0, TABLE_SIZE[1] // 10 * 6),
                         (TABLE_SIZE[0], TABLE_SIZE[1] // 10 * 6),
                         (TABLE_SIZE[0], TABLE_SIZE[1]),
                         (0, TABLE_SIZE[1])],
                        1,
                        "#406B02",
                        "#406B02")
    
    dealer_hand.draw(
                     canvas,
                     [TABLE_SIZE[0] // 2 -
                      len(dealer_hand.card_list) * CARD_SIZE[0] // 2,
                      TABLE_SIZE[1] // 10 * 4],
                     in_play)
    
    player_hand.draw(
                     canvas,
                     [TABLE_SIZE[0] // 2 -
                      len(player_hand.card_list) * CARD_SIZE[0] // 2,
                      TABLE_SIZE[1] // 10 * 7],
                     False)
    
    title = "Blackjack"
    title_width = frame.get_canvas_textwidth(title, 50, 'sans-serif')
    canvas.draw_text(
                     title,
                     [TABLE_SIZE[0] // 2 - title_width // 2,
                     TABLE_SIZE[1] // 10],
                     50,
                     '#73C002',
                     'sans-serif') 
    
    score_txt = "Score: " + str(score)
    score_txt_width = frame.get_canvas_textwidth(score_txt, 30, 'sans-serif')
    canvas.draw_text(
                     score_txt,
                     [TABLE_SIZE[0] // 2 - score_txt_width // 2,
                     TABLE_SIZE[1] // 10 * 2],
                     30,
                     '#FBFFED',
                     'sans-serif') 
    
    outcome_width = frame.get_canvas_textwidth(outcome, 30, 'sans-serif')
    canvas.draw_text(
                     outcome,
                     [TABLE_SIZE[0] // 2 - outcome_width // 2,
                      TABLE_SIZE[1] // 10 * 3],
                     30,
                     '#FD0100',
                     'sans-serif')
    
    outcome_expl_width = frame.get_canvas_textwidth(
                                                    outcome_expl,
                                                    10,
                                                    'sans-serif')
    canvas.draw_text(
                     outcome_expl,
                     [TABLE_SIZE[0] // 2 - outcome_expl_width // 2,
                      TABLE_SIZE[1] // 10 * 3 + 20],
                     10,
                     '#73C002',
                     'sans-serif')


# Initialize
frame = simplegui.create_frame("Blackjack", TABLE_SIZE[0], TABLE_SIZE[1])
frame.set_canvas_background('#264000')
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

score = 0
in_play = False
deal()
frame.start()
# Implementation of card game - Memory

import simplegui
import random


CARD_BACK_COLOR = "#588F27"
CARD_BORDER_COLOR = "#A9CF54"
CARD_FACE_COLOR = "#CAFCD8"
CARD_SIZE = (50, 100)
CARD_TEXT_COLOR = "#04BFBF"
CARD_TEXT_OFFSET = (-7, 7)


def new_game():
    """
    Sets everything for a new game. Everything is implemented
    according to the specification/suggestions.
    """
    global deck, exposed, state, guess_1, guess_2, turn_num
    
    guess_1 = None
    guess_2 = None
    
    state = 0
    turn_num = 0
    label.set_text("Turns = " + str(turn_num))
    
    deck = range(8) * 2
    random.shuffle(deck)

    exposed = [False] * len(deck)
    
    # Uncomment the line below to make testing easier:
    # print deck


def mouseclick(pos):
    """ Mouse click event handler, handles all the game logics. """
    global state, guess_1, guess_2, turn_num
    
    card_x_borders = [0, CARD_SIZE[0]] # left and right card border
   
    for idx, card in enumerate(deck):
        if (pos[0] >= card_x_borders[0] and
            pos[0] < card_x_borders[1] and
            exposed[idx] == False):
            
            exposed[idx] = True
            
            if state == 0:
                state = 1
            elif state == 1: # 2nd card is flipped
                state = 2
                turn_num += 1
                label.set_text("Turns = " + str(turn_num))
            else:
                state = 1
        
            if guess_1 is not None and guess_2 is not None:
                
                if deck[guess_1] == deck[guess_2]:
                    guess_1 = None
                    guess_2 = None
                
                elif state == 1:
                    exposed[guess_1] = False
                    exposed[guess_2] = False
            
            if state == 1:
                guess_1 = idx
                guess_2 = None
            elif state == 2:
                guess_2 = idx

        card_x_borders[0] += CARD_SIZE[0]
        card_x_borders[1] += CARD_SIZE[0]


def draw(canvas):
    """
    Draw handler, draws 16 stylized cards and imitates
    their flipping.
    """
    pos_card_right = CARD_SIZE[0]
    
    for idx, card in enumerate(deck):
        if exposed[idx]:
            card_back_color = CARD_FACE_COLOR
            card_text_color = CARD_TEXT_COLOR
        else:
            card_back_color = CARD_BACK_COLOR
            card_text_color = CARD_BACK_COLOR
        
        canvas.draw_polygon([(pos_card_right - CARD_SIZE[0], 0),
                            (pos_card_right, 0),
                            (pos_card_right, CARD_SIZE[1]),
                            (pos_card_right - CARD_SIZE[0], CARD_SIZE[1])],
                            2, CARD_BORDER_COLOR, card_back_color)
        canvas.draw_text(str(card),
                         (pos_card_right - CARD_SIZE[0] // 2 + CARD_TEXT_OFFSET[0],
                          CARD_SIZE[1] // 2 + CARD_TEXT_OFFSET[1]),
                         30, card_text_color, "serif")
        
        pos_card_right += CARD_SIZE[0]


frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()
# "Guess the number" mini-project
import simplegui
import math
import random
import re


def new_game():
    """
    Starts a new game by generating a new number to guess,
    and a number of guesses to do that.
    """
    
    global secret_number, num_of_guesses
    
    print "\nNew game started!"
    print "You should guess a number from a [0, " + str(high) + ") range."
    
    if high > 0:
        secret_number = random.randrange(0, high)
        num_of_guesses = int(math.ceil(math.log(high + 1, 2)))

    else:
        print "Wrong range upper >" + str(stop) + "< bound"


def range100():
    """
    Event handler to change the range to [0,100) and
    start a new game.
    """
    
    global high
    high = 100
    
    new_game()


def range1000():
    """
    Event handler to change the range to [0,1000) and
    start a new game.
    """    
    global high
    high = 1000
    
    new_game()

    
def input_guess(guess):
    """
    Event handler to check if a human player's guess is correct.
    """
    
    global num_of_guesses

    if num_of_guesses > 0:
        
        guess = guess.strip() # trims whitespace
        print "Guess was " + guess
        
        # Checks if the input is in digits only
        if re.match(r'^[0-9]+$', guess):
            guess = int(guess)

            if guess > secret_number:
                hint = "Lower, "
            elif guess == secret_number:
                hint = "Correct, "
                num_of_guesses = 0
            elif guess < secret_number:
                hint = "Higher, "
            else:
                hint = "How is that possible, "
            
        else:
            guess = None
            print "Sorry, it's not a number"
            hint = ""
            
        num_of_guesses -= 1
        
        if num_of_guesses > 0:
            print hint + "You have " + str(num_of_guesses),
            print "guesses remaining"
        else:
            print hint + "game is over."
            new_game()
            
    else:
        new_game()


# Start up
frame = simplegui.create_frame("Guess the number", 200, 200)
frame.add_button("Range: 0 - 100", range100, 150)
frame.add_button("Range: 0 - 1000", range1000, 150)
frame.add_input("Guess", input_guess, 200)
frame.start()

high = 100
new_game()

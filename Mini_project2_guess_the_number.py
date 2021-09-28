# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

#We define a global variable for the range lenght, by default is set to 100
n = 100

# helper function to start and restart the game
def new_game():
    global secret_number
    global remaining_guesses
    secret_number = random.randrange(0, n)
    if n == 100:
        remaining_guesses = 7
    else:
        remaining_guesses = 10
    print "\nNew game ", "[0,"+str(n)+")"

# define event handlers for control panel
def range100():
    """ button that changes the range to [0,100) and starts a new game """
    global n
    n = 100
    new_game()

def range1000():
    """ button that changes the range to [0,1000) and starts a new game """     
    global n
    n = 1000
    new_game()
    
def input_guess(guess):
    """ enter a number that is compared to secret number """
    global remaining_guesses
    remaining_guesses += -1
    print "Your guess was ", guess
    if int(guess) > secret_number:
        print "Lower"
        print "Remaining guesses",remaining_guesses
    elif int(guess) < secret_number:
        print "Higher"
        print "Remaining guesses",remaining_guesses
    else:
        print "Correct!"
        new_game()
    if remaining_guesses == 0:
        print "Game over!"
        new_game()
             
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_input("Guess", input_guess, 100) 
frame.add_button("Range [0,100)", range100, 150)
frame.add_button("Range [0,1000)", range1000, 150)

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric

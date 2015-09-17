import random
import math
import simplegui

# initialize global variables used in your code

secret_number=0
remaining_guesses = 0

def range100():
    global secret_number, remaining_guesses
    secret_number = random.randrange(100)
    remaining_guesses = 7
    print ""
    print "New Game! Range is from 0 to 100"
    print "Number of remaining guesses is " + str(remaining_guesses)

def range1000():
    global secret_number, remaining_guesses
    secret_number = random.randrange(1000)
    remaining_guesses = 10
    print ""
    print "New Game! Range is from 0 to 1000"
    print "Number of remaining guesses is " + str(remaining_guesses)

    
def input_guess(guess):
    global secret_number, remaining_guesses
    try:     
        print ""
        print "Guess was " + guess
        remaining_guesses -= 1
        print "Number of remaining guesses is " + str(remaining_guesses)
        if int(guess)<secret_number:
            print "Higher!"
        elif int(guess)>secret_number:
            print "Lower!"
        else:
            print "Correct!"
            range100()
        if remaining_guesses == 0:
            print ""
            print "Game Over! You ran out of guesses. The number was ", secret_number
            range100()
    except:
        print "Error! You must write a number!"
    
    
# create frame

frame = simplegui.create_frame('Guess The Number', 300, 300)

# register event handlers for control elements

frame.add_button('Range [0..100]', range100, 100)
frame.add_button('Range [0..1000]', range1000, 100)
frame.add_input('Enter a guess', input_guess, 200)

# call new_game and start frame

range100()

frame.start()


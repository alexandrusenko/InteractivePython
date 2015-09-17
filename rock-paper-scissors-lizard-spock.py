# Rock-paper-scissors-lizard-Spock template

import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return 404



def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Error"

    

def rpsls(player_choice): 
        print ""
        player_number = name_to_number(player_choice)
        if player_number!=404:
            print "Player chooses " + player_choice
            comp_number = random.randrange(0,5)
            computer_choise = number_to_name(comp_number)
            print "Computer chooses " + computer_choise
            diff = (player_number-comp_number)%5
            if diff == 0:
                print "Player and computer tie!"
            elif diff == 1 or diff == 2:
                print "Player wins!"
            elif diff > 2:
                print "Computer wins!"
        else:
            print "Error!"
                    
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric



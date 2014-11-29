import random


def name_to_number(name):
    """Converts a named choice into a number."""
    
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
        print "Wrong name>" + str(name) + "<"
        return None


def number_to_name(number):
    """Converts a number into a named choice."""
    
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
        print "Wrong number>" + str(number) + "<"
        return None
    

def rpsls(player_choice): 
    """Rock-paper-scissors-lizard-Spock"""
    
    print "\nPlayer chooses " + player_choice
    player_number = name_to_number(player_choice)

    comp_number = random.randrange(0, 5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses " + comp_choice

    choice_diff = (comp_number - player_number) % 5
    if choice_diff == 0:
        print "Player and computer tie!"
    elif choice_diff in [1, 2]:
        print "Computer wins!"
    elif choice_diff in [3, 4]:
        print "Player wins!"
    else:
        print "Unhandled situation, choice_diff>" + str(choice_diff) + "<"



rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

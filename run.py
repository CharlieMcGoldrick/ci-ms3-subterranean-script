import random


def roll_stats():
    """
    Rolls stats for a new D&D character. The six main attributes of D&D:
    Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma,
    are determined by rolling 4 six-sided dice (d6) and discarding the lowest
    roll, then adding up the remaining three.
    """
    attributes = ['Strength', 'Dexterity', 'Constitution', 'Intelligence',
                  'Wisdom', 'Charisma']
    attribute_values = {}

    for attribute in attributes:
        rolls = [random.randint(1, 6) for _ in range(4)]
        rolls.remove(min(rolls))  # Remove the lowest roll
        attribute_values[attribute] = sum(rolls)

    return attribute_values


def enter_name():
    """
    Prompts the user for a valid player name. A valid name only contains
    alphabetic characters and is not longer than 20 characters. If a valid
    name is entered, this function calls `play_game(player_name)`. If 'exit'
    is entered, the function returns and the game is terminated.
    """
    while True:
        player_name = input("\nWhat does it say?\n")
        if player_name.lower() == 'exit':
            return
        try:
            if not player_name.isalpha() or player_name.lower() == 'exit':
                raise ValueError("These appear to be letters, not numbers or"
                                 "symbols, on your arm.")
            elif len(player_name) > 20:
                raise ValueError("The etching on your arm can't be that long.")
            print(f"\n{player_name}, that appears to be my name...")
            print("I suppose that's as good a start as any.")
            break  # Correct name breaks the inner while loop
        except ValueError as e:
            print(str(e))
   
    # After the player enters their name, introduce the stat rolling
    print("\nAs you navigate the darkness, your competency comes flooding back"
          "...")
   
    stats = roll_stats()
 
    for stat, value in stats.items():
        print(f"\nYour {stat} is {value}")

    # Return from the function once the stats are rolled
    return


def start_game():
    """
    Initiates the game by prompting the user to enter 'enter' or 'Enter'.
    If a different input is received, a ValueError is raised and the prompt
    is shown again. If 'exit' is entered, a farewell message is printed and
    the game is terminated. If 'enter' or 'Enter' is entered, a game
    introduction message is printed and the `enter_name()` function is called.
    """
    while True:
        user_input = input("").lower()
        if user_input.lower() == 'exit':
            print()
            print("\nMaybe it's all just a dream...")
            return
        try:
            if user_input != 'enter':
                raise ValueError("Are you lost? Type 'enter' or 'Enter'.")
            else:
                print()
                print("Awakening in a room, a sense of déjà vu strikes you...")
                print("Have you visited this place before?")
                print("A shroud of darkness wraps the space, its cold grip")
                print("only punctuated by the echoing drip of water against")
                print("stone walls. In the feeble light, an inscription comes")
                print("to view on your arm, etched crudely by an apparent")
                print("blade.")
                #  Call enter_name function
                enter_name()
                #  Correct input breaks the while loop and the game starts
                break
        except ValueError as e:
            print(str(e))


while True:
    print("        __       _     _                                          ")
    print("       / _\_   _| |__ | |_ ___ _ __ _ __ ___  __ _ _ __           ")
    print("       \ \| | | | '_ \| __/ _ \ '__| '__/ _ \/ _` | '_ \          ")
    print("       _\ \ |_| | |_) | ||  __/ |  | | |  __/ (_| | | | |         ")
    print("       \__/\__,_|_.__/ \__\___|_|  |_|  \___|\__,_|_| |_|         ")
    print("                   __           _       _                         ")
    print("                  / _\ ___ _ __(_)_ __ | |_                       ")
    print("                  \ \ / __| '__| | '_ \| __|                      ")
    print("                  _\ \ (__| |  | | |_) | |_                       ")
    print("                  \__/\___|_|  |_| .__/ \__|                      ")
    print("                                 |_|                              ")
    print("                                                                  ")
    print("         Welcome to the depths of 'Subterranean Script'!          ")
    print("       This is a text-based, choice-driven adventure game.        ")
    print("         Navigate through the all-encompassing darkness           ")
    print("        where every door opens a new path, a new destiny.         ")
    print("                                                                  ")
    print("     Note: Whisper 'help' anytime to conjure the command list     ")
    print("                                                                  ")
    print("     Ready to step into the unknown? Type 'Enter' if you dare     ")

    start_game()
    
    # Break the outer loop if the game has started or 'exit' was entered
    break
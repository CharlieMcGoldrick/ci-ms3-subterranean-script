import random
from colorama import Fore, Back, Style, init
#init colorama
init()

import game_states
import weapons
import utilities

# Global dictionary to hold the current character's stats.
character = {
    "name": None,
    "stats": {
        "Strength": 0,
        "Dexterity": 0,
        "Constitution": 0,
        "Intelligence": 0,
        "Wisdom": 0,
        "Charisma": 0,
        "Weapon": {
            "name": "Fists",
            "description": "Your own bare hands."
        }
    }
}

def print_help(current_state, previous_state):
    """
    Prints a help message describing the available commands based on the
    current state and previous state of the game.

    This function provides contextual guidance to the player, offering
    different commands and information depending on the current state of
    the game. The help message may include basic commands like
    'Return' and 'Exit', and specific guidance based on the player's current
    location or situation within the game.

    :param current_state: The current state of the game, used to determine
           what specific guidance should be provided.
    :param previous_state: The previous state of the game, also used to
           provide context-specific help.
    """
    print("\nYou whispered for help... The shadows respond:")
    print("'Return': Resume your previous action.")
    print("'Exit' : Wake from the dream and return to reality.")
    if previous_state == game_states.STATE_NAME:
        print("\nType your name to continue, a name is more than just an"
              "identity here...")
    # ... More states will go here!


def handle_universal_commands(user_input, current_state, previous_state):
    """
    Handles universal commands that are available in multiple states of the
    game.

    :param user_input: The input provided by the user.
    :param current_state: The current state of the game.
    :param previous_state: The previous state of the game.

    :return: The next game state if a universal command is recognized and
             handled, or None if the user input does not correspond to a
             universal command. The 'stats' command is only recognized if
             both the name and stats attributes of the character are
             initialized.
    """
    if user_input == 'help':
        print_help(current_state, previous_state)
        return game_states.STATE_HELP
    elif user_input == 'exit':
        print("\nMaybe it's all just a dream...")
        exit(0)
    elif (user_input == 'stats' and character['name']
          is not None and character['stats'] is not None):
        print_stats()
        return previous_state
    return None


def print_stats():
    """
    Prints the current character's stats in a formatted manner.

    This function retrieves the character's name and stats from the global
    'character' dictionary, and prints them line by line, aligning the
    stat names to the left with a specific width for a clean presentation.

    :note: Assumes that the 'character' dictionary contains 'name' and
           'stats' keys with valid values.
    """
    print(f"{character['name']}, your current stats are:")
    for stat, value in character["stats"].items():
        if stat != 'Weapon':
            print(f"Your {stat:<15} is {value}")

    weapon_details = character["stats"]["Weapon"]

    if weapon_details['name'] == "Fists":
        print("\nYou have no weapon... only your fists.")
    else:
        print(f"\nYou are wielding a {weapon_details['name']}")
        print(weapon_details['description'])


def roll_stats():
    """
    Rolls stats for a new character using the 4d6 drop lowest method.

    This function rolls four 6-sided dice for each attribute, removes the
    lowest roll, and sums the remaining three to generate the value for
    each attribute. The attributes being rolled for are: Strength,
    Dexterity, Constitution, Intelligence, Wisdom, and Charisma.

    :return: A dictionary containing the rolled values for each attribute.
    """
    attributes = ['Strength', 'Dexterity', 'Constitution', 'Intelligence',
                  'Wisdom', 'Charisma']
    attribute_values = {}
    for attribute in attributes:
        rolls = [random.randint(1, 6) for _ in range(4)]
        rolls.remove(min(rolls))  # Remove the lowest roll
        attribute_values[attribute] = sum(rolls)
    return attribute_values
    

def handle_start_state(user_input):
    """
    Handles the starting state of the game where the player is prompted to
    enter the game.

    :param user_input: The input provided by the user. It must be the string
                       'enter'.

    :return: The next game state, which is the state for entering the
             character's name, if the user types 'enter'.

    :raises ValueError: If the user input is not 'enter', an error message
                        is raised to prompt the player to type 'Enter'.
    """
    if user_input != 'enter':
        raise ValueError("\nThe shadows were quite explicit. Type 'Enter'.")
    print("\nAwakening in a room, a sense of déjà vu strikes you...")
    print("Have you visited this place before?")
    print("A shroud of darkness wraps the space, its cold grip")
    print("only punctuated by the echoing drip of " + Fore.WHITE +
          Back.BLUE + "water" + Fore.RESET + Back.RESET + " against")
    print("stone walls. In the feeble light, an inscription comes")
    print("to view on your arm, " + Fore.WHITE +
          Back.RED + "etched" + Fore.RESET + Back.RESET + 
          " crudely by an apparent blade.")
    return game_states.STATE_NAME


def handle_name_state(user_input):
    """
    Handles the state where the player is prompted to enter their character's
    name.

    :param user_input: The input provided by the user. It must be a valid name
                       consisting of alphabetic characters, not exceeding 20
                       characters.

    :return: The next game state, which is the state following the entry of,
              the name if the user provides a valid name.

    :raises ValueError: If the user input contains numbers or symbols, is
                        empty, or exceeds 20 characters, an error message
                        is raised to guide the player to input a valid name.
    """
    if not user_input.isalpha() or user_input.lower() == 'exit':
        raise ValueError("\nThese appear to be letters, not numbers"
                         " or symbols, on your arm.")
    elif len(user_input) > 20:
        raise ValueError("\nThe etching on your arm can't be that"
                         " long.")
    character["name"] = user_input
    print(f"\n{user_input}, that appears to be my name...")
    print("I suppose that's as good a start as any.\n")

    # Roll the stats here
    rolled_stats = roll_stats()
    for key, value in rolled_stats.items():
        character["stats"][key] = value
    # Print the stats here
    print_stats()

    # Flavour Text for next function
    if 'weapon_picked' not in character:
        weapon_choice = random.choice(weapons.WEAPONS_FIRST_LAYER)
        character['weapon'] = weapon_choice
        print(f"\nA strange chill fills the room, and your eyes are drawn to a"
              " faint glow.")
        print(f"Upon closer inspection, it's a {weapon_choice['name']} lying"
              " at your feet.")
        print(weapon_choice['description'])
    return game_states.STATE_PICK_UP_WEAPON_FIRST_LAYER


def handle_pick_up_weapon_first_layer(user_input):
    weapon_choice = random.choice(weapons.WEAPONS_FIRST_LAYER)
    if user_input == 'pick up':
        print("\nYour hand trembles as you approach the object, memories"
              "and emotions swirling within you.")
        print("The air feels thick, and a voice in the back of your mind"
              "urges you to make a choice.")
        print(f"\nYou have picked up the {weapon_choice['name']}!")
        character['stats']['Weapon'] = weapon_choice
        for stat, change in weapon_choice["stat_changes"].items():
            character["stats"][stat] += change
        print_stats()
        # Mark the weapon as picked up
        character['weapon_picked'] = True
        return game_states.STATE_DIRECTION_DECISION_FIRST_LAYER
    else:
        raise ValueError("The shadows whisper: 'Make a choice.'")
    return game_states.STATE_PICK_UP_WEAPON_FIRST_LAYER


def handle_direction_decision_first_layer(user_input):
    if 'weapon_picked' in character:
        print("\nTwo doors, faintly illuminated by candlelight, beckon from"
              " the darkness.")
        print("A mysterious force urges you to make a choice.")

        if user_input == 'left':
            print("You chose the left door...")
            return game_states.STATE_LEFT_ROOM
        elif user_input == 'right':
            print("You chose the right door...")
            return game_states.STATE_RIGHT_ROOM
        else:
            raise ValueError("The shadows whisper: 'Make a choice.'")

    return game_states.STATE_DIRECTION_DECISION_FIRST_LAYER


def main_game_loop():
    """
    Manages the main gameplay loop, orchestrating the progression between
    different game states.

    This function maintains a loop that keeps the game running, managing
    transitions between different states according to user inputs and
    current game conditions. It prompts the player for inputs based
    on the current state and manages how the game responds.

    The game states handled by this loop include:
        - Help state (providing help and guidance)
        - Stats state (displaying character's statistics)
        - Start state (initial entry into the game)
        - Name state (naming the character)

    Exceptions such as ValueError will be caught and handled, allowing for
    the game loop to continue.

    :note: The user can type 'return' in specific states to go back to a
           previous state.
    :note: The function utilizes helper functions like handle_start_state,
           handle_name_state, etc., to manage specific states.
    """
    current_state = game_states.STATE_START
    # Store the previous state to return to
    previous_state = None
    while True:
        if current_state == game_states.STATE_HELP:
            prompt = "What do you demand of the shadows? Type 'return' to go"
            "back."
        elif current_state == game_states.STATE_STATS:
            prompt = "If you've finished looking at yourself, type 'return'"
        elif current_state == game_states.STATE_START:
            prompt = ("\nReady to step into the unknown? Type 'Enter' if you"
            " dare." + Fore.RESET)
        elif current_state == game_states.STATE_NAME:
            prompt = "\nWhat does it say on your arm?"
        elif current_state == game_states.STATE_PICK_UP_WEAPON_FIRST_LAYER:
            prompt = "\nDo you 'Pick Up' the weapon?"
        elif current_state == game_states.STATE_DIRECTION_DECISION_FIRST_LAYER:
            prompt = "Do you go 'left', or go 'right'?\n"
        else:
            prompt = "What do you do?"

        try:
            user_input = input(f"{prompt}\n").lower()
            print(f"\n" + utilities.return_divider())

            # Check for universal commands
            new_state = handle_universal_commands(user_input, current_state,
                                                  previous_state)
            if new_state is not None:
                if current_state != new_state:
                    previous_state = current_state
                current_state = new_state
                continue

            if (user_input == 'return' and current_state in
               (game_states.STATE_HELP, game_states.STATE_STATS)):
                # return to the previous state or a default state
                current_state = previous_state or game_states.STATE_NAME
                continue

            # Handle State Inputs
            if current_state == game_states.STATE_START:
                current_state = handle_start_state(user_input)
            elif current_state == game_states.STATE_NAME:
                current_state = handle_name_state(user_input)
            elif current_state == game_states.STATE_PICK_UP_WEAPON_FIRST_LAYER:
                current_state = handle_pick_up_weapon_first_layer(user_input)
            elif current_state == \
                    game_states.STATE_DIRECTION_DECISION_FIRST_LAYER:
                current_state = \
                    handle_direction_decision_first_layer(user_input)

        except ValueError as e:
            print(f"{e}")
            continue
        # Transition to the next state...
        # current_state = STATE_NEXT


def start_game():
    """
    Initiates the text-based adventure game 'Subterranean Script'.

    This function displays the game's title, a brief introduction, and a
    welcome message to guide players into the mysterious and all-encompassing
    darkness of the game world.

    It then calls the main_game_loop() function to start the gameplay.

    :note: Whisper 'help' anytime in the game to view a list of commands.
    """
    lines = [
        "                                                                  ",
        "                                                                  ",
        "                                                                  ",
        " __       _     _                                                 ",
        "/ _\\_   _| |__ | |_ ___ _ __ _ __ ___  __ _ _ __                 ",
        "\\ \\| | | | '_ \\| __/ _ \\ '__| '__/ _ \\/ _` | '_ \\           ",
        "_\\ \\ |_| | |_) | ||  __/ |  | | |  __/ (_| | | | |              ",
        "\\__/\\__,_|_.__/ \\__\\___|_|  |_|  \\___|\\__,_|_| |_|          ",
        " __           _       _                                           ",
        "/ _\\ ___ _ __(_)_ __ | |_                                        ",
        "\\ \\ / __| '__| | '_ \\| __|                                     ",
        "_\\ \\ (__| |  | | |_) | |_                                       ",
        "\\__/\\___|_|  |_| .__/ \\__|                                     ",
        "               |_|                                                ",
        "                                                                  ",
        "Welcome to the depths of 'Subterranean Script'!                   ",
        "This is a text-based, choice-driven adventure game.               ",
        "Navigate through the all-encompassing darkness where every door   ",
        "opens a new path, a new destiny.                                  ",
        "                                                                  ",
        "Whisper 'help' anytime to conjure the command list.               "
    ]

    # Find the maximum length of the lines
    max_length = max(len(line) for line in lines)

    # Print each line with a background color
    for line in lines:
        # Fill the line with spaces to the maximum length
        filled_line = line.ljust(max_length)
        # Print with the desired foreground and background colors
        print(Fore.RED + filled_line)

    # Call Main Game Loop
    main_game_loop()


start_game()

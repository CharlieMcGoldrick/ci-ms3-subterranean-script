import random
from colorama import Fore, Back, Style
# colorama.init()

import game_states

# Global dictionary to hold the current character's stats.
character = {
    "name": None,
    "stats": None
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
    print(Back.RED + Fore.RED + "\n---------------------------------"
          "---------------------" + Style.RESET_ALL)
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
        print(f"Your {stat:<15} is {value}")


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
    print(Back.RED + Fore.RED + "\n---------------------------------"
          "---------------------" + Style.RESET_ALL)
    print("\nAwakening in a room, a sense of déjà vu strikes you...")
    print("Have you visited this place before?")
    print("A shroud of darkness wraps the space, its cold grip")
    print("only punctuated by the echoing drip of " + Fore.BLUE +
          Back.BLACK + "water" + Fore.RESET + Back.RESET + " against")
    print("stone walls. In the feeble light, an inscription comes")
    print("to view on your arm, etched crudely by an apparent")
    print("blade.")
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
    if user_input == 'help':
        print("Type your name to continue. A name is more than just an"
              "identity here.")
        print("'Help' : Seek guidance from the shadows.")
        print("'Exit' : Wake from the dream and return to reality.")
        return game_states.STATE_NAME  # Stay in the same state
    if not user_input.isalpha() or user_input.lower() == 'exit':
        raise ValueError(Back.RED + Fore.RED + "\n----------------------------"
                         "--------------------------\n" + Style.RESET_ALL +
                         "These appear to be letters, not numbers or symbols, "
                         "on your arm.")
    elif len(user_input) > 20:
        raise ValueError(Back.RED + Fore.RED + "\n----------------------------"
                         "--------------------------\n" + Style.RESET_ALL +
                         "The etching on your arm can't be that long.")
    character["name"] = user_input
    print(Back.RED + Fore.RED + "\n---------------------------------"
          "---------------------" + Style.RESET_ALL)
    print(f"\n{user_input}, that appears to be my name...")
    print("I suppose that's as good a start as any.\n")
    # Roll the stats here
    character["stats"] = roll_stats()
    # Print the stats here
    print_stats()
    return game_states.STATE_ROOM_FIRST_LAYER


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
            prompt = "\nReady to step into the unknown? Type 'Enter' if you"
            "dare."
        elif current_state == game_states.STATE_NAME:
            prompt = "\nWhat does it say on your arm?"
        else:
            prompt = "What do you do?"

        try:
            user_input = input(f"{prompt}\n").lower()

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

            if current_state == game_states.STATE_START:
                current_state = handle_start_state(user_input)
            elif current_state == game_states.STATE_NAME:
                current_state = handle_name_state(user_input)

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
        "                |_|                                               ",
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
        print(Back.RED + Fore.WHITE + filled_line + Back.RESET + Fore.RESET)

    # Call Main Game Loop
    main_game_loop()


start_game()

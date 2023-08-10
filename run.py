import random
import colorama

import game_states

# Global dictionary to hold the current character's stats.
character = {
    "name": None,
    "stats": None
}


def print_help(current_state, previous_state):
    """
    Prints a help message describing the available commands based on the
    current state.
    """
    print("------------------------------------------------------")
    print("\nYou whispered for help... The shadows respond:")
    print("'Return': Resume your previous action.")
    print("'Exit' : Wake from the dream and return to reality.")
    if previous_state == game_states.STATE_NAME:
        print("\nType your name to continue, a name is more than just an identity here...")
    # ... More states will go here!


def handle_universal_commands(user_input, current_state, previous_state):
    if user_input == 'help':
        print_help(current_state, previous_state)
        return game_states.STATE_HELP
    elif user_input == 'stats' and character['name'] is not None and character['stats'] is not None:
        print_stats()
        return previous_state
    return None


def print_stats():
    """
    Prints the current character's stats.
    """
    print(f"{character['name']}, your current stats are:")
    for stat, value in character["stats"].items():
        print(f"Your {stat:<15} is {value}")


def roll_stats():
    """
    Rolls stats for a new character.
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
    if user_input != 'enter':
        raise ValueError("\nThe shadows were quite explicit. Type 'Enter'.")
    print("------------------------------------------------------")
    print("Awakening in a room, a sense of déjà vu strikes you...")
    print("Have you visited this place before?")
    print("A shroud of darkness wraps the space, its cold grip")
    print("only punctuated by the echoing drip of water against")
    print("stone walls. In the feeble light, an inscription comes")
    print("to view on your arm, etched crudely by an apparent")
    print("blade.")
    return game_states.STATE_NAME


def handle_name_state(user_input):
    if user_input == 'help':
        print("Type your name to continue. A name is more than just an identity here.")
        print("'Help' : Seek guidance from the shadows.")
        print("'Exit' : Wake from the dream and return to reality.")
        return game_states.STATE_NAME  # Stay in the same state
    if not user_input.isalpha() or user_input.lower() == 'exit':
        raise ValueError("\n-------------------------------------------------"
                         "-----\n"
                         "These appear to be letters, not numbers or symbols, "
                         "on your arm.")
    elif len(user_input) > 20:
        raise ValueError("\n-------------------------------------------------"
                         "-----\n"
                         "The etching on your arm can't be that long.")
    character["name"] = user_input
    print("------------------------------------------------------")
    print(f"\n{user_input}, that appears to be my name...")
    print("I suppose that's as good a start as any.\n")
    # Roll the stats here
    character["stats"] = roll_stats()
    # Print the stats here
    print_stats()
    return game_states.STATE_NEXT


# def handle_stats_state():
#     character["stats"] = roll_stats()
#     print("------------------------------------------------------")
#     print("As you navigate the darkness, your competency comes flooding"
#           " back...")
#     for stat, value in character["stats"].items():
#         print(f"Your {stat:<15} is {value}")
#     # Placeholder
#     return game_states.STATE_NEXT


def main_game_loop():
    current_state = game_states.STATE_START
    # Store the previous state to return to
    previous_state = None
    while True:
        if current_state == game_states.STATE_HELP:
            prompt = "What do you demand of the shadows? Type 'return' to go back."
        elif current_state == game_states.STATE_STATS:
            prompt = "If you've finished looking at yourself, type 'return'"
        elif current_state == game_states.STATE_START:
            prompt = "Ready to step into the unknown? Type 'Enter' if you dare."
        elif current_state == game_states.STATE_NAME:
            prompt = "What does it say on your arm?"
        else:
            prompt = "What do you do?"

        try:
            user_input = input(f"\n{prompt}\n").lower()

            # Check for universal commands
            new_state = handle_universal_commands(user_input, current_state, previous_state)
            if new_state is not None:
                if current_state != new_state:
                    previous_state = current_state
                current_state = new_state
                continue

            if user_input == 'return' and current_state in (game_states.STATE_HELP, game_states.STATE_STATS):
                current_state = previous_state or game_states.STATE_NAME  # return to the previous state or a default state
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
    print(" __       _     _                                                 ")
    print("/ _\\_   _| |__ | |_ ___ _ __ _ __ ___  __ _ _ __                 ")
    print("\\ \\| | | | '_ \\| __/ _ \\ '__| '__/ _ \\/ _` | '_ \\           ")
    print("_\\ \\ |_| | |_) | ||  __/ |  | | |  __/ (_| | | | |              ")
    print("\\__/\\__,_|_.__/ \\__\\___|_|  |_|  \\___|\\__,_|_| |_|          ")
    print("  __           _       _                                          ")
    print(" / _\\ ___ _ __(_)_ __ | |_                                       ")
    print(" \\ \\ / __| '__| | '_ \\| __|                                    ")
    print(" _\\ \\ (__| |  | | |_) | |_                                      ")
    print(" \\__/\\___|_|  |_| .__/ \\__|                                    ")
    print("                |_|                                               ")
    print("                                                                  ")
    print("Welcome to the depths of 'Subterranean Script'!                   ")
    print("This is a text-based, choice-driven adventure game.               ")
    print("Navigate through the all-encompassing darkness where every door   ")
    print("opens a new path, a new destiny.                                  ")
    print("                                                                  ")
    print("Whisper 'help' anytime to conjure the command list.               ")
    main_game_loop()


start_game()

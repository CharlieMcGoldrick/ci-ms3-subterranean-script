import game_states
import weapons
import utilities
import random
from colorama import Fore, Back, Style, init
# init colorama
init()


class Character:
    def __init__(self, name=None):
        """
        Initializes a Character object with default attributes and a given
        name.

        :param name: (Optional) The name of the character. Defaults to None.
        """
        self.name = name
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.weapon = {
            "name": "Fists",
            "description": "Your own bare hands."
        }
        self.weapon_picked = False

    def print_stats(self, stat_changes=None):
        """
        Prints the current character's stats, including Strength, Dexterity,
        Constitution, Intelligence, Wisdom, Charisma, and weapon details.

        :note: Assumes that all attributes are already set and prints them
               in a formatted manner. If the character has no weapon, it will
               print a special message indicating that they only have their
               fists.
        """
        print(f"{self.name}, your current stats are:")
        print(f"Your Strength       is {self.strength}" +
              f"{self.format_stat_change(stat_changes, 'Strength')}")
        print(f"Your Dexterity      is {self.dexterity}" +
              f"{self.format_stat_change(stat_changes, 'Dexterity')}")
        print(f"Your Constitution   is {self.constitution}" +
              f"{self.format_stat_change(stat_changes, 'Constitution')}")
        print(f"Your Intelligence   is {self.intelligence}" +
              f"{self.format_stat_change(stat_changes, 'Intelligence')}")
        print(f"Your Wisdom         is {self.wisdom}" +
              f"{self.format_stat_change(stat_changes, 'Wisdom')}")
        print(f"Your Charisma       is {self.charisma}" +
              f"{self.format_stat_change(stat_changes, 'Charisma')}")

        weapon_details = self.weapon

        if weapon_details['name'] == "Fists":
            print("\nYou have no weapon... only your fists.")
        else:
            print(f"\nYou are wielding a {weapon_details['name']}")
            print(weapon_details['description'])

    def format_stat_change(self, stat_changes, stat_name):
        """
        Formats a stat change to include in the printed stat display.

        :param stat_changes: A dictionary containing changes to the
                            character's stats.
        :param stat_name: The name of the stat to format the change for.
        :return: A string representing the change to the stat, or an empty
                string if there is no change.
        """
        if stat_changes is None or stat_changes.get(stat_name) is None:
            return ""
        change = stat_changes[stat_name]
        if change != 0:
            sign = " +" if change > 0 else " -"
            return f"{sign} {abs(change)}"
        return ""

    def roll_stats(self):
        """
        Rolls stats for a new character using the 4d6 drop lowest method.

        For each attribute (Strength, Dexterity, Constitution, Intelligence,
        Wisdom, Charisma), this function rolls four 6-sided dice, removes the
        lowest roll, and sums the remaining three to generate the value for
        that attribute.

        :return: A dictionary containing the rolled values for each attribute.
        """
        attributes = ['Strength', 'Dexterity', 'Constitution', 'Intelligence',
                      'Wisdom', 'Charisma']
        attribute_values = {}
        for attribute in attributes:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.remove(min(rolls))
            attribute_values[attribute] = sum(rolls)
        return attribute_values


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


def handle_universal_commands(user_input, current_state,
                              previous_state, character):
    """
    Handles universal commands that are available in multiple states of the
    game.

    :param user_input: The input provided by the user.
    :param current_state: The current state of the game.
    :param previous_state: The previous state of the game.
    :param character: The character object for the player.
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
    elif user_input == 'stats' and character.name is not None:
        character.print_stats()
        return previous_state
    return None


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


def handle_name_state(character, user_input):
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
    character.name = user_input
    print(f"\n{user_input}, that appears to be my name...")
    print("I suppose that's as good a start as any.\n")

    # Roll the stats here
    rolled_stats = character.roll_stats()
    character.strength = rolled_stats['Strength']
    character.dexterity = rolled_stats['Dexterity']
    character.constitution = rolled_stats['Constitution']
    character.intelligence = rolled_stats['Intelligence']
    character.wisdom = rolled_stats['Wisdom']
    character.charisma = rolled_stats['Charisma']
    # Print the stats here
    character.print_stats()

    # Flavour Text for next function
    if not hasattr(character, 'weapon_picked'):
        weapon_choice = random.choice(weapons.WEAPONS_FIRST_LAYER)
        character.weapon = weapon_choice
        print(f"\nA strange chill fills the room, and your eyes are drawn to a"
              " faint glow.")
        print(f"Upon closer inspection, it's a {weapon_choice['name']} lying"
              " at your feet.")
        print(weapon_choice['description'])
    return game_states.STATE_PICK_UP_WEAPON_FIRST_LAYER


def handle_pick_up_weapon_first_layer(character, user_input):
    weapon_choice = random.choice(weapons.WEAPONS_FIRST_LAYER)
    if user_input == 'Pick Up':
        print("\nYour hand trembles as you approach the object, memories"
              " and emotions swirling within you.")
        print("The air feels thick, and a voice in the back of your mind"
              " urges you to make a choice.")
        print(f"\nYou have picked up the {weapon_choice['name']}!")
        character.weapon = weapon_choice
        print("\nAs you grasp the weapon, you feel its power infusing your"
              " very being:")
        character.print_stats(stat_changes=weapon_choice["stat_changes"])

        # Mark the weapon as picked up
        character.weapon_picked = True

    elif user_input == 'Leave':
        print("\nYou decide to leave the weapon, feeling a strange sense"
              " of resolve as you move forward.")

    else:
        raise ValueError("\nThe shadows whisper: 'Make a choice:"
                         " Pick up or Leave.'")

    return game_states.STATE_DIRECTION_DECISION_FIRST_LAYER


def handle_direction_decision_first_layer(character, user_input):
    if character.weapon_picked:
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
    character = Character()
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
            prompt = "\nDo you 'Pick Up' or 'Leave' the weapon?"
        elif current_state == game_states.STATE_DIRECTION_DECISION_FIRST_LAYER:
            prompt = "\nDo you go 'left', or go 'right'?"
        else:
            prompt = "What do you do?"

        try:
            user_input = input(f"{prompt}\n").lower()
            print(f"\n" + utilities.return_divider())

            # Check for universal commands
            new_state = handle_universal_commands(user_input, current_state,
                                                  previous_state, character)
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
                current_state = handle_name_state(character, user_input)
            elif current_state == game_states.STATE_PICK_UP_WEAPON_FIRST_LAYER:
                current_state = \
                    handle_pick_up_weapon_first_layer(character, user_input)
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

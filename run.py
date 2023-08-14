import game_states
import dungeon_areas
import enemies
import objects
import utilities
import random
from colorama import Fore, Back, Style, init
# init colorama
init()


class Entity:
    def __init__(self, entity_type, name, strength, dexterity, constitution,
                 intelligence, wisdom, charisma):
        self.entity_type = entity_type
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.weapon = None
        self.calculate_hit_points()

    def calculate_hit_points(self):
        # Base hit points
        base_hit_points = 10
        constitution_modifier = (self.constitution - 10) // 2

        # Additional hit points based on type
        type_modifier = 0
        if self.entity_type == "beast":
            type_modifier = 5
        elif self.entity_type == "humanoid":
            type_modifier = 3
        elif self.entity_type == "spirit":
            type_modifier = 2
        elif self.entity_type == "undead":
            type_modifier = 4
        elif self.entity_type == "wraith":
            type_modifier = 1
        elif self.entity_type == "aquatic":
            type_modifier = 6

        # Total hit points
        self.hit_points = (base_hit_points + constitution_modifier
                           + type_modifier)

    def attack(self):
        # Code for basic attack here
        pass


class Character(Entity):
    """
    Initializes a Character object with default attributes and a given
    name.

    :param name: (Optional) The name of the character. Defaults to None.
    """
    def __init__(self, name=None):
        super().__init__(entity_type="humanoid", name=name, strength=0,
                         dexterity=0, constitution=0, intelligence=0,
                         wisdom=0, charisma=0)
        self.weapon = {
            "name": "Fists",
            "description": "Your own bare hands."
        }
        self.stat_changes = {}
        self.object_picked_FL = False

    def print_stats(self, stat_changes=None):
        """
        Prints the current character's stats, including Strength, Dexterity,
        Constitution, Intelligence, Wisdom, Charisma, and weapon details.

        :note: Assumes that all attributes are already set and prints them
            in a formatted manner. If the character has no weapon, it will
            print a special message indicating that they only have their
            fists.
        """
        '''
        If stat_changes is not provided,
        Use the character's stored stat_changes
        '''
        if stat_changes is None:
            stat_changes = self.stat_changes

        print(f"\n{self.name}, your current stats are:")
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
            print(f"\nYou are wielding a {weapon_details['name']}.")
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
        change = stat_changes.get(stat_name, 0)
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
        for attribute in attributes:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.remove(min(rolls))
            setattr(self, attribute.lower(), sum(rolls))


class Enemy(Entity):
    def __init__(self, enemy_type, name, strength, dexterity, constitution,
                 intelligence, wisdom, charisma):
        super().__init__(enemy_type, name, strength, dexterity, constitution,
                         intelligence, wisdom, charisma)
        self.enemy_type = enemy_type
        # Other enemy-specific attributes and methods

    def special_attack(self):
        # Code for a special attack that only enemies can do
        pass


class Game:
    def __init__(self):
        """
        Initializes a new instance of the Game class.

        The constructor sets up the initial state of the game, including:
        - previous_state: Set to None, representing no previous state.
        - character: A new Character object, representing the player's
                     character.
        - current_room: Set to 'starting_room', the initial location within
                        the game.
        - handle_initialise: A method call to handle the game's initialization
                             logic, including displaying the title and
                             introduction.

        This method sets the stage for the game to begin and prepares the
        player to enter the mysterious and all-encompassing darkness of the
        game world.
        """
        self.previous_state = None
        self.character = Character()
        self.current_room = dungeon_areas.ROOMS['first_layer']['starting_room']
        self.handle_initialise()
        self.object_choice = None

    def run(self):
        """
        Executes the main game loop, handling user input and transitions
        between game states.

        The method does the following in a continuous loop:
        1. Retrieves the current prompt based on the game's state by calling
           the get_prompt method.
        2. Waits for the user's input and converts it to lowercase.
        3. Prints a divider using a utility function.
        4. Calls handle_universal_commands to check for any universal commands
           (e.g., 'help', 'exit').
        5. If a universal command is detected, updates the state and continues
           to the next iteration.
        6. If no universal command is detected, calls handle_input to handle
           state-specific input.

        This method drives the core gameplay, ensuring smooth transitions
        between different stages of the game, and responding appropriately to
        the player's choices and commands.
        """
        while True:
            prompt = self.get_prompt()
            user_input = input(f"{prompt}\n").lower()
            print("\n" + utilities.return_divider())
            new_state = (self.handle_universal_commands(user_input, self.state,
                         self.previous_state, self.character))
            if new_state is not None:
                # Save the current state before updating
                self.previous_state = self.state
                self.state = new_state
                continue
            self.handle_input(user_input)

    def print_help(self, current_state, previous_state):
        """
        Prints a help message describing the available commands based on the
        current state and previous state of the game.

        This function provides contextual guidance to the player, offering
        different commands and information depending on the current state of
        the game. The help message may include basic commands like
        'Return' and 'Exit', and specific guidance based on the player's
        current location or situation within the game.

        :param current_state: The current state of the game, used to determine
            what specific guidance should be provided.
        :param previous_state: The previous state of the game, also used to
            provide context-specific help.
        """
        if current_state == game_states.GENERAL_GAME_STATES['CHARACTER_STATS']:
            print("\nIf you've finished looking at yourself then 'return'")
        else:
            print("\nYou whispered for help... The shadows respond:")
            print("'Return': Resume your previous action.")
            print("'Exit' : Wake from the dream and return to reality.")
            if current_state == (game_states.FIRST_LAYER_STATES
                                 ['CHARACTER_CREATION']):
                print("'Name' : Type what you see on your arm to continue")
            elif current_state == (game_states.FIRST_LAYER_STATES
                                   ['ROOM_PICKUP_FIRST_LAYER']):
                print("'Pick Up' : Pick the object up")
                print("'Leave' : Leave the object")
            elif current_state == (game_states.FIRST_LAYER_STATES
                                   ['ROOM_DOOR_CHOICE_FIRST_LAYER']):
                print("'Left' : Choose the left door")
                print("'Right' : Choose the right door")
        # ... More states will go here!

    def handle_universal_commands(self, user_input, current_state,
                                  previous_state, character):
        """
        Handles universal commands that can be invoked in multiple game states.

        This method is responsible for managing the common commands that can
        be executed at various stages of the game. The recognized universal
        commands include:
        - 'help': Prints the help menu.
        - 'stats': Displays the character's statistics if the name has been
                   initialized, and provides the option to 'return' to the
                   previous state.
        - 'exit': Exits the game.
        - 'return': Allows the player to return to the previous state from the
                    'help' or 'stats' screens.

        :param user_input: The input provided by the user (string).
        :param current_state: The current state of the game, used to determine
                            specific behavior in some commands.
        :param previous_state: The previous state of the game, can be used in
                            'return' command to return to a previous game
                            state.
        :param character: The character object for the player, used to handle
                        character-specific commands.

        :return: The next game state if a universal command is recognized and
                handled, or None if the user input does not correspond to a
                universal command.
        """
        if user_input == 'help':
            self.print_help(current_state, previous_state)
            return game_states.GENERAL_GAME_STATES['HELP']
        elif user_input == 'stats' and character.name is not None:
            character.print_stats()
            return game_states.GENERAL_GAME_STATES['CHARACTER_STATS']
        elif user_input == 'exit':
            print("\nMaybe it's all just a dream...")
            exit(0)
        elif user_input == 'return' and current_state in (
                game_states.GENERAL_GAME_STATES['HELP'],
                game_states.GENERAL_GAME_STATES['CHARACTER_STATS']):
            return previous_state
        return None

    def handle_initialise(self):
        """
        Initiates the text-based adventure game 'Subterranean Script'.

        This function displays the game's title, a brief introduction, and a
        welcome message to guide players into the mysterious and
        all-encompassing darkness of the game world.

        :note: Whisper 'help' anytime in the game to view a list of commands.
        """
        lines = [
            " __       _     _                                               ",
            "/ _\\_   _| |__ | |_ ___ _ __ _ __ ___  __ _ _ __               ",
            "\\ \\| | | | '_ \\| __/ _ \\ '__| '__/ _ \\/ _` | '_ \\         ",
            "_\\ \\ |_| | |_) | ||  __/ |  | | |  __/ (_| | | | |            ",
            "\\__/\\__,_|_.__/ \\__\\___|_|  |_|  \\___|\\__,_|_| |_|        ",
            " __           _       _                                         ",
            "/ _\\ ___ _ __(_)_ __ | |_                                      ",
            "\\ \\ / __| '__| | '_ \\| __|                                   ",
            "_\\ \\ (__| |  | | |_) | |_                                     ",
            "\\__/\\___|_|  |_| .__/ \\__|                                   ",
            "               |_|                                              ",
            "                                                                ",
            "Welcome to the depths of 'Subterranean Script'!                 ",
            "This is a text-based, choice-driven adventure game,             ",
            "inspired by classic Choose-Your-Own-Adventure books.            ",
            "and D&D. Navigate through the all-encompassing darkness         ",
            "of the mysterious dungeon environment, where every door         ",
            "opens a new path, a new destiny.                                ",
            "                                                                ",
            "Whisper 'help' anytime to conjure the command list.             "
        ]

        # Find the maximum length of the lines
        max_length = max(len(line) for line in lines)

        # Print each line with a background color
        for line in lines:
            # Fill the line with spaces to the maximum length
            filled_line = line.ljust(max_length)
            # Print with the desired foreground and background colors
            print(Fore.RED + filled_line)
        self.state = game_states.FIRST_LAYER_STATES['GAME_START']

    def get_prompt(self):
        """
        Returns a prompt text based on the current state of the game.

        The method checks the current state of the game and returns a string
        containing the appropriate prompt for the player. The prompt may
        include instructions, questions, or descriptions designed to guide the
        player's choices and actions within the game.

        :return: A string containing the appropriate prompt text for the
                 current game state. This may include:
            - An introductory challenge for the 'GAME_START' state.
            - A description and question regarding the character's surroundings
              for the 'CHARACTER_CREATION' state.
            - A decision-making scenario for picking up objects in the
              'ROOM_PICKUP_FIRST_LAYER' state.
            - A navigation decision between doors for the
              'ROOM_DOOR_CHOICE_FIRST_LAYER' state.

        The returned text is used to solicit user input and move the game
        forward based on the current state.
        """
        # PROMPT - GAME STATE - GENERAL - HELP
        if self.state == game_states.GENERAL_GAME_STATES['HELP']:
            return "\nYou whispered for help... The shadows respond."
        # PROMPT - GAME STATE - GENERAL - CHARACTER STATS
        elif self.state == game_states.GENERAL_GAME_STATES['CHARACTER_STATS']:
            return "\nIf you've finished looking at yourself then 'Return'"
        # PROMPT - GAME STATE - FIRST LAYER - GAME START
        elif self.state == game_states.FIRST_LAYER_STATES['GAME_START']:
            return (f"\nReady to step into the unknown?"
                    " Type 'Enter' if you dare.")
        # PROMPT - GAME STATE - FIRST LAYER - CHARACTER CREATION
        elif self.state == (game_states.FIRST_LAYER_STATES
                            ['CHARACTER_CREATION']):
            flavor_text_intro = self.current_room['flavor_text_intro']
            prompt_text = (
                flavor_text_intro +
                "\nWhat does it say on your arm?"
            )
            return prompt_text
        # PROMPT - GAME STATE - FIRST LAYER - ROOM PICKUP
        elif (self.state ==
              game_states.FIRST_LAYER_STATES['ROOM_PICKUP_FIRST_LAYER']):
            if self.object_choice is None:
                self.object_choice = random.choice(objects.OBJECTS_FIRST_LAYER)
            prompt_text = (
                "\nA strange chill fills the room, and your eyes are drawn to"
                " a faint glow.\n"
                f"\nUpon closer inspection, it's a"
                f" {self.object_choice['name']} lying at your feet."
                f"\n{self.object_choice['description']}\n"
                "\nDo you 'Pick Up' or 'Leave' the weapon?"
            )
            return prompt_text
        # PROMPT - GAME STATE - FIRST LAYER - ROOM DOOR CHOICE
        elif (self.state ==
              game_states.FIRST_LAYER_STATES['ROOM_DOOR_CHOICE_FIRST_LAYER']):
            prompt_text = (
                "\nTwo doors, faintly illuminated by candlelight, beckon from"
                " the darkness."
                "\nA mysterious force urges you to make a choice.\n"
                "\nDo you go 'left', or go 'right'?"
            )
            return prompt_text
        # PROMPT - GAME STATE - SECOND LAYER - FIGHT
        elif (self.state ==
              game_states.SECOND_LAYER_STATES['FIGHT_SECOND_LAYER']):
            prompt_text = (
                "\nYou are in a fight! Do you want to 'attack', 'defend', or"
                " 'flee'?"
            )
            return prompt_text

    def handle_input(self, user_input):
        """
        Processes user input based on the current game state.

        This method is responsible for handling user input and calling the
        appropriate method based on the current game state. The game state
        will determine the specific action to be taken in response to the
        user's input.

        The handled states include:
        - 'INITIALISE': Calls the initialization method.
        - 'GAME_START': Handles the game start state.
        - 'CHARACTER_CREATION': Handles the character stats state.
        - 'ROOM_PICKUP_FIRST_LAYER': Handles the pickup of an object in a room.
        - 'ROOM_DOOR_CHOICE_FIRST_LAYER': Handles the door choice in a room.

        :param user_input: The input provided by the user (string).
        """
        if self.state == game_states.FIRST_LAYER_STATES['INITIALISE']:
            self.handle_initialise()
        elif self.state == game_states.FIRST_LAYER_STATES['GAME_START']:
            self.handle_start_state(user_input)
        elif self.state == (game_states.FIRST_LAYER_STATES
                            ['CHARACTER_CREATION']):
            self.handle_character_state(user_input)
        elif (self.state ==
              game_states.FIRST_LAYER_STATES['ROOM_PICKUP_FIRST_LAYER']):
            self.handle_room_pickup(user_input)
        elif (self.state ==
              game_states.FIRST_LAYER_STATES['ROOM_DOOR_CHOICE_FIRST_LAYER']):
            self.handle_room_door_choice(user_input)
        elif (self.state ==
              game_states.SECOND_LAYER_STATES['FIGHT_SECOND_LAYER']):
            self.handle_fight(user_input)

    def handle_start_state(self, user_input):
        """
        Handles the input for the game's start state.

        This method processes the user's input during the game's starting
        state. If the input is 'enter', the game progresses to the character
        stats state. Any other input will raise a ValueError, and a message
        will be printed to inform the user that they must type 'Enter'.

        :param user_input: The input provided by the user (string), expected
                           to be 'enter' to proceed.
        :raises ValueError: If the input is anything other than 'enter'.
        """
        try:
            if user_input == 'enter':
                print("\nGood luck. You'll need it...")
                # Save the current state before updating
                self.previous_state = self.state
                # Transition to next state
                self.state = (game_states.FIRST_LAYER_STATES
                              ['CHARACTER_CREATION'])
            else:
                raise ValueError("\nThe shadows were quite explicit."
                                 " Type 'Enter'.")
        except ValueError as e:
            print(e)

    def handle_character_state(self, user_input):
        """
        Handles the state where the player is prompted to enter their
        character's name.

        :param user_input: The input provided by the user. It must be a valid
                        name consisting of alphabetic characters and not
                        exceeding 20 characters. If the input is 'exit' or
                        contains non-alphabetic characters, a ValueError will
                        be raised.

        :raises ValueError: If the user input contains numbers or symbols, is
                            empty, or exceeds 20 characters, an error message
                            is raised to guide the player to input a valid
                            name.
        """
        try:
            if not user_input.isalpha() or user_input.lower() == 'exit':
                raise ValueError("\nThese appear to be letters, not numbers"
                                 " or symbols, on your arm.")
            elif len(user_input) > 20:
                raise ValueError("\nThe etching on your arm can't be that"
                                 " long.")
            self.character.name = user_input
            print(f"\n{user_input}, that appears to be my name...")
            print("I suppose that's as good a start as any.\n")

            # Roll the stats here
            self.character.roll_stats()
            # Print the stats here
            self.character.print_stats()

            # Transition to next state
            self.state = (game_states.FIRST_LAYER_STATES
                          ['ROOM_PICKUP_FIRST_LAYER'])
        except ValueError as e:
            # Print the error message that was raised
            print(e)

    def handle_room_pickup(self, user_input):
        try:
            object_choice = random.choice(objects.OBJECTS_FIRST_LAYER)
            if user_input == 'pick up':
                print("\nYour hand trembles as you approach the object,"
                      " memories and emotions swirling\n"
                      "within you.")
                print("The air feels thick, and a voice in the back of your"
                      " mind urges you to make a\n"
                      "choice.")
                print(f"\nYou have picked up the {object_choice['name']}!")

                # Compute the stat changes
                stat_changes = object_choice["stat_changes"]

                # Apply the stat changes to the character
                for stat, change in stat_changes.items():
                    setattr(self.character, stat.lower(),
                            getattr(self.character, stat.lower()) + change)
                    # Add the new change to any existing change for this stat
                    existing_change = self.character.stat_changes.get(stat, 0)
                    self.character.stat_changes[stat] = (existing_change +
                                                         change)

                self.character.weapon = object_choice
                print("\nAs you grasp the weapon, you feel its power infusing"
                      " your very being:")
                self.character.print_stats(stat_changes=stat_changes)

                # Mark the weapon as picked up
                self.character.object_picked_FL = True

                # Transition to next state
                self.state = (game_states.FIRST_LAYER_STATES
                              ['ROOM_DOOR_CHOICE_FIRST_LAYER'])
            elif user_input == 'leave':
                print("\nYou decide to leave the weapon, feeling a strange"
                      " sense of resolve\n"
                      "as you move forward.")
                # Transition to next state
                self.state = (game_states.FIRST_LAYER_STATES
                              ['ROOM_DOOR_CHOICE_FIRST_LAYER'])
            else:
                raise ValueError("\nThe shadows whisper: 'Make a choice:"
                                 " 'Pick Up' or 'Leave'.")

        except ValueError as e:
            # Print the error message that was raised
            print(e)

    def handle_room_door_choice(self, user_input):
        if user_input in ['left', 'right']:
            room_choice = random.choice(dungeon_areas.ROOMS_SECOND_LAYER)
            print(f"You chose the {user_input} door and discover a"
                  f" {room_choice['name']}...")
            print(room_choice['description'])
            print(room_choice['prompt'])
            # Transition to next state
            self.state = game_states.SECOND_LAYER_STATES['FIGHT_SECOND_LAYER']
        else:
            raise ValueError("The shadows whisper:"
                             "'Make a choice: left or right.'")

    def handle_fight(self, user_input):
        try:
            # Check if the user input is valid for a fight action
            if user_input not in ['attack', 'defend', 'flee']:
                raise ValueError("Invalid action! Choose 'attack',"
                                 "'defend', or 'flee'.")
            # Implement logic for the user's choice
            if user_input == 'attack':
                return "You attacked the enemy!"
            elif user_input == 'defend':
                return "You defended against the enemy's attack!"
            elif user_input == 'dodge':
                return "You successfully fled from the fight!"
        except ValueError as e:
            return str(e)

        # Return a default message if something unexpected occurs
        return "An unexpected error occurred in the fight."


game = Game()
game.run()

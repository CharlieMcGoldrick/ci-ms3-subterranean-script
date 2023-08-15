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
        self.calculate_hit_points()
        self.weapon = None
        self.armor_bonus = None
        self.shield_bonus = None
        self.other_bonuses = None

    def calculate_modifier(self, ability_score):
        return (ability_score - 5) // 2

    def calculate_hit_points(self):
        # Base hit points
        base_hit_points = 10
        constitution_modifier = self.calculate_modifier(self.constitution)

        # Additional hit points based on type
        type_modifier = utilities.HP_TYPE_MODIFIERS.get(self.entity_type, 0)

        # Total hit points
        self.hit_points = (base_hit_points + constitution_modifier
                           + type_modifier)

    def calculate_ac(self):
        # Base AC
        ac = 10
        # Add Dexterity modifier
        ac += self.calculate_modifier(self.dexterity)
        # Entity type-based AC
        type_modifier = utilities.AC_TYPE_MODIFIERS.get(self.entity_type, 0)
        ac += type_modifier
        # Add Armor Bonus if available
        if self.armor_bonus is not None:
            ac += self.armor_bonus
        # Add Shield Bonus if available
        if self.shield_bonus is not None:
            ac += self.shield_bonus
        # Add Other Bonuses if available
        if self.other_bonuses is not None:
            ac += self.other_bonuses
        return ac


class Character(Entity):
    """
    Initializes a Character object with default attributes and a given
    name.

    :param name: (Optional) The name of the character. Defaults to None.
    """
    def __init__(self, name=None):
        super().__init__(entity_type="hero", name=name, strength=0,
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
        use the character's stored stat_changes
        '''
        if stat_changes is None:
            stat_changes = self.stat_changes

        print(f"\n{self.name.capitalize()}, your current stats are:")
        print(f"Health       is {self.hit_points}")
        print(f"Armour Class is {self.calculate_ac()}")
        print(f"Strength     is {self.strength}" +
              f"{self.format_stat_change(stat_changes, 'Strength')}")
        print(f"Dexterity    is {self.dexterity}" +
              f"{self.format_stat_change(stat_changes, 'Dexterity')}")
        print(f"Constitution is {self.constitution}" +
              f"{self.format_stat_change(stat_changes, 'Constitution')}")
        print(f"Intelligence is {self.intelligence}" +
              f"{self.format_stat_change(stat_changes, 'Intelligence')}")
        print(f"Wisdom       is {self.wisdom}" +
              f"{self.format_stat_change(stat_changes, 'Wisdom')}")
        print(f"Charisma     is {self.charisma}" +
              f"{self.format_stat_change(stat_changes, 'Charisma')}")

        weapon_details = self.weapon

        if weapon_details['name'] == "Fists":
            print("You have no weapon... only your fists.")
        else:
            print(f"You are wielding a {weapon_details['name']}.")
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
    def __init__(self, entity_type, name, strength, dexterity, constitution,
                 intelligence, wisdom, charisma, weapon):
        super().__init__(entity_type, name, strength, dexterity, constitution,
                         intelligence, wisdom, charisma)
        self.weapon = weapon

    @staticmethod
    def generate_enemy(current_room):
        # Select random enemy
        possible_enemies = (dungeon_areas.ROOMS['second_layer']
                            ['common_enemies'])
        specific_enemy = (dungeon_areas.ROOMS['second_layer']
                          ['specific_enemies'].get(current_room))
        if specific_enemy:
            possible_enemies.append(specific_enemy)

        enemy_dict = random.choice(possible_enemies)
        # Create Enemy instance
        return Enemy(
            enemy_dict['entity_type'],
            enemy_dict['name'],
            enemy_dict['strength'],
            enemy_dict['dexterity'],
            enemy_dict['constitution'],
            enemy_dict['intelligence'],
            enemy_dict['wisdom'],
            enemy_dict['charisma'],
            enemy_dict['weapon']
        )


class Fight:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def roll_die(self, sides=20):
        return random.randint(1, sides)

    def initiative(self):
        attacker_initiative = (self.roll_die() +
                               self.attacker.calculate_modifier
                               (self.attacker.dexterity))
        defender_initiative = (self.roll_die() +
                               self.defender.calculate_modifier
                               (self.defender.dexterity))
        print(f"{self.attacker.name} rolls an"
              f" initiative of {attacker_initiative}!")
        print(f"{self.defender.name} rolls an"
              f" initiative of {defender_initiative}!")
        if attacker_initiative >= defender_initiative:
            print(f"{self.attacker.name} goes first!")
            return self.attacker
        else:
            print(f"{self.defender.name} goes first!")
            return self.defender

    def dodge(self, entity):
        # Define how the dodge bonus is calculated
        dodge_bonus = (self.roll_die(sides=6) +
                       entity.calculate_modifier(entity.dexterity))
        return dodge_bonus

    def check_death(self, entity):
        if entity.hit_points <= 0:
            return True
        return False

    def attack(self, attack_type="quick", defender_dodging=False):
        try:
            if attack_type == "quick":
                modifier = (self.attacker.calculate_modifier
                            (self.attacker.dexterity))
                base_damage = 5
            elif attack_type == "heavy":
                modifier = (self.attacker.calculate_modifier
                            (self.attacker.strength))
                base_damage = 10
            else:
                raise ValueError(f"You must use a 'quick' or 'heavy' attack")

            attack_roll = self.roll_die() + modifier

            dodge_bonus = 0
            if defender_dodging:
                dodge_bonus = self.dodge(self.defender)
                print(f"{self.defender.name} attempts to dodge!")

            if attack_roll >= (self.defender.calculate_ac() + dodge_bonus):
                damage = base_damage + modifier
                self.defender.hit_points -= damage
                print(f"{self.attacker.name} attacks"
                      f" {self.defender.name} with a {attack_type} attack,"
                      f" dealing {damage} damage!")
                # Check if defender is dead after the attack
                if self.check_death(self.defender):
                    return
            else:
                print(f"{self.attacker.name} swings at"
                      f" {self.defender.name}, but misses!")
        except ValueError as e:
            print(e)


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
        self.room_choice_name = None
        self.enemy_instance = None

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
            # Only prompt for user input if the current state requires it
            if self.state not in game_states.SECOND_LAYER_STATES.values():
                user_input = input(f"{prompt}\n").lower()
                print("\n" + utilities.return_divider())
                new_state = (self.handle_universal_commands(user_input,
                             self.state, self.previous_state, self.character))
                if new_state is not None:
                    # Save the current state before updating
                    self.previous_state = self.state
                    self.state = new_state
                    continue
            else:
                user_input = None
                print(prompt)
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
        # PROMPT - GAME STATE = GENERAL - HELP
        if self.state == game_states.GENERAL_GAME_STATES['HELP']:
            return "\nYou whispered for help... The shadows respond."
        # PROMPT - GAME STATE = GENERAL - CHARACTER STATS
        elif self.state == game_states.GENERAL_GAME_STATES['CHARACTER_STATS']:
            return "\nIf you've finished looking at yourself then 'Return'"
        # PROMPT - GAME STATE = FIRST LAYER - GAME START
        elif self.state == game_states.FIRST_LAYER_STATES['GAME_START']:
            return (f"\nReady to step into the unknown?"
                    " Type 'Enter' if you dare.")
        # PROMPT - GAME STATE = FIRST LAYER - CHARACTER CREATION
        elif self.state == (game_states.FIRST_LAYER_STATES
                            ['CHARACTER_CREATION']):
            flavor_text_intro = self.current_room['flavor_text_intro']
            prompt_text = (
                flavor_text_intro +
                "\nWhat does it say on your arm?"
            )
            return prompt_text
        # PROMPT - GAME STATE = FIRST LAYER - ROOM PICKUP
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
        # PROMPT - GAME STATE = FIRST LAYER - ROOM DOOR CHOICE
        elif (self.state ==
              game_states.FIRST_LAYER_STATES['ROOM_DOOR_CHOICE_FIRST_LAYER']):
            prompt_text = (
                "\nTwo doors, faintly illuminated by candlelight, beckon from"
                " the darkness."
                "\nA mysterious force urges you to make a choice.\n"
                "\nDo you go 'left', or go 'right'?"
            )
            return prompt_text
        # PROMPT - GAME STATE = SECOND LAYER - FIGHT
        elif (self.state ==
              game_states.SECOND_LAYER_STATES['FIGHT_SECOND_LAYER']):
            if self.enemy_instance is None:
                self.enemy_instance = Enemy.generate_enemy(self.
                                                           room_choice_name)
            prompt_text = (
                "\nA sinister growl echoes through the room, and your eyes"
                f" lock with a {self.enemy_instance.entity_type}.\n"
                f"It's a {self.enemy_instance.name},"
                " I should be wary of its"
                f" {self.enemy_instance.weapon['name']}.\n"
                "\nYou're in a fight!"
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
            if self.enemy_instance is None:
                self.enemy_instance = Enemy.generate_enemy(self.
                                                           room_choice_name)
            self.handle_battle(self.character, self.enemy_instance)

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
            print(f"\n{user_input.capitalize()},"
                  " that appears to be my name...")

            print("I suppose that's as good a start as any.")

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
                print("As you grasp the weapon, you feel its power infusing"
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
        try:
            if user_input in ['left', 'right']:
                room_choice_dict = random.choice(dungeon_areas.
                                                 ROOMS_SECOND_LAYER)
                self.room_choice_name = room_choice_dict['name']
                print(f"\nYou chose the {user_input} door and discover a"
                      f" {self.room_choice_name}...")
                print(room_choice_dict['description'])
                print(room_choice_dict['prompt'])
                # Transition to next state
                self.state = (game_states.SECOND_LAYER_STATES
                              ['FIGHT_SECOND_LAYER'])
            else:
                raise ValueError("The shadows whisper:"
                                 "'Make a choice: left or right.'")
        except ValueError as e:
            # Print the error message that was raised
            print(e)

    def handle_battle(self, player, enemy):
        # Create a Fight object
        fight = Fight(player, enemy)

        # Determine who goes first based on initiative
        current_attacker = fight.initiative()
        current_defender = (fight.defender if current_attacker ==
                            fight.attacker else fight.attacker)

        # Continue the fight until one of the characters is defeated
        while player.hit_points > 0 and enemy.hit_points > 0:
            # Reset user_input at the beginning of the loop
            user_input = None

            # Print player and enemy HP once at the start of the turn
            print(f"Player HP: {player.hit_points},"
                  f"Enemy HP: {enemy.hit_points}")
            # Get the user's choice if the player is the attacker
            if current_attacker == player:
                # Keep asking until a valid input is entered
                while True:
                    user_input = input("\nChoose to 'quick' attack, 'heavy'"
                                       " attack, or 'dodge' the enemies"
                                       " attack: \n")
                    utilities.return_divider()
                    if user_input in ['dodge', 'quick', 'heavy']:
                        break
                    else:
                        print(f"\n{utilities.return_divider()}\n")

                if user_input == 'dodge':
                    print(f"{player.name} prepares to dodge the next attack!")
                elif user_input in ['quick', 'heavy']:
                    fight.attack(attack_type=user_input)
            # Enemy's turn
            else:
                enemy_action = random.choice(['quick', 'heavy', 'dodge'])
                if enemy_action == 'dodge':
                    print(f"{enemy.name} prepares to dodge the next attack!")
                else:
                    defender_dodging = (user_input ==
                                        'dodge' if current_defender ==
                                        player else False)
                    fight.attack(attack_type=enemy_action,
                                 defender_dodging=defender_dodging)
            # Switch attacker and defender for the next turn
            current_attacker, current_defender = (current_defender,
                                                  current_attacker)
            # Check if the fight has ended
            prompt_text = ""

            if enemy.hit_points <= 0:
                prompt_text = (
                    "\nExhausted and panting after the intense battle,"
                    " you take a moment to catch your"
                    " breath.\n"
                    "The room falls silent except for the distant echoes of"
                    " the dungeon, and your mind\n"
                    "begins to wander.\n"
                    "Slowly, your eyes close, and you feel a strange pull"
                    " towards the beginning,\nas if the very fabric "
                    "of this place is beckoning you to start anew.\n"
                )
            elif player.hit_points <= 0:
                prompt_text = (
                    "Struggling to maintain your stance, you see"
                    f"{self.enemy_instance.name} preparing for one last"
                    "attack.\n"
                    "Before you can react, a fatal blow lands,"
                    " darkens around you.\n"
                    "The last thing you hear is the triumphant cackle of your"
                    " foe as you slip away,\ndefeated and broken.\n"
                )
            print(prompt_text)
            self.state = (game_states.FIRST_LAYER_STATES['CHARACTER_CREATION']
                          if fight.check_death(enemy) else
                          game_states.FIRST_LAYER_STATES['CHARACTER_CREATION'])


game = Game()
game.run()

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
    """
    Represents a generic entity in a game, including attributes such as
    strength, dexterity, and hit points.
    """
    def __init__(self, entity_type, name, strength, dexterity, constitution,
                 intelligence, wisdom, charisma):
        """
        Initialises the Entity with the given attributes.

        Parameters
        ----------
        entity_type : str
            The type of the entity.
        name : str
            The name of the entity.
        strength : int
            The entity's strength attribute.
        dexterity : int
            The entity's dexterity attribute.
        constitution : int
            The entity's constitution attribute.
        intelligence : int
            The entity's intelligence attribute.
        wisdom : int
            The entity's wisdom attribute.
        charisma : int
            The entity's charisma attribute.
        """
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
        """
        Calculates the ability modifier based on the given ability score.

        Parameters
        ----------
        ability_score : int
            The ability score to calculate the modifier for.

        Returns
        -------
        int
            The calculated ability modifier.
        """
        return (ability_score - 5) // 2

    def calculate_hit_points(self):
        """
        Calculates the total hit points of the entity based on base hit
        points, constitution modifier, and entity type.
        """
        # Base hit points
        base_hit_points = 10
        constitution_modifier = self.calculate_modifier(self.constitution)

        # Additional hit points based on type
        type_modifier = utilities.HP_TYPE_MODIFIERS.get(self.entity_type, 0)

        # Total hit points
        self.hit_points = (base_hit_points + constitution_modifier
                           + type_modifier)

    def calculate_ac(self):
        """
        Calculates the armor class (AC) of the entity based on dexterity,
        entity type, and bonuses from equipped items.

        Returns
        -------
        int
            The calculated armor class.
        """
        # Base AC
        ac = 0
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
    Represents a specific character in a game, extending the Entity class
    with additional properties related to the character's stats, weapon, and
    behavior.
    """

    def __init__(self, name=None):
        """
        Initialises a Character object with default attributes and a given
        name.

        Parameters
        ----------
        name : str, optional
            The name of the character. Defaults to None.
        """
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

        Parameters
        ----------
        stat_changes : dict, optional
            Changes to the character's stats. Defaults to None.

        Notes
        -----
        Assumes that all attributes are already set and prints them in a
        formatted manner.
        If the character has no weapon, it will print a message indicating
        that they only have their fists.
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

        Parameters
        ----------
        stat_changes : dict
            A dictionary containing changes to the character's stats.
        stat_name : str
            The name of the stat to format the change for.

        Returns
        -------
        str
            A string representing the change to the stat, or an empty
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

        Returns
        -------
        dict
            A dictionary containing the rolled values for each attribute.
        """
        attributes = ['Strength', 'Dexterity', 'Constitution', 'Intelligence',
                      'Wisdom', 'Charisma']
        for attribute in attributes:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.remove(min(rolls))
            setattr(self, attribute.lower(), sum(rolls))


class Enemy(Entity):
    """
    Represents an enemy character in the game, extending the Entity class
    with specific properties related to the enemy's weapon.
    """
    def __init__(self, entity_type, name, strength, dexterity, constitution,
                 intelligence, wisdom, charisma, weapon):
        """
        Initialises an Enemy object with specific attributes and a given
        weapon.

        Parameters
        ----------
        entity_type : str
            The type of entity.
        name : str
            The name of the enemy.
        strength : int
            The strength of the enemy.
        dexterity : int
            The dexterity of the enemy.
        constitution : int
            The constitution of the enemy.
        intelligence : int
            The intelligence of the enemy.
        wisdom : int
            The wisdom of the enemy.
        charisma : int
            The charisma of the enemy.
        weapon : dict
            The weapon of the enemy.
        """
        super().__init__(entity_type, name, strength, dexterity, constitution,
                         intelligence, wisdom, charisma)
        self.weapon = weapon

    @staticmethod
    def generate_enemy(current_room):
        """
        Generates a random enemy based on the current room and available enemy
        templates.

        Parameters
        ----------
        current_room : str
            The identifier of the current room within the dungeon.

        Returns
        -------
        Enemy
            An instance of the Enemy class representing the generated enemy.
        """
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
    """
    Represents a fight between characters in the game, managing the mechanics
    of combat such as initiative, dodging, attacking, and checking for death.
    """
    def __init__(self):
        """
        Initialises a Fight object with flags for dodging.
        """
        self.dodge_flags = {}

    def roll_die(self, sides=20):
        """
        Rolls a die with a given number of sides.

        Parameters
        ----------
        sides : int, optional
            The number of sides on the die. Defaults to 20.

        Returns
        -------
        int
            The result of the die roll.
        """
        return random.randint(1, sides)

    def initiative(self, player, enemy):
        """
        Determines which combatant goes first in a fight based on a die roll
        and dexterity modifiers.

        Parameters
        ----------
        player : Entity
            The player's character.
        enemy : Entity
            The enemy character.

        Returns
        -------
        Entity
            The entity that has the initiative and will go first.
        """
        player_initiative = (self.roll_die() +
                             player.calculate_modifier(player.dexterity))
        enemy_initiative = (self.roll_die() +
                            enemy.calculate_modifier(enemy.dexterity))
        if player_initiative >= enemy_initiative:
            print(f"Time to fight! {player.name.capitalize()} has the"
                  " initiative.")
            return player
        else:
            print(f"Time to fight! {enemy.name} has the initiative.")
            return enemy

    def dodge(self, entity):
        """
        Calculates a dodge bonus for a given entity.

        Parameters
        ----------
        entity : Entity
            The entity attempting to dodge.

        Returns
        -------
        int
            The dodge bonus value.
        """
        # Define how the dodge bonus is calculated
        dodge_bonus = (self.roll_die(sides=6) +
                       entity.calculate_modifier(entity.dexterity))
        return dodge_bonus

    def check_death(self, entity):
        """
        Checks if a given entity is dead.

        Parameters
        ----------
        entity : Entity
            The entity to check.

        Returns
        -------
        bool
            True if the entity is dead, False otherwise.
        """
        if entity.hit_points <= 0:
            return True
        return False

    def attack(self, attacker, defender, attack_type="quick",
               defender_dodging=False):
        """
        Simulates an attack between two entities, calculating hit, damage, and
        checking for death.

        Parameters
        ----------
        attacker : Entity
            The entity initiating the attack.
        defender : Entity
            The entity defending against the attack.
        attack_type : str, optional
            The type of attack ("quick" or "heavy"). Defaults to "quick".
        defender_dodging : bool, optional
            Whether the defender is attempting to dodge. Defaults to False.

        Raises
        ------
        ValueError
            If an invalid attack_type is provided.
        """
        if self.dodge_flags[attacker]:
            return
        try:
            if attack_type == "quick":
                modifier = (attacker.calculate_modifier
                            (attacker.dexterity))
                base_damage = 5
            elif attack_type == "heavy":
                modifier = (attacker.calculate_modifier
                            (attacker.strength))
                base_damage = 10
            else:
                raise ValueError(f"You must use a 'quick' or 'heavy' attack")

            attack_roll = self.roll_die() + modifier

            dodge_bonus = 0
            if defender_dodging:
                dodge_bonus = self.dodge(defender)
                print(f"{defender.name} attempts to dodge!")
            if attack_roll >= (defender.calculate_ac() + dodge_bonus):
                damage = base_damage + modifier
                defender.hit_points -= damage
                print(f"{attacker.name.capitalize()} attacks"
                      f" {defender.name.capitalize()} with a {attack_type}"
                      f" attack, dealing {damage} damage!")
                # Check if defender is dead after the attack
                if self.check_death(defender):
                    return
            else:
                print(f"{attacker.name} swings at"
                      f" {defender.name}, but misses!")
        except ValueError as e:
            print(e)


class Game:
    """
    Represents the main game control and logic, handling initialisation,
    state transitions, user input, and overall game flow. It maintains
    the game state and facilitates transitions between different parts
    of the game, including interactions with characters, navigation through
    rooms, and combat with enemies.
    """
    def __init__(self):
        """
        Initializes a new instance of the Game class. This method calls the
        reset_game method to set all game-related attributes to their initial
        values, ensuring a fresh start. It then calls the handle_initialise
        method to display the game's title, introduction, and prepare the
        player to enter the game world.
        """
        self.reset_game()
        self.handle_initialise()

    def reset_game(self):
        """
        Resets the game to its initial state, clearing any previous game
        progress and resetting all relevant attributes. This allows for a new
        game to start or a current game to restart.

        Attributes
        ----------
        previous_state : None
            Resets to None for starting the game fresh.
        character : Character
            Resets the player's character to a new instance.
        current_room : str
            Resets to the starting room identifier.
        object_choice : None
            Resets to None for starting the game fresh.
        room_choice_name : None
            Resets to None for starting the game fresh.
        enemy_instance : None
            Resets to None for starting the game fresh.
        """
        self.previous_state = None
        self.character = Character()
        self.current_room = dungeon_areas.ROOMS['first_layer']['starting_room']
        self.object_choice = None
        self.room_choice_name = None
        self.enemy_instance = None

    def run(self):
        """
        Executes the main game loop, constantly reading user input and
        responding accordingly. The method handles transitions between
        different game states, including navigation, combat, dialogue, and
        more.

        Attributes
        ----------
        prompt : str
            The prompt or message to be displayed to the user.
        user_input : str or None
            The user's input, or None if no input is required.
        new_state : str or None
            The new game state if a state transition occurs.
        """
        while True:
            prompt = self.get_prompt()
            # Only prompt for user input if the current state requires it
            if self.state not in game_states.SECOND_LAYER_STATES.values():
                user_input = input(f"{prompt}\n").lower()
                print("\n" + utilities.return_divider())
                new_state = self.handle_universal_commands(user_input,
                                                           self.state,
                                                           self.previous_state,
                                                           self.character)
                if new_state is not None:
                    self.state = new_state
                    continue
            else:
                user_input = None
                print(prompt)
            self.handle_input(user_input)

    def print_help(self, previous_state):
        """
        Prints a help message describing the available commands based on the
        current state and previous state of the game.

        This function provides contextual guidance to the player, offering
        different commands and information depending on the current state of
        the game. The help message may include basic commands like 'Return'
        and 'Exit', and specific guidance based on the player's current
        location or situation within the game.

        Parameters
        ----------
        previous_state : str
            The previous state of the game, used to provide context-specific
             elp.

        Returns
        -------
        str
            The help text to be displayed to the player.
        """
        help_text = "\nYou whispered for help... The shadows respond:"
        help_text += "\n'Return'  : Resume your previous action."
        if previous_state not in [
            game_states.FIRST_LAYER_STATES['GAME_START'],
            game_states.FIRST_LAYER_STATES['CHARACTER_CREATION']
        ]:
            help_text += "\n'Stats'   : Understand what you're made of and"
            "equipped with."

        if previous_state == (game_states.GENERAL_GAME_STATES
                              ['CHARACTER_STATS']):
            help_text += "\nIf you've finished looking at yourself then"
            " 'return'."
        elif previous_state == (game_states.FIRST_LAYER_STATES
                                ['CHARACTER_CREATION']):
            help_text += "\n'Name'    : Type what you see on your arm to"
            "continue."
        elif previous_state == (game_states.FIRST_LAYER_STATES
                                ['ROOM_PICKUP_FIRST_LAYER']):
            help_text += "\n'Pick Up' : Pick the object up."
            help_text += "\n'Leave'   : Leave the object."
        elif previous_state == (game_states.FIRST_LAYER_STATES
                                ['ROOM_DOOR_CHOICE_FIRST_LAYER']):
            help_text += "\n'Left'    : Choose the left door."
            help_text += "\n'Right'   : Choose the right door."
        elif previous_state == (game_states.SECOND_LAYER_STATES
                                ['FIGHT_SECOND_LAYER']):
            help_text += "\n'Quick'   : Deftly strike with a quick attack."
            help_text += "\n'Heavy'   : Unleash a powerful heavy attack."
            help_text += "\n'Dodge'   : Focus on avoiding the next attack."
        help_text += "\n'Exit'    : Wake from the dream and return to"
        "reality."

        return help_text

    def handle_universal_commands(self, user_input, current_state,
                                  previous_state, character):
        """
        Handles universal commands that can be invoked in multiple game
        states.

        This method is responsible for managing the common commands that can
        be executed at various stages of the game. The recognised universal
        commands include:
        - 'help'  : Prints the help menu.
        - 'stats' : Displays the character's statistics if the name has been
                    initialised, and provides the option to 'return' to the
                    previous state.
        - 'exit'  : Exits the game.
        - 'return': Allows the player to return to the previous state from the
                    'help' or 'stats' screens.

        Parameters
        ----------
        user_input : str
            The input provided by the user.
        current_state : str
            The current state of the game, used to determine specific behavior
            in some commands.
        previous_state : str
            The previous state of the game, can be used in 'return' command to
            return to a previous game state.
        character : Character
            The character object for the player, used to handle
            character-specific commands.

        Returns
        -------
        str or None
            The next game state if a universal command is recognised and
            handled,
            or None if the user input does not correspond to a universal
            command.
        """
        if user_input == 'help':
            '''
            Store the current state as the previous state if it's not a
            'HELP' or 'CHARACTER_STATS' state
            '''
            self.previous_state = current_state if current_state not in (
                game_states.GENERAL_GAME_STATES
                ['HELP'],
                game_states.GENERAL_GAME_STATES
                ['CHARACTER_STATS']) else self.previous_state
            return game_states.GENERAL_GAME_STATES['HELP']
        elif user_input == 'stats' and character.name is not None:
            character.print_stats()
            self.previous_state = current_state if current_state not in (
                game_states.GENERAL_GAME_STATES['HELP'],
                game_states.GENERAL_GAME_STATES['CHARACTER_STATS']) \
                else self.previous_state
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

        Notes
        -----
        Whisper 'help' anytime in the game to view a list of commands.
        """
        utilities.display_intro(utilities.lines)
        self.state = game_states.FIRST_LAYER_STATES['GAME_START']

    def get_prompt(self):
        """
        Returns a prompt text based on the current state of the game.

        Depending on the game's current state, the method returns a string
        containing the appropriate prompt for the player. This can include
        various scenarios such as:
            - Prompting for help and displaying character stats.
            - Introducing the game and creating the character.
            - Choosing objects to pick up or leave.
            - Making navigation decisions between doors.
            - Initiating a fight with an enemy.

        Returns
        -------
        str
            A string containing the prompt text for the current game state.
            The text may include:
            - A help message if the state is 'HELP'.
            - A return or help option if the state is 'CHARACTER_STATS'.
            - An introductory challenge if the state is 'GAME_START'.
            - A character creation prompt if the state is
              'CHARACTER_CREATION'.
            - A decision-making scenario for objects if the state is
              'ROOM_PICKUP_FIRST_LAYER'.
            - A navigation decision between doors if the state is
              'ROOM_DOOR_CHOICE_FIRST_LAYER'.
            - A fight initiation prompt if the state is 'FIGHT_SECOND_LAYER'.
        """
        # PROMPT - GAME STATE = GENERAL - HELP
        if self.state == game_states.GENERAL_GAME_STATES['HELP']:
            return self.print_help(self.previous_state)
        # PROMPT - GAME STATE = GENERAL - CHARACTER STATS
        elif self.state == game_states.GENERAL_GAME_STATES['CHARACTER_STATS']:
            return ("\nIf you've finished looking at yourself then 'Return'"
                    " or ask for 'Help'")
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
                self.object_choice = (
                    random.choice(objects.OBJECTS_FIRST_LAYER))
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
            )
            return prompt_text

    def handle_input(self, user_input):
        """
        Processes user input based on the current game state.

        This method receives the user's input and takes the appropriate action
        based on the current game state. It calls specific handling methods
        that correspond to the current state of the game.

        Parameters
        ----------
        user_input : str
            The input provided by the user. Depending on the game state,
            different strings will be expected to perform various actions.
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
        Handles the state where the player is prompted to enter their
        character's name.

        This method processes the user's input for naming their character.
        The name must consist of alphabetic characters, not exceed 20
        characters, and not be 'exit'. If the input is valid, the
        character's name is set, stats are rolled, and the game progresses
        to the room pickup state.

        Parameters
        ----------
        user_input : str
            The input provided by the user. It must be a valid name
            consisting of alphabetic characters and not exceeding 20
            characters. If the input is 'exit' or contains non-alphabetic
            characters, a ValueError will be raised.

        Raises
        ------
        ValueError
            If the user input contains numbers or symbols, is empty, or
            exceeds 20 characters, this exception is raised, and an error
            message is printed to guide the player to input a valid name.
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

        This method processes the user's input for naming their character.
        The name must consist of alphabetic characters, not exceed 20
        characters, and not be 'exit'. If the input is valid, the character's
        name is set, and further actions may be taken based on the game logic.

        Parameters
        ----------
        user_input : str
            The input provided by the user. It must be a valid name consisting
            of alphabetic characters and not exceeding 20 characters. If the
            input is 'exit' or contains non-alphabetic characters, a
            ValueError will be raised.

        Raises
        ------
        ValueError
            If the user input contains numbers or symbols, is empty, or
            exceeds 20 characters, an error message is raised to guide
            the player to input a valid name.
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
        """
        Handles the room pickup state of the game.

        This method processes the user's input when they encounter an object
        that can be picked up. The player can either 'pick up' or 'leave' the
        object. If the user picks up the object, it may change the character's
        stats and mark the object as picked up, then transition to the room
        door choice state. If the player leaves the object, it transitions
        directly to the room door choice state. If the input is neither
        'pick up' nor 'leave', a ValueError is raised.

        Parameters
        ----------
        user_input : str
            The input provided by the user, expected to be either 'pick up' or
            'leave'. Other inputs will raise a ValueError.

        Raises
        ------
        ValueError
            If the user input is anything other than 'pick up' or 'leave',
            this exception is raised, and an error message is printed to
            guide the player.
        """
        try:
            if user_input == 'pick up':
                print("\nYour hand trembles as you approach the object,"
                      " memories and emotions swirling\n"
                      "within you.")

                # Compute the stat changes
                stat_changes = self.object_choice["stat_changes"]

                # Apply the stat changes to the character
                for stat, change in stat_changes.items():
                    setattr(self.character, stat.lower(),
                            getattr(self.character, stat.lower()) + change)
                    # Add the new change to any existing change for this stat
                    existing_change = self.character.stat_changes.get(stat, 0)
                    self.character.stat_changes[stat] = (existing_change +
                                                         change)

                self.character.weapon = self.object_choice
                print(f"As you grasp the {self.object_choice['name']}, you"
                      " feel its power infusing your very being:")
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
                raise ValueError("\n\nThe shadows whisper: 'Make a choice:"
                                 " 'Pick Up' or 'Leave'.")

        except ValueError as e:
            # Print the error message that was raised
            print(e)

    def handle_room_door_choice(self, user_input):
        """
        Handles the room door choice state of the game.

        This method processes the user's input when faced with a choice of
        doors to enter, either 'left' or 'right'. Upon making a valid choice,
        the player discovers a room, and the game transitions to the fight
        state. If the user's input is neither 'left' nor 'right', a ValueError
        is raised.

        Parameters
        ----------
        user_input : str
            The input provided by the user, expected to be either 'left' or
            'right'. Other inputs will raise a ValueError.

        Raises
        ------
        ValueError
            If the user input is anything other than 'left' or 'right', this
            exception is raised, and an error message is printed to guide the
            player.
        """
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
        """
        Handles the battle sequence between the player and an enemy.

        This method manages the turn-based combat between the player and an
        enemy, utilising the Fight class. It continues until one character is
        defeated. The battle includes actions such as 'quick' attack, 'heavy'
        attack, and 'dodge', and the user will be prompted for input if the
        player is the attacker.

        Parameters
        ----------
        player : Character
            The player's character, participating in the battle as one of the
            combatants.
        enemy : Character
            The enemy character, participating in the battle against the
            player.

        Notes
        -----
        The battle is conducted in turns, and the initiative is determined at
        the start. Both characters have hit points, and the battle continues
        until one of them reaches 0. The user's choices dictate the player's
        actions, while the enemy's actions are randomly chosen from the same
        set of actions. If the player's hit points reach 0, a defeat message
        is printed and the game resets. If the enemy's hit points reach 0, a
        victory message is printed.
        """
        # Create a Fight object
        fight = Fight()
        fight.dodge_flags[player] = False
        fight.dodge_flags[enemy] = False

        # Determine who goes first based on initiative
        current_attacker = fight.initiative(player, enemy)

        # Continue the fight until one of the characters is defeated
        while player.hit_points > 0 and enemy.hit_points > 0:
            # Get the user's choice if the player is the attacker
            if current_attacker == player:
                # Print player and enemy HP once at the start of the turn
                print(f"{player.name.capitalize()} HP: {player.hit_points},"
                      f" {enemy.name} HP: {enemy.hit_points}")
                # Reset user_input at the beginning of the users turn
                user_input = None
                # Keep asking until a valid input is entered
                while True:
                    user_input = input("Choose to 'quick' attack, 'heavy'"
                                       " attack, or 'dodge' the enemies"
                                       " attack: \n").lower()
                    print("\n" + utilities.return_divider())
                    if user_input in ['dodge', 'quick', 'heavy']:
                        break
                    else:
                        print()

                if user_input == 'dodge':
                    fight.dodge_flags[player] = True
                    print(f"\n{player.name.capitalize()} prepares to dodge the"
                          " next attack!")
                else:
                    fight.attack(
                        attacker=current_attacker,
                        defender=(player if current_attacker ==
                                  enemy else enemy),
                        attack_type=user_input,
                        defender_dodging=fight.dodge_flags[enemy]
                    )
                    fight.dodge_flags[player] = False
            else:
                # Enemy's turn
                enemy_action = random.choice(['quick', 'heavy', 'dodge'])
                if enemy_action == 'dodge':
                    fight.dodge_flags[enemy] = True
                    print(f"{enemy.name} prepares to dodge the next attack!")
                else:
                    fight.attack(
                        attacker=current_attacker,
                        defender=(player if current_attacker ==
                                  enemy else enemy),
                        attack_type=enemy_action,
                        defender_dodging=fight.dodge_flags[player]
                    )
                    fight.dodge_flags[enemy] = False

            # Switch attacker and defender for the next turn
            current_attacker = player if current_attacker == enemy else enemy
            # Reset dodge flags at the end of the turn
            fight.dodge_flags[player] = False
            fight.dodge_flags[enemy] = False
            # Check if the fight has ended
            prompt_text = ""

            if enemy.hit_points <= 0:
                prompt_text = (
                    "\nExhausted and panting after the intense battle,"
                    " you take a moment to catch your\n"
                    "breath.\n"
                    "The room falls silent except for the distant echoes of"
                    " the dungeon, and your\n"
                    "mind begins to wander.\n"
                    "Slowly, your eyes close, and you feel a strange pull"
                    " towards the beginning,\nas if the very fabric "
                    "of this place is beckoning you to start anew."
                )
            elif player.hit_points <= 0:
                prompt_text = (
                    "Struggling to maintain your stance, you see"
                    f"the {enemy.name} preparing for\n"
                    "one last attack.\n"
                    "Before you can react, a fatal blow lands,"
                    " darkens around you.\n"
                    "The last thing you hear is the triumphant cackle of your"
                    " foe as you slip away,\ndefeated and broken."
                )
            self.reset_game()
            print(prompt_text)
            self.state = (game_states.FIRST_LAYER_STATES
                          ['CHARACTER_CREATION']
                          if fight.check_death(enemy) else
                          game_states.FIRST_LAYER_STATES
                          ['CHARACTER_CREATION'])


game = Game()
game.run()

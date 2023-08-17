# Subterraneon Script

The project, "Subterranean Script," is my innovative approach to the text-based, choice-driven adventure genre, deeply rooted in the spirit of iconic Choose-Your-Own-Adventure books. It adds a unique twist by plunging players into a sprawling, enigmatic dungeon world, with their destiny dictated by the doors they elect to pass through.

Drawing inspiration from the rich tradition of Dungeons & Dragons, Subterranean Script incorporates a series of well-established rules and mechanics from the legendary tabletop game. This blend of elements aims to enrich the gameplay experience, inviting players to engage with a complex web of decisions that mirror a D&D campaign's depth and dynamism.

At its core, Subterranean Script aims to capture players with its layered, immersive narrative and dynamic choice-driven gameplay, challenging their decision-making skills at every turn. It is meticulously crafted for those who appreciate the immersive allure of traditional text-based games but crave an additional level of interactive mystery and suspense, reminiscent of a well-rounded D&D adventure.

<details>
<summary><h2>User Experience Design (UXD)</h2></summary>

<details>
<summary><h3>Strategy</h3></summary>

<details>
<summary><h4>User Stories</h4></summary>

##### First Time Visitor Goals #####
##### Understanding Gameplay: #####
As a First Time user, I want to easily understand the main concept of the game and its gameplay mechanics.
##### Navigating Commands: #####
As a First Time user, I want to be able to effortlessly navigate through the game commands and decision-making processes.
##### Experiencing Narrative: #####
As a First Time user, I want to experience a compelling introduction to the game world and its narrative.

##### Returning Visitor Goals #####
##### Exploring New Content: #####
As a Returning user, I want to find and explore new paths, narratives, and experiences within the game that deepen my immersion.
##### Understanding Consequences: #####
As a Returning user, I want to see the consequences of my previous choices and understand how they shape my current gameplay.
##### Varied Experiences: #####
As a Returning user, I want the ability to reset the game or make different decisions, enabling varied experiences and outcomes.

#### Frequent Visitor Goals ####
##### Ongoing Adventure: #####
As a Frequent user, I want to continue my ongoing adventure, with the game storing my progress.
##### Updates and Developments: #####
As a Frequent user, I want to see if there are any new updates or developments in the game’s narrative or mechanics.
##### Social Interaction: #####
As a Frequent user, I want to share my gaming experience with others or compare my decisions and game outcomes with them.
</details>

<details>

<summary><h4>CLI Owner Goals</h4></summary>

##### Engaging Gameplay: #####
As a Command Line Application Owner, I want to offer an intuitive and immersive text-based adventure game that engages users and draws them into its narrative world.
##### User Notification: #####
As a Command Line Application Owner, I want to notify users of new game content or changes, keeping them interested and up-to-date.
##### Gathering Feedback: #####
As a Command Line Application Owner, I want to gather user feedback and experiences, which can be used to refine and expand the game.
##### Community Building: #####
As a Command Line Application Owner, I want to build a community of engaged players who are invested in the game's world and narrative.
##### Showcasing Creativity: #####
As a Command Line Application Owner, I want to be able to showcase the creative team behind the game, to promote their work and foster a deeper connection with the player base.
</details>

<details>
<summary><h4>Strategy Tradeoffs</h4></summary>

![Subterranean Script Tradeoff Table](assets/images/readme/uxd/strategy/subterranean_scipt_strategy-tradeoffs-table.png)

![Subterranean Script Tradeoff_Graph](assets/images/readme/uxd/strategy/subterranean_scipt_strategy_tradeoffs_graph.png)
</details>
</details>

<details>
<summary><h3>Scope</h3></summary>

#### Sprint 1 Features ####
- Intro to game
- Player can pick up weapon
- Player can choose a door to progress
- Player can fight an enemy
- Help text to educate the player
#### Sprint 1 Requirement Types ####
- Languages: Python
- Library: [Colorma](https://pypi.org/project/colorama/)

#### Sprint 2 Features ####
- Longer game with more choices
- Sound such as music and attack sounds
#### Sprint 2 Requirement Types ####
- Languages: Python
- Library: [PyAudio](https://pypi.org/project/PyAudio/)

#### Sprint 3 Features ####
- Ability to save
- Adaptive difficulty levels
- Player choices affect other people's games
- Social mnedia presense
- Monetisation
#### Sprint 3 Requirement Types ####
- Languages: Python
</details>

<details>
    <summary><h3>Structure</h3></summary>

Touchpoints - Command Line Interface

![Subterranean Script Information Architecture](assets/images/readme/uxd/structure/subterranean_script-information-architecture.png)

Whilst the player has the choice of left and right, this choice will be populated by a dictionary. This design will help for expansion in later scripts. In the first sprint I plan to have the first room and then a choice to enter the second room, but this diagram is an example of how it would be in the future.
</details>

<details>
    <summary><h3>Surface</h3></summary>

Colours will be based on the [Colorma](https://pypi.org/project/colorama/) library. They will be used to add to the atmosphere of the game.


<summary><h4>Technologies Used</h4></summary>

<details>
<summary><h5>Language</h5></summary>

- Python

</details>

<details>
<summary><h5>Websites, Software & other Tools</h5></summary>

- [Codeanywhere](https://codeanywhere.com/solutions/collaborate) This is was my IDE for the project.
- [CodePen](codepen.io) I used this to test code outside of [Codeanywhere](https://codeanywhere.com/solutions/collaborate) so that I didn't use up hours unnecessarily.
- [Git](https://git-scm.com/) Used to commit and push code to [Github](https://github.com/).
- [Github](https://github.com/) This was used as a remote repository.
- [Heroku](https://heroku.com) I used this to deploy my app.
- [PEP - Python](https://peps.python.org/pep-0008/) This was used to learn more about PEP-8.
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) Used to learn and stick to a conventional commit framework.
- [Photoshop](https://www.adobe.com/uk/products/photoshop.html) Used for readme images.
- [Python Docs](https://docs.python.org/3/) Used to learn more about Python.

</details>
</details>
</details>

<details>

<summary><h2>Features</h2></summary>

<details>

<summary><h3>Start Screen</h3></summary>

The Start Screen State serves as the introduction and entry point to the text-based adventure game "Subterranean Script." It's a combination of two phases that guide the player into the game world.

Initialisation Phase (handle_initialise method): This part displays the game's visually engaging ASCII title and presents a welcome message, providing players with a glimpse into the game's mysterious dungeon environment. It hints at the choice-driven nature of the game, inspiring comparisons to classic Choose-Your-Own-Adventure books and Dungeons & Dragons. It also informs the player that they can whisper 'help' at any time to view a list of commands. After presenting this information, the game transitions to the start state.

Start State (handle_start_state method): This state handles the next stage where the player is prompted to enter the game. The player must type 'enter' to proceed, reinforcing the thematic atmosphere of stepping into a dark and unknown world. If the input is valid, a foreboding message wishing the player "Good luck" is displayed, and the game moves to the character creation state. If the player enters anything other than 'enter,' a ValueError is raised, and the shadow-themed error message is printed to guide the player.

Together, these two stages form a cohesive starting experience, introducing players to the tone, setting, and mechanics of the game. The Start Screen State not only welcomes players but also challenges them to take the first step into an adventure filled with choices, mysteries, and uncertainties.

![Start Screen](assets/images/readme/features/start-of-battle-state.png)

</details>

<details>

<summary><h3>Name Input State</h3></summary>

The Name Input State is a critical stage in the game where the player is prompted to name their character. This state provides an opportunity for personalisation, setting the tone for the player's relationship with their character.

Valid Name Input: The player must enter a name consisting solely of alphabetic characters, not exceeding 20 characters, and not being 'exit'. If these conditions are met, the character's name is assigned, followed by a reflective print statement that appears to come from the character itself. The game then proceeds to roll and print the character's stats before transitioning to the room pickup state.

Invalid Name Input: If the player's input contains non-alphabetic characters or exceeds 20 characters, a ValueError is raised with an in-game themed error message to guide the player towards a valid name.

By weaving game mechanics with storytelling elements, the Name Input State establishes a connection between the player and their character while maintaining the immersive atmosphere of the game. It ensures that the character naming process is not only a functional requirement but also a meaningful step in the player's journey within the game world.

![Name Input](assets/images/readme/features/player-name-input.png)

</details>

<details>

<summary><h3>Pick Up Object State</h3></summary>

The Pick Up Object State manages the gameplay scenario when a player encounters an object they can collect. In this state, the player is faced with the choice to either 'pick up' or 'leave' the object.

![Pick Up Object](assets/images/readme/features/example-of-object-choice.png)

If the player chooses to 'pick up': The method processes a series of actions, such as making the object part of the character's stats and marking it as picked up. An emotional description is printed to engage the player, and the game transitions to the room door choice state.

![Stat Change](assets/images/readme/features/example-of-stat-change.png)

If the player decides to 'leave': A message is printed reflecting the character's resolve, and the game moves directly to the room door choice state.

For any other input: A ValueError is raised, accompanied by an error message guiding the player to make a valid choice.

This state intricately ties the player's decisions with the game's mechanics and storytelling, enhancing immersion and strategic planning.

</details>

<details>

<summary><h3>Choose Door State</h3></summary>

The Room Door Choice State represents a crucial juncture in the game where players are faced with the decision to choose between two doors: 'left' or 'right'. This moment encapsulates the essence of choice-driven gameplay, embodying the adventure's core mechanic of branching paths and the unknown consequences that lie beyond each decision.

Making a Choice: The player's input is processed, expected to be either 'left' or 'right'. The chosen direction determines the room they will discover, randomly selected from a predefined set of dungeon areas.

Discovering a Room: Upon making a valid choice, the player's chosen door opens to reveal a room with a specific name and description. This provides flavor text to the scenario, immersing the player in the mysterious dungeon environment and setting the stage for the next challenge.

Transition to the Fight State: The door choice state also includes a prompt that segues into the fight state, the next phase of gameplay where players must confront challenges within the room they've discovered.

Error Handling: If the player's input is anything other than 'left' or 'right', a ValueError is raised, and an atmospheric error message is printed to guide the player. This guidance, framed within the game's shadowy and mystical theme, maintains immersion even in the face of an incorrect choice.

The Room Door Choice State serves as a metaphorical crossroads within "Subterranean Script." It challenges players to make decisions without knowing what lies ahead, echoing the unpredictable and mysterious nature of the game's dungeon environment. By integrating thematic storytelling, user choice, and a transition to further gameplay challenges, this state effectively builds tension and engagement, keeping players invested in their adventure.

![Pick Up Object](assets/images/readme/features/example-door-choice.png)

</details>

<details>

<summary><h3>Battle State/h3></summary>

The Battle State within "Subterranean Script" is an intense and dynamic part of the game that pits the player's character against an enemy in a turn-based combat scenario. This state encapsulates the heart-pounding action of the dungeon experience, providing an engaging gameplay loop that challenges the player's decision-making and strategy.

Initialisation: A Fight object is created, and the initiative (who attacks first) is determined between the player and the enemy. Dodge flags are set to False at the beginning, meaning no one is prepared to dodge.

![Start Of Battle State](assets/images/readme/features/start-of-battle-state.png)

Turn-Based Combat: The battle ensues in turns until either the player or the enemy's hit points reach 0.

Player's Turn: If the player is the attacker, they are prompted to choose between 'quick' attack, 'heavy' attack, or 'dodge'. Each choice has implications for the attack's success, damage dealt, and the likelihood of dodging an incoming attack.
Enemy's Turn: If the enemy is the attacker, a random choice is made between the same set of actions ('quick', 'heavy', 'dodge'), and the chosen action is executed.
Attack Mechanics: The attack method within the Fight class is called to resolve the combat action. The attack's success and damage depend on the type of attack and whether the defender is dodging.

Dodge Mechanics: Both players and enemies can choose to dodge an attack. If successful, this move prevents damage in the following attack. Dodge flags are used to track whether a character is prepared to dodge.

![Dodge Mechanic](assets/images/readme/features/example-of-dodge-and-taking-damage-in-battle-state.png)

Switching Turns: After each turn, the attacker and defender switch roles, and the dodge flags are reset.

Resolution and Transitions: When the battle ends, victory or defeat messages are printed based on the outcome. Thematic flavor text conveys the aftermath of the battle, enhancing immersion.

Victory: If the enemy is defeated, a victory message emphasises the intensity of the battle and hints at the mysterious nature of the dungeon.
Defeat: If the player is defeated, a defeat message conveys the dramatic end and the triumph of the enemy.
Game Reset: After the fight concludes, the game resets, and the player is transitioned back to the character creation state, allowing them to start anew.

![Attack And Game Reset](assets/images/readme/features/example-of-dealing-damage-winning-fight-and-game-loop.png)

The Battle State's complexity and depth lie in the interplay between choice and randomness, strategy, and adaptability. By weaving together mechanics of attack, dodge, and turn-based dynamics, this state creates a thrilling and unpredictable combat experience. The detailed feedback and atmospheric text further deepen the immersion, making each battle a memorable and integral part of the overall dungeon adventure.

</details>

<details>

<summary><h3>Help and Universal Commands</h3></summary>

Within "Subterranean Script," the player might need guidance on their available options or access to certain universal commands that are applicable across different game states. These functionalities are managed by two distinct methods: print_help and handle_universal_commands.

1. Help State (print_help method)
The Help State provides contextual assistance to players, offering tailored guidance based on the current and previous states of the game.

Basic Structure: The method begins with a thematic introduction, signaling that the player is seeking assistance from the shadows of the dungeon. It then provides general commands like 'Return' and 'Exit'.
Contextual Guidance: Depending on the player's location or situation within the game, specific commands and information are provided. These might include navigation options, combat actions, character creation instructions, etc.
Return to Gameplay: The help text encourages players to 'Return' to resume their previous action or to explore additional options pertinent to their current situation.
The help text effectively serves as a dynamic guide, adjusting its content to match the player's needs at any given point in the game.

![Help State](assets/images/readme/features/example-of-help-state.png)

2. Universal Commands State (handle_universal_commands method)
The Universal Commands State handles common commands that can be invoked in various game states, adding consistency and flexibility to the player's control scheme. The recognised universal commands include:

- 'help': Transitions to the Help State, where players receive information on available commands based on their current situation.
- 'stats': If the player's name has been initialised, this command displays the character's statistics and provides the option to 'return' to the previous state.
![Stat State](assets/images/readme/features/example-of-stat-state.png)
- 'exit': Allows the player to exit the game with a thematic farewell message.
- 'return': Enables the player to return to the previous state from the 'help' or 'stats' screens, ensuring a smooth navigation experience.

These universal commands add an extra layer of accessibility and usability, allowing players to call upon essential functions from nearly any point in the game.

</details>

<details>

<summary><h3>Scalable</h3></summary>

The scalability of the project is largely derived from the thoughtful use of data structures, such as dictionaries to contain entities like enemies and dungeon areas, and classes to represent characters and enemies. By organising data into well-defined structures, it will easier to manage, expand, and modify various aspects of the game, as detailed below:

1. Integration with Classes:
My project's use of classes for character and enemy modelling complements the dictionary-based approach. Classes encapsulate behaviours, making it easy for me to define how characters interact with objects or enemies. By combining classes with rich data structures, I've set the project to offer seamless integration of content and logic, making the system adaptable and scalable.

2. Making Enemies Feel Different:
The current structure of the enemy dictionary sets the stage for customisation, allowing for further differentiation among enemies. Here's how I can accomplish this:

Behavioural Patterns: By implementing different AI behaviours or attack patterns for various enemy types, I can create a more diversified combat experience. This can be done by adding methods to the enemy class or adding attributes to the dictionary that describe specific actions or responses in given situations.

Visual Representation: I can associate different sprites or visual effects with different enemies. By linking an image or visual identifier to each enemy in the dictionary, I can render unique appearances for each creature quickly.

Sound Effects: Integrating unique sounds for different enemies can enhance the immersive experience. Associating specific audio files or sound effects with particular enemies in the dictionary can achieve this.

Special Abilities: Introducing unique abilities or special attacks for specific enemies can make encounters more engaging. Adding an "abilities" list to the enemy dictionaries and implementing corresponding methods in the enemy classes will allow for this differentiation.

3. Room Definition:
Another use of dictionaries can be found in defining the dungeon's rooms within my project. I've structured the ROOMS dictionary in layers, with each room possessing specific attributes like "name," "description," and "prompt." This layered approach enables me to add new rooms or modify existing ones easily, allowing for the dynamic scaling of the dungeon as the game evolves.

4. Object Management:
I've also used dictionaries to manage objects that can be found in different layers of the dungeon. These objects have specific attributes like "name" and "description," and even stat changes, making them vital to the gameplay. By organising these objects within dictionaries, I've made it simple to add new items or modify existing ones without altering the core game code.

</details>

</details>
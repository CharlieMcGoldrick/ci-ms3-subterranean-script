def start_game():
    """
    Initiates the game by prompting the user to enter 'enter' or 'Enter'. 
    If a different input is received, a ValueError is raised and the prompt 
    is shown again. If 'exit' is entered, a farewell message is printed and 
    the game is terminated. If 'enter' or 'Enter' is entered, a game 
    introduction message is printed and the `enter_name()` function is called.
    """
    while True:
        user_input = input("")
        if user_input.lower() == 'exit':
            print()
            print("\nMaybe it's all just a dream...")
            return
        try:
            if user_input not in ['enter', 'Enter']:
                raise ValueError("Are you lost? Type 'enter' or 'Enter'.")
            else:
                print()
                print("Awakening in a room, a sense of déjà vu strikes you...")
                print("Have you visited this place before?")
                print("A shroud of darkness wraps the space, its cold grip only")
                print("punctuated by the echoing drip of water against stone walls.")
                print("In the feeble light, an inscription comes to view on")
                print("your arm, etched crudely by an apparent blade.")
                # Correct input breaks the while loop and the game starts
                break
        except ValueError as e:
            print(str(e))


while True:
    print("           __       _     _                                           ")
    print("          / _\_   _| |__ | |_ ___ _ __ _ __ ___  __ _ _ __            ")
    print("          \ \| | | | '_ \| __/ _ \ '__| '__/ _ \/ _` | '_ \           ")
    print("          _\ \ |_| | |_) | ||  __/ |  | | |  __/ (_| | | | |          ")
    print("          \__/\__,_|_.__/ \__\___|_|  |_|  \___|\__,_|_| |_|          ")
    print("                      __           _       _                          ")
    print("                     / _\ ___ _ __(_)_ __ | |_                        ")
    print("                     \ \ / __| '__| | '_ \| __|                       ")
    print("                     _\ \ (__| |  | | |_) | |_                        ")
    print("                     \__/\___|_|  |_| .__/ \__|                       ")
    print("                                    |_|                               ")
    print("                                                                      ")
    print("            Welcome to the depths of 'Subterranean Script'!           ")
    print("          This is a text-based, choice-driven adventure game.         ")
    print("            Navigate through the all-encompassing darkness            ")
    print("           where every door opens a new path, a new destiny.          ")
    print("                                                                      ")
    print("        Note: Whisper 'help' anytime to conjure the command list      ")
    print("                                                                      ")
    print("        Ready to step into the unknown? Type 'Enter' if you dare      ")


    start_game()


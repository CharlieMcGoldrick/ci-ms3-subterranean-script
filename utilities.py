from colorama import Fore, Back, Style, init
init()

# Ascii and intro
lines = [
    " __       _     _                                                    ",
    "/ _\\_   _| |__ | |_ ___ _ __ _ __ __ _ _ __   ___  __ _ _ __        ",
    "\\ \\| | | | '_ \\| __/ _ \\ '__| '__/ _` | '_ \\ / _ \\/ _` | '_ \\ ",
    "_\\ \\ |_| | |_) | ||  __/ |  | | | (_| | | | |  __/ (_| | | | |     ",
    "\\__/\\__,_|_.__/ \\__\\___|_|  |_|  \\__,_|_| |_|\\___|\\__,_|_| |_|",
    " __            _       _                                             ",
    "/ _\\ ___ _ __(_)_ __ | |_                                           ",
    "\\ \\ / __| '__| | '_ \\| __|                                        ",
    "_\\ \\ (__| |  | | |_) | |_                                          ",
    "\\__/\\___|_|  |_| .__/ \\__|                                        ",
    "               |_|                                                   ",
    "                                                                     ",
    "Welcome to the depths of 'Subterranean Script'!                      ",
    "This is a text-based, choice-driven adventure game,                  ",
    "inspired by classic Choose-Your-Own-Adventure books.                 ",
    "and D&D. Navigate through the all-encompassing darkness              ",
    "of the mysterious dungeon environment, where every door              ",
    "opens a new path, a new destiny.                                     ",
    "Whisper 'help' anytime to conjure the command list.                  "
]


def display_intro(lines):
    """
    Display the introductory lines for the game, aligned and color-coded.

    This function takes a list of strings representing the game's
    introductory text, including ASCII art, and prints them to the console.
    The lines are left-aligned and printed in red using the colorama package.

    Args:
        lines (List[str]): A list of strings representing the introductory
        text.
    """
    # Find the maximum length of the lines
    max_length = max(len(line) for line in lines)

    # Print each line with a background color
    for line in lines:
        # Fill the line with spaces to the maximum length
        filled_line = line.ljust(max_length)
        # Print with the desired foreground and background colors
        print(Fore.RED + filled_line)


# Divider
def return_divider():
    return Back.RED + Fore.RED + "-" * 80 + Style.RESET_ALL


# HP TYPE MODIFIERS
HP_TYPE_MODIFIERS = {
    "hero": 30,
    "beast": 5,
    "humanoid": 3,
    "spirit": 2,
    "undead": 4,
    "wraith": 1,
    "aquatic": 6,
}

# AC Type Modifiers
AC_TYPE_MODIFIERS = {
    "hero": 2,
    "beast": 1,
    "humanoid": 0,
    "spirit": -1,
    "undead": 3,
    "wraith": 4,
    "aquatic": 1,
}

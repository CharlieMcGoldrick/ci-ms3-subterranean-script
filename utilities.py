from colorama import Fore, Back, Style, init
init()


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

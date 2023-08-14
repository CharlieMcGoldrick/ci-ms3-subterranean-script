from colorama import Fore, Back, Style, init
init()


# Divider
def return_divider():
    return Back.RED + Fore.RED + "-" * 80 + Style.RESET_ALL


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
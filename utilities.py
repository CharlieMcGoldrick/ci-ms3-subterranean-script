from colorama import Fore, Back, Style, init
init()


def return_divider():
    return Back.RED + Fore.RED + "-" * 80 + Style.RESET_ALL

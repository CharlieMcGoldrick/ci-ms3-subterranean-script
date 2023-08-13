import objects
from colorama import Fore, Back, Style, init
# init colorama
init()

entering_room_flavour_text = (
    "a chill runs down your spine. The ominous\n"
    "creaking of metal reverberates  through the air,"
    " and with a thunderous crash,\n"
    "bars slide down, sealing the doors behind you shut.\n"
    "\nYour heart pounds in your chest as you notice two other doors in the"
    " shadowy\n"
    "corners of the room, only to watch as they too are sealed shut"
    " by sliding\n"
    "metal bars."
)

ROOMS_SECOND_LAYER = [
    {
        "name": "torture chamber",
        "description": ("A grim room filled with instruments of pain and"
                        " torment, echoes of past\n"
                        "suffering linger in the air."),
        "prompt": (f"\nAs you step into the chamber,"
                   f"{entering_room_flavour_text}")
    },
    {
        "name": "alchemist's lab",
        "description": ("Shelves lined with mysterious potions and alchemical"
                        " tools.\n"
                        "The scent of strange chemicals fills the room."),
        "prompt": (f"\nAs you step into the lab,"
                   f"{entering_room_flavour_text}")
    },
    {
        "name": "guard barracks",
        "description": ("A room containing bunks and personal belongings of"
                        " the dungeon's guards.\n It's eerily quiet."),
        "prompt": (f"\nAs you step into the barracks,"
                   f"{entering_room_flavour_text}")
    },
    {
        "name": "crypt of forgotten souls",
        "description": ("A dimly lit crypt, filled with ancient coffins and"
                        " marked by an unsettling\nstillness."),
        "prompt": (f"\nAs you step into the crypt,"
                   f"{entering_room_flavour_text}")
    },
    {
        "name": "underground lake",
        "description": ("A subterranean lake, its dark waters reflecting"
                        " the flicker of distant torches.\n"
                        "Something moves beneath the surface."),
        "prompt": (f"\nAs you step into the cavern,"
                   f"{entering_room_flavour_text}")
    }
]

ROOMS = {
    'first_layer': {
        'starting_room': {
            'object_choices': objects.OBJECTS_FIRST_LAYER,
            'door_choices': ['left', 'right'],
            'flavor_text_intro': (
                "\nAwakening in a room, a sense of déjà vu strikes you...\n"
                "Have you visited this place before?\n"
                "A shroud of darkness wraps the space, its cold grip only\n"
                "punctuated by the echoing drip of " + Fore.WHITE + Back.BLUE +
                "water" + Fore.RESET + Back.RESET + " against stone walls.\n"
                "In the feeble light, an inscription comes to view on your"
                " arm,\n"
                + Fore.WHITE + Back.RED + "etched" + Fore.RESET + Back.RESET +
                " crudely by an apparent blade.\n"
            ),
        },
    },
    'second_layer': {
        'rooms': ROOMS_SECOND_LAYER,
        'object_choices': objects.OBJECTS_SECOND_LAYER,
        'door_choices': ['left', 'right'],
        'flavor_text': "You find yourself in a new room...",
    },
}

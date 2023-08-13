import objects

ROOMS_SECOND_LAYER = [
    {
        "name": "Torture Chamber",
        "description": ("A grim room filled with instruments of pain and"
                        "torment, echoes of past suffering linger in the air.")
    },
    {
        "name": "Alchemist's Lab",
        "description": ("Shelves lined with mysterious potions and alchemical"
                        " tools. The scent of strange chemicals fills the"
                        " room.")
    },
    {
        "name": "Guard Barracks",
        "description": ("A room containing bunks and personal belongings of"
                        " the dungeon's guards. It's eerily quiet.")
    },
    {
        "name": "Crypt of Forgotten Souls",
        "description": ("A dimly lit crypt, filled with ancient coffins and"
                        " marked by an unsettling stillness.")
    },
    {
        "name": "Underground Lake",
        "description": ("A subterranean lake, its dark waters reflecting"
                        " the flicker of distant torches. Something moves"
                        " beneath the surface.")
    }
]

ROOMS = {
    'first_layer': {
        'starting_room': {
            'object_choices': objects.OBJECTS_FIRST_LAYER,
            'door_choices': ['left', 'right'],
            'flavor_text_intro': (
                "A strange chill fills the room, and your eyes are drawn to a"
                " faint glow. Upon closer inspection, it's a {weapon_name}"
                " lying at your feet. {weapon_description}"
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

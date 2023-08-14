ENEMIES = {
    "common_enemies": [
        {
            "name": "Dungeon Rat",
            "entity_type": "beast",
            "strength": 2,
            "dexterity": 3,
            "constitution": 2,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 1,
            "weapon": {
                "name": "teeth",
                "description": "Sharp little teeth."
            }
        },
        {
            "name": "Cave Spider",
            "entity_type": "beast",
            "strength": 3,
            "dexterity": 5,
            "constitution": 3,
            "intelligence": 1,
            "wisdom": 2,
            "charisma": 1,
            "weapon": {
                "name": "venomous bite",
                "description": "A bite that injects painful venom."
            }
        },
        {
            "name": "Dungeon Goblin",
            "entity_type": "humanoid",
            "strength": 4,
            "dexterity": 4,
            "constitution": 4,
            "intelligence": 2,
            "wisdom": 2,
            "charisma": 2,
            "weapon": {
                "name": "crude club",
                "description": "A simple and roughly-made wooden club."
                }
        }
    ],
    "torture chamber": {
        "name": "Tortured Spirit",
        "entity_type": "spirit",
        "strength": 4,
        "dexterity": 4,
        "constitution": 3,
        "intelligence": 3,
        "wisdom": 5,
        "charisma": 1,
        "weapon": {
            "name": "ethereal chains",
            "description": "Ethereal chains that bind and choke."
        }
    },
    "alchemist's lab": {
        "name": "Mutated Alchemist",
        "entity_type": "humanoid",
        "strength": 3,
        "dexterity": 4,
        "constitution": 5,
        "intelligence": 6,
        "wisdom": 4,
        "charisma": 2,
        "weapon": {
            "name": "potion bombs",
            "description": "Explosive concoctions with various effects."
        }
    },
    "guard barracks": {
        "name": "Undead Guard",
        "entity_type": "undead",
        "strength": 5,
        "dexterity": 3,
        "constitution": 4,
        "intelligence": 2,
        "wisdom": 2,
        "charisma": 1,
        "weapon": {
            "name": "rusty sword",
            "description": "A sword worn with age and neglect."
        }
    },
    "crypt of forgotten souls": {
        "name": "Restless Wraith",
        "entity_type": "wraith",
        "strength": 3,
        "dexterity": 5,
        "constitution": 3,
        "intelligence": 4,
        "wisdom": 5,
        "charisma": 4,
        "weapon": {
            "name": "chill touch",
            "description": "A ghostly touch that freezes the soul."
        }
    },
    "underground lake": {
        "name": "Water Horror",
        "entity_type": "aquatic",
        "strength": 6,
        "dexterity": 3,
        "constitution": 5,
        "intelligence": 2,
        "wisdom": 1,
        "charisma": 1,
        "weapon": {
            "name": "tentacles",
            "description": "Long, slimy tentacles that grab and constrict."
        }
    }
}

# Extracting the common enemies
COMMON_ENEMIES = ENEMIES["common_enemies"]

# Extracting the specific enemies
SPECIFIC_ENEMIES = {
    "torture chamber": ENEMIES["torture chamber"],
    "alchemist's lab": ENEMIES["alchemist's lab"],
    "guard barracks": ENEMIES["guard barracks"],
    "crypt of forgotten souls": ENEMIES["crypt of forgotten souls"],
    "underground lake": ENEMIES["underground lake"]
}

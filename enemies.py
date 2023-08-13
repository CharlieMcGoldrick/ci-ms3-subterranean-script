ENEMIES = {
    "common_enemies": [
        {
            "name": "Dungeon Rat",
            "strength": 2,
            "dexterity": 3,
            "constitution": 2,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 1,
            "weapon": {
                "name": "Teeth",
                "description": "Sharp little teeth."
            }
        },
        {
            "name": "Cave Spider",
            "strength": 3,
            "dexterity": 5,
            "constitution": 3,
            "intelligence": 1,
            "wisdom": 2,
            "charisma": 1,
            "weapon": {
                "name": "Venomous Bite",
                "description": "A bite that injects painful venom."
            }
        },
        {
            "name": "Dungeon Goblin",
            "strength": 4,
            "dexterity": 4,
            "constitution": 4,
            "intelligence": 2,
            "wisdom": 2,
            "charisma": 2,
            "weapon": {
                "name": "Crude Club",
                "description": "A simple and roughly-made wooden club."
                }
        }
    ],
    "torture chamber": {
        "name": "Tortured Spirit",
        "strength": 4,
        "dexterity": 4,
        "constitution": 3,
        "intelligence": 3,
        "wisdom": 5,
        "charisma": 1,
        "weapon": {
            "name": "Chains",
            "description": "Ethereal chains that bind and choke."
        }
    },
    "alchemist's lab": {
        "name": "Mutated Alchemist",
        "strength": 3,
        "dexterity": 4,
        "constitution": 5,
        "intelligence": 6,
        "wisdom": 4,
        "charisma": 2,
        "weapon": {
            "name": "Potion Bombs",
            "description": "Explosive concoctions with various effects."
        }
    },
    "guard barracks": {
        "name": "Undead Guard",
        "strength": 5,
        "dexterity": 3,
        "constitution": 4,
        "intelligence": 2,
        "wisdom": 2,
        "charisma": 1,
        "weapon": {
            "name": "Rusty Sword",
            "description": "A sword worn with age and neglect."
        }
    },
    "crypt of forgotten souls": {
        "name": "Restless Wraith",
        "strength": 3,
        "dexterity": 5,
        "constitution": 3,
        "intelligence": 4,
        "wisdom": 5,
        "charisma": 4,
        "weapon": {
            "name": "Chill Touch",
            "description": "A ghostly touch that freezes the soul."
        }
    },
    "underground lake": {
        "name": "Water Horror",
        "strength": 6,
        "dexterity": 3,
        "constitution": 5,
        "intelligence": 2,
        "wisdom": 1,
        "charisma": 1,
        "weapon": {
            "name": "Tentacles",
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
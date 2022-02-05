import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""

test_data = {
    "game": {
        "id": "game-00fe20da-94ad-11ea-bb37",
        "ruleset": {"name": "standard", "version": "v.1.2.3"},
        "timeout": 500,
    },
    "turn": 14,
    "board": {
        "height": 11,
        "width": 11,
        "food": [{"x": 5, "y": 5}, {"x": 9, "y": 0}, {"x": 2, "y": 6}],
        "hazards": [{"x": 3, "y": 2}],
        "snakes": [
            {
                "id": "snake-508e96ac-94ad-11ea-bb37",
                "name": "My Snake",
                "health": 54,
                "body": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}],
                "latency": "111",
                "head": {"x": 0, "y": 0},
                "length": 3,
                "shout": "why are we shouting??",
                "squad": "",
                "customizations": {
                    "color": "#FF0000",
                    "head": "pixel",
                    "tail": "pixel",
                },
            },
            {
                "id": "snake-b67f4906-94ae-11ea-bb37",
                "name": "Another Snake",
                "health": 16,
                "body": [
                    {"x": 0, "y": 1},
                    {"x": 5, "y": 3},
                    {"x": 6, "y": 3},
                    {"x": 6, "y": 2},
                ],
                "latency": "222",
                "head": {"x": 5, "y": 4},
                "length": 4,
                "shout": "I'm not really sure...",
                "squad": "",
                "customizations": {
                    "color": "#26CF04",
                    "head": "silly",
                    "tail": "curled",
                },
            },
        ],
    },
    "you": {
        "id": "snake-508e96ac-94ad-11ea-bb37",
        "name": "My Snake",
        "health": 54,
        "body": [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}],
        "latency": "111",
        "head": {"x": 0, "y": 0},
        "length": 3,
        "shout": "why are we shouting??",
        "squad": "",
        "customizations": {"color": "#FF0000", "head": "pixel", "tail": "pixel"},
    },
}

attack_lines = [
    "Get your stinking paws off me you damn dirty ape!",
    "It's tail time!",
    "YYYEEESSS!",
    "That's for 12 years of Full House!",
    "Now, that's what I call getting some tail.",
    "All right! It's tail time!",
    "My tail's gonna kick your butt!",
    "Time to go postal!",
    "Say hello to the floor!",
    "Put that in your pipe and smoke it.",
    "I'm doing this for you!",
    "Gecko-chop baby yeah!",
    "Gecko-chop baby!",
    "Karate-chop!",
    "Watch me use my tail to kick your butt.",
    "This is for Mr. Sinatra.",
    "You're nothing see, you're nothing!",
    "I'll give you such a pinch!",
    "Move like a butterfly sting like a gecko!",
    "This is for all the angels in heaven.",
    "Eat this!",
    "File this under 'ouch'!",
    "Judo-chop baby!",
    "Judo-chop baby yeah!",
]

eating_lines = [
    "Mmmm... buttery.",
    "Tastes are licking and...ehhhhhhh we heard it.",
    "Spock, load the tongue.",
    "Burp!",
    "That's the sweet stuff darling.",
    "Mmm... TVs instead of potatoes.",
    "All right that's the spot.",
]


possible_moves = ["up", "down", "left", "right"]


def derive_secondary(data: dict):
    secondary_dict = {}
    x = data["you"]["head"]["x"]
    y = data["you"]["head"]["y"]
    x_limits = (-1, data["board"]["width"] + 1)
    y_limits = (-1, data["board"]["height"] + 1)
    enemy_positions = []
    for snake in data["board"]["snakes"]:
        if snake["id"] != data["you"]["id"]:
            enemy_positions.extend(snake["body"])
    for direction, formula in {
        "up": (x, y + 1),
        "down": (x, y - 1),
        "left": (x - 1, y),
        "right": (x + 1, y),
    }.items():
        position = {"x": formula, "y": formula}
        secondary_dict[direction] = {}
        secondary_dict[direction]["position"] = position
        secondary_dict[direction]["wall"] = (
            True if position["x"] in x_limits or position["y"] in y_limits else False
        )
        secondary_dict[direction]["food"] = (
            True if position in data["board"]["food"] else False
        )
        secondary_dict[direction]["hazard"] = (
            True if position in data["board"]["hazards"] else False
        )
        secondary_dict[direction]["self"] = (
            True if position in data["you"]["body"] else False
        )
        secondary_dict[direction]["enemy"] = (
            True if position in enemy_positions else False
        )
    return secondary_dict


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.
    """

    secondary_dict = derive_secondary(data)

    viable_moves = [
        move
        for move in possible_moves
        if not secondary_dict[move]["wall"]
        and not secondary_dict[move]["hazard"]
        and not secondary_dict[move]["self"]
        and not secondary_dict[move]["enemy"]
    ]

    if len(viable_moves) == 0:
        return random.choice(possible_moves)

    for move in viable_moves:
        if secondary_dict[move]["food"]:
            return move

    return random.choice(viable_moves)

import json
import random


def read_players() -> list:
    with open("players.json", "r") as f:
        return json.load(f)

players = read_players()

def random_player():
    return random.choice(players)


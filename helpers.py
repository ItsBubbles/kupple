import json
import random


def random_player():
    def players_list():
        with open("players.json", "r") as f:
            players = json.load(f)
            return players

    players = players_list()

    return random.choice(players)



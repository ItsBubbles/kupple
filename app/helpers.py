import json
import random

from pydantic import BaseModel

class Player(BaseModel):
    name: str
    pos: str
    age: int
    height: str
    team: str
    number: str
    div: str
    conf: str


def read_players() -> list:
    with open("app/players.json", "r") as f:
        return json.load(f)

players = read_players()

def random_player():
    return random.choice(players)

answer = random_player()

def compare_player(player, answer):
    if player != answer: 
        return "Try again!"
    else: 
        return player
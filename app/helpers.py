from collections import namedtuple
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
    
    def compare_(self, answer):
        cmp_arr = []

        # go through each attribute used for comparison (Team, Div, Pos, Ht, Age, Jersey#)
        cmp_arr.append(bool(self.pos == answer.pos))
        cmp_arr.append(answer.age - self.age)
        cmp_arr.append(int(answer.height) - int(self.height))
        cmp_arr.append(int(answer.number) - int(self.number))
        cmp_arr.append(bool(self.conf == answer.conf))
        cmp_arr.append(bool(self.div == answer.div))

        res_arr = []

        for res in cmp_arr:
            
            type_ = f"{type(res)}"

            print(type_)

            match type_:
                case "<class 'bool'>":
                    if res: res_arr.append(res)
                    else: res_arr.append(res)

                case "<class 'int'>":
                    if res==0: res_arr.append(0)
                    elif res>0: res_arr.append(1)
                    elif res<0: res_arr.append(-1)

        return res_arr



def read_players() -> list:
    with open("app/players.json", "r") as f:
        return json.load(f)

players = read_players()

def random_player():
    player = random.choice(players)
    player = namedtuple("Player", player.keys())(*player.values())
    return player

answer = random_player()

def compare_player(player, answer):
    # if player.compare(answer):
    #     return "Try again!"
    if player != answer:
        return "Try again!"
    else: 
        return player
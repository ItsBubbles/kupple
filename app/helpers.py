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
        player_attr = ["pos", "div", "conf", "age", "height", "number"]
        # go through each attribute used for comparison (Team, Div, Pos, Ht, Age, Jersey#)
        cmp_arr.append(bool(self.pos == answer.pos))
        cmp_arr.append(bool(self.div == answer.div))
        cmp_arr.append(bool(self.conf == answer.conf))
        cmp_arr.append(answer.age - self.age)
        cmp_arr.append(int(answer.height) - int(self.height))
        cmp_arr.append(int(answer.number) - int(self.number))

        res_arr = []

        for res in cmp_arr:
            type_ = f"{type(res)}"

            match type_:
                case "<class 'bool'>":
                    if res: res_arr.append("has-background-success has-text-primary-light has-text-weight-bold")
                    else: res_arr.append("has-background-danger-dark has-text-primary-light has-text-weight-bold")

                # first 3 array elements are for table data: <td class=res_arr[:3]>, third is for arrow div: <div class=res_arr[3]>
                case "<class 'int'>":
                    if res==0: res_arr.append("has-background-success has-text-primary-light has-text-weight-bold")

                    elif res>0 and res>5: res_arr.append("has-background-danger-dark has-text-primary-light has-text-weight-bold triangle_up")
                    elif res>0 and res<5: res_arr.append("has-background-warning has-text-black-bis has-text-weight-bold triangle_up")

                    elif res<0 and res>-5: res_arr.append("has-background-warning has-text-black-bis has-text-weight-bold triangle_down")
                    elif res<0 and res<-5: res_arr.append("has-background-danger has-text-black-bis has-text-weight-bold triangle_down")

        res_dict = {}

        for i in range(6):
            k = player_attr[i]
            v = res_arr[i]
            res_dict[k] = [v]

        print(res_dict)

        return res_dict

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
import json
import random

from pydantic import BaseModel
from collections import namedtuple

class Player(BaseModel):
    name: str
    pos: str
    age: int
    height: str
    team: str
    number: str
    div: str
    conf: str
    
    def compare_(self, answer) -> dict | int:
        if dict(self) == answer._asdict():
            return 1
        print(answer)
        
        cmp_arr = []
        player_attr = ["posClass", "confClass", "divClass", "ageClass", "heightClass", "numberClass", "nameClass", "teamClass"]
        # go through each attribute used for comparison (Team, Div, Pos, Ht, Age, Jersey#)

        cmp_arr.append(bool(self.pos == answer.pos))
        cmp_arr.append(bool(self.conf == answer.conf))
        cmp_arr.append(bool(self.div == answer.div))
        cmp_arr.append(answer.age - self.age)
        cmp_arr.append(int(answer.height) - int(self.height))
        cmp_arr.append(int(answer.number) - int(self.number))
        cmp_arr.append(bool(self.name == answer.name))
        cmp_arr.append(bool(self.team == answer.team))

        res_arr = []

        i = 0
        for res in cmp_arr:
            type_ = f"{type(res)}"

            match type_:
                case "<class 'bool'>":
                    if i != 2:
                        if res: res_arr.append("has-background-success has-text-primary-light has-text-weight-bold")
                        else: res_arr.append("has-background-danger-dark has-text-primary-light has-text-weight-bold")
                    else:
                        conf_bool = cmp_arr[1]
                        if not conf_bool: res_arr.append("has-background-danger-dark has-text-primary-light has-text-weight-bold")
                        elif conf_bool and not res: res_arr.append("has-background-warning has-text-black-bis has-text-weight-bold")
                        else: res_arr.append("has-background-success has-text-primary-light has-text-weight-bold")

                # first 3 array elements are for table data: <td class=res_arr[:3]>, third is for arrow div: <div class=res_arr[3]>
                case "<class 'int'>":
                    if res==0: res_arr.append("has-background-success has-text-primary-light has-text-weight-bold")

                    elif res>0 and res>=5: res_arr.append("has-background-danger-dark has-text-primary-light has-text-weight-bold triangle_up")
                    elif res>0 and res<5: res_arr.append("has-background-warning has-text-black-bis has-text-weight-bold triangle_up")

                    elif res<0 and res>-5: res_arr.append("has-background-warning has-text-black-bis has-text-weight-bold triangle_down")
                    elif res<0 and res<=-5: res_arr.append("has-background-danger-dark has-text-primary-light has-text-weight-bold triangle_down")
            i+=1
        res_dict = {}

        for i in range(8):
            k = player_attr[i]
            
            try:
                v = res_arr[i]
            except IndexError:
                print(f"Index {i} is out of range for an array of length {len(res_arr)}...\nArray: {res_arr}")

            res_dict[k] = [v]
        return res_dict


def read_players() -> list:
    with open("data/players.json", "r") as f:
        return json.load(f)

players = read_players()

def random_player() -> Player:
    player = random.choice(players)
    player = namedtuple("Player", player.keys())(*player.values())
    return player
from typing import Optional
from collections import namedtuple
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_session, counter_check, new_game

from app.helpers import Player, read_players

# from mangum import Mangum


origins = [
    "http://127.0.0.1:5500"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# handler = Mangum(app)

@app.get("/")
async def get_players_route():
    return read_players()


# route to compare player objects
@app.post("/compare")
async def compare_player_route(player: Player, tkn: Optional[str]=Header(None)):
    counter = counter_check(tkn)

    if counter == 8: return {"results": counter, "player": None, "counter": counter}

    answer = init_session(tkn)["answer"]
    answer = namedtuple("Player", answer.keys())(*answer.values())

    results = player.compare_(answer)
    return {"results": results, "player": player, "counter": counter}


# route to session the user
@app.post("/init_session")
def init_session_route(tkn: Optional[str]=Header(None)):
    counter = init_session(tkn)["counter"]
    return {"counter": counter}

@app.get("/new_game")
def new_game_route(tkn: Optional[str]=Header(None)): 
    return new_game(tkn)

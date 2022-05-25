from collections import namedtuple
from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_session, counter_check, new_game

from app.helpers import Player, read_players

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

@app.get("/")
async def get_players_route():
    return read_players()


# route to compare player objects
@app.post("/compare")
async def compare_player_route(player: Player, tkn: Optional[str]=Header(None)):
    counter = counter_check(tkn)
    # if counter is None: new_game(tkn); return {"results": 403, "player": None}

    answer = init_session(tkn)["answer"]
    answer = namedtuple("Player", answer.keys())(*answer.values())

    results = player.compare_(answer)
    return {"results": results, "player": player}
    

# @app.get("/counter")
# def counter_check_route(request: Request):
#     user_ip = str(request.client.host)
#     return {"counter": counter_check(user_ip)}


# route to session the user
@app.post("/init_session")
def init_session_route(tkn: Optional[str]=Header(None)):
    return init_session(tkn)


@app.get("/new_game")
def new_game_route(request: Request):
    user_ip = str(request.client.host) 
    
    return new_game(user_ip)    


# @app.post("/delete_session")
# async def del_session(user_ip: str, response: Response):
#     await backend.delete(user_ip)
#     # cookie.delete_from_response(response)
#     return "deleted session"
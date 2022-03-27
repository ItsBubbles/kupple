import string
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from helpers import random_player, read_players

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

player = random_player()
class Player(BaseModel):
    name: str
    pos: str
    age: int
    height: str
    team: str
    number: str
    div: str
    conf: str

@app.get("/")
async def get_players_route():
    return read_players()

@app.post("/compare")
async def compare_player(player: Player):
    return player

# secret
@app.get("/answer")
async def random_player_route():
    return random_player()
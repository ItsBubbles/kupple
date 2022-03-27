from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def get_players_route():
    return read_players()

@app.post("/")
async def compare_player():
    ...


# secret
@app.get("/answer")
async def random_player_route():
    return random_player()
import string
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.helpers import Player, answer, random_player, read_players

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

# temporary until "sessions" (cookies?) are implemeneted
print(f"The current global answer to the puzzle is {answer}!")

@app.get("/")
async def get_players_route():
    return read_players()

@app.post("/compare")
async def compare_player_route(player: Player):
    # passing 'answer' from helpers, will be refactored to an individual's session
    results = player.compare_(answer)
    return results

# secret
@app.get("/answer")
async def random_player_route():
    return random_player()
from helpers import random_player
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def random_player_route():
    return random_player()
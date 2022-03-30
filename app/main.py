from uuid import UUID, uuid4

from fastapi import FastAPI
from fastapi import HTTPException, FastAPI, Response, Depends

from fastapi.middleware.cors import CORSMiddleware

from app.verifier import SessionData, backend, cookie
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

# secret
@app.get("/answer")
async def random_player_route():
    return random_player()

# route to compare player objects
@app.post("/compare")
async def compare_player_route(player: Player):
    # passing 'answer' from helpers, will be refactored to an individual's session
    
    results = player.compare_(answer)
    returnDict = {
        "results": results,
        "player": player
    }
    return returnDict

# route to session the user
@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):

    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"

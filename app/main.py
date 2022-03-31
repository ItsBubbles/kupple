from uuid import UUID, uuid4

from fastapi import FastAPI
from fastapi import HTTPException, FastAPI, Response, Depends

from fastapi.middleware.cors import CORSMiddleware

from app.session import SessionData, backend, cookie, verifier
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


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return {"user_ip": session_data.user_ip}

# route to compare player objects
@app.post("/compare", dependencies=[Depends(cookie)])
async def compare_player_route(player: Player, session_data: SessionData = Depends(verifier)):
    # passing 'answer' from helpers, will be refactored to an individual's session
    
    results = player.compare_(session_data.answer)
    returnDict = {
        "results": results,
        "player": player
    }
    return returnDict

# route to session the user
@app.post("/create_session/{user_ip}")
async def create_session(user_ip: str, response: Response):
    sessions = [s.user_ip for s in list(backend.data.values())]
    if user_ip in sessions:
        return "session already exists!"
        
    answer = random_player()

    session = uuid4()
    data = SessionData(
                    user_ip=user_ip, 
                    answer=answer._asdict()
                )

    
    await backend.create(session, data)

    cookie.attach_to_response(response, session)
    
    # return f"created session for {user_ip} \n answer for user -> {answer}"
    return data.user_ip


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
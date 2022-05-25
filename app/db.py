from http import HTTPStatus
import sqlite3
from sqlite3.dbapi2 import Connection

from json import dumps, loads

# from helpers import random_player
from app.helpers import random_player


def init_db():
    try: 
        return sqlite3.connect("data/data.db", timeout=10)
    except:
        return "Failed to connect to database"

def db_query(query: str, conn: Connection, commit: bool=False):
    print("no execute")
    res = conn.execute(query)
    print("execute")
    if commit: conn.commit()
    return list(res)


def init_session(user_ip: str):
    """Queries database by user_ip. Returns tuple of user answer and counter for the current session."""
    def create_user(user_ip: str):
        answer = random_player()

        query = f"insert or ignore into user_data (user_ip, answer, counter) values ('{user_ip}','{dumps(answer._asdict())}', 0);"
        try:
            db_query(query=query, conn=init_db(), commit=True)
            return {"answer": answer._asdict(), "counter": 0}


        except sqlite3.IntegrityError:
            return 409

    def user_exists(user_ip) -> int | tuple:
        query = f"select answer, counter from user_data where user_ip='{user_ip}';"
        
        res = db_query(query=query, conn=init_db())

        if res: return {"answer": loads(list(res)[0][0]), "counter": res[0][1]}
        return 0
    
    if user_exists(user_ip): return user_exists(user_ip)
    
    return create_user(user_ip=user_ip)


def counter_check(user_ip: str):
    query_check = f"select counter from user_data where user_ip='{user_ip}';"
    
    counter = db_query(query=query_check, conn=init_db())[0][0]

    if counter <= 7:
        query_update = f"update user_data set counter=counter+1 where user_ip='{user_ip}';"
        db_query(query=query_update, conn=init_db())
        return counter+1
    
    else:
        return None
    

def new_game(user_ip: str):
    answer = random_player()
    query = f"update user_data set answer='{dumps(answer._asdict())}', counter=0 where user_ip='{user_ip}';"
    db_query(query=query, conn=init_db())
    return {"answer": answer._asdict(), "counter": 0}


def close_db(conn: Connection):
    conn.close()

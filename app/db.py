import sqlite3
from sqlite3.dbapi2 import Connection

from json import dumps, loads

from app.helpers import random_player


def init_db():
    try: 
        return sqlite3.connect("data/data.db", timeout=10)
    except:
        return "Failed to connect to database"

def db_query(query: str, conn: Connection, commit: bool=False):
    res = conn.execute(query)
    if commit: conn.commit()
    return list(res)


def init_session(tkn: str):
    """Queries database by tkn. Returns tuple of user answer and counter for the current session."""
    counter = counter_check(tkn, query=True)
    
    def create_user(tkn: str):
        answer = random_player()

        query = f"insert or ignore into user_data (tkn, answer, counter) values ('{tkn}','{dumps(answer._asdict())}', 0);"
        try:
            db_query(query=query, conn=init_db(), commit=True)
            return {"answer": answer._asdict(), "counter": 0}

        except sqlite3.IntegrityError:
            return 409

    def user_exists(tkn) -> int | tuple:
        query = f"select answer, counter from user_data where tkn='{tkn}';"
        
        res = db_query(query=query, conn=init_db())

        if res: 
            counter = res[0][1]
            if counter != None: return {"answer": loads(list(res)[0][0]),"counter": counter}
        return 0
    
    if user_exists(tkn): 
        if counter is None: return new_game(tkn)
        return user_exists(tkn)
    
    return create_user(tkn=tkn)


def counter_check(tkn: str, query=False):
    query_check = f"select counter from user_data where tkn='{tkn}';"
    
    counter = db_query(query=query_check, conn=init_db())[0][0]

    if query: return counter

    if counter <= 7:
        query_update = f"update user_data set counter=counter+1 where tkn='{tkn}';"
        db_query(query=query_update, conn=init_db(), commit=True)
        return counter+1
    
    elif counter > 8:
        return 8

    else:
        return counter
    

def new_game(tkn: str):
    answer = random_player()
    query = f"update user_data set answer='{dumps(answer._asdict())}', counter=0 where tkn='{tkn}';"
    db_query(query=query, conn=init_db(), commit=True)
    return {"counter": 0}


def close_db(conn: Connection):
    conn.close()

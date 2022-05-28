# import sqlite3
# from sqlite3.dbapi2 import Connection
import mysql.connector

from json import dumps, loads

from app.helpers import random_player


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="root",
    database ="kupple",
    port=3307
)
cursor = db.cursor(dictionary=True)

def db_query(query: str, values, cursor):
    cursor.execute(query, values)
    res = list(cursor.fetchall())
    db.commit()
    
    return list(res)


def init_session(tkn: str):
    
    """Queries database by tkn. Returns tuple of user answer and counter for the current session."""
    def create_user(tkn: str):
        answer = random_player()

        query = f"insert into user_data (tkn, answer, counter) values (%s, %s, %s)"
        values = (tkn, dumps(answer._asdict()), 0)

        db_query(query=query,values=values, cursor=cursor)


        return {"answer": answer._asdict(), "counter": 0}

   

    def user_exists(tkn) -> int | tuple:
        query = f"select answer, counter from user_data where tkn=%s"
        values = (tkn,)
        res = db_query(query=query, values=values, cursor=cursor)
        if res: 
            counter = res[0]["counter"]
            if counter != None: return {"answer": res[0]["answer"],"counter": counter}
        return 0
    
    results = user_exists(tkn)
    
    if results:
        if results["counter"] is None: return new_game(tkn)
        return results
    
    return create_user(tkn=tkn)


def counter_check(tkn: str):
    query_check = f"select counter from user_data where tkn=%s"
    values =(tkn,)
    counter= db_query(query_check,values=values, cursor=cursor)
    if counter != None: counter = counter[0]["counter"]

    if counter <= 8:
        query_update = f"update user_data set counter=counter+1 where tkn=%s"
        values = (tkn,)
        db_query(query=query_update,values=values, cursor=cursor)
        return counter
    
    elif counter > 8:
        return 8

    else:
        return counter
    

def new_game(tkn: str):
    answer = random_player()
    query = f"update user_data set answer=%s, counter=0 where tkn=%s"
    values = dumps(answer._asdict()), tkn
    db_query(query=query, values=values, cursor=cursor)
    return {"counter": 0}


# def close_db(conn: Connection):
#     conn.close()

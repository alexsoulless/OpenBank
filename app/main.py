# from typing import Union
# from pydantic import BaseModel
from fastapi import FastAPI
from contextlib import asynccontextmanager
import dbRequests as dbr
from OBclasses import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Жизненный цикл приложения. Всё до yield выполняется при запуске программы, всё что после - при завершении работы
    print("===APP SETUP===")
    global pool
    pool = dbr.connectionPool()
    if pool is None:
        print("db connection - failed")
    print("db connection - success")
    yield
    print("bye-bye")


app = FastAPI(lifespan=lifespan)


@app.get("/ping/")
def ping(q : int):
    return {
        "responce": "pong",
        "q" : q
    }


@app.get("/getUser/")
async def getUser(
    id: int | None = None, username: str | None = None, FIO: str | None = None
):
    global pool
    return dbr.getUser(pool, id, username, FIO)

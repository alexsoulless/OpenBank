from fastapi import FastAPI
from contextlib import asynccontextmanager
import dbRequests as dbr
from classes import User


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
def ping():
    return {
        "responce": "pong",
    }


@app.get("/getUser/")
async def getUser(
    id: int | None = None, username: str | None = None, FIO: str | None = None
) -> User:
    global pool
    return dbr.getUser(pool, id, username, FIO)


from fastapi import APIRouter
import dbRequests as dbr

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def getUser(
    id: int | None = None, username: str | None = None, FIO: str | None = None
) -> dict | None:
    global pool
    res = dbr.getUser(pool, id, username, FIO)
    if res is not None:
        return res
    else:
        return {"result": None}


@router.post("/{id}")
async def setUserStats(
    id: int, balance: int | None = None, isBanned: bool | None = None
):
    pass


@router.get("/find")
async def findUser(pattern: str) -> list[dict]:
    global pool
    pattern = pattern.lower()
    return dbr.findUser(pool, pattern)

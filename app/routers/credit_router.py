from fastapi import APIRouter
import dbRequests as dbr

router = APIRouter(
    prefix="/credits",
    tags=["credits"]
)

@router.get("/")
async def getCreditRequests():
    pass


@router.get("/{id}")
async def getCreditRequest(id : int):
    pass

@router.post("/")
async def postCreditRequest():
    pass


@router.post("/{id}")
async def setCreditRequestStatus(id : int, newStatus: int):
    pass
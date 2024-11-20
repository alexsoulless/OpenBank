from fastapi import APIRouter
import dbRequests as dbr
from schemas import CreditRequest, CreditRequestSchema

router = APIRouter(
    prefix="/credits",
    tags=["credits"]
)

@router.get("/")
async def getCreditRequests() -> list[CreditRequestSchema]:
    return [CreditRequestSchema.from_credit_request(i) for i in dbr.getCreditRequests()]


@router.get("/{id}")
async def getCreditRequest(id : int):
    res = dbr.getCreditRequest(id)
    if res is not None:
        return CreditRequestSchema.from_credit_request(res)
    return None

@router.post("/")
async def postCreditRequest():
    pass


@router.post("/{id}")
async def setCreditRequestStatus(id : int, newStatus: int):
    pass
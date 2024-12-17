from fastapi import APIRouter, Query, HTTPException, status
import dbRequests as dbr
from schemas import TransactionSchema, Decimal

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("")
async def post_transaction(
    sender_id: int = Query(..., ge=1),
    recipient_id: int = Query(..., ge=1),
    amount: Decimal = Query(..., gt=0),
    forced: bool = Query(False),
) -> TransactionSchema:
    if sender_id == recipient_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sender and recipient cannot be the same")
    res = await dbr.exec_transaction(sender_id, recipient_id, amount, forced)
    if isinstance(res, int):
        match res:
            case 0:
                message = "cant find sender"
            case 1:
                message = "cant find recipient"
            case 2:
                message = "not enough money"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    else:
        return TransactionSchema.from_transaction(res)


@router.get("")
async def get_transactions(
    user_id: int = Query(..., ge=1),
    start: int = Query(0, ge=0),
    count: int = Query(15, ge=1),
) -> list[TransactionSchema]:
    res = await dbr.get_transactions(user_id, start, count)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if len(res) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="transactions not found")
    return [TransactionSchema.from_transaction(t) for t in res]

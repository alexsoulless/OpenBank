from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import List
import dbRequests as dbr
from schemas import CreditRequestSchema, CreditPaymentSchema
from decimal import Decimal

router = APIRouter(prefix="/credits", tags=["credits"])


@router.get("", response_model=List[CreditRequestSchema])
async def get_credit_requests() -> List[CreditRequestSchema]:
    credits = await dbr.get_credit_requests()
    if not credits:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No credit requests found"
        )
    return [CreditRequestSchema.from_credit_request(credit) for credit in credits]


@router.post(
    "", response_model=CreditRequestSchema, status_code=status.HTTP_201_CREATED
)
async def post_credit_request(
    user_id: int = Query(..., ge=1),
    purpose: str = Query(...),
    amount: Decimal = Query(..., gt=0),
) -> CreditRequestSchema:
    res = await dbr.post_credit_request(
        user_id=user_id,
        purpose=purpose,
        amount=amount,
        status=0
    )
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create credit request",
        )
    return CreditRequestSchema.from_credit_request(res)


@router.get("/{id}", response_model=CreditRequestSchema)
async def get_credit_request(id: int = Path(..., ge=1)) -> CreditRequestSchema:
    res = await dbr.get_credit_request(id)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credit request not found"
        )
    return CreditRequestSchema.from_credit_request(res)


@router.patch("/{id}")
async def set_credit_request_status(
    id: int = Path(..., ge=1),
    new_status: int = Query(
        ...,
        ge=0,
        le=4,
    ),
) -> CreditRequestSchema:
    """ 
    Статус кредитной заявки\n
    0 - создана \n
    1 - отправлена\n
    2 - рассматривается\n
    3 - одобрена\n
    4 - отклонена\n
    """
    res = await dbr.set_credit_request_status(id, new_status)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credit request not found or update failed",
        )
    return CreditRequestSchema.from_credit_request(res)


@router.get("/{id}/payments")
async def get_credits_payments(
    credit_request_id: int = Path(..., ge=1),
):
    payments = dbr.get_credit_payments(credit_request_id)
    if not payments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Credit request has no payments"
        )
    return [CreditPaymentSchema.from_credit_payment(payments) for payments in payments]

# TODO: 
# 1) одобрить кредитную заяку (в тч создание платежей)
# 2) оплата платежа
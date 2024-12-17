from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query, Path
import dbRequests as dbr
from schemas import TaxSchema, TaxPaymentSchema, Decimal, UserSchema

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.get("")
async def get_taxes() -> list[TaxSchema]:
    taxes = await dbr.get_taxes()
    if not taxes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No taxes found")
    return [TaxSchema.from_tax(i) for i in taxes]


@router.post("")
async def post_tax(
    name: str = Query(), 
    due_datetime: datetime = Query("2000-01-01T00:00:00", description="YYYY-MM-DDTHH:mm:ss"), 
    amount: Decimal = Query(0, gt = 0, lt=100000)
) -> TaxSchema:
    res = await dbr.new_tax(name, due_datetime, amount)
    if res is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tax creation failed")
    return TaxSchema.from_tax(res)


@router.patch("/{tax_id}")
async def edit_tax(
    tax_id: int = Path(..., ge=1),
    new_name: str = Query(),
    new_datetime: datetime = Query("2000-01-01T00:00:00", description="YYYY-MM-DDTHH:mm:ss"),
    new_amount: Decimal = Query(0, gt = 0, lt=100000),
) -> TaxSchema:
    res = await dbr.edit_tax(tax_id, new_name, new_datetime, new_amount)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tax not found")
    return TaxSchema.from_tax(res)


@router.post("/payments")
async def new_tax_payment(
    user_id: int = Query(..., ge=1), 
    tax_id: int = Query(..., ge=1)
) -> TaxPaymentSchema:
    res = await dbr.new_tax_payment(user_id, tax_id)
    if res is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment creation failed")
    return TaxPaymentSchema.from_tax_payment(res)


@router.get("/{tax_id}")
async def get_tax(tax_id: int = Path(..., ge=1)) -> TaxSchema:
    res = await dbr.get_tax(tax_id)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tax not found")
    return TaxSchema.from_tax(res)


@router.get("/{tax_id}/stats")
async def get_tax_stats(tax_id: int = Path(..., ge=1)):
    stats = await dbr.get_tax_stats(tax_id)
    if stats is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tax not found")
    return stats 


@router.get("/{tax_id}/defaulters")
async def get_tax_defaulters(tax_id: int = Path(..., ge=1)) -> list[UserSchema]:
    defaulters = await dbr.get_tax_defaulters(tax_id)
    if defaulters is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tax not found")
    return [UserSchema.from_user(i) for i in defaulters]
    

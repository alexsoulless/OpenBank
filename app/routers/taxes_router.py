from datetime import datetime
from fastapi import APIRouter
import dbRequests as dbr
from schemas import TaxSchema, TaxPaymentSchema, CurrencyPD

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.get("/")
async def getTaxes() -> list[TaxSchema]:
    return [TaxSchema.from_tax(i) for i in dbr.getTaxes()]


@router.post("/")
async def newTax(name: str, datetime: datetime, sum: CurrencyPD):
    res = dbr.newTax(name, datetime, sum)
    if res is not None:
        return TaxSchema.from_tax(res)
    return None


@router.put("/{taxId}")
async def editTax(taxId: int, newDateTime: datetime, newName: str, newSum: int):
    pass


@router.post("/payments")
async def newTaxPayment(userId: int, taxId: int):
    pass


@router.get("/{taxId}")
async def getTax(taxId: int):
    pass


@router.get("/{taxId}/stats")
async def getTaxStats(taxId: int):
    pass


@router.get("/{taxId}/defaulters")
async def getTaxDefaulters(taxId: int):
    pass

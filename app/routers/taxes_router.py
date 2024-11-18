from datetime import datetime
from fastapi import APIRouter
import dbRequests as dbr

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.get("/")
async def getTaxes():
    pass


@router.post("/")
async def newTax():
    pass


@router.post("/{taxId}")
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

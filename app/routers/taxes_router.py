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


@router.get("/{id}")
async def getTax(id: int):
    pass


@router.get("/{id}/stats")
async def getTaxStats(id: int):
    pass


@router.get("/{id}/defaulters")
async def getTaxDefaulters(id: int):
    pass


@router.get("/{id}/stats")
async def getTaxStats(id: int):
    pass

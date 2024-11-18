from fastapi import APIRouter
import dbRequests as dbr

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

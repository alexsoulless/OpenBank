from fastapi import APIRouter
import dbRequests as dbr

router = APIRouter(
    prefix="/credits",
    tags=["credits"]
)

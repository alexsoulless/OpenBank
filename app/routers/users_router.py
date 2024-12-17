from fastapi import APIRouter, HTTPException, Query, Path, Body, status
from typing import Optional
import dbRequests as dbr
from schemas import UserSchema, UserUpdateSchema, CreditRequestSchema, CreditPaymentSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UserSchema)
async def get_user(
    id: Optional[int] = Query(None, ge=1, description="User ID"),
    username: Optional[str] = Query(None, description="Username"),
    FIO: Optional[str] = Query(None, description="Full name"),
) -> UserSchema:
    if [id, username, FIO].count(None) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide only one of the ID, username and FIO",
        )
    res = await dbr.getUser(id, username, FIO)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserSchema.from_user(res)


@router.get("/all", response_model=list[UserSchema])
async def get_users() -> list[UserSchema]:
    users = await dbr.getUsers()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return [UserSchema.from_user(i) for i in users]


@router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int = Path(..., title="The ID of the user to update", ge=1),
    user_update: UserUpdateSchema = Body(..., title="User data to update"),
) -> UserSchema:
    if not user_update.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad user data"
        )
    try:
        updated_user = await dbr.updateUser(
            user_id, user_update.model_dump(exclude_unset=True)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserSchema.from_user(updated_user)


@router.get("/{user_id}/credits")
async def get_users_credits(
    user_id: int = Path(..., ge=1)
):
    credits = await dbr.getUsersCredits(user_id)

    if not credits:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User has no credits"
        )
    return [CreditRequestSchema.from_credit_request(credit) for credit in credits]


@router.get("/{user_id}/payments")
async def get_user_payments(
    user_id: int = Path(..., ge=1)
):
    payments = await dbr.get_user_payments(user_id)
    if not payments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="payments not found")
    return [CreditPaymentSchema.from_credit_payment(payment) for payment in payments]


@router.get("/find")
async def find_user(pattern: str = Query(min_length=3)) -> list[UserSchema]:
    pattern = pattern.lower()
    users = await dbr.findUser(pattern)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return [UserSchema.from_user(user) for user in users]

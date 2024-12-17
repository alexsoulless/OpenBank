from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import update, DECIMAL, or_
from sqlalchemy.sql import func
from datetime import datetime
from config import DB_PASSWORD, DB_USER, DB_HOST, DB_NAME, DB_PORT
from classes import User, Transaction, Tax, TaxPayment, CreditRequest, CreditPayment
from models import (
    UserModel,
    TaxModel,
    TaxPaymentModel,
    TransactionModel,
    CreditRequestModel,
    CreditPaymentModel,
)
import pytz

TIMEZONEINFO = pytz.timezone("Europe/Moscow")

engine = create_async_engine(
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def getUsers() -> list[User]:
    async for session in get_session():
        try:
            result = await session.execute(select(UserModel))
            users = [
                User(
                    user.id,
                    user.username,
                    user.FIO,
                    user.balance,
                    user.is_banned,
                    user.is_org,
                )
                for user in result.scalars().all()
            ]
            return users
        finally:
            await session.close()


async def getUser(id=None, username=None, FIO=None):
    if [id, username, FIO].count(None) != 2:
        return None

    async for session in get_session():
        try:
            query = None
            if id:
                query = select(UserModel).filter_by(id=id)
            elif username:
                query = select(UserModel).filter_by(username=username)
            elif FIO:
                query = select(UserModel).filter_by(FIO=FIO)

            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                return User.from_model(user)
            return None
        finally:
            await session.close()


async def updateUser(id: int, update_data: dict) -> User | None:
    async for session in get_session():
        try:
            stmt = update(UserModel).where(UserModel.id == id).values(**update_data)
            result = await session.execute(stmt)
            stmt = select(UserModel).where(UserModel.id == id)

            result = await session.execute(stmt)
            updated_user = result.scalar_one_or_none()

            if updated_user:
                await session.commit()
                return User.from_model(updated_user)
            else:
                return None
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def findUser(pattern):
    async for session in get_session():
        try:
            query = None
            if any(ord(c) in range(1040, 1104) for c in pattern):
                query = select(UserModel).filter(UserModel.FIO.like(f"%{pattern}%"))
            else:
                query = select(UserModel).filter(
                    UserModel.username.like(f"%{pattern}%")
                )

            result = await session.execute(query)
            users = result.scalars().all()
            return [
                User(u.id, u.username, u.FIO, u.balance, u.is_banned, u.is_org)
                for u in users
            ]
        finally:
            await session.close()


async def getUsersCredits(user_id):
    async for session in get_session():
        try:
            result = await session.execute(
                select(CreditRequestModel).filter_by(user_id=user_id)
            )
            requests = result.scalars().all()
            return [
                CreditRequest(r.id, r.user_id, r.purpose, r.amount, r.status)
                for r in requests
            ]
        finally:
            await session.close()


async def get_credit_requests():
    async for session in get_session():
        try:
            result = await session.execute(select(CreditRequestModel))
            requests = result.scalars().all()
            return [
                CreditRequest(r.id, r.user_id, r.purpose, r.amount, r.status)
                for r in requests
            ]
        finally:
            await session.close()


async def get_credit_request(id):
    async for session in get_session():
        try:
            result = await session.execute(select(CreditRequestModel).filter_by(id=id))
            request = result.scalars().first()
            if request:
                return CreditRequest(
                    request.id,
                    request.user_id,
                    request.purpose,
                    request.amount,
                    request.status,
                )
            return None
        finally:
            await session.close()


async def post_credit_request(user_id, purpose, amount, status):
    async for session in get_session():
        try:
            new_request = CreditRequestModel(
                user_id=user_id, purpose=purpose, amount=amount, status=status
            )
            session.add(new_request)
            await session.commit()
            return CreditRequest(
                new_request.id,
                new_request.user_id,
                new_request.purpose,
                new_request.amount,
                new_request.status,
            )
        finally:
            await session.close()


async def set_credit_request_status(id, newStatus):
    async for session in get_session():
        try:
            result = await session.execute(select(CreditRequestModel).filter_by(id=id))
            request = result.scalars().first()
            if request:
                request.status = newStatus
                await session.commit()
                return CreditRequest(
                    request.id,
                    request.user_id,
                    request.purpose,
                    request.amount,
                    request.status,
                )
            return None
        finally:
            await session.close()


async def get_taxes():
    async for session in get_session():
        try:
            result = await session.execute(select(TaxModel))
            taxes = result.scalars().all()
            return [Tax(t.id, t.name, t.due_datetime, t.amount) for t in taxes]
        finally:
            await session.close()


async def new_tax(name: str, due_datetime: datetime, amount: DECIMAL):
    async for session in get_session():
        try:
            new_tax = TaxModel(name=name, due_datetime=due_datetime, amount=amount)
            session.add(new_tax)
            await session.commit()
            return Tax(new_tax.id, new_tax.name, new_tax.due_datetime, new_tax.amount)
        finally:
            await session.close()


async def edit_tax(taxId, newName=None, newDueDateTime=None, newAmount=None):
    async for session in get_session():
        try:
            result = await session.execute(select(TaxModel).filter_by(id=taxId))
            tax = result.scalars().first()
            if tax:
                if newName:
                    tax.name = newName
                if newDueDateTime:
                    tax.due_datetime = newDueDateTime
                if newAmount:
                    tax.amount = newAmount
                await session.commit()
                return Tax(tax.id, tax.name, tax.due_datetime, tax.amount)
            return None
        finally:
            await session.close()


async def new_tax_payment(user_id, tax_id):
    async for session in get_session():
        try:
            new_payment = TaxPaymentModel(user_id=user_id, tax_id=tax_id)
            session.add(new_payment)
            await session.commit()
            return TaxPayment(new_payment.id, new_payment.user_id, new_payment.tax_id)
        finally:
            await session.close()


async def get_tax(taxId):
    async for session in get_session():
        try:
            result = await session.execute(select(TaxModel).filter_by(id=taxId))
            tax = result.scalars().first()
            if tax:
                return Tax(tax.id, tax.name, tax.due_datetime, tax.amount)
            return None
        finally:
            await session.close()


async def get_tax_stats(tax_id) -> dict | None:
    async for session in get_session():
        try:
            result = await session.execute(select(TaxModel).filter_by(id=tax_id))
            tax = result.scalars().first()
            if not tax:
                return None

            paid_users = (
                await session.execute(
                    select(func.count(TaxPaymentModel.user_id)).filter_by(tax_id=tax_id)
                )
            ).scalar()
            total_users = (
                await session.execute(
                    select(func.count(UserModel.id)).filter_by(is_org=False)
                )
            ).scalar()
            return {
                "tax_id": tax_id,
                "paid": paid_users,
                "total": total_users,
            }
        finally:
            await session.close()


async def get_tax_defaulters(tax_id) -> list[User] | None:
    async for session in get_session():
        try:
            result = await session.execute(select(TaxModel).filter_by(id=tax_id))
            tax = result.scalars().first()
            if not tax:
                return None

            subquery = (
                select(TaxPaymentModel.user_id).filter_by(tax_id=tax_id).subquery()
            )
            result = await session.execute(
                select(UserModel).filter(
                    ~UserModel.id.in_(subquery), UserModel.is_org == False  # noqa: E712
                )
            )
            defaulters = result.scalars().all()
            return [
                User(u.id, u.username, u.FIO, u.balance, u.is_banned, u.is_org)
                for u in defaulters
            ]
        finally:
            await session.close()


async def exec_transaction(sender_id, recipient_id, amount, forced) -> int | Transaction:
    """
    exit codes
    0 - cant find sender
    1 - cant find recipient
    2 - not enough money (if not forced)
    """
    async for session in get_session():
        try:

            async def _get_user(id):
                query = select(UserModel).filter_by(id=id)
                res = await session.execute(query)
                user = res.scalars().first()
                return user

            sender = await _get_user(sender_id)
            if not sender:
                return 0

            recipient = await _get_user(recipient_id)
            if not recipient:
                return 1

            if (sender.balance < amount) and not forced:
                return 2

            transaction = TransactionModel(
                sender_id=sender_id,
                recipient_id=recipient_id,
                amount=amount,
                transaction_datetime=datetime.now(TIMEZONEINFO),
            )

            sender.balance -= amount
            recipient.balance += amount

            session.add(transaction)
            await session.commit()
            return Transaction.from_model(transaction)

        finally:
            await session.close()


async def get_transactions(user_id, start, count) -> None | list[Transaction]:
    async for session in get_session():
        try:
            query = select(UserModel).filter_by(id=user_id)
            res = await session.execute(query)
            user = res.scalars().first()
            if not user:
                return None

            query = (
                select(TransactionModel)
                .filter(
                    or_(
                        TransactionModel.sender_id == user_id,
                        TransactionModel.recipient_id == user_id,
                    )
                )
                .offset(start)
                .limit(count)
            )
            query = query.order_by(TransactionModel.transaction_datetime.desc())
            res = await session.execute(query)
            transactions = res.scalars().all()
            return [Transaction.from_model(t) for t in transactions]
        finally:
            await session.close()


async def get_user_payments(user_id):
    async for session in get_session():
        try:
            query = select(CreditPaymentModel).filter(
                CreditPaymentModel.user_id == user_id
            )
            res = await session.execute(query)
            payments = [CreditPayment.from_model(p) for p in res.scalars().all()]
            return payments
        finally:
            await session.close()


async def get_credit_payments(credit_request_id):
    async for session in get_session():
        try:
            query = select(CreditPaymentModel).filter(
                CreditPaymentModel.credit_request_id == credit_request_id
            )
            res = await session.execute(query)
            payments = [CreditPayment.from_model(p) for p in res.scalars().all()]
            return payments
        finally:
            await session.close()


if __name__ == "__main__":
    pass

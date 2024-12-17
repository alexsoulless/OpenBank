from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
from models import UserModel, TransactionModel, CreditPaymentModel
from typing import Any
from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema


class Entry:
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)


class Currency(Decimal):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetJsonSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_schema(
            core_schema.decimal_schema(),
            description="A custom currency type with two decimal places"
        )

    def __new__(cls, value):
        return super().__new__(cls, cls.validate(value))

    @classmethod
    def validate(cls, value):
        if isinstance(value, Decimal):
            return value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    def __repr__(self):
        return f"Currency('{super().__str__()}')"


class User(Entry):
    def __init__(
        self,
        id: int,
        username: str,
        FIO: str,
        balance: Decimal,
        is_banned: bool,
        is_org: bool,
    ):
        self.id = id
        self.username = username
        self.FIO = FIO
        self.balance = balance
        self.is_banned = is_banned
        self.is_org = is_org

    @classmethod
    def from_model(self, user_model: UserModel):
        return User(user_model.id, user_model.username, user_model.FIO, user_model.balance, user_model.is_banned, user_model.is_org)

class Transaction(Entry):
    def __init__(
        self,
        id: int,
        sender_id: int,
        recipient_id: int,
        amount: Decimal,
        transaction_datetime: datetime,
    ):
        self.id = id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.amount = amount
        self.transaction_datetime = transaction_datetime

    @classmethod
    def from_model(self, model: TransactionModel):
        return Transaction(
            model.id,
            model.sender_id,
            model.recipient_id,
            model.amount,
            model.transaction_datetime,
        )


class CreditPlan(Entry):
    def __init__(
        self, payment_count: int, payment_period: timedelta, interest_rate: float):
        self.payment_count = payment_count
        self.payment_period = payment_period
        self.interest_rate = interest_rate


class CreditPayment(Entry):
    def __init__(
        self,
        id: int | None,
        credit_request_id: int,
        user_id: int,
        payment_datetime: datetime,
        amount: Decimal,
        is_paid: bool,
    ):
        self.id = id
        self.credit_request_id = credit_request_id
        self.user_id = user_id
        self.payment_datetime = payment_datetime
        self.amount = amount
        self.is_paid = is_paid

    @classmethod
    def from_model(self, model: CreditPaymentModel):
        return CreditPayment(
            model.id,
            model.credit_request_id,
            model.user_id,
            model.payment_datetime,
            model.amount,
            model.is_paid,
        )

class CreditRequest(Entry):
    """
    Статус кредитной заявки
    0 - создана
    1 - отправлена
    2 - рассматривается
    3 - одобрена
    4 - отклонена
    """

    def __init__(
        self,
        id: int,
        user_id: int,
        purpose: str,
        amount: Decimal,
        status: int,
    ):
        self.id = id
        self.user_id = user_id
        self.purpose = purpose
        self.amount = amount
        self.status = status

    def getCreditPayments(self, plan: CreditPlan) -> list[CreditPayment]:
        payments = []
        payment_amount = self.amount * plan.interest_rate / plan.payment_count
        for i in range(plan.payment_count):
            payment_datetime = datetime.now() + (i + 1) * plan.payment_period
            payments.append(CreditPayment(
                id=None,
                credit_request_id=self.id,
                user_id=self.user_id,
                payment_datetime=payment_datetime,
                amount=payment_amount,
                is_paid=False,
            ))
        return payments        

class Tax(Entry):
    def __init__(self, id: int, name: str, due_datetime: datetime, amount: Decimal):
        self.id = id
        self.name = name
        self.due_datetime = due_datetime
        self.amount = amount


class TaxPayment(Entry):
    def __init__(self, id: int, user_id: int, tax_id: int):
        self.id = id
        self.user_id = user_id
        self.tax_id = tax_id


GenenralCreditPlan = CreditPlan(4, timedelta(hours=6), 0.2)

if __name__ == '__main__':
    pass
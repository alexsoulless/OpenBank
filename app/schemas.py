from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from classes import User, Transaction, CreditRequest, Tax, TaxPayment, CreditPayment, Decimal


class UserSchema(BaseModel):
    id: int
    username: str
    FIO: str
    balance: Decimal
    is_banned: bool
    is_org: bool

    def to_user(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            FIO=self.FIO,
            balance=self.balance,
            is_banned=self.is_banned,
            is_org=self.is_org,
        )

    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
            FIO=user.FIO,
            balance=user.balance,
            is_banned=user.is_banned,
            is_org=user.is_org,
        )


class TransactionSchema(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    amount: Decimal
    transaction_datetime: datetime

    def to_transaction(self) -> Transaction:
        return Transaction(
            self.id,
            self.sender_id,
            self.recipient_id,
            self.transaction_datetime,
            self.amount,
        )

    @classmethod
    def from_transaction(cls, transaction: Transaction):
        return cls(
            id=transaction.id,
            sender_id=transaction.sender_id,
            recipient_id=transaction.recipient_id,
            transaction_datetime=transaction.transaction_datetime,
            amount=transaction.amount,
        )


class TaxPaymentSchema(BaseModel):
    id: int
    user_id: int
    tax_id: int

    def to_tax_payment(self) -> TaxPayment:
        return TaxPayment(self.id, self.user_id, self.tax_id)

    @classmethod
    def from_tax_payment(cls, tax_payment: TaxPayment):
        return cls(
            id=tax_payment.id, user_id=tax_payment.user_id, tax_id=tax_payment.tax_id
        )


class TaxSchema(BaseModel):
    id: int
    name: str
    due_datetime: datetime
    amount: Decimal

    def to_tax(self) -> Tax:
        return Tax(self.id, self.name, self.due_datetime, self.amount)

    @classmethod
    def from_tax(cls, tax: Tax):
        return cls(
            id=tax.id, name=tax.name, due_datetime=tax.due_datetime, amount=tax.amount
        )


class CreditRequestSchema(BaseModel):
    id: int
    user_id: int
    purpose: str
    amount: Decimal
    status: int

    def to_credit_request(self) -> CreditRequest:
        return CreditRequest(
            id=self.id,
            user_id=self.user_id,
            purpose=self.purpose,
            amount=self.amount,
            status=self.status,
        )

    @classmethod
    def from_credit_request(cls, credit_request: CreditRequest):
        return cls(
            id=credit_request.id,
            user_id=credit_request.user_id,
            purpose=credit_request.purpose,
            amount=credit_request.amount,
            status=credit_request.status,
        )


class CreditPaymentSchema(BaseModel):
    id: int
    credit_request_id: int
    user_id: int
    payment_datetime: datetime
    amount: Decimal
    is_paid: bool

    def to_credit_payment(self) -> CreditPayment:
        return CreditPayment(
            id=self.id,
            credit_request_id=self.credit_request_id,
            user_id=self.user_id,
            payment_datetime=self.payment_datetime,
            amount=self.amount,
            is_paid=self.is_paid,
        )

    @classmethod
    def from_credit_payment(cls, credit_payment: CreditPayment):
        return cls(
            id=credit_payment.id,
            credit_request_id=credit_payment.credit_request_id,
            user_id=credit_payment.user_id,
            payment_datetime=credit_payment.payment_datetime,
            amount=credit_payment.amount,
            is_paid=credit_payment.is_paid,
        )


class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, description="Username of the user")
    FIO: Optional[str] = Field(None, description="Full name of the user")
    balance: Optional[Decimal] = Field(None, description="Balance of the user")
    is_banned: Optional[bool] = Field(None, description="Banned status of the user")
    is_org: Optional[bool] = Field(None, description="Organization status of the user")

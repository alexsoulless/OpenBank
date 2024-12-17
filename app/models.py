from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    DECIMAL
)
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    FIO = Column(String(64), nullable=False)
    balance = Column(DECIMAL, default=0)
    is_banned = Column(Boolean, default=False)
    is_org = Column(Boolean, default=False)


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    transaction_datetime = Column(DateTime, default=func.now())

    sender = relationship("UserModel", foreign_keys=[sender_id])
    recipient = relationship("UserModel", foreign_keys=[recipient_id])


class CreditRequestModel(Base):
    __tablename__ = "credit_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    purpose = Column(String(128), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    status = Column(Integer, default=0)

    user = relationship("UserModel")


class TaxModel(Base):
    __tablename__ = "taxes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    due_datetime = Column(DateTime, nullable=False)
    amount = Column(DECIMAL, nullable=False)


class TaxPaymentModel(Base):
    __tablename__ = "tax_payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tax_id = Column(Integer, ForeignKey("taxes.id"), nullable=False)

    user = relationship("UserModel")
    tax = relationship("TaxModel")
    
class CreditPaymentModel(Base):
    __tablename__ = "credit_payments"
    
    id = Column(Integer, primary_key=True)
    credit_request_id = Column(Integer, ForeignKey("credit_requests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    payment_datetime = Column(DateTime, nullable=False)
    is_paid = Column(Boolean, default=False)

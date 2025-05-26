from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel
from typing import Literal, Union

class Account(Base):
    __tablename__ = "account"

    id = Column(String, primary_key=True, index=True)
    balance = Column(Integer, nullable=False, default=0)

class DepositEvent(BaseModel):
    type: Literal["deposit"]
    destination: str
    amount: int

class WithdrawEvent(BaseModel):
    type: Literal["withdraw"]
    origin: str
    amount: int

class TransferEvent(BaseModel):
    type: Literal["transfer"]
    origin: str
    destination: str
    amount: int

# Union
BankEvent = Union[DepositEvent, WithdrawEvent, TransferEvent]
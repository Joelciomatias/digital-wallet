from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel

class Account(Base):
    __tablename__ = "account"

    id = Column(String, primary_key=True, index=True)
    balance = Column(Integer, nullable=False, default=0)



class Event(BaseModel):
    type: str
    destination: str = None
    origin: str = None
    amount: int

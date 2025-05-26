
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models import Account, Base


def handle_balance(account_id, db):

    return db.query(Account).filter(Account.id == account_id).first()


def handle_reset(db):
    # Create table 
    Base.metadata.create_all(bind=engine)
    # Clear (SQLite)
    db.execute(text("DELETE FROM account"))
    db.commit()
    return {"message": "reset done"}


def handle_deposit(account_id: str, amount: int, db: Session):
    account = db.query(Account).filter(Account.id == account_id).first()

    if account:
        account.balance += amount
    else:
        account = Account(id=account_id, balance=amount)
        db.add(account)

    db.commit()
    return {"destination": {"id": account.id, "balance": account.balance}}, 201


def handle_withdraw(account_id: str, amount: int, db: Session):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account or account.balance < amount:
        raise HTTPException(status_code=404, detail="0")

    account.balance -= amount
    db.commit()

    return {"origin": {"id": account.id, "balance": account.balance}}, 201


def handle_transfer(origin_id: str, destination_id: str, amount: int, db: Session):
    origin = db.query(Account).filter(Account.id == origin_id).first()

    if not origin or origin.balance < amount:
        raise HTTPException(status_code=404, detail="0")

    destination = db.query(Account).filter(Account.id == destination_id).first()

    if not destination:
        destination = Account(id=destination_id, balance=0)
        db.add(destination)

    origin.balance -= amount
    destination.balance += amount
    db.commit()

    return {
        "origin": {"id": origin.id, "balance": origin.balance},
        "destination": {"id": destination.id, "balance": destination.balance},
    }, 201

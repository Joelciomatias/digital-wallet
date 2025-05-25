from sqlalchemy import text
from app.database import Base, engine
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import Account,Event
from app.database import SessionLocal, Base, engine
router = APIRouter()


# Dependência para obter a sessão DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/reset", status_code=200)
def reset_db(db: Session = Depends(get_db)):
    # Garante que a tabela foi criada
    Base.metadata.create_all(bind=engine)

    # Faz truncate da tabela (modo SQLite)
    db.execute(text("DELETE FROM account"))
    db.commit()
    return {"message": "reset done"}

@router.get("/balance")
def get_balance(account_id: str = Query(...), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account.balance

@router.post("/event")
def handle_event(event: Event, db: Session = Depends(get_db)):
    if event.type == "deposit":
        return handle_deposit(event.destination, event.amount, db)
    elif event.type == "withdraw":
        return handle_withdraw(event.origin, event.amount, db)
    elif event.type == "transfer":
        return handle_transfer(event.origin, event.destination, event.amount, db)


    raise HTTPException(status_code=400, detail="Invalid event type")

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

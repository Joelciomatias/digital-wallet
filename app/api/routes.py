from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import Event
from app.core import handle_deposit, handle_transfer, handle_withdraw, handle_reset, handle_balance
from app.database import  get_db
router = APIRouter()


@router.post("/reset", status_code=200)
def reset_db(db: Session = Depends(get_db)):

    return handle_reset(db)

@router.get("/balance")
def balance(account_id: str = Query(...), db: Session = Depends(get_db)):
    account = handle_balance(account_id, db)
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


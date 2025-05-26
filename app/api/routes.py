from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from app.core import (
    handle_balance,
    handle_deposit,
    handle_reset,
    handle_transfer,
    handle_withdraw,
)
from app.database import get_db
from app.models import BankEvent, DepositEvent, TransferEvent, WithdrawEvent

router = APIRouter()


@router.post("/reset", status_code=200)
def reset_db(db: Session = Depends(get_db)):
    
    handle_reset(db)
    return JSONResponse(
        status_code=200,
        content="OK"
    )


@router.get("/balance")
def balance(account_id: str = Query(...), db: Session = Depends(get_db)):
    account = handle_balance(account_id, db)
    if not account:
        return JSONResponse(content=0, status_code=404)


    return JSONResponse(
        status_code=200,
        content=account.balance
    )

@router.post("/event")
def handle_event(event: BankEvent = Body(..., discriminator='type'), db: Session = Depends(get_db)):

    res = None
    if isinstance(event, DepositEvent):
        res = handle_deposit(event.destination, event.amount, db)
    elif isinstance(event, WithdrawEvent):
        res = handle_withdraw(event.origin, event.amount, db)
    elif isinstance(event, TransferEvent):
        res = handle_transfer(event.origin, event.destination, event.amount, db)
    
    if res:
        return JSONResponse(
            status_code=201,
            content=res
        )

    return JSONResponse(content=0, status_code=404)

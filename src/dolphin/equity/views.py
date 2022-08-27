import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dolphin.database.core import get_db
from dolphin.models import PrimaryKey

from .models import EquityAdd, EquityAddResponse, EquityUpdate
from .service import get, get_by_ticker, add, update, delete


router = APIRouter()


@router.post("", response_model=EquityAddResponse)
def add_equity(equity_in: EquityAdd, db_session: Session = Depends(get_db)):
    equity = add(db_session=db_session, equity_in=equity_in)
    return equity


@router.get("/{equity_id}")
def get_equity_by_id(*, db_session: Session = Depends(get_db), equity_id: PrimaryKey):
    equity = get(db_session=db_session, equity_id=equity_id)
    if not equity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A equity with this id does not exist"}],
        )
    return json.dumps(equity.to_dict())


@router.put("/{equity_id}")
def update_equity(
    *, db_session: Session = Depends(get_db), equity_id: PrimaryKey, equity_in: EquityUpdate
):
    equity = get(db_session=db_session, equity_id=equity_id)
    if not equity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A equity with this id does not exist"}],
        )

    return update(db_session=db_session, equity=equity, equity_in=equity_in)


@router.get("/ticker/{equity_ticker}")
def get_equity_by_ticker(*, db_session: Session = Depends(get_db), equity_ticker: str):
    equity = get_by_ticker(db_session=db_session, ticker=equity_ticker)
    if not equity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A equity with this id does not exist"}],
        )
    return json.dumps(equity.to_dict())


@router.delete("/{equity_id}")
def delete_equity(*, db_session: Session = Depends(get_db), equity_id: PrimaryKey):
    equity = get(db_session=db_session, equity_id=equity_id)
    if not equity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A equity with this id does not exist"}],
        )
    delete(db_session=db_session, equity=equity)

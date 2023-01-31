import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dolphin.database.core import get_db
from dolphin.models import PrimaryKey
from dolphin.database.service import search_filter_sort_paginate

from .models import (
    Equity,
    EquityAdd,
    EquityAddResponse,
    EquityPagination,
    EquityRead,
    EquityUpdate
)

from .service import get, get_by_ticker, add, update, delete, get_all


router = APIRouter()


@router.get("", response_model=EquityPagination)
def get_equities(db_session: Session = Depends(get_db)):

    items = search_filter_sort_paginate(db_session, model="Equity")

    return {
        "total": items["total"],
        "items": [
            {
                "id": u.id,
                "ticker": u.ticker,
                "name": u.name,
                "description": u.description,
                "street1": u.street1,
                "street2": u.street2,
                "city": u.city,
                "state": u.state,
                "zip": u.zip,
                "country_code": u.country_code,
                "exchange": u.exchange,
                "ein": u.ein,
                "phone": u.phone,
                "cik": u.cik,
                "state_of_incorporation": u.state_of_incorporation,
                "website": u.website,
                "sector": u.sector,
                "industry": u.industry
            }
            for u in items["items"]
        ],
    }


@router.post("", response_model=EquityAddResponse)
def add_equity(equity_in: EquityAdd, db_session: Session = Depends(get_db)):
    equity = add(db_session=db_session, equity_in=equity_in)
    return equity


@router.get("/{equity_id}", response_model=EquityRead)
def get_equity_by_id(*, db_session: Session = Depends(get_db), equity_id: PrimaryKey):
    equity = get(db_session=db_session, equity_id=equity_id)
    if not equity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A equity with this id does not exist"}],
        )
    return equity


@router.put("/{equity_id}", response_model=EquityRead)
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


@router.get("/ticker/{equity_ticker}", response_model=EquityRead)
def get_equity_by_ticker(*, db_session: Session = Depends(get_db), equity_ticker: str):
    equity = get_by_ticker(db_session=db_session, ticker=equity_ticker)
    if not equity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A equity with this id does not exist"}],
        )
    return equity


@router.delete("/{equity_id}")
def delete_equity(*, db_session: Session = Depends(get_db), equity_id: PrimaryKey):
    equity = get(db_session=db_session, equity_id=equity_id)
    if not equity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A equity with this id does not exist"}],
        )
    delete(db_session=db_session, equity=equity)

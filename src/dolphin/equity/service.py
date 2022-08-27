from typing import Optional

from dolphin import log

from .models import Equity, EquityUpdate


def get(*, db_session, equity_id: int) -> Optional[Equity]:
    log.debug("Getting equity by ID: {}".format(equity_id))
    return db_session.query(Equity).filter(Equity.id == equity_id).one_or_none()


def get_by_ticker(*, db_session, ticker: str) -> Optional[Equity]:
    log.debug("Getting equity by ticker: {}".format(ticker))
    return db_session.query(Equity).filter(Equity.ticker == ticker).one_or_none()


def add(*, db_session, equity_in: Equity) -> Equity:
    log.debug("Adding new equity")
    equity = Equity(**equity_in.dict())
    db_session.add(equity)
    db_session.commit()
    return equity


def update(*, db_session, equity: Equity, equity_in: EquityUpdate) -> Equity:
    log.debug("Updating equity: {}".format(equity.id))
    equity_data = equity.dict()

    update_data = equity_in.dict()
    for field in equity_data:
        if field in update_data:
            setattr(equity, field, update_data[field])
    db_session.commit()
    return equity


def delete(*, db_session, equity: Equity):
    log.debug("Deleting equity: {}".format(equity.id))
    db_session.delete(equity)
    db_session.commit()

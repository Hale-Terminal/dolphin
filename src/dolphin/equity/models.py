from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func
from pydantic import Field

from dolphin.database.core import Base
from dolphin.models import DolphinBase, TimeStampMixin, PrimaryKey


class Equity(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    ticker = Column(String(50), nullable=False, unique=True)
    name = Column(String(150))
    description = Column(String(3000))
    street1 = Column(String(150))
    street2 = Column(String(150))
    city = Column(String(150))
    state = Column(String(150))
    zip = Column(String(150))
    country_code = Column(String(5))
    exchange = Column(String(50))
    ein = Column(String(150))
    phone = Column(String(50))
    cik = Column(Integer)
    state_of_incorporation = Column(String(50))
    website = Column(String(150))
    sector = Column(String(150))
    industry = Column(String(150))


class EquityBase(DolphinBase):
    ticker: str


class EquityAdd(EquityBase):
    name: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)
    street1: Optional[str] = Field(None, nullable=True)
    street2: Optional[str] = Field(None, nullable=True)
    city: Optional[str] = Field(None, nullable=True)
    state: Optional[str] = Field(None, nullable=True)
    zip: Optional[str] = Field(None, nullable=True)
    country_code: Optional[str] = Field(None, nullable=True)
    exchange: Optional[str] = Field(None, nullable=True)
    ein: Optional[str] = Field(None, nullable=True)
    phone: Optional[str] = Field(None, nullable=True)
    cik: Optional[int] = Field(None, nullable=True)
    state_of_incorporation: Optional[str] = Field(None, nullable=True)
    website: Optional[str] = Field(None, nullable=True)
    sector: Optional[str] = Field(None, nullable=True)
    industry: Optional[str] = Field(None, nullable=True)


class EquityAddResponse(DolphinBase):
    message: Optional[str] = Field(None, nullable=True)


class EquityUpdate(DolphinBase):
    ticker: Optional[str] = Field(None, nullable=True)
    name: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)
    street1: Optional[str] = Field(None, nullable=True)
    street2: Optional[str] = Field(None, nullable=True)
    city: Optional[str] = Field(None, nullable=True)
    state: Optional[str] = Field(None, nullable=True)
    zip: Optional[str] = Field(None, nullable=True)
    country_code: Optional[str] = Field(None, nullable=True)
    exchange: Optional[str] = Field(None, nullable=True)
    ein: Optional[str] = Field(None, nullable=True)
    phone: Optional[str] = Field(None, nullable=True)
    cik: Optional[int] = Field(None, nullable=True)
    state_of_incorporation: Optional[str] = Field(None, nullable=True)
    website: Optional[str] = Field(None, nullable=True)
    sector: Optional[str] = Field(None, nullable=True)
    industry: Optional[str] = Field(None, nullable=True)


class EquityRead(EquityBase):
    id: PrimaryKey
    name: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)
    street1: Optional[str] = Field(None, nullable=True)
    street2: Optional[str] = Field(None, nullable=True)
    city: Optional[str] = Field(None, nullable=True)
    state: Optional[str] = Field(None, nullable=True)
    zip: Optional[str] = Field(None, nullable=True)
    country_code: Optional[str] = Field(None, nullable=True)
    exchange: Optional[str] = Field(None, nullable=True)
    ein: Optional[str] = Field(None, nullable=True)
    phone: Optional[str] = Field(None, nullable=True)
    cik: Optional[int] = Field(None, nullable=True)
    state_of_incorporation: Optional[str] = Field(None, nullable=True)
    website: Optional[str] = Field(None, nullable=True)
    sector: Optional[str] = Field(None, nullable=True)
    industry: Optional[str] = Field(None, nullable=True)


class EquityPagination(DolphinBase):
    total: int
    items: List[EquityRead] = []

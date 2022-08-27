from typing import Optional
from sqlalchemy import Column, String, Integer, DateTime, func
from pydantic import Field

from dolphin.database.core import Base
from dolphin.models import DolphinBase, TimeStampMixin


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
    date_added = Column(DateTime, default=func.utc_timestamp())
    last_updated = Column(DateTime, default=func.utc_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "name": self.name,
            "description": self.description,
            "street1": self.street1,
            "street2": self.street2,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "country_code": self.country_code,
            "exchange": self.exchange,
            "ein": self.ein,
            "phone": self.phone,
            "cik": self.cik,
            "state_of_incorporation": self.state_of_incorporation,
            "website": self.website,
            "sector": self.sector,
            "industry": self.industry,
            "date_added": self.date_added.timestamp(),
            "last_updated": self.last_updated.timestamp(),
        }


class EquityBase(DolphinBase):
    ticker: str


class EquityAdd(EquityBase):
    name: str
    description: str
    street1: str
    street2: str
    city: str
    state: str
    zip: str
    country_code: str
    exchange: str
    ein: str
    phone: str
    cik: int
    state_of_incorporation: str
    website: str
    sector: str
    industry: str


class EquityAddResponse(DolphinBase):
    message: Optional[str] = Field(None, nullable=True)


class EquityUpdate(DolphinBase):
    ticker: str
    name: str
    description: str
    street1: str
    street2: str
    city: str
    state: str
    zip: str
    country_code: str
    exchange: str
    ein: str
    phone: str
    cik: int
    state_of_incorporation: str
    website: str
    sector: str
    industry: str

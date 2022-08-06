import uuid

from pytz import UTC
from datetime import datetime

from faker import Faker

from factory import Sequence, post_generation, SubFactory, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyDateTime, FuzzyInteger

from dolphin.auth.models import DolphinUser

from .database import Session


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class TimeStampBaseFactory(BaseFactory):
    created_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    updated_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))

import re
import functools
from typing import Any

from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic import BaseModel

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session

from starlette.requests import Request

from dolphin import config


engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_size=config.DATABASE_ENGINE_POOL_SIZE,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine)


def resolve_table_name(name):
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


raise_attribute_error = object()


def resolve_attr(obj, attr, default=None):
    try:
        return functools.reduce(getattr, attr.split("."), obj)
    except AttributeError:
        return default


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        else:
            return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    "{} has incorrect attribute '{}' in"
                    "__repr__attrs__".format(self.__class__, key)
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."

            if wrap_in_quote:
                value = "'{}'".format(value)
            values.append(value if single else "{}:{}".format(key, value))

        return " ".join(values)

    def __repr__(self):
        id_str = ("#" + self._id_str) if self._id_str else ""
        return "<{} {}{}>".format(
            self.__class__.__name__,
            id_str,
            " " + self._repr_attrs_str if self._repr_attrs_str else "",
        )


Base = declarative_base(cls=CustomBase)


def get_db(request: Request):
    return request.state.db


def get_db_temp():
    return scoped_session(sessionmaker(bind=engine))


def get_class_by_tablename(table_fullname: str) -> Any:

    def _find_class(name):
        for c in Base._decl_class_registry.values():
            if hasattr(c, "__table__"):
                if c.__table__.fullname.lower() == name.lower():
                    return c

    mapped_name = resolve_table_name(table_fullname)
    mapped_class = _find_class(mapped_name)

    if not mapped_class:
        raise ValidationError()

    return mapped_class

from typing import List, Optional
from datetime import datetime, timedelta, date

import bcrypt
from jose import jwt
from pydantic import validator, Field

from sqlalchemy import Column, String, LargeBinary, Integer, Boolean, Date

from dolphin.config import DOLPHIN_JWT_ALG, DOLPHIN_JWT_EXP, DOLPHIN_JWT_SECRET
from dolphin.database.core import Base
from dolphin.models import DolphinBase, TimeStampMixin, PrimaryKey
from dolphin.enums import UserRoles


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class User(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    birthday = Column(Date)
    company = Column(String)
    title = Column(String)
    phone_number = Column(String)
    active = Column(Boolean, default=True)
    role = Column(String, default=UserRoles.member)


    # type = Column(Integer, default=1)

    # Account Types
    #
    # 1 - Basic User
    #

    # search_vector = Column(
    #    TSVectorType(
    #        "username",
    #        "email",
    #        "first_name",
    #        "middle_name",
    #        "last_name",
    #        "company",
    #        "title",
    #        weights={
    #            "username": "A",
    #            "first_name": "B",
    #            "middle_name": "C",
    #            "last_name": "D",
    #            "email": "E",
    #            "company": "F",
    #            "title": "G",
    #        },
    #    )
    # )

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=DOLPHIN_JWT_EXP)).timestamp()
        data = {"exp": exp, "username": self.username}
        return jwt.encode(data, DOLPHIN_JWT_SECRET, algorithm=DOLPHIN_JWT_ALG)


class UserBase(DolphinBase):
    username: Optional[str] = Field(None, nullable=True)


class UserLogin(UserBase):
    password: str


class UserRegister(UserLogin):
    email: Optional[str] = Field(None, nullable=True)
    first_name: Optional[str] = Field(None, nullable=True)
    middle_name: Optional[str] = Field(None, nullable=True)
    last_name: Optional[str] = Field(None, nullable=True)
    gender: Optional[str] = Field(None, nullable=True)
    birthday: Optional[date] = Field(None, nullable=True)
    company: Optional[str] = Field(None, nullable=True)
    title: Optional[str] = Field(None, nullable=True)
    phone_number: Optional[str] = Field(None, nullable=True)
    password: Optional[str] = Field(None, nullable=True)
    role: Optional[str] = Field(None, nullable=True)

    @validator("password", pre=True, always=True)
    def password_required(cls, v):
        return hash_password(str(v))


class UserLoginResponse(DolphinBase):
    token: Optional[str] = Field(None, nullable=True)


class UserRegisterResponse(DolphinBase):
    token: Optional[str] = Field(None, nullable=True)


class UserRead(UserBase):
    id: PrimaryKey
    email: Optional[str] = Field(None, nullable=True)
    first_name: Optional[str] = Field(None, nullable=True)
    middle_name: Optional[str] = Field(None, nullable=True)
    last_name: Optional[str] = Field(None, nullable=True)
    gender: Optional[str] = Field(None, nullable=True)
    birthday: Optional[date] = Field(None, nullable=True)
    company: Optional[str] = Field(None, nullable=True)
    title: Optional[str] = Field(None, nullable=True)
    phone_number: Optional[str] = Field(None, nullable=True)
    password: Optional[str] = Field(None, nullable=True)
    active: Optional[bool] = Field(None, nullable=True)
    role: Optional[str] = Field(None, nullable=True)
    created_at: Optional[datetime] = Field(None, nullable=True)
    updated_at: Optional[datetime] = Field(None, nullable=True)


class UserUpdate(DolphinBase):
    id: PrimaryKey
    email: Optional[str] = Field(None, nullable=True)
    first_name: Optional[str] = Field(None, nullable=True)
    middle_name: Optional[str] = Field(None, nullable=True)
    last_name: Optional[str] = Field(None, nullable=True)
    gender: Optional[str] = Field(None, nullable=True)
    birthday: Optional[date] = Field(None, nullable=True)
    company: Optional[str] = Field(None, nullable=True)
    title: Optional[str] = Field(None, nullable=True)
    phone_number: Optional[str] = Field(None, nullable=True)
    password: Optional[str] = Field(None, nullable=True)
    active: Optional[bool] = Field(None, nullable=True)
    role: Optional[str] = Field(None, nullable=True)

    @validator("password", pre=True)
    def hash(cls, v):
        return hash_password(str(v))


class UserPagination(DolphinBase):
    total: int
    items: List[UserRead] = []

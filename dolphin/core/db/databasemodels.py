from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Text, ForeignKey, Float, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(250))
    phone_number = Column(String(150))

    def to_dict(self):
        return {
            'Id': self.id,
            'Username': self.username,
            'Password': self.password,
            'Status': self.active,
            'FirstName': self.first_name,
            'LastName': self.last_name,
            'Email': self.email,
            'PhoneNo': self.phone_number
        }

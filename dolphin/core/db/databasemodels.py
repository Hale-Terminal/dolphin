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
    created = Column(DateTime, default=func.utc_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'active': self.active,
            'created': self.created.timestamp()
        }

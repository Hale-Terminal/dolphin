from typing import List, Text

from dolphin.core.db.databasemodels import User


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def login(self, username: Text, password: Text):
        return self.db_session.query(User).filter(User.username == username, User.password == password).first()

    def add(self, item):
        self.db_session.add(item)

    def find_by_id(self, id: int) -> User:
        return self.db_session.query(User).filter(User.id == id).first()

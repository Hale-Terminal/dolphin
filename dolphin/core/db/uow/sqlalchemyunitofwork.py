from sqlalchemy.orm import scoped_session

from dolphin.core.db.repository.userrepository import UserRepository

from dolphin.core.db.uow.unitofwork import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = scoped_session(session_factory)

    def __enter__(self):
        self.session = self.session_factory()
        return self 

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @property
    def users(self) -> UserRepository:
        return UserRepository(self.session)

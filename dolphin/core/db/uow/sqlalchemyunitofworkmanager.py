from sqlalchemy.orm import sessionmaker

from dolphin.core.db.uow.sqlalchemyunitofwork import SqlAlchemyUnitOfWork
from dolphin.core.db.uow.unitofworkmanager import UnitOfWorkManager

class SqlAlchemyUnitOfWorkManager(UnitOfWorkManager):
    def __init__(self, db_engine):
        self.session_maker = sessionmaker(bind=db_engine, expire_on_commit=False)

    def start(self):
        return SqlAlchemyUnitOfWork(self.session_maker)

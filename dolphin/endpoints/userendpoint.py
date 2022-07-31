import json
from datetime import datetime
from typing import Text

from falcon import Request, Response, HTTPNotFound

from dolphin.core.db.uow.unitofworkmanager import UnitOfWorkManager


class UserServe:
    def on_get(self, req: Request, resp: Response, id, uowm):
        with uowm.start() as uow:
            user = uow.users.find_by_id(id)
            result = user.to_dict()
        resp.body = json.dumps(result)


class UserEndpoint:
    def __init__(self, uowm: UnitOfWorkManager):
        self.uowm = uowm

    def on_get(self, req: Request, resp: Response):
        pass

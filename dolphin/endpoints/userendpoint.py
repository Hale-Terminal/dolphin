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

    def on_get_user(self, req: Request, resp: Response, user: int):
        with self.uowm.start() as uow:
            user = uow.users.find_by_id(user)
            result = user.to_dict()
        resp.body = json.dumps(result)

    def on_get_login(self, req: Request, resp: Response):
        username = req.get_header('username', required=True)
        password = req.get_header('password', required=True)
        if username == "ADMIN" and password == "password":
            response = {
                "token": "WTG435eoigier5"
            }
            resp.body = json.dumps(response)

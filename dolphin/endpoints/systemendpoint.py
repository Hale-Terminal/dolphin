import json

from falcon import Request, Response, HTTPNotFound


class SystemEndpoint:
    def __init__(self):
        pass
    
    def on_get(self, req: Request, resp: Response):
        response = {
            "message": "Hello from Dolphin!"
        }
        resp.body = json.dumps(response)

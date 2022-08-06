from dolphin.plugins.base import Plugin
from starlette.requests import Request


class AuthenticationProviderPlugin(Plugin):
    type = "auth-provider"

    def get_current_user(self, request: Request, **kwargs):
        raise NotImplemented

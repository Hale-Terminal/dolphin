import base64
import json
import logging

import requests
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param

from jose import JWTError, jwt
from jose.exceptions import JWKError
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.requests import Request

from dolphin.plugins import dolphin_core as dolphin_plugin
from dolphin.plugins.bases import AuthenticationProviderPlugin

from dolphin.config import DOLPHIN_JWT_SECRET

log = logging.getLogger(__name__)


class BasicAuthProviderPlugin(AuthenticationProviderPlugin):
    title = "Dolphin Plugin - Basic Authentication Provider"
    slug = "dolphin-auth-provider-basic"
    description = "Generic basic authentication provider."
    version = dolphin_plugin.__version__

    author = "Hale Terminal LLC"
    author_url = "https://github.com/hale-terminal/dolphin.git"

    def get_current_user(self, request: Request, **kwargs):
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            log.exception(
                f"Malformed authorization header. Scheme: {scheme} Param: {param} Authorization {authorization}"
            )
            return

        token = authorization.split()[1]

        try:
            data = jwt.decode(token, DOLPHIN_JWT_SECRET)
        except (JWKError, JWTError) as e:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=[{"msg": str(e)}])
        return data["username"]

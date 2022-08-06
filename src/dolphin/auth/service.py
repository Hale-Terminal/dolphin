import logging
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param

from jose import JWTError, jwt
from jose.exceptions import JWKError

from dolphin.config import DOLPHIN_JWT_SECRET

from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import User, UserRegister, UserUpdate


log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
)


def get(*, db_session, user_id: int) -> Optional[User]:
    return db_session.query(User).filter(User.id == user_id).one_or_none()


def get_by_email(*, db_session, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).one_or_none()


def get_by_username(*, db_session, username: str) -> Optional[User]:
    return db_session.query(User).filter(User.username == username).one_or_none()


def create(*, db_session, user_in: UserRegister) -> User:
    password = bytes(user_in.password, "utf-8")

    user = User(**user_in.dict(exclude={"password"}), password=password)

    db_session.add(user)
    db_session.commit()
    return user


def update(*, db_session, user: User, user_in: UserUpdate) -> User:
    user_data = user.dict()

    update_data = user_in.dict(exclude={"password"}, skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    if user_in.password:
        password = bytes(user_in.password, "utf-8")
        user.password = password

    db_session.commit()
    return user


def get_current_user(request: Request) -> User:
    username = _get_current_user(request)

    if not username:
        log.exception("Unable to determine username based on configured auth provider.")
        raise InvalidCredentialException

    return get_by_username(db_session=request.state.db, username=username)


def _get_current_user(request: Request):
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

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dolphin.database.core import get_db
from dolphin.models import PrimaryKey

from .models import (
    User,
    UserLogin,
    UserLoginResponse,
    UserPagination,
    UserRead,
    UserRegister,
    UserRegisterResponse,
    UserUpdate,
)

from .service import get_by_username, create, get, update, get_current_user


auth_router = APIRouter()
user_router = APIRouter()


@user_router.get("", response_model=UserPagination)
def get_users():
    pass


@user_router.get("/{user_id}", response_model=UserRead)
def get_user(*, db_session: Session = Depends(get_db), user_id: PrimaryKey):
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )
    return user


@user_router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    db_session: Session = Depends(get_db),
    user_id: PrimaryKey,
    user_in: UserUpdate,
):
    user = get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )

    return update(db_session=db_session, user=user, user_in=user_in)


@auth_router.get("/me", response_model=UserRead)
def get_me(
    *, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return current_user


@auth_router.post("/login", response_model=UserLoginResponse)
def login_user(user_in: UserLogin, db_session: Session = Depends(get_db)):
    user = get_by_username(db_session=db_session, username=user_in.username)
    if user and user.check_password(user_in.password):
        return {"token": user.token}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )


@auth_router.post("/register", response_model=UserRegisterResponse)
def register_user(user_in: UserRegister, db_session: Session = Depends(get_db)):
    user = create(db_session=db_session, user_in=user_in)
    return user

from fastapi import APIRouter, Depends

from dolphin.auth.service import get_current_user
from dolphin.auth.views import auth_router, user_router


api_router = APIRouter()


authenticated_api_router = APIRouter()


authenticated_api_router.include_router(user_router, prefix="/users", tags=["users"])


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


api_router.include_router(authenticated_api_router, dependencies=[Depends(get_current_user)])

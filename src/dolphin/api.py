from fastapi import APIRouter, Depends

from dolphin.auth.service import get_current_user
from dolphin.auth.views import auth_router, user_router
from dolphin.equity.views import router as equity_router
from dolphin.search.views import router as search_router


api_router = APIRouter()


authenticated_api_router = APIRouter()


authenticated_api_router.include_router(user_router, prefix="/users", tags=["users"])

authenticated_api_router.include_router(equity_router, prefix="/equity", tags=["equity"])
authenticated_api_router.include_router(search_router, prefix="/search", tags=["search"])


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])


@api_router.get("/health", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


@api_router.get("/serialnumber")
def serial():
    return {"serialNumber": "XXXXADKNORJ"}


api_router.include_router(authenticated_api_router, dependencies=[Depends(get_current_user)])

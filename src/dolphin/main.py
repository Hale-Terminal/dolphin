import time
import logging
from uuid import uuid1
from contextvars import ContextVar
from typing import Final, Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError

from sentry_asgi import SentryMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.routing import compile_path
from starlette.responses import Response, StreamingResponse

from sqlalchemy.orm import scoped_session

from .api import api_router
from .database.core import engine, sessionmaker
from .metrics import provider as metric_provider
from .common.utils.cli import install_plugins
from .extensions import configure_extensions


log = logging.getLogger(__name__)


configure_extensions()


async def not_found(request, exc):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)


exception_handlers = {404: not_found}


REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


app = FastAPI(exception_handlers=exception_handlers)

api = FastAPI(
    title="Dolphin",
    description="Welcome to Dolphin's API documentation! Here you will be able to discover all of the ways you can interact with the Dolphin API.",
    root_path="/api/v1",
    docs_url="/docs",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)


def get_path_params_from_request(request: Request) -> str:
    path_params = {}
    for r in api_router.routes:
        path_regex, path_format, param_converters = compile_path(r.path)
        path = request["path"].removeprefix("/api/v1")
        match = path_regex.match(path)
        if match:
            path_params = match.groupdict()
    return path_params


def get_path_template(request: Request) -> str:
    if hasattr(request, "path"):
        return ",".join(request.path.split("/")[1:])
    return ".".join(request.url.path.split("/")[1:])


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())

    ctx_token = _request_id_ctx_var.set(request_id)

    try:
        session = scoped_session(sessionmaker(bind=engine))
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        request.state.db.close()

    _request_id_ctx_var.reset(ctx_token)
    return response


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path_template = get_path_template(request)

        method = request.method
        tags = {"method": method, "endpoint": path_template}

        try:
            start = time.perf_counter()
            response = await call_next(request)
            elapsed_time = time.perf_counter() - start
        except Exception as e:
            metric_provider.counter("server.call.exception.counter", tags=tags)
            raise e from None
        else:
            tags.update({"status_code": response.status_code})
            metric_provider.timer("server.call.elapsed", value=elapsed_time, tags=tags)
            metric_provider.counter("server.call.counter", tags=tags)

        return response


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> StreamingResponse:
        try:
            response = await call_next(request)
        except ValidationError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": e.errors()}
            )
        except ValueError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]},
            )

        return response


api.add_middleware(SentryMiddleware)


# api.add_middleware(MetricsMiddleware)


api.add_middleware(ExceptionMiddleware)


install_plugins()


api.include_router(api_router)

app.mount("/api/v1", app=api)

import logging
import os
from typing import List
from pydantic import BaseModel

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

log = logging.getLogger(__name__)


class BaseConfigurationModel(BaseModel):
    pass


def get_env_tags(tag_list: List[str]) -> dict:
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")
        env_value = os.environ.get(env_key)
        if env_value:
            tags.update({tag_key: env_value})
    return tags


config = Config(".env")


LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")

ENV_TAG_LIST = config("ENV_TAGS", cast=CommaSeparatedStrings, default="")
ENV_TAGS = get_env_tags(ENV_TAG_LIST)

DOLPHIN_JWT_SECRET = config("DOLPHIN_JWT_SECRET", default=None)
DOLPHIN_JWT_ALG = config("DOLPHIN_JWT_ALG", default="HS256")
DOLPHIN_JWT_EXP = config("DOLPHIN_JWT_EXP", cast=int, default=86400)

SENTRY_ENABLED = config("SENTRY_ENABLED", cast=int, default=0)
SENTRY_DSN = config("SENTRY_DSN", default="")

DATABASE_ENABLED = config("DATABASE_ENABLED", cast=int, default=1)
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
DATABASE_USERNAME = config("DATABASE_USERNAME")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_NAME = config("DATABASE_NAME")
DATABASE_PORT = config("DATABASE_PORT", default="3306")
DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

INFLUX_ENABLED = config("INFLUX_ENABLED", cast=int, default=0)
INFLUX_HOST = config("INFLUX_HOST")
INFLUX_PORT = config("INFLUX_PORT", cast=int, default=8086)
INFLUX_DATABASE = config("INFLUX_DATABASE")
INFLUX_USER = config("INFLUX_USER")
INFLUX_PASSWORD = config("INFLUX_PASSWORD")
INFLUX_TIMEOUT = config("INFLUX_TIMEOUT", cast=int, default=5)
INFLUX_POOL_SIZE = config("INFLUX_POOL_SIZE", cast=int, default=50)
INFLUX_RETRY_TIME_SECONDS = config("INFLUX_RETRY_TIME_SECONDS", cast=int, default=120)
INFLUX_SUCCESSIVE_FAILURES = config("INFLUX_SUCCESSIVE_FAILURES", cast=int, default=3)

APP_NAME = config("APP_NAME", default="")
AMI_ID = config("AMI_ID", default="")
INSTANCE_ID = config("INSTANCE_ID", default="")
AVAILABILITY_ZONE = config("AVAILABILITY_ZONE", default="")
INSTANCE_TYPE = config("INSTANCE_TYPE", default="")
PORT = config("PORT", cast=int, default=0)

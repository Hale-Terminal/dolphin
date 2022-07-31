from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


def get_db_engine():
    connection_uri = URL.create(
        "mysql+pymysql",
        username="dolphin-dev",
        password="dolphin-dev",
        host="18.117.149.47",
        database="dolphin"
    )
    return create_engine(connection_uri, echo=False, pool_size=50, pool_pre_ping=True)

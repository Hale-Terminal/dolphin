import pytest

from sqlalchemy_utils import drop_database
from starlette.testclient import TestClient
from starlette.config import environ


# set test config
environ["DATABASE_CREDENTIALS"] = "postgres:dolphin"
environ["DATABASE_HOSTNAME"] = "localhost"
environ["DATABASE_NAME"] = "dolphin-test"
environ["DOLPHIN_ENCRYPTION_KEY"] = "test123"
environ["DOLPHIN_UI_URL"] = "https://example.com"
environ["ENV"] = "pytest"
environ["JWKS_URL"] = "example.com"
environ["DOLPHIN_JWT_SECRET"] = "test123"
environ["SECRET_PROVIDER"] = ""
environ["STATIC_DIR"] = ""  # we don't need static files for tests

from dolphin import config
from dolphin.database.core import engine
from dolphin.database.manage import init_database


from .database import Session


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")

    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed ({0})".format(previousfailed.name))


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


@pytest.fixture(scope="session")
def testapp():
    # we only want to use test plugins so unregister everybody else
    from dolphin.plugins.base import unregister, plugins
    from dolphin.main import app

    for p in plugins.all():
        unregister(p)

    yield app


@pytest.fixture(scope="session")
def db():
    init_database(engine)
    schema_engine = engine.execution_options(
        schema_translate_map={
            None: "dolphin_organization_default",
            "dolphin_core": "dolphin_core",
        }
    )
    Session.configure(bind=schema_engine)
    yield
    drop_database(str(config.SQLALCHEMY_DATABASE_URI))


@pytest.fixture(scope="function", autouse=True)
def session(db):
    """
    Creates a new database session with (with working transaction)
    for test duration.
    """
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()

import pytest
from click.testing import CliRunner
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient as StarletteTestClient

from alembic import command
from alembic.config import Config
from canarypy.api.db.base import Base
from canarypy.api.main import app


@pytest.fixture(autouse=True)
def monkeypatch_data_api_connection_vars(monkeypatch):
    monkeypatch.setenv("POSTGRES_USER", "data_api_service")
    monkeypatch.setenv("POSTGRES_PASSWORD", "defaultPassword")


def run_alembic(host, port, user, password, dbname):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option(
        "sqlalchemy.url", f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    )
    command.upgrade(alembic_cfg, "head")


api_postgres_proc = factories.postgresql_proc(load=[run_alembic])

api_postgres_db = factories.postgresql("api_postgres_proc")


@pytest.fixture(autouse=True)
def monkeypatch_migration_connection_vars(monkeypatch, api_postgres_db):
    monkeypatch.setenv("POSTGRES_USER", api_postgres_db.info.user)
    monkeypatch.setenv("POSTGRES_PASSWORD", api_postgres_db.info.password)
    monkeypatch.setenv("POSTGRES_HOST", api_postgres_db.info.host)
    monkeypatch.setenv("POSTGRES_PORT", str(api_postgres_db.info.port))
    monkeypatch.setenv("POSTGRES_DB", api_postgres_db.info.dbname)


# Move this to a proper fixture
# @pytest.fixture(autouse=True)
# def monkeypatch_migration_connection_vars(monkeypatch):
#     monkeypatch.setenv("POSTGRES_USER", 'postgres')
#     monkeypatch.setenv("POSTGRES_PASSWORD", 'password')
#     monkeypatch.setenv("POSTGRES_HOST", 'localhost')
#     monkeypatch.setenv("POSTGRES_PORT", '6543')
#     monkeypatch.setenv("POSTGRES_DB", 'canarypy')


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def client():

    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def db_session(api_postgres_db):
    """Database session for the unit tests."""

    def dbcreator():
        return api_postgres_db.cursor().connection

    engine = create_engine("postgresql+psycopg2://", creator=dbcreator)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

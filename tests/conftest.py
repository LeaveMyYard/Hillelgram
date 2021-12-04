from app import app
from core import db
from flask.testing import FlaskClient
from typing import Iterator
from sqlite3 import Connection
import pytest
from shutil import copyfile


@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    return app.test_client()


TEST_DB_FILE = "data/test.sqlite3"
TEST_DB_CURRENT_FILE = "data/current_test.sqlite3"


@pytest.fixture(scope="function")
def conn() -> Iterator[Connection]:
    initial_db = db.DB_FILE

    copyfile(TEST_DB_FILE, TEST_DB_CURRENT_FILE)
    db.DB_FILE = TEST_DB_CURRENT_FILE

    with db.get_connection() as conn:
        yield conn

    db.DB_FILE = initial_db

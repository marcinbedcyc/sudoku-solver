import os
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_server.api.dependencies import get_db
from fastapi_server.core.config import BASE_DIR
from fastapi_server.db.base import Base
from fastapi_server.main import app
from fastapi_server.models import User
from tests.test_data.users import USERS


TEST_DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'test.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@contextmanager
def test_db():
    """Simple context manager for database session connection"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def get_test_db():
    """Database dependency for override"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Client fixture with overrides database dependency"""
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def with_db():
    """Init empty database and drop all data on exit"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def users_data(with_db):
    """Init database with users' data to database and drop all data on exit"""
    with test_db() as db:
        for user in USERS:
            user_db = User(**user)
            db.add(user_db)
            db.commit()
            db.refresh(user_db)

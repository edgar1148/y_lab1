import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base


# Тестовая база данных
@pytest.fixture(scope="session")
def test_db():
    engine = create_engine("postgresql://testuser:testpassword@testdb:5432/testdb")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    SessionLocal.override_bind = engine
    db = SessionLocal()
    yield db
    db.close()

# Тестовый клиент FastAPI
@pytest.fixture
def client():
    return TestClient(app)

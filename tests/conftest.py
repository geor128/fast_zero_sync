import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from fast_zero.models import table_registry
from fast_zero.app import app
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    client = TestClient(app)
    return client

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    # aqui que processa o banco
    # gerenciamento de contexto
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)
    #return engine.connect()

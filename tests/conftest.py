from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.main import app, get_lrs


class InMemoryStore:
    """Simple in-memory store to capture xAPI statements during tests."""

    def __init__(self) -> None:
        self.statements: list[dict] = []

    def save_statement(self, statement: dict) -> None:
        self.statements.append(statement)


@pytest.fixture
def memory_store() -> InMemoryStore:
    return InMemoryStore()


@pytest.fixture
def client(memory_store: InMemoryStore):
    app.dependency_overrides[get_lrs] = lambda: memory_store
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

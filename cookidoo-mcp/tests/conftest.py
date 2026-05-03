import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
import os

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("COOKIDOO_EMAIL", "test@example.com")
    monkeypatch.setenv("COOKIDOO_PASSWORD", "test_password")
    monkeypatch.setenv("MCP_API_KEY", "test_api_key")
    monkeypatch.setenv("LOG_LEVEL", "ERROR")

@pytest.fixture
def mock_cookidoo():
    with patch("src.cookidoo_client.Cookidoo") as mock:
        instance = AsyncMock()
        instance.login = AsyncMock()
        mock.return_value = instance
        yield mock

@pytest.fixture
def client(mock_env, mock_cookidoo):
    from src.server import app
    with TestClient(app) as c:
        yield c

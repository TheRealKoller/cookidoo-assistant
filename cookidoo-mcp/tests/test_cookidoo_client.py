import pytest
from unittest.mock import AsyncMock, patch
from src.cookidoo_client import CookidooConnection

@pytest.mark.asyncio
async def test_cookidoo_connection_requires_credentials():
    with patch.dict("os.environ", {}, clear=True):
        conn = CookidooConnection()
        with pytest.raises(ValueError, match="COOKIDOO_EMAIL and COOKIDOO_PASSWORD must be set"):
            await conn.connect()

@pytest.mark.asyncio
async def test_cookidoo_connection_login(monkeypatch):
    monkeypatch.setenv("COOKIDOO_EMAIL", "test@example.com")
    monkeypatch.setenv("COOKIDOO_PASSWORD", "test_password")
    
    with patch("src.cookidoo_client.Cookidoo") as mock_cookidoo:
        mock_instance = AsyncMock()
        mock_instance.login = AsyncMock()
        mock_cookidoo.return_value = mock_instance
        
        conn = CookidooConnection()
        client = await conn.connect()
        
        mock_instance.login.assert_called_once_with("test@example.com", "test_password")
        assert client == mock_instance

@pytest.mark.asyncio
async def test_cookidoo_connection_disconnect(monkeypatch):
    monkeypatch.setenv("COOKIDOO_EMAIL", "test@example.com")
    monkeypatch.setenv("COOKIDOO_PASSWORD", "test_password")
    
    with patch("src.cookidoo_client.Cookidoo") as mock_cookidoo:
        mock_instance = AsyncMock()
        mock_cookidoo.return_value = mock_instance
        
        conn = CookidooConnection()
        await conn.connect()
        await conn.disconnect()
        
        assert conn._client is None

@pytest.mark.asyncio
async def test_cookidoo_client_property_raises_when_not_connected():
    conn = CookidooConnection()
    
    with pytest.raises(RuntimeError, match="Not connected"):
        _ = conn.client

import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import Request
from fastapi.responses import JSONResponse
from src.middleware import auth_middleware

@pytest.mark.asyncio
async def test_auth_middleware_allows_health_endpoint(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test_key")
    
    request = Mock(spec=Request)
    request.url.path = "/health"
    
    call_next = AsyncMock(return_value=JSONResponse({"status": "ok"}))
    
    response = await auth_middleware(request, call_next)
    
    call_next.assert_called_once()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_auth_middleware_validates_api_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "valid_key")
    
    request = Mock(spec=Request)
    request.url.path = "/api/test"
    request.headers.get = Mock(return_value="valid_key")
    
    call_next = AsyncMock(return_value=JSONResponse({"data": "ok"}))
    
    response = await auth_middleware(request, call_next)
    
    call_next.assert_called_once()
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_auth_middleware_rejects_invalid_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "valid_key")
    
    request = Mock(spec=Request)
    request.url.path = "/api/test"
    request.headers.get = Mock(return_value="invalid_key")
    request.client.host = "127.0.0.1"
    
    call_next = AsyncMock()
    
    response = await auth_middleware(request, call_next)
    
    call_next.assert_not_called()
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_auth_middleware_rejects_missing_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "valid_key")
    
    request = Mock(spec=Request)
    request.url.path = "/api/test"
    request.headers.get = Mock(return_value=None)
    request.client.host = "127.0.0.1"
    
    call_next = AsyncMock()
    
    response = await auth_middleware(request, call_next)
    
    call_next.assert_not_called()
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_auth_middleware_handles_missing_env_key(monkeypatch):
    monkeypatch.delenv("MCP_API_KEY", raising=False)
    
    request = Mock(spec=Request)
    request.url.path = "/api/test"
    request.headers.get = Mock(return_value="some_key")
    
    call_next = AsyncMock()
    
    response = await auth_middleware(request, call_next)
    
    call_next.assert_not_called()
    assert response.status_code == 500

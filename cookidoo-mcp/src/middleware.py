from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import os
from typing import Callable
from src.logging_config import logger

async def auth_middleware(request: Request, call_next: Callable):
    if request.url.path == "/health":
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    expected_key = os.getenv("MCP_API_KEY")
    
    if not expected_key:
        logger.error("MCP_API_KEY not configured")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Server misconfigured"}
        )
    
    if not api_key or api_key != expected_key:
        logger.warning(f"Unauthorized access attempt from {request.client.host}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid API key"}
        )
    
    return await call_next(request)

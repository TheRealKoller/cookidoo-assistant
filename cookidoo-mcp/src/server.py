import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.logging_config import logger
from src.middleware import auth_middleware
from src.cookidoo_client import cookidoo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting cookidoo-mcp server")
    try:
        await cookidoo_connection.connect()
        logger.info("Cookidoo connection established")
    except Exception as e:
        logger.error(f"Failed to connect to Cookidoo: {e}")
        raise
    
    yield
    
    logger.info("Shutting down cookidoo-mcp server")
    await cookidoo_connection.disconnect()

app = FastAPI(
    title="Cookidoo MCP Server",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.middleware("http")(auth_middleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "ok",
        "service": "cookidoo-mcp",
        "version": "0.1.0",
        "cookidoo_connected": cookidoo_connection._client is not None
    })

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

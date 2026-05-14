import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.logging_config import logger
from src.middleware import auth_middleware
from src.cookidoo_client import cookidoo_connection
from src.tools.recipe_details import get_recipe_details
from src.tools.search_recipes import search_recipes
from src.tools.recipe_nutrition import get_recipe_nutrition
from src.tools.types import SearchRecipesRequest

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

@app.post("/tools/get_recipe_details")
async def handle_get_recipe_details(recipe_id: str):
    """Get full recipe details by ID"""
    try:
        details = await get_recipe_details(recipe_id)
        return JSONResponse(details.model_dump())
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    except Exception as e:
        logger.error(f"Error in get_recipe_details: {e}", exc_info=True)
        return JSONResponse({"error": "Internal error"}, status_code=500)


@app.post("/tools/search_recipes")
async def handle_search_recipes(request: SearchRecipesRequest):
    """Search for recipes with various filters"""
    try:
        results = await search_recipes(
            query=request.query,
            ingredients=request.ingredients,
            diet=request.diet,
            exclude_ingredients=request.exclude_ingredients,
            max_results=request.max_results,
            offset=request.offset,
        )
        return JSONResponse(results.model_dump())
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        logger.error(f"Error in search_recipes: {e}", exc_info=True)
        return JSONResponse({"error": "Internal error"}, status_code=500)


@app.post("/tools/get_recipe_nutrition")
async def handle_get_recipe_nutrition(recipe_id: str):
    """Get nutritional information for a recipe"""
    try:
        nutrition = await get_recipe_nutrition(recipe_id)
        return JSONResponse(nutrition.model_dump())
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    except Exception as e:
        logger.error(f"Error in get_recipe_nutrition: {e}", exc_info=True)
        return JSONResponse({"error": "Internal error"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

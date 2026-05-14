"""Search recipes tool implementation."""

import re
from typing import Optional

from cookidoo_api import CookidooShoppingRecipeDetails

from ..cookidoo_client import cookidoo_connection
from .types import SearchRecipeResult, SearchRecipesResponse


async def search_recipes(
    query: Optional[str] = None,
    ingredients: Optional[list[str]] = None,
    diet: Optional[str] = None,
    exclude_ingredients: Optional[list[str]] = None,
    max_results: int = 20,
    offset: int = 0,
) -> SearchRecipesResponse:
    """Search for recipes with various filters.
    
    NOTE: Current implementation uses managed collections as the cookidoo-api 
    library does not expose a native search endpoint. This provides basic 
    functionality but may not cover all recipes in the Cookidoo database.
    
    Future improvement: Reverse engineer and implement direct search API endpoint.
    
    Args:
        query: Freetext search query (searches in title and description)
        ingredients: List of ingredients to search for
        diet: Dietary filter (omnivor, vegetarian, vegan, pescetarian)
        exclude_ingredients: Ingredients to exclude
        max_results: Maximum number of results to return (1-100)
        offset: Pagination offset
        
    Returns:
        SearchRecipesResponse with matching recipes and metadata
        
    Raises:
        ValueError: If parameters are invalid
        RuntimeError: If Cookidoo client is not connected
    """
    # Validate parameters
    if max_results < 1 or max_results > 100:
        raise ValueError("max_results must be between 1 and 100")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if diet and diet not in ["omnivor", "vegetarian", "vegan", "pescetarian"]:
        raise ValueError(f"Invalid diet filter: {diet}")
    
    # Get client
    client = cookidoo_connection.client
    
    # Normalize inputs for case-insensitive matching
    ingredients_lower = [ing.lower() for ing in (ingredients or [])]
    exclude_ingredients_lower = [ing.lower() for ing in (exclude_ingredients or [])]
    query_lower = query.lower() if query else None
    
    # Collect recipes from managed collections
    # We'll fetch multiple pages to get a good sample size
    all_recipe_ids: set[str] = set()
    collections_to_fetch = 5  # Fetch first 5 pages of collections
    
    for page in range(collections_to_fetch):
        try:
            collections = await client.get_managed_collections(page=page)
            if not collections:
                break
                
            for collection in collections:
                for chapter in collection.chapters:
                    for recipe in chapter.recipes:
                        all_recipe_ids.add(recipe.id)
        except Exception:
            # If we fail to get a page, just continue with what we have
            break
    
    # Now filter recipes based on search criteria
    matching_recipes: list[SearchRecipeResult] = []
    
    for recipe_id in all_recipe_ids:
        try:
            # Get full recipe details for filtering
            details = await client.get_recipe_details(recipe_id)
            
            # Apply filters
            if not _matches_filters(
                details,
                query_lower,
                ingredients_lower,
                exclude_ingredients_lower,
                diet,
            ):
                continue
            
            # Convert to search result
            search_result = _convert_to_search_result(details)
            matching_recipes.append(search_result)
            
        except Exception:
            # Skip recipes that fail to load
            continue
    
    # Sort by title for consistent ordering
    matching_recipes.sort(key=lambda r: r.title)
    
    # Apply pagination
    total = len(matching_recipes)
    paginated_recipes = matching_recipes[offset : offset + max_results]
    
    return SearchRecipesResponse(
        recipes=paginated_recipes,
        total=total,
        offset=offset,
        limit=max_results,
    )


def _matches_filters(
    details: CookidooShoppingRecipeDetails,
    query: Optional[str],
    ingredients: list[str],
    exclude_ingredients: list[str],
    diet: Optional[str],
) -> bool:
    """Check if recipe matches all filters."""
    
    # Query filter (searches in title and description)
    if query:
        title_lower = details.name.lower()
        desc_lower = (details.description or "").lower()
        
        if query not in title_lower and query not in desc_lower:
            return False
    
    # Get ingredient names from recipe
    recipe_ingredient_names = [
        ing.name.lower() 
        for ing in details.ingredients
    ]
    
    # Ingredients filter (all must be present)
    if ingredients:
        for required_ing in ingredients:
            if not any(required_ing in rec_ing for rec_ing in recipe_ingredient_names):
                return False
    
    # Exclude ingredients filter (none must be present)
    if exclude_ingredients:
        for excluded_ing in exclude_ingredients:
            if any(excluded_ing in rec_ing for rec_ing in recipe_ingredient_names):
                return False
    
    # Diet filter
    if diet:
        if not _matches_diet(recipe_ingredient_names, diet):
            return False
    
    return True


def _matches_diet(ingredient_names: list[str], diet: str) -> bool:
    """Check if recipe matches dietary restrictions.
    
    This is a basic implementation using common ingredient patterns.
    Could be improved with a more comprehensive ingredient database.
    """
    # Common meat/fish/animal product keywords
    meat_keywords = [
        "beef", "pork", "chicken", "turkey", "lamb", "duck", "meat",
        "bacon", "ham", "sausage", "salami", "prosciutto", "steak",
    ]
    fish_keywords = [
        "fish", "salmon", "tuna", "cod", "trout", "shrimp", "prawn",
        "crab", "lobster", "seafood", "anchovy", "sardine",
    ]
    dairy_keywords = [
        "milk", "cream", "cheese", "butter", "yogurt", "yoghurt",
    ]
    egg_keywords = ["egg"]
    
    has_meat = any(
        any(keyword in ing for keyword in meat_keywords)
        for ing in ingredient_names
    )
    has_fish = any(
        any(keyword in ing for keyword in fish_keywords)
        for ing in ingredient_names
    )
    has_dairy = any(
        any(keyword in ing for keyword in dairy_keywords)
        for ing in ingredient_names
    )
    has_eggs = any(
        any(keyword in ing for keyword in egg_keywords)
        for ing in ingredient_names
    )
    
    if diet == "vegan":
        return not (has_meat or has_fish or has_dairy or has_eggs)
    elif diet == "vegetarian":
        return not (has_meat or has_fish)
    elif diet == "pescetarian":
        return not has_meat
    elif diet == "omnivor":
        # Omnivores can eat anything
        return True
    
    return True


def _convert_to_search_result(
    details: CookidooShoppingRecipeDetails,
) -> SearchRecipeResult:
    """Convert full recipe details to search result."""
    # Extract image URL from image data if available
    image_url = None
    if hasattr(details, 'image') and details.image:
        # The image might be a URL or a data structure
        if isinstance(details.image, str):
            image_url = details.image
        elif hasattr(details.image, 'url'):
            image_url = details.image.url
    
    # Get cooking time in minutes
    cooking_time = None
    if hasattr(details, 'total_time') and details.total_time:
        cooking_time = details.total_time // 60  # Convert seconds to minutes
    
    # Extract difficulty if available
    difficulty = None
    if hasattr(details, 'difficulty'):
        difficulty = details.difficulty
    
    return SearchRecipeResult(
        id=details.id,
        title=details.name,
        description=details.description,
        image_url=image_url,
        cooking_time=cooking_time,
        difficulty=difficulty,
    )

from typing import Optional
from src.cookidoo_client import cookidoo_connection
from src.tools.types import RecipeDetails, RecipeIngredient, RecipeStep
from src.logging_config import logger


async def get_recipe_details(recipe_id: str) -> RecipeDetails:
    """
    Retrieve full recipe details from Cookidoo API.
    
    Args:
        recipe_id: Cookidoo recipe ID
        
    Returns:
        RecipeDetails object with complete recipe information
        
    Raises:
        ValueError: If recipe_id is invalid or recipe not found
    """
    if not recipe_id:
        raise ValueError("recipe_id is required")
    
    try:
        client = cookidoo_connection.client
        details = await client.get_recipe_details(recipe_id)
        
        # Parse ingredients
        ingredients = []
        for group in details.nutrition_groups:
            for ingredient in group.get("ingredients", []):
                ingredients.append(RecipeIngredient(
                    name=ingredient.get("name", ""),
                    quantity=ingredient.get("quantity"),
                    unit=ingredient.get("unit")
                ))
        
        # Parse instructions (from notes)
        instructions = []
        if details.notes:
            for idx, note in enumerate(details.notes, 1):
                instructions.append(RecipeStep(
                    step_number=idx,
                    instruction=note.get("text", ""),
                    duration=note.get("duration")
                ))
        
        # Parse equipment
        equipment = [u.get("name", "") for u in details.utensils] if details.utensils else []
        
        # Parse tags
        tags = []
        if details.categories:
            tags.extend(details.categories)
        if details.collections:
            tags.extend([c.get("name", "") for c in details.collections])
        
        return RecipeDetails(
            id=recipe_id,
            title=details.get("title", "Unknown"),
            description=details.get("description"),
            image_url=details.get("image_url"),
            cooking_time=details.total_time // 60 if details.total_time else None,
            prep_time=details.active_time // 60 if details.active_time else None,
            difficulty=details.difficulty,
            servings=details.serving_size,
            ingredients=ingredients,
            instructions=instructions,
            tags=list(set(tags)),  # dedupe
            equipment=equipment
        )
        
    except Exception as e:
        logger.error(f"Failed to get recipe details for {recipe_id}: {e}")
        raise ValueError(f"Recipe not found or API error: {e}")

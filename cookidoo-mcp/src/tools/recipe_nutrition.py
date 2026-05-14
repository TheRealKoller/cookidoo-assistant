"""Get recipe nutrition information tool implementation."""

from typing import Optional

from ..cookidoo_client import cookidoo_connection
from .types import RecipeNutrition, NutrientInfo


async def get_recipe_nutrition(recipe_id: str) -> RecipeNutrition:
    """Get nutritional information for a recipe.
    
    Args:
        recipe_id: Cookidoo recipe ID
        
    Returns:
        RecipeNutrition object with nutritional data per serving
        
    Raises:
        ValueError: If recipe_id is invalid or recipe not found
        RuntimeError: If Cookidoo client is not connected
    """
    if not recipe_id:
        raise ValueError("recipe_id is required")
    
    try:
        client = cookidoo_connection.client
        details = await client.get_recipe_details(recipe_id)
        
        # Initialize nutrition data
        serving_size = details.serving_size or 1
        
        # Extract all nutrients from nutrition_groups
        nutrients = []
        calories = None
        protein = None
        carbohydrates = None
        fat = None
        fiber = None
        sugar = None
        sodium = None
        saturated_fat = None
        
        # Parse nutrition_groups
        for nutrition_group in details.nutrition_groups:
            for recipe_nutrition in nutrition_group.recipe_nutritions:
                for nutrition in recipe_nutrition.nutritions:
                    nutrient_type = nutrition.type.lower()
                    value = nutrition.number
                    unit = nutrition.unittype
                    
                    # Store full nutrient info
                    nutrients.append(NutrientInfo(
                        value=value,
                        unit=unit,
                        type=nutrition.type
                    ))
                    
                    # Map to common fields based on nutrient type
                    if nutrient_type == "energy" or nutrient_type == "calories":
                        # Energy is usually in kcal or kJ
                        if unit.lower() in ["kcal", "cal"]:
                            calories = value
                        elif unit.lower() == "kj":
                            # Convert kJ to kcal (1 kcal = 4.184 kJ)
                            calories = value / 4.184
                    
                    elif nutrient_type == "protein" or "protein" in nutrient_type:
                        if unit.lower() == "g":
                            protein = value
                    
                    elif nutrient_type == "carbohydrate" or "carbohydrate" in nutrient_type:
                        if unit.lower() == "g":
                            carbohydrates = value
                    
                    elif nutrient_type == "fat" or nutrient_type == "total fat":
                        if unit.lower() == "g":
                            fat = value
                    
                    elif "saturated" in nutrient_type and "fat" in nutrient_type:
                        if unit.lower() == "g":
                            saturated_fat = value
                    
                    elif nutrient_type == "fiber" or "fiber" in nutrient_type or "fibre" in nutrient_type:
                        if unit.lower() == "g":
                            fiber = value
                    
                    elif nutrient_type == "sugar" or "sugar" in nutrient_type:
                        if unit.lower() == "g":
                            sugar = value
                    
                    elif nutrient_type == "sodium" or "sodium" in nutrient_type:
                        if unit.lower() == "mg":
                            sodium = value
                        elif unit.lower() == "g":
                            sodium = value * 1000  # Convert g to mg
        
        return RecipeNutrition(
            recipe_id=recipe_id,
            serving_size=serving_size,
            calories=calories,
            protein=protein,
            carbohydrates=carbohydrates,
            fat=fat,
            fiber=fiber,
            sugar=sugar,
            sodium=sodium,
            saturated_fat=saturated_fat,
            nutrients=nutrients,
        )
        
    except Exception as e:
        raise ValueError(f"Failed to get recipe nutrition: {str(e)}")

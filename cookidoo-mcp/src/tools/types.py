from typing import Optional
from pydantic import BaseModel, Field


class RecipeIngredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None


class RecipeStep(BaseModel):
    step_number: int
    instruction: str
    duration: Optional[int] = None  # seconds


class RecipeDetails(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    cooking_time: Optional[int] = None  # minutes
    prep_time: Optional[int] = None  # minutes
    difficulty: Optional[str] = None
    servings: Optional[int] = None
    ingredients: list[RecipeIngredient] = Field(default_factory=list)
    instructions: list[RecipeStep] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    equipment: list[str] = Field(default_factory=list)


class SearchRecipeResult(BaseModel):
    """Simplified recipe result for search operations."""
    id: str
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    cooking_time: Optional[int] = None  # minutes
    difficulty: Optional[str] = None


class SearchRecipesRequest(BaseModel):
    """Request parameters for recipe search."""
    query: Optional[str] = None
    ingredients: list[str] = Field(default_factory=list)
    diet: Optional[str] = None  # omnivor, vegetarian, vegan, pescetarian
    exclude_ingredients: list[str] = Field(default_factory=list)
    max_results: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class SearchRecipesResponse(BaseModel):
    """Response containing search results and metadata."""
    recipes: list[SearchRecipeResult] = Field(default_factory=list)
    total: int
    offset: int
    limit: int


class NutrientInfo(BaseModel):
    """Single nutrient information."""
    value: float
    unit: str
    type: str  # e.g., "energy", "protein", "carbohydrate", etc.


class RecipeNutrition(BaseModel):
    """Nutritional information for a recipe."""
    recipe_id: str
    serving_size: int
    calories: Optional[float] = None  # kcal per serving
    protein: Optional[float] = None  # grams per serving
    carbohydrates: Optional[float] = None  # grams per serving
    fat: Optional[float] = None  # grams per serving
    fiber: Optional[float] = None  # grams per serving
    sugar: Optional[float] = None  # grams per serving
    sodium: Optional[float] = None  # mg per serving
    saturated_fat: Optional[float] = None  # grams per serving
    nutrients: list[NutrientInfo] = Field(default_factory=list)  # All available nutrients

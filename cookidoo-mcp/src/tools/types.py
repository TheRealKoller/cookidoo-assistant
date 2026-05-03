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

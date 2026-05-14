# get_recipe_nutrition MCP Tool

Retrieve nutritional information for Cookidoo recipes.

## Endpoint

`POST /tools/get_recipe_nutrition`

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `recipe_id` | string | Yes | Cookidoo recipe ID |

## Response

Returns `RecipeNutrition` object:

```json
{
  "recipe_id": "r123456",
  "serving_size": 4,
  "calories": 450.0,
  "protein": 25.5,
  "carbohydrates": 50.0,
  "fat": 15.0,
  "fiber": 8.0,
  "sugar": 12.0,
  "sodium": 500.0,
  "saturated_fat": 3.5,
  "nutrients": [
    {
      "value": 450.0,
      "unit": "kcal",
      "type": "energy"
    },
    {
      "value": 25.5,
      "unit": "g",
      "type": "protein"
    }
  ]
}
```

## Fields

### RecipeNutrition
- `recipe_id` - Cookidoo recipe ID
- `serving_size` - Number of servings (default: 1 if not specified)
- `calories` - Total calories per serving in kcal (optional)
- `protein` - Protein in grams per serving (optional)
- `carbohydrates` - Carbohydrates in grams per serving (optional)
- `fat` - Total fat in grams per serving (optional)
- `fiber` - Dietary fiber in grams per serving (optional)
- `sugar` - Sugar in grams per serving (optional)
- `sodium` - Sodium in milligrams per serving (optional)
- `saturated_fat` - Saturated fat in grams per serving (optional)
- `nutrients[]` - Complete list of all available nutrients

### NutrientInfo
- `value` - Nutrient value (numeric)
- `unit` - Unit of measurement (e.g., "g", "mg", "kcal")
- `type` - Nutrient type/name (e.g., "protein", "energy")

## Behavior

### Energy Conversion
- Energy values in kJ are automatically converted to kcal (1 kcal = 4.184 kJ)
- Both kcal and kJ values are supported

### Sodium Conversion
- Sodium values in grams are automatically converted to milligrams
- Both g and mg values are supported

### Missing Data
- If a recipe has no nutrition data, all nutrient fields will be `null`
- The `nutrients` array will be empty
- `serving_size` defaults to 1 if not provided

### Per-Serving Values
- All values are calculated per serving
- Use `serving_size` to calculate total recipe nutrition

## Errors

- `404` - Recipe not found, invalid ID, or failed to retrieve nutrition data
- `500` - Internal server error

## Examples

### Basic Request
Get nutrition information for a recipe:
```bash
curl -X POST http://localhost:3000/tools/get_recipe_nutrition \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  --data-urlencode "recipe_id=r123456"
```

### With Query Parameters
```bash
curl -X POST "http://localhost:3000/tools/get_recipe_nutrition?recipe_id=r123456" \
  -H "X-API-Key: your-api-key"
```

### Response with Complete Data
```json
{
  "recipe_id": "r123456",
  "serving_size": 4,
  "calories": 450.0,
  "protein": 25.5,
  "carbohydrates": 50.0,
  "fat": 15.0,
  "fiber": 8.0,
  "sugar": 12.0,
  "sodium": 500.0,
  "saturated_fat": 3.5,
  "nutrients": [
    {"value": 450.0, "unit": "kcal", "type": "energy"},
    {"value": 25.5, "unit": "g", "type": "protein"},
    {"value": 50.0, "unit": "g", "type": "carbohydrate"},
    {"value": 15.0, "unit": "g", "type": "fat"},
    {"value": 8.0, "unit": "g", "type": "fiber"},
    {"value": 12.0, "unit": "g", "type": "sugar"},
    {"value": 500.0, "unit": "mg", "type": "sodium"},
    {"value": 3.5, "unit": "g", "type": "saturated fat"}
  ]
}
```

### Response without Nutrition Data
```json
{
  "recipe_id": "r999999",
  "serving_size": 2,
  "calories": null,
  "protein": null,
  "carbohydrates": null,
  "fat": null,
  "fiber": null,
  "sugar": null,
  "sodium": null,
  "saturated_fat": null,
  "nutrients": []
}
```

### Response with Partial Data
Some recipes may have incomplete nutrition information:
```json
{
  "recipe_id": "r555555",
  "serving_size": 2,
  "calories": 300.0,
  "protein": 20.0,
  "carbohydrates": null,
  "fat": null,
  "fiber": null,
  "sugar": null,
  "sodium": null,
  "saturated_fat": null,
  "nutrients": [
    {"value": 300.0, "unit": "kcal", "type": "energy"},
    {"value": 20.0, "unit": "g", "type": "protein"}
  ]
}
```

## Use Cases

### Meal Planning
Calculate total daily nutrition by summing values across multiple recipes:
```python
# Get nutrition for multiple recipes
breakfast = await get_recipe_nutrition("r111111")
lunch = await get_recipe_nutrition("r222222")
dinner = await get_recipe_nutrition("r333333")

# Calculate daily totals
total_calories = (breakfast.calories or 0) + (lunch.calories or 0) + (dinner.calories or 0)
total_protein = (breakfast.protein or 0) + (lunch.protein or 0) + (dinner.protein or 0)
```

### Dietary Goals
Check if recipe meets dietary requirements:
```python
nutrition = await get_recipe_nutrition("r123456")

# High protein, low carb check
if nutrition.protein and nutrition.carbohydrates:
    protein_ratio = nutrition.protein / nutrition.carbohydrates
    if protein_ratio > 0.5:
        print("High protein recipe!")
```

### Scaling Recipes
Calculate nutrition for different serving sizes:
```python
nutrition = await get_recipe_nutrition("r123456")
desired_servings = 8

# Scale up from 4 servings to 8
scale_factor = desired_servings / nutrition.serving_size
scaled_calories = (nutrition.calories or 0) * scale_factor
```

## Notes

- Recipe IDs can be obtained from `search_recipes` or `get_recipe_details`
- Not all recipes have complete nutrition data
- Always check for `null` values before performing calculations
- Nutrition values are extracted from `nutrition_groups` in the Cookidoo API
- The `nutrients` array contains all raw nutrition data from the API

## Related Tools

- `get_recipe_details` - Get full recipe details including ingredients
- `search_recipes` - Search for recipes by criteria

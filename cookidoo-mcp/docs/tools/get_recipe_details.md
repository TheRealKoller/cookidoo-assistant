# get_recipe_details MCP Tool

Retrieve full recipe details from Cookidoo.

## Endpoint

`POST /tools/get_recipe_details`

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `recipe_id` | string | Yes | Cookidoo recipe ID |

## Response

Returns `RecipeDetails` object:

```json
{
  "id": "r123456",
  "title": "Tomato Soup",
  "description": "A delicious creamy tomato soup",
  "image_url": "https://cookidoo.com/images/...",
  "cooking_time": 30,
  "prep_time": 10,
  "difficulty": "easy",
  "servings": 4,
  "ingredients": [
    {
      "name": "Tomatoes",
      "quantity": 500,
      "unit": "g"
    }
  ],
  "instructions": [
    {
      "step_number": 1,
      "instruction": "Add ingredients to bowl",
      "duration": 120
    }
  ],
  "tags": ["vegetarian", "soup", "main-dish"],
  "equipment": ["Thermomix", "Spatula"]
}
```

## Fields

- `id` - Cookidoo recipe ID
- `title` - Recipe name
- `description` - Recipe description (optional)
- `image_url` - Recipe image URL (optional)
- `cooking_time` - Total cooking time in minutes (optional)
- `prep_time` - Preparation time in minutes (optional)
- `difficulty` - Difficulty level: easy, medium, hard (optional)
- `servings` - Number of servings (optional)
- `ingredients[]` - List of ingredients
  - `name` - Ingredient name
  - `quantity` - Amount (optional)
  - `unit` - Unit of measurement (optional)
- `instructions[]` - Cooking steps
  - `step_number` - Step order
  - `instruction` - Step description
  - `duration` - Step duration in seconds (optional)
- `tags[]` - Categories and tags
- `equipment[]` - Required equipment

## Errors

- `404` - Recipe not found or invalid ID
- `500` - Internal server error

## Example

```bash
curl -X POST http://localhost:3000/tools/get_recipe_details \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"recipe_id": "r123456"}'
```

## Notes

- Recipe IDs can be obtained from collections or calendar endpoints
- Some fields may be null if not provided by Cookidoo API
- Tags are deduplicated from categories and collections
- Times are converted from seconds to minutes

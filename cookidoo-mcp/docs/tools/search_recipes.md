# search_recipes MCP Tool

Search for recipes on Cookidoo with support for text queries, ingredient filters, dietary restrictions, and more.

## Endpoint

`POST /tools/search_recipes`

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `query` | string | No | - | Freetext search query (searches in title and description) |
| `ingredients` | string[] | No | [] | List of ingredients that must be present in the recipe |
| `diet` | string | No | - | Dietary filter: `omnivor`, `vegetarian`, `vegan`, or `pescetarian` |
| `exclude_ingredients` | string[] | No | [] | Ingredients that must NOT be in the recipe |
| `max_results` | number | No | 20 | Maximum number of results (1-100) |
| `offset` | number | No | 0 | Pagination offset (0-based) |

## Response

Returns `SearchRecipesResponse` object:

```json
{
  "recipes": [
    {
      "id": "r123456",
      "title": "Tomato Soup",
      "description": "A delicious creamy tomato soup",
      "image_url": "https://cookidoo.com/images/...",
      "cooking_time": 30,
      "difficulty": "easy"
    }
  ],
  "total": 42,
  "offset": 0,
  "limit": 20
}
```

## Fields

### SearchRecipesResponse
- `recipes[]` - Array of matching recipes
- `total` - Total number of matching recipes (before pagination)
- `offset` - Current pagination offset
- `limit` - Maximum results per page

### SearchRecipeResult
- `id` - Cookidoo recipe ID
- `title` - Recipe name
- `description` - Recipe description (optional)
- `image_url` - Recipe image URL (optional)
- `cooking_time` - Total cooking time in minutes (optional)
- `difficulty` - Difficulty level: easy, medium, hard (optional)

## Filters

### Query Filter
Searches for text in both recipe title and description (case-insensitive):
```json
{"query": "pasta"}
```

### Ingredient Filter
All specified ingredients must be present in the recipe:
```json
{"ingredients": ["tomato", "basil", "garlic"]}
```

### Diet Filter
Filters recipes based on dietary restrictions:
- `vegan` - No meat, fish, dairy, or eggs
- `vegetarian` - No meat or fish (dairy and eggs allowed)
- `pescetarian` - No meat (fish, dairy, and eggs allowed)
- `omnivor` - No restrictions

```json
{"diet": "vegan"}
```

### Exclude Ingredients
Filters out recipes containing specified ingredients:
```json
{"exclude_ingredients": ["nuts", "gluten"]}
```

### Pagination
Use `offset` and `max_results` for pagination:
```json
{
  "max_results": 10,
  "offset": 0
}
```

## Errors

- `400` - Invalid parameters (e.g., invalid diet, max_results out of range)
- `500` - Internal server error

## Examples

### Basic Search
Search for recipes containing "soup":
```bash
curl -X POST http://localhost:3000/tools/search_recipes \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "soup"}'
```

### Search with Ingredients
Find recipes with tomatoes and basil:
```bash
curl -X POST http://localhost:3000/tools/search_recipes \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": ["tomato", "basil"]
  }'
```

### Vegan Recipes
Find vegan recipes:
```bash
curl -X POST http://localhost:3000/tools/search_recipes \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "diet": "vegan"
  }'
```

### Complex Search
Search for vegetarian pasta recipes without nuts:
```bash
curl -X POST http://localhost:3000/tools/search_recipes \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "pasta",
    "diet": "vegetarian",
    "exclude_ingredients": ["nuts"],
    "max_results": 10
  }'
```

### Pagination
Get second page of results (items 20-39):
```bash
curl -X POST http://localhost:3000/tools/search_recipes \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "max_results": 20,
    "offset": 20
  }'
```

## Implementation Notes

**Current Limitations:**
- The cookidoo-api library does not expose a native search endpoint
- Current implementation uses managed collections as a data source
- This may not cover all recipes in the Cookidoo database
- Performance may be slower for large result sets due to client-side filtering

**Future Improvements:**
- Reverse engineer and implement direct Cookidoo search API endpoint
- Add caching for collection data
- Implement full-text search indexing
- Add more sophisticated ingredient matching

**Filter Behavior:**
- All filters are combined with AND logic (all must match)
- Text search is case-insensitive
- Ingredient matching is partial (e.g., "tomato" matches "cherry tomatoes")
- Diet filters use keyword-based detection and may have false positives/negatives

## Tips

1. **Start Broad**: Begin with fewer filters and refine as needed
2. **Pagination**: Use reasonable `max_results` values (10-50) for better performance
3. **Ingredient Names**: Use common ingredient names (e.g., "tomato" not "tomatoes")
4. **Diet Filter**: Combine with ingredient filters for more accurate results
5. **Total Count**: Use the `total` field to implement pagination UI

## Related Tools

- `get_recipe_details` - Get full details for a specific recipe by ID

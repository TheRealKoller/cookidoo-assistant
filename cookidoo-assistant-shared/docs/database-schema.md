# Database Schema Documentation

## Overview

The Cookidoo Assistant database schema is designed to store user data, preferences, health information, and meal planning data. It consists of 8 core tables with PostgreSQL as the database.

## Entity Relationship Diagram

```
users (1) ──┬── (1) user_profiles
            ├── (1) dietary_preferences
            ├── (*) allergies
            ├── (1) health_data
            ├── (*) recipe_ratings
            └── (*) week_plans
                    └── (*) week_plan_meals
```

## Tables

### 1. `users`
Core user table containing only basic metadata.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key (auto-generated) |
| created_at | TIMESTAMP | Auto-generated creation timestamp |
| updated_at | TIMESTAMP | Auto-updated modification timestamp |

**Relationships:**
- One-to-one with `user_profiles`
- One-to-one with `dietary_preferences`
- One-to-many with `allergies`
- One-to-one with `health_data`
- One-to-many with `recipe_ratings`
- One-to-many with `week_plans`

---

### 2. `user_profiles`
Physical attributes and basic user information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| user_id | UUID | FK, UNIQUE, NOT NULL | Reference to users |
| height | DECIMAL(5,2) | - | Height in cm (e.g., 175.50) |
| weight | DECIMAL(5,2) | - | Weight in kg (e.g., 70.50) |
| age | INTEGER | CHECK (age > 0 AND age < 150) | User age |
| gender | VARCHAR(20) | CHECK (male, female, other) | User gender |
| created_at | TIMESTAMP | - | Auto-generated |
| updated_at | TIMESTAMP | - | Auto-updated |

**Indexes:**
- `idx_user_profiles_user_id` on `user_id`

---

### 3. `dietary_preferences`
User's dietary type (only one per user).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| user_id | UUID | FK, UNIQUE, NOT NULL | Reference to users |
| diet_type | VARCHAR(50) | CHECK (omnivor, vegetarian, vegan, pescetarian) | Diet type |
| created_at | TIMESTAMP | - | Auto-generated |
| updated_at | TIMESTAMP | - | Auto-updated |

**Indexes:**
- `idx_dietary_preferences_user_id` on `user_id`

---

### 4. `allergies`
User allergies and intolerances (multiple allowed).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| user_id | UUID | FK, NOT NULL | Reference to users |
| allergen | VARCHAR(100) | NOT NULL | Allergen name |
| severity | VARCHAR(20) | CHECK (mild, moderate, severe) | Allergy severity |
| created_at | TIMESTAMP | - | Auto-generated |
| updated_at | TIMESTAMP | - | Auto-updated |

**Indexes:**
- `idx_allergies_user_id` on `user_id`
- `idx_allergies_allergen` on `allergen`

---

### 5. `health_data`
Health goals and nutrition targets (one per user).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| user_id | UUID | FK, UNIQUE, NOT NULL | Reference to users |
| activity_level | VARCHAR(50) | CHECK (sedentary, light, moderate, active, very_active) | Activity level |
| health_goal | VARCHAR(50) | CHECK (lose_weight, maintain_weight, gain_weight) | Health goal |
| calorie_target | INTEGER | CHECK (> 0) | Daily calorie target |
| protein_target | DECIMAL(6,2) | CHECK (>= 0) | Daily protein in grams |
| fat_target | DECIMAL(6,2) | CHECK (>= 0) | Daily fat in grams |
| carbs_target | DECIMAL(6,2) | CHECK (>= 0) | Daily carbs in grams |
| auto_calculated | BOOLEAN | DEFAULT TRUE | Were targets auto-calculated? |
| created_at | TIMESTAMP | - | Auto-generated |
| updated_at | TIMESTAMP | - | Auto-updated |

**Indexes:**
- `idx_health_data_user_id` on `user_id`

---

### 6. `recipe_ratings`
User recipe preferences and ratings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| user_id | UUID | FK, NOT NULL | Reference to users |
| recipe_id | VARCHAR(100) | NOT NULL | Cookidoo recipe ID |
| liked | BOOLEAN | NOT NULL | true=liked, false=disliked |
| automatic | BOOLEAN | DEFAULT FALSE | Auto-tracked vs manual feedback |
| count | INTEGER | DEFAULT 1, CHECK (> 0) | Number of times this rating occurred |
| created_at | TIMESTAMP | - | Auto-generated |
| updated_at | TIMESTAMP | - | Auto-updated |

**Constraints:**
- UNIQUE(user_id, recipe_id)

**Indexes:**
- `idx_recipe_ratings_user_id` on `user_id`
- `idx_recipe_ratings_recipe_id` on `recipe_id`
- `idx_recipe_ratings_liked` on `liked`
- `idx_recipe_ratings_user_recipe` on `(user_id, recipe_id)`

---

### 7. `week_plans`
Weekly meal plans.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| user_id | UUID | FK, NOT NULL | Reference to users |
| week_start_date | DATE | NOT NULL | Start date of the week |
| status | VARCHAR(20) | CHECK (draft, active, completed, archived) | Plan status |
| created_at | TIMESTAMP | - | Auto-generated |
| updated_at | TIMESTAMP | - | Auto-updated |

**Indexes:**
- `idx_week_plans_user_id` on `user_id`
- `idx_week_plans_status` on `status`
- `idx_week_plans_week_start` on `week_start_date`
- `idx_week_plans_user_week` on `(user_id, week_start_date)`

---

### 8. `week_plan_meals`
Individual meals within a week plan.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| week_plan_id | UUID | FK, NOT NULL | Reference to week_plans |
| day_of_week | INTEGER | CHECK (>= 0 AND <= 6) | 0=Monday, 6=Sunday |
| recipe_id | VARCHAR(100) | NOT NULL | Cookidoo recipe ID |
| recipe_title | VARCHAR(255) | NOT NULL | Recipe title (cached) |
| position | INTEGER | DEFAULT 0, CHECK (>= 0) | For multiple options: 0=first, 1=second |
| selected | BOOLEAN | DEFAULT TRUE | Is this option currently selected? |
| created_at | TIMESTAMP | - | Auto-generated |
| updated_at | TIMESTAMP | - | Auto-updated |

**Indexes:**
- `idx_week_plan_meals_week_plan_id` on `week_plan_id`
- `idx_week_plan_meals_recipe_id` on `recipe_id`
- `idx_week_plan_meals_day` on `day_of_week`

---

## Features

### Automatic Timestamps
All tables have `created_at` and `updated_at` columns that are automatically managed:
- `created_at`: Set to NOW() on insert
- `updated_at`: Automatically updated on any row modification via triggers

### Cascade Deletes
Foreign key constraints use `ON DELETE CASCADE`, so deleting a user automatically deletes all related data:
- user_profiles
- dietary_preferences
- allergies
- health_data
- recipe_ratings
- week_plans (and their week_plan_meals via another cascade)

### Data Validation
- CHECK constraints ensure valid enum values
- Age must be between 1 and 149
- All targets must be positive
- Day of week must be 0-6

### Performance Optimizations
- Indexes on all foreign keys
- Composite indexes for common query patterns (e.g., `user_id + recipe_id`)
- Indexes on frequently filtered columns (status, week_start_date, liked)

---

## Usage Examples

### Create a User with Profile

```sql
-- Insert user
INSERT INTO users (id) VALUES (uuid_generate_v4())
RETURNING id;

-- Insert profile
INSERT INTO user_profiles (user_id, height, weight, age, gender)
VALUES ('user-uuid', 175.0, 75.5, 30, 'male');
```

### Track Recipe Preferences

```sql
-- User likes a recipe (first time)
INSERT INTO recipe_ratings (user_id, recipe_id, liked, automatic, count)
VALUES ('user-uuid', 'r123456', true, false, 1);

-- User likes same recipe again (increment count)
UPDATE recipe_ratings 
SET count = count + 1, updated_at = NOW()
WHERE user_id = 'user-uuid' AND recipe_id = 'r123456';
```

### Create Week Plan with Meals

```sql
-- Create week plan
INSERT INTO week_plans (id, user_id, week_start_date, status)
VALUES (uuid_generate_v4(), 'user-uuid', '2026-05-12', 'active')
RETURNING id;

-- Add meal for Monday
INSERT INTO week_plan_meals (week_plan_id, day_of_week, recipe_id, recipe_title)
VALUES ('plan-uuid', 0, 'r123456', 'Spaghetti Carbonara');

-- Add alternative meal for Monday (position 1)
INSERT INTO week_plan_meals (week_plan_id, day_of_week, recipe_id, recipe_title, position, selected)
VALUES ('plan-uuid', 0, 'r123457', 'Caesar Salad', 1, false);
```

---

## Migrations

### Running Migrations

```typescript
import { db } from 'cookidoo-assistant-shared/db';
import { migrationManager } from 'cookidoo-assistant-shared/db';

// Connect to database
await db.connect({
  host: 'localhost',
  port: 5432,
  database: 'cookidoo',
  username: 'postgres',
  password: 'password'
});

// Run migrations
await migrationManager.runMigrations('./migrations');
```

### Migration Files

Migrations are stored in `migrations/` directory:
- `001_initial_schema.sql` - Creates all tables, indexes, triggers
- `002_seed_data.sql` - Test data for development

Migration files must follow naming pattern: `NNN_description.sql`

---

## Environment Setup

### PostgreSQL Configuration

```bash
# Required PostgreSQL version: 12+
# Required extensions: uuid-ossp

# Create database
createdb cookidoo

# Enable extensions (run as superuser)
psql -d cookidoo -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

### Environment Variables

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cookidoo
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Testing

Run migration tests:

```bash
cd cookidoo-assistant-shared
npm test tests/migrations.test.ts
```

Tests verify:
- All tables created
- Foreign keys enforced
- Indexes exist
- Triggers work
- Data integrity constraints
- Cascade deletes
- Seed data loaded

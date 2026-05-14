-- Migration 001: Initial Database Schema
-- Description: Create all core tables for user data, preferences, health tracking, and meal planning

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. User Profile table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    height DECIMAL(5,2), -- in cm (e.g., 175.50)
    weight DECIMAL(5,2), -- in kg (e.g., 70.50)
    age INTEGER CHECK (age > 0 AND age < 150),
    gender VARCHAR(20) CHECK (gender IN ('male', 'female', 'other')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 3. Dietary Preferences table
CREATE TABLE dietary_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    diet_type VARCHAR(50) NOT NULL CHECK (diet_type IN ('omnivor', 'vegetarian', 'vegan', 'pescetarian')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 4. Allergies table
CREATE TABLE allergies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    allergen VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('mild', 'moderate', 'severe')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Health Data table
CREATE TABLE health_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_level VARCHAR(50) NOT NULL CHECK (activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active')),
    health_goal VARCHAR(50) NOT NULL CHECK (health_goal IN ('lose_weight', 'maintain_weight', 'gain_weight')),
    calorie_target INTEGER CHECK (calorie_target > 0),
    protein_target DECIMAL(6,2) CHECK (protein_target >= 0), -- in grams
    fat_target DECIMAL(6,2) CHECK (fat_target >= 0), -- in grams
    carbs_target DECIMAL(6,2) CHECK (carbs_target >= 0), -- in grams
    auto_calculated BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 6. Recipe Ratings table
CREATE TABLE recipe_ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id VARCHAR(100) NOT NULL, -- Cookidoo recipe ID
    liked BOOLEAN NOT NULL, -- true=liked, false=disliked
    automatic BOOLEAN DEFAULT FALSE, -- auto-tracked vs manual feedback
    count INTEGER DEFAULT 1 CHECK (count > 0), -- how many times this rating occurred
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, recipe_id)
);

-- 7. Week Plans table
CREATE TABLE week_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    week_start_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('draft', 'active', 'completed', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8. Week Plan Meals table
CREATE TABLE week_plan_meals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    week_plan_id UUID NOT NULL REFERENCES week_plans(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6), -- 0=Monday, 6=Sunday
    recipe_id VARCHAR(100) NOT NULL, -- Cookidoo recipe ID
    recipe_title VARCHAR(255) NOT NULL, -- cached for convenience
    position INTEGER DEFAULT 0 CHECK (position >= 0), -- for future: 0=option1, 1=option2
    selected BOOLEAN DEFAULT TRUE, -- is this option selected?
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance

-- User profile lookup
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);

-- Dietary preferences lookup
CREATE INDEX idx_dietary_preferences_user_id ON dietary_preferences(user_id);

-- Allergies lookup
CREATE INDEX idx_allergies_user_id ON allergies(user_id);
CREATE INDEX idx_allergies_allergen ON allergies(allergen);

-- Health data lookup
CREATE INDEX idx_health_data_user_id ON health_data(user_id);

-- Recipe ratings lookup and filtering
CREATE INDEX idx_recipe_ratings_user_id ON recipe_ratings(user_id);
CREATE INDEX idx_recipe_ratings_recipe_id ON recipe_ratings(recipe_id);
CREATE INDEX idx_recipe_ratings_liked ON recipe_ratings(liked);
CREATE INDEX idx_recipe_ratings_user_recipe ON recipe_ratings(user_id, recipe_id);

-- Week plans lookup and filtering
CREATE INDEX idx_week_plans_user_id ON week_plans(user_id);
CREATE INDEX idx_week_plans_status ON week_plans(status);
CREATE INDEX idx_week_plans_week_start ON week_plans(week_start_date);
CREATE INDEX idx_week_plans_user_week ON week_plans(user_id, week_start_date);

-- Week plan meals lookup
CREATE INDEX idx_week_plan_meals_week_plan_id ON week_plan_meals(week_plan_id);
CREATE INDEX idx_week_plan_meals_recipe_id ON week_plan_meals(recipe_id);
CREATE INDEX idx_week_plan_meals_day ON week_plan_meals(day_of_week);

-- Create function for automatic updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dietary_preferences_updated_at BEFORE UPDATE ON dietary_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_allergies_updated_at BEFORE UPDATE ON allergies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_health_data_updated_at BEFORE UPDATE ON health_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recipe_ratings_updated_at BEFORE UPDATE ON recipe_ratings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_week_plans_updated_at BEFORE UPDATE ON week_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_week_plan_meals_updated_at BEFORE UPDATE ON week_plan_meals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE users IS 'Core users table';
COMMENT ON TABLE user_profiles IS 'User profile information including physical attributes';
COMMENT ON TABLE dietary_preferences IS 'User dietary preferences (vegetarian, vegan, etc.)';
COMMENT ON TABLE allergies IS 'User allergies and intolerances';
COMMENT ON TABLE health_data IS 'User health goals and nutrition targets';
COMMENT ON TABLE recipe_ratings IS 'User recipe ratings and preferences (liked/disliked)';
COMMENT ON TABLE week_plans IS 'User weekly meal plans';
COMMENT ON TABLE week_plan_meals IS 'Individual meals within a week plan';

COMMENT ON COLUMN recipe_ratings.automatic IS 'Whether rating was automatically tracked (vs manual feedback)';
COMMENT ON COLUMN recipe_ratings.count IS 'Number of times this rating occurred';
COMMENT ON COLUMN week_plan_meals.position IS 'Position for multiple recipe options (0=first option)';
COMMENT ON COLUMN week_plan_meals.selected IS 'Whether this recipe option is currently selected';

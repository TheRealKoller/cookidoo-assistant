import { BaseRepository } from './base.repository.js';
import {
  UserProfile,
  DietaryPreference,
  Allergy,
  HealthData,
  RecipeRating,
  WeekPlan,
  WeekPlanMeal,
} from '../models/entities.js';

/**
 * User Profile Repository
 */
export class UserProfileRepository extends BaseRepository<UserProfile> {
  constructor() {
    super('user_profiles');
  }

  async findByUserId(userId: string): Promise<UserProfile | null> {
    const rows = await this.sql<UserProfile[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId}
    `;
    return rows[0] || null;
  }

  async findByEmail(email: string): Promise<UserProfile | null> {
    const rows = await this.sql<UserProfile[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE email = ${email}
    `;
    return rows[0] || null;
  }
}

/**
 * Dietary Preference Repository
 */
export class DietaryPreferenceRepository extends BaseRepository<DietaryPreference> {
  constructor() {
    super('dietary_preferences');
  }

  async findByUserId(userId: string): Promise<DietaryPreference[]> {
    return await this.sql<DietaryPreference[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId}
      ORDER BY created_at DESC
    `;
  }

  async findActiveByUserId(userId: string): Promise<DietaryPreference[]> {
    return await this.sql<DietaryPreference[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId} AND is_active = true
      ORDER BY created_at DESC
    `;
  }
}

/**
 * Allergy Repository
 */
export class AllergyRepository extends BaseRepository<Allergy> {
  constructor() {
    super('allergies');
  }

  async findByUserId(userId: string): Promise<Allergy[]> {
    return await this.sql<Allergy[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId}
      ORDER BY severity DESC, name ASC
    `;
  }

  async findBySeverity(userId: string, severity: Allergy['severity']): Promise<Allergy[]> {
    return await this.sql<Allergy[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId} AND severity = ${severity}
      ORDER BY name ASC
    `;
  }
}

/**
 * Health Data Repository
 */
export class HealthDataRepository extends BaseRepository<HealthData> {
  constructor() {
    super('health_data');
  }

  async findByUserId(userId: string, limit?: number): Promise<HealthData[]> {
    if (limit) {
      return await this.sql<HealthData[]>`
        SELECT * FROM ${this.sql(this.tableName)}
        WHERE user_id = ${userId}
        ORDER BY recorded_at DESC
        LIMIT ${limit}
      `;
    }
    return await this.sql<HealthData[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId}
      ORDER BY recorded_at DESC
    `;
  }

  async findByType(
    userId: string,
    dataType: HealthData['dataType'],
    limit?: number
  ): Promise<HealthData[]> {
    if (limit) {
      return await this.sql<HealthData[]>`
        SELECT * FROM ${this.sql(this.tableName)}
        WHERE user_id = ${userId} AND data_type = ${dataType}
        ORDER BY recorded_at DESC
        LIMIT ${limit}
      `;
    }
    return await this.sql<HealthData[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId} AND data_type = ${dataType}
      ORDER BY recorded_at DESC
    `;
  }
}

/**
 * Recipe Rating Repository
 */
export class RecipeRatingRepository extends BaseRepository<RecipeRating> {
  constructor() {
    super('recipe_ratings');
  }

  async findByUserId(userId: string): Promise<RecipeRating[]> {
    return await this.sql<RecipeRating[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId}
      ORDER BY created_at DESC
    `;
  }

  async findByRecipeId(recipeId: string): Promise<RecipeRating[]> {
    return await this.sql<RecipeRating[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE recipe_id = ${recipeId}
      ORDER BY created_at DESC
    `;
  }

  async findByUserAndRecipe(userId: string, recipeId: string): Promise<RecipeRating | null> {
    const rows = await this.sql<RecipeRating[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId} AND recipe_id = ${recipeId}
    `;
    return rows[0] || null;
  }
}

/**
 * Week Plan Repository
 */
export class WeekPlanRepository extends BaseRepository<WeekPlan> {
  constructor() {
    super('week_plans');
  }

  async findByUserId(userId: string): Promise<WeekPlan[]> {
    return await this.sql<WeekPlan[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId}
      ORDER BY week_start_date DESC
    `;
  }

  async findActiveByUserId(userId: string): Promise<WeekPlan | null> {
    const rows = await this.sql<WeekPlan[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId} AND is_active = true
      ORDER BY week_start_date DESC
      LIMIT 1
    `;
    return rows[0] || null;
  }

  async findByWeekStartDate(userId: string, weekStartDate: Date): Promise<WeekPlan | null> {
    const rows = await this.sql<WeekPlan[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE user_id = ${userId} AND week_start_date = ${weekStartDate}
    `;
    return rows[0] || null;
  }
}

/**
 * Week Plan Meal Repository
 */
export class WeekPlanMealRepository extends BaseRepository<WeekPlanMeal> {
  constructor() {
    super('week_plan_meals');
  }

  async findByWeekPlanId(weekPlanId: number): Promise<WeekPlanMeal[]> {
    return await this.sql<WeekPlanMeal[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE week_plan_id = ${weekPlanId}
      ORDER BY day_of_week ASC, meal_type ASC
    `;
  }

  async findByDay(
    weekPlanId: number,
    dayOfWeek: WeekPlanMeal['dayOfWeek']
  ): Promise<WeekPlanMeal[]> {
    return await this.sql<WeekPlanMeal[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE week_plan_id = ${weekPlanId} AND day_of_week = ${dayOfWeek}
      ORDER BY meal_type ASC
    `;
  }

  async findByMealType(
    weekPlanId: number,
    mealType: WeekPlanMeal['mealType']
  ): Promise<WeekPlanMeal[]> {
    return await this.sql<WeekPlanMeal[]>`
      SELECT * FROM ${this.sql(this.tableName)}
      WHERE week_plan_id = ${weekPlanId} AND meal_type = ${mealType}
      ORDER BY day_of_week ASC
    `;
  }
}

// Export singleton instances
export const userProfileRepository = new UserProfileRepository();
export const dietaryPreferenceRepository = new DietaryPreferenceRepository();
export const allergyRepository = new AllergyRepository();
export const healthDataRepository = new HealthDataRepository();
export const recipeRatingRepository = new RecipeRatingRepository();
export const weekPlanRepository = new WeekPlanRepository();
export const weekPlanMealRepository = new WeekPlanMealRepository();

import { BaseEntity } from './base.js';

/**
 * User profile entity
 */
export interface UserProfile extends BaseEntity {
  userId: string;
  name: string;
  email: string;
  avatarUrl?: string;
  preferences?: Record<string, unknown>;
}

/**
 * Dietary preference entity
 */
export interface DietaryPreference extends BaseEntity {
  userId: string;
  type:
    | 'vegetarian'
    | 'vegan'
    | 'pescatarian'
    | 'keto'
    | 'paleo'
    | 'low-carb'
    | 'gluten-free'
    | 'dairy-free'
    | 'other';
  description?: string;
  isActive: boolean;
}

/**
 * Allergy entity
 */
export interface Allergy extends BaseEntity {
  userId: string;
  name: string;
  severity: 'mild' | 'moderate' | 'severe';
  notes?: string;
}

/**
 * Health data entity
 */
export interface HealthData extends BaseEntity {
  userId: string;
  dataType: 'weight' | 'height' | 'blood-pressure' | 'blood-sugar' | 'cholesterol' | 'other';
  value: number;
  unit: string;
  notes?: string;
  recordedAt: Date;
}

/**
 * Recipe rating entity
 */
export interface RecipeRating extends BaseEntity {
  userId: string;
  recipeId: string;
  rating: number;
  comment?: string;
  wouldMakeAgain: boolean;
}

/**
 * Week plan entity
 */
export interface WeekPlan extends BaseEntity {
  userId: string;
  weekStartDate: Date;
  name?: string;
  isActive: boolean;
}

/**
 * Week plan meal entity
 */
export interface WeekPlanMeal extends BaseEntity {
  weekPlanId: number;
  recipeId: string;
  dayOfWeek: 0 | 1 | 2 | 3 | 4 | 5 | 6; // 0 = Sunday, 6 = Saturday
  mealType: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  servings?: number;
  notes?: string;
}

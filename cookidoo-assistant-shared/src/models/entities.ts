import { BaseEntity } from './base.js';

/**
 * User entity - core user table
 */
export interface User extends BaseEntity {
  // Only contains id, createdAt, updatedAt from BaseEntity
}

/**
 * User profile entity - physical attributes and basic info
 */
export interface UserProfile extends BaseEntity {
  userId: string;
  height?: number; // in cm
  weight?: number; // in kg
  age?: number;
  gender?: 'male' | 'female' | 'other';
}

/**
 * Dietary preference entity - user's diet type
 */
export interface DietaryPreference extends BaseEntity {
  userId: string;
  dietType: 'omnivor' | 'vegetarian' | 'vegan' | 'pescetarian';
}

/**
 * Allergy entity - user allergies and intolerances
 */
export interface Allergy extends BaseEntity {
  userId: string;
  allergen: string;
  severity: 'mild' | 'moderate' | 'severe';
}

/**
 * Health data entity - health goals and nutrition targets
 */
export interface HealthData extends BaseEntity {
  userId: string;
  activityLevel: 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
  healthGoal: 'lose_weight' | 'maintain_weight' | 'gain_weight';
  calorieTarget?: number; // daily target
  proteinTarget?: number; // in grams
  fatTarget?: number; // in grams
  carbsTarget?: number; // in grams
  autoCalculated: boolean; // was target auto-calculated?
}

/**
 * Recipe rating entity - user recipe preferences
 */
export interface RecipeRating extends BaseEntity {
  userId: string;
  recipeId: string; // Cookidoo recipe ID
  liked: boolean; // true=liked, false=disliked
  automatic: boolean; // auto-tracked vs manual feedback
  count: number; // how many times this rating occurred
}

/**
 * Week plan entity - weekly meal plans
 */
export interface WeekPlan extends BaseEntity {
  userId: string;
  weekStartDate: Date;
  status: 'draft' | 'active' | 'completed' | 'archived';
}

/**
 * Week plan meal entity - individual meals in a week plan
 */
export interface WeekPlanMeal extends BaseEntity {
  weekPlanId: string;
  dayOfWeek: number; // 0=Monday, 6=Sunday
  recipeId: string; // Cookidoo recipe ID
  recipeTitle: string; // cached for convenience
  position: number; // for multiple options: 0=option1, 1=option2
  selected: boolean; // is this option selected?
}

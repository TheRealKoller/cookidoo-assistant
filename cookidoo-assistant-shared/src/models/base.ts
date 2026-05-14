/**
 * Base entity interface for all database models
 */
export interface BaseEntity {
  id: string; // UUID
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Omit base entity fields for create operations
 */
export type CreateEntity<T extends BaseEntity> = Omit<T, 'id' | 'createdAt' | 'updatedAt'>;

/**
 * Partial entity for update operations
 */
export type UpdateEntity<T extends BaseEntity> = Partial<Omit<T, 'id' | 'createdAt' | 'updatedAt'>>;

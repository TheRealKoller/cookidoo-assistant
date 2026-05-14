import { Sql } from 'postgres';
import { db } from '../db/connection.js';
import { BaseEntity, CreateEntity, UpdateEntity } from '../models/base.js';
import { NotFoundError, DatabaseError } from '../utils/errors.js';
import { logger } from '../utils/logger.js';

/**
 * Base repository with common CRUD operations
 */
export abstract class BaseRepository<T extends BaseEntity> {
  protected sql: Sql;

  constructor(protected tableName: string) {
    this.sql = db.getClient();
  }

  /**
   * Find entity by ID
   */
  async findById(id: string): Promise<T | null> {
    try {
      const rows = await this.sql<T[]>`
        SELECT * FROM ${this.sql(this.tableName)}
        WHERE id = ${id}
      `;
      return rows[0] || null;
    } catch (error) {
      const err = error as Error;
      logger.error(`Error finding ${this.tableName} by id ${id}`, err);
      throw new DatabaseError(`Failed to find ${this.tableName}`, err);
    }
  }

  /**
   * Find entity by ID or throw
   */
  async findByIdOrFail(id: string): Promise<T> {
    const entity = await this.findById(id);
    if (!entity) {
      throw new NotFoundError(this.tableName, id);
    }
    return entity;
  }

  /**
   * Find all entities
   */
  async findAll(limit?: number, offset?: number): Promise<T[]> {
    try {
      let query = this.sql<T[]>`SELECT * FROM ${this.sql(this.tableName)} ORDER BY id DESC`;

      if (limit !== undefined) {
        query = this.sql<T[]>`
          SELECT * FROM ${this.sql(this.tableName)}
          ORDER BY id DESC
          LIMIT ${limit}
          ${offset !== undefined ? this.sql`OFFSET ${offset}` : this.sql``}
        `;
      }

      return await query;
    } catch (error) {
      const err = error as Error;
      logger.error(`Error finding all ${this.tableName}`, err);
      throw new DatabaseError(`Failed to find ${this.tableName}`, err);
    }
  }

  /**
   * Create new entity
   */
  async create(data: CreateEntity<T>): Promise<T> {
    try {
      const rows = await this.sql<T[]>`
        INSERT INTO ${this.sql(this.tableName)}
        ${this.sql(data as Record<string, unknown>)}
        RETURNING *
      `;
      logger.info(`Created ${this.tableName}`, { id: rows[0].id });
      return rows[0];
    } catch (error) {
      const err = error as Error;
      logger.error(`Error creating ${this.tableName}`, err);
      throw new DatabaseError(`Failed to create ${this.tableName}`, err);
    }
  }

  /**
   * Update entity
   */
  async update(id: string, data: UpdateEntity<T>): Promise<T> {
    try {
      const rows = await this.sql<T[]>`
        UPDATE ${this.sql(this.tableName)}
        SET ${this.sql(data as Record<string, unknown>)},
            updated_at = NOW()
        WHERE id = ${id}
        RETURNING *
      `;

      if (rows.length === 0) {
        throw new NotFoundError(this.tableName, id);
      }

      logger.info(`Updated ${this.tableName}`, { id });
      return rows[0];
    } catch (error) {
      if (error instanceof NotFoundError) {
        throw error;
      }
      const err = error as Error;
      logger.error(`Error updating ${this.tableName} ${id}`, err);
      throw new DatabaseError(`Failed to update ${this.tableName}`, err);
    }
  }

  /**
   * Delete entity
   */
  async delete(id: string): Promise<void> {
    try {
      const rows = await this.sql`
        DELETE FROM ${this.sql(this.tableName)}
        WHERE id = ${id}
        RETURNING id
      `;

      if (rows.length === 0) {
        throw new NotFoundError(this.tableName, id);
      }

      logger.info(`Deleted ${this.tableName}`, { id });
    } catch (error) {
      if (error instanceof NotFoundError) {
        throw error;
      }
      const err = error as Error;
      logger.error(`Error deleting ${this.tableName} ${id}`, err);
      throw new DatabaseError(`Failed to delete ${this.tableName}`, err);
    }
  }

  /**
   * Count total entities
   */
  async count(): Promise<number> {
    try {
      const result = await this.sql<[{ count: string }]>`
        SELECT COUNT(*) as count FROM ${this.sql(this.tableName)}
      `;
      return parseInt(result[0].count, 10);
    } catch (error) {
      const err = error as Error;
      logger.error(`Error counting ${this.tableName}`, err);
      throw new DatabaseError(`Failed to count ${this.tableName}`, err);
    }
  }

  /**
   * Check if entity exists
   */
  async exists(id: number): Promise<boolean> {
    try {
      const result = await this.sql<[{ exists: boolean }]>`
        SELECT EXISTS(
          SELECT 1 FROM ${this.sql(this.tableName)} WHERE id = ${id}
        ) as exists
      `;
      return result[0].exists;
    } catch (error) {
      const err = error as Error;
      logger.error(`Error checking existence of ${this.tableName} ${id}`, err);
      throw new DatabaseError(`Failed to check ${this.tableName} existence`, err);
    }
  }
}

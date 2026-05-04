import { db } from './connection.js';
import { logger } from '../utils/logger.js';
import { DatabaseError } from '../utils/errors.js';
import fs from 'fs/promises';
import path from 'path';

export interface Migration {
  id: number;
  name: string;
  executedAt: Date;
}

/**
 * Migration manager for database schema changes
 */
export class MigrationManager {
  private migrationsTable = 'schema_migrations';

  /**
   * Create migrations table if it doesn't exist
   */
  async init(): Promise<void> {
    const sql = db.getClient();
    try {
      await sql`
        CREATE TABLE IF NOT EXISTS ${sql(this.migrationsTable)} (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
      `;
      logger.info('Migrations table initialized');
    } catch (error) {
      const err = error as Error;
      logger.error('Failed to initialize migrations table', err);
      throw new DatabaseError('Migration initialization failed', err);
    }
  }

  /**
   * Get list of executed migrations
   */
  async getExecutedMigrations(): Promise<Migration[]> {
    const sql = db.getClient();
    try {
      const rows = await sql<Migration[]>`
        SELECT id, name, executed_at as "executedAt"
        FROM ${sql(this.migrationsTable)}
        ORDER BY id ASC
      `;
      return rows;
    } catch (error) {
      const err = error as Error;
      throw new DatabaseError('Failed to fetch executed migrations', err);
    }
  }

  /**
   * Record a migration as executed
   */
  async recordMigration(id: number, name: string): Promise<void> {
    const sql = db.getClient();
    try {
      await sql`
        INSERT INTO ${sql(this.migrationsTable)} (id, name)
        VALUES (${id}, ${name})
      `;
      logger.info(`Migration recorded: ${id} - ${name}`);
    } catch (error) {
      const err = error as Error;
      throw new DatabaseError(`Failed to record migration ${id}`, err);
    }
  }

  /**
   * Run pending migrations from a directory
   */
  async runMigrations(migrationsDir: string): Promise<void> {
    await this.init();

    try {
      // Read migration files
      const files = await fs.readdir(migrationsDir);
      const migrationFiles = files.filter((f) => f.endsWith('.sql')).sort();

      if (migrationFiles.length === 0) {
        logger.info('No migration files found');
        return;
      }

      // Get executed migrations
      const executed = await this.getExecutedMigrations();
      const executedIds = new Set(executed.map((m) => m.id));

      // Run pending migrations
      for (const file of migrationFiles) {
        const match = file.match(/^(\d+)_(.+)\.sql$/);
        if (!match) {
          logger.warn(`Skipping invalid migration filename: ${file}`);
          continue;
        }

        const id = parseInt(match[1], 10);
        const name = match[2];

        if (executedIds.has(id)) {
          logger.debug(`Migration ${id} already executed, skipping`);
          continue;
        }

        // Read and execute migration
        const filePath = path.join(migrationsDir, file);
        const sql = await fs.readFile(filePath, 'utf-8');

        logger.info(`Running migration ${id} - ${name}`);
        await db.transaction(async (trx) => {
          await trx.unsafe(sql);
        });

        await this.recordMigration(id, name);
        logger.info(`Migration ${id} completed successfully`);
      }

      logger.info('All migrations completed');
    } catch (error) {
      const err = error as Error;
      logger.error('Migration failed', err);
      throw new DatabaseError('Migration execution failed', err);
    }
  }
}

// Export singleton instance
export const migrationManager = new MigrationManager();

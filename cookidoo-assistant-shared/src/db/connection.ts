import postgres, { Sql, TransactionSql } from 'postgres';
import { logger } from '../utils/logger.js';
import { DatabaseError } from '../utils/errors.js';

export interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
  max?: number;
  idleTimeout?: number;
  connectionTimeout?: number;
  ssl?: boolean;
}

class DatabaseConnection {
  private sql: Sql | null = null;

  /**
   * Initialize database connection
   */
  async connect(config: DatabaseConfig): Promise<void> {
    if (this.sql) {
      logger.warn('Database connection already exists');
      return;
    }

    try {
      this.sql = postgres({
        host: config.host,
        port: config.port,
        database: config.database,
        username: config.username,
        password: config.password,
        max: config.max || 10,
        idle_timeout: config.idleTimeout || 30,
        connect_timeout: config.connectionTimeout || 10,
        ssl: config.ssl ? 'require' : undefined,
      });

      // Test connection
      await this.sql`SELECT 1`;
      logger.info('Database connected successfully', {
        host: config.host,
        database: config.database,
      });
    } catch (error) {
      const err = error as Error;
      logger.error('Failed to connect to database', err);
      throw new DatabaseError('Database connection failed', err);
    }
  }

  /**
   * Get database client
   */
  getClient(): Sql {
    if (!this.sql) {
      throw new DatabaseError('Database not connected. Call connect() first.');
    }
    return this.sql;
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.sql !== null;
  }

  /**
   * Close database connection
   */
  async disconnect(): Promise<void> {
    if (!this.sql) {
      logger.warn('No active database connection to close');
      return;
    }

    try {
      await this.sql.end();
      this.sql = null;
      logger.info('Database disconnected successfully');
    } catch (error) {
      const err = error as Error;
      logger.error('Error closing database connection', err);
      throw new DatabaseError('Failed to close database connection', err);
    }
  }

  /**
   * Execute a transaction
   */
  async transaction<T>(callback: (sql: TransactionSql) => Promise<T>): Promise<T> {
    const client = this.getClient();
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return
    return client.begin(callback) as Promise<T>;
  }
}

// Export singleton instance
export const db = new DatabaseConnection();

// Export types
export type { Sql, TransactionSql };

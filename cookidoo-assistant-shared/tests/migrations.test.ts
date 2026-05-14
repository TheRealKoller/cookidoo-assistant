import { db, DatabaseConfig } from '../src/db/connection.js';
import { migrationManager } from '../src/db/migrations.js';
import path from 'path';

describe('Database Migrations', () => {
  const testConfig: DatabaseConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    database: process.env.DB_NAME || 'cookidoo_test',
    username: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    ssl: false,
  };

  beforeAll(async () => {
    await db.connect(testConfig);
  });

  afterAll(async () => {
    await db.disconnect();
  });

  describe('Migration System', () => {
    it('should initialize migrations table', async () => {
      await migrationManager.init();

      const sql = db.getClient();
      const result = await sql`
        SELECT EXISTS (
          SELECT FROM information_schema.tables 
          WHERE table_name = 'schema_migrations'
        ) as exists
      `;

      expect(result[0].exists).toBe(true);
    });

    it('should run migrations successfully', async () => {
      const migrationsDir = path.resolve(__dirname, '../migrations');
      await migrationManager.runMigrations(migrationsDir);

      const executed = await migrationManager.getExecutedMigrations();
      expect(executed.length).toBeGreaterThan(0);
    });

    it('should not re-run already executed migrations', async () => {
      const migrationsDir = path.resolve(__dirname, '../migrations');
      const executedBefore = await migrationManager.getExecutedMigrations();

      await migrationManager.runMigrations(migrationsDir);

      const executedAfter = await migrationManager.getExecutedMigrations();
      expect(executedAfter.length).toBe(executedBefore.length);
    });
  });

  describe('Schema Validation', () => {
    it('should have created all 8 tables', async () => {
      const sql = db.getClient();
      const tables = await sql`
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
      `;

      const tableNames = tables.map((t) => t.table_name);

      expect(tableNames).toContain('users');
      expect(tableNames).toContain('user_profiles');
      expect(tableNames).toContain('dietary_preferences');
      expect(tableNames).toContain('allergies');
      expect(tableNames).toContain('health_data');
      expect(tableNames).toContain('recipe_ratings');
      expect(tableNames).toContain('week_plans');
      expect(tableNames).toContain('week_plan_meals');
    });

    it('should have UUID extension enabled', async () => {
      const sql = db.getClient();
      const result = await sql`
        SELECT EXISTS (
          SELECT FROM pg_extension WHERE extname = 'uuid-ossp'
        ) as exists
      `;

      expect(result[0].exists).toBe(true);
    });

    it('should have foreign key constraints', async () => {
      const sql = db.getClient();
      const constraints = await sql`
        SELECT
          tc.table_name,
          tc.constraint_name,
          kcu.column_name,
          ccu.table_name AS foreign_table_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
      `;

      expect(constraints.length).toBeGreaterThan(0);

      // Check specific foreign keys exist
      const fkNames = constraints.map(
        (c) => `${c.table_name}.${c.column_name}->${c.foreign_table_name}`
      );
      expect(fkNames).toContain('user_profiles.user_id->users');
      expect(fkNames).toContain('dietary_preferences.user_id->users');
      expect(fkNames).toContain('allergies.user_id->users');
      expect(fkNames).toContain('health_data.user_id->users');
      expect(fkNames).toContain('recipe_ratings.user_id->users');
      expect(fkNames).toContain('week_plans.user_id->users');
      expect(fkNames).toContain('week_plan_meals.week_plan_id->week_plans');
    });

    it('should have indexes for performance', async () => {
      const sql = db.getClient();
      const indexes = await sql`
        SELECT
          tablename,
          indexname
        FROM pg_indexes
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname
      `;

      const indexNames = indexes.map((i) => i.indexname);

      // Check critical indexes exist
      expect(indexNames).toContain('idx_user_profiles_user_id');
      expect(indexNames).toContain('idx_recipe_ratings_user_recipe');
      expect(indexNames).toContain('idx_week_plans_user_week');
      expect(indexNames).toContain('idx_week_plan_meals_week_plan_id');
    });

    it('should have updated_at triggers', async () => {
      const sql = db.getClient();
      const triggers = await sql`
        SELECT
          trigger_name,
          event_object_table
        FROM information_schema.triggers
        WHERE trigger_schema = 'public'
        AND trigger_name LIKE '%updated_at%'
      `;

      expect(triggers.length).toBe(8); // One for each table

      const tableNames = triggers.map((t) => t.event_object_table);
      expect(tableNames).toContain('users');
      expect(tableNames).toContain('user_profiles');
      expect(tableNames).toContain('dietary_preferences');
      expect(tableNames).toContain('allergies');
      expect(tableNames).toContain('health_data');
      expect(tableNames).toContain('recipe_ratings');
      expect(tableNames).toContain('week_plans');
      expect(tableNames).toContain('week_plan_meals');
    });
  });

  describe('Data Integrity', () => {
    it('should enforce unique constraints', async () => {
      const sql = db.getClient();

      // Try to insert duplicate user_profile for same user
      const userId = 'test-unique-' + Date.now();
      await sql`INSERT INTO users (id) VALUES (${userId})`;
      await sql`INSERT INTO user_profiles (user_id, height) VALUES (${userId}, 175)`;

      await expect(
        sql`INSERT INTO user_profiles (user_id, height) VALUES (${userId}, 180)`
      ).rejects.toThrow();
    });

    it('should enforce check constraints', async () => {
      const sql = db.getClient();
      const userId = 'test-check-' + Date.now();
      await sql`INSERT INTO users (id) VALUES (${userId})`;

      // Try to insert invalid age
      await expect(
        sql`INSERT INTO user_profiles (user_id, age) VALUES (${userId}, 200)`
      ).rejects.toThrow();

      // Try to insert invalid gender
      await expect(
        sql`INSERT INTO user_profiles (user_id, gender) VALUES (${userId}, 'invalid')`
      ).rejects.toThrow();
    });

    it('should cascade deletes', async () => {
      const sql = db.getClient();
      const userId = 'test-cascade-' + Date.now();

      // Insert user and related data
      await sql`INSERT INTO users (id) VALUES (${userId})`;
      await sql`INSERT INTO user_profiles (user_id, height) VALUES (${userId}, 175)`;
      await sql`INSERT INTO allergies (user_id, allergen, severity) VALUES (${userId}, 'test', 'mild')`;

      // Delete user
      await sql`DELETE FROM users WHERE id = ${userId}`;

      // Verify related data was deleted
      const profiles = await sql`SELECT * FROM user_profiles WHERE user_id = ${userId}`;
      const allergies = await sql`SELECT * FROM allergies WHERE user_id = ${userId}`;

      expect(profiles.length).toBe(0);
      expect(allergies.length).toBe(0);
    });

    it('should auto-update updated_at on changes', async () => {
      const sql = db.getClient();
      const userId = 'test-timestamp-' + Date.now();

      await sql`INSERT INTO users (id) VALUES (${userId})`;
      const before = await sql`SELECT updated_at FROM users WHERE id = ${userId}`;

      // Wait a bit to ensure timestamp difference
      await new Promise((resolve) => setTimeout(resolve, 100));

      await sql`UPDATE users SET created_at = created_at WHERE id = ${userId}`;
      const after = await sql`SELECT updated_at FROM users WHERE id = ${userId}`;

      expect(new Date(after[0].updated_at).getTime()).toBeGreaterThan(
        new Date(before[0].updated_at).getTime()
      );
    });
  });

  describe('Seed Data', () => {
    it('should have inserted seed users', async () => {
      const sql = db.getClient();
      const users = await sql`
        SELECT * FROM users 
        WHERE id LIKE 'a0000000-0000-0000-0000-%'
      `;

      expect(users.length).toBeGreaterThanOrEqual(3);
    });

    it('should have inserted seed profiles', async () => {
      const sql = db.getClient();
      const profiles = await sql`
        SELECT * FROM user_profiles 
        WHERE id LIKE 'b0000000-0000-0000-0000-%'
      `;

      expect(profiles.length).toBeGreaterThanOrEqual(3);
    });

    it('should have inserted seed week plans with meals', async () => {
      const sql = db.getClient();
      const weekPlans = await sql`
        SELECT * FROM week_plans 
        WHERE id LIKE 'g0000000-0000-0000-0000-%'
      `;

      const meals = await sql`
        SELECT * FROM week_plan_meals 
        WHERE id LIKE 'h0000000-0000-0000-0000-%'
      `;

      expect(weekPlans.length).toBeGreaterThanOrEqual(3);
      expect(meals.length).toBeGreaterThanOrEqual(9);
    });
  });
});

import { z } from 'zod';
import { validate, validateSafe, commonSchemas } from '../../src/utils/validation';
import { ValidationError } from '../../src/utils/errors';

describe('Validation Utils', () => {
  describe('validate', () => {
    const schema = z.object({
      name: z.string().min(1),
      age: z.number().positive(),
      email: z.string().email(),
    });

    it('should validate correct data', () => {
      const data = {
        name: 'John',
        age: 30,
        email: 'john@example.com',
      };

      const result = validate(schema, data);
      expect(result).toEqual(data);
    });

    it('should throw ValidationError for invalid data', () => {
      const data = {
        name: '',
        age: -5,
        email: 'not-an-email',
      };

      expect(() => validate(schema, data)).toThrow(ValidationError);
    });

    it('should include field names in error message', () => {
      const data = {
        name: '',
        age: 30,
        email: 'john@example.com',
      };

      try {
        validate(schema, data);
        fail('Should have thrown ValidationError');
      } catch (error) {
        expect(error).toBeInstanceOf(ValidationError);
        expect((error as ValidationError).message).toContain('name');
      }
    });
  });

  describe('validateSafe', () => {
    const schema = z.object({
      name: z.string().min(1),
      age: z.number().positive(),
    });

    it('should return success for valid data', () => {
      const data = { name: 'John', age: 30 };
      const result = validateSafe(schema, data);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(data);
      }
    });

    it('should return errors for invalid data', () => {
      const data = { name: '', age: -5 };
      const result = validateSafe(schema, data);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.errors.length).toBeGreaterThan(0);
      }
    });
  });

  describe('commonSchemas', () => {
    it('should validate email', () => {
      expect(() => commonSchemas.email.parse('test@example.com')).not.toThrow();
      expect(() => commonSchemas.email.parse('not-an-email')).toThrow();
    });

    it('should validate url', () => {
      expect(() => commonSchemas.url.parse('https://example.com')).not.toThrow();
      expect(() => commonSchemas.url.parse('not-a-url')).toThrow();
    });

    it('should validate uuid', () => {
      expect(() => commonSchemas.uuid.parse('123e4567-e89b-12d3-a456-426614174000')).not.toThrow();
      expect(() => commonSchemas.uuid.parse('not-a-uuid')).toThrow();
    });

    it('should validate positive integer', () => {
      expect(() => commonSchemas.positiveInt.parse(5)).not.toThrow();
      expect(() => commonSchemas.positiveInt.parse(-5)).toThrow();
      expect(() => commonSchemas.positiveInt.parse(5.5)).toThrow();
    });

    it('should validate non-empty string', () => {
      expect(() => commonSchemas.nonEmptyString.parse('test')).not.toThrow();
      expect(() => commonSchemas.nonEmptyString.parse('')).toThrow();
    });

    it('should validate date', () => {
      expect(() => commonSchemas.date.parse('2024-01-01')).not.toThrow();
      expect(() => commonSchemas.date.parse(new Date())).not.toThrow();
    });
  });
});

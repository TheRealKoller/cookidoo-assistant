# TypeScript Development Skill

This skill provides workflows and best practices for developing the TypeScript services (shared, assistant-mcp, api).

## Quick Commands

### Setup
```bash
# Install all dependencies (from monorepo root)
npm install

# Install for specific service
npm install --workspace=cookidoo-assistant-shared
```

### Run Tests
```bash
# Run all tests (all services)
npm test

# Run tests for specific service
npm test --workspace=cookidoo-assistant-mcp

# Run with coverage
npm run test:coverage --workspace=cookidoo-assistant-mcp

# Run in watch mode
npm run test:watch --workspace=cookidoo-assistant-mcp

# Run specific test file
npm test --workspace=cookidoo-assistant-mcp -- src/services/UserService.test.ts
```

### Code Quality
```bash
# Lint all services
npm run lint

# Lint specific service
npm run lint --workspace=cookidoo-assistant-mcp

# Fix auto-fixable issues
npm run lint:fix --workspace=cookidoo-assistant-mcp

# Format code
npm run format --workspace=cookidoo-assistant-mcp

# Type checking
npm run type-check --workspace=cookidoo-assistant-mcp

# Run all quality checks
npm run lint && npm run type-check && npm test
```

### Development
```bash
# Run in dev mode with hot reload
npm run dev --workspace=cookidoo-assistant-mcp

# Build
npm run build --workspace=cookidoo-assistant-mcp

# Start production build
npm start --workspace=cookidoo-assistant-mcp
```

## Creating New Features

### Step 1: Create Types

Define types in `src/types/<feature>.types.ts`:

```typescript
// src/types/user-profile.types.ts

export interface UserProfile {
  id: string;
  userId: string;
  age?: number;
  gender?: 'male' | 'female' | 'other';
  activityLevel: ActivityLevel;
  goal: HealthGoal;
  createdAt: Date;
  updatedAt: Date;
}

export enum ActivityLevel {
  SEDENTARY = 'sedentary',
  LIGHT = 'light',
  MODERATE = 'moderate',
  ACTIVE = 'active',
  VERY_ACTIVE = 'very_active'
}

export enum HealthGoal {
  MAINTAIN = 'maintain',
  LOSE_WEIGHT = 'lose_weight',
  GAIN_WEIGHT = 'gain_weight',
  BUILD_MUSCLE = 'build_muscle'
}

export interface CreateUserProfileDTO {
  userId: string;
  age?: number;
  gender?: 'male' | 'female' | 'other';
  activityLevel: ActivityLevel;
  goal: HealthGoal;
}

export interface UpdateUserProfileDTO {
  age?: number;
  gender?: 'male' | 'female' | 'other';
  activityLevel?: ActivityLevel;
  goal?: HealthGoal;
}
```

### Step 2: Create Model (Database Entity)

For TypeORM:

```typescript
// src/models/UserProfile.entity.ts

import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn } from 'typeorm';
import { ActivityLevel, HealthGoal } from '../types/user-profile.types';

@Entity('user_profiles')
export class UserProfile {
  @PrimaryGeneratedColumn('uuid')
  id!: string;

  @Column({ unique: true })
  userId!: string;

  @Column({ nullable: true })
  age?: number;

  @Column({ nullable: true })
  gender?: string;

  @Column({
    type: 'enum',
    enum: ActivityLevel,
    default: ActivityLevel.MODERATE
  })
  activityLevel!: ActivityLevel;

  @Column({
    type: 'enum',
    enum: HealthGoal,
    default: HealthGoal.MAINTAIN
  })
  goal!: HealthGoal;

  @CreateDateColumn()
  createdAt!: Date;

  @UpdateDateColumn()
  updatedAt!: Date;
}
```

### Step 3: Create Repository

```typescript
// src/repositories/UserProfileRepository.ts

import { Repository, DataSource } from 'typeorm';
import { UserProfile } from '../models/UserProfile.entity';
import { CreateUserProfileDTO, UpdateUserProfileDTO } from '../types/user-profile.types';

export class UserProfileRepository {
  private repository: Repository<UserProfile>;

  constructor(dataSource: DataSource) {
    this.repository = dataSource.getRepository(UserProfile);
  }

  async findByUserId(userId: string): Promise<UserProfile | null> {
    return this.repository.findOne({ where: { userId } });
  }

  async create(data: CreateUserProfileDTO): Promise<UserProfile> {
    const profile = this.repository.create(data);
    return this.repository.save(profile);
  }

  async update(id: string, data: UpdateUserProfileDTO): Promise<UserProfile | null> {
    await this.repository.update(id, data);
    return this.repository.findOne({ where: { id } });
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.repository.delete(id);
    return (result.affected ?? 0) > 0;
  }

  async findAll(): Promise<UserProfile[]> {
    return this.repository.find();
  }
}
```

### Step 4: Create Service (Business Logic)

```typescript
// src/services/UserProfileService.ts

import { UserProfileRepository } from '../repositories/UserProfileRepository';
import { UserProfile, CreateUserProfileDTO, UpdateUserProfileDTO } from '../types/user-profile.types';
import { AppError } from '../utils/errors';

export class UserProfileService {
  constructor(private repository: UserProfileRepository) {}

  async getUserProfile(userId: string): Promise<UserProfile> {
    const profile = await this.repository.findByUserId(userId);
    
    if (!profile) {
      throw new AppError(`User profile not found for user ${userId}`, 404);
    }
    
    return profile;
  }

  async createUserProfile(data: CreateUserProfileDTO): Promise<UserProfile> {
    // Check if profile already exists
    const existing = await this.repository.findByUserId(data.userId);
    
    if (existing) {
      throw new AppError(`User profile already exists for user ${data.userId}`, 409);
    }
    
    return this.repository.create(data);
  }

  async updateUserProfile(userId: string, data: UpdateUserProfileDTO): Promise<UserProfile> {
    const profile = await this.repository.findByUserId(userId);
    
    if (!profile) {
      throw new AppError(`User profile not found for user ${userId}`, 404);
    }
    
    const updated = await this.repository.update(profile.id, data);
    
    if (!updated) {
      throw new AppError('Failed to update user profile', 500);
    }
    
    return updated;
  }

  async deleteUserProfile(userId: string): Promise<void> {
    const profile = await this.repository.findByUserId(userId);
    
    if (!profile) {
      throw new AppError(`User profile not found for user ${userId}`, 404);
    }
    
    const deleted = await this.repository.delete(profile.id);
    
    if (!deleted) {
      throw new AppError('Failed to delete user profile', 500);
    }
  }

  async listAllProfiles(): Promise<UserProfile[]> {
    return this.repository.findAll();
  }
}
```

### Step 5: Create MCP Tool (for assistant-mcp)

```typescript
// src/tools/user-profile.tools.ts

import { Tool } from '@modelcontextprotocol/sdk/types.js';
import { UserProfileService } from '../services/UserProfileService';
import { CreateUserProfileDTO, UpdateUserProfileDTO } from '../types/user-profile.types';

export function createUserProfileTools(service: UserProfileService) {
  return {
    tools: [
      {
        name: 'get_user_profile',
        description: 'Get user health profile including age, activity level, and health goals',
        inputSchema: {
          type: 'object',
          properties: {
            userId: {
              type: 'string',
              description: 'User ID'
            }
          },
          required: ['userId']
        }
      } as Tool,
      {
        name: 'create_user_profile',
        description: 'Create a new user health profile',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            age: { type: 'number', description: 'Age in years' },
            gender: { 
              type: 'string', 
              enum: ['male', 'female', 'other'],
              description: 'Gender'
            },
            activityLevel: {
              type: 'string',
              enum: ['sedentary', 'light', 'moderate', 'active', 'very_active'],
              description: 'Physical activity level'
            },
            goal: {
              type: 'string',
              enum: ['maintain', 'lose_weight', 'gain_weight', 'build_muscle'],
              description: 'Health goal'
            }
          },
          required: ['userId', 'activityLevel', 'goal']
        }
      } as Tool,
      {
        name: 'update_user_profile',
        description: 'Update an existing user health profile',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            age: { type: 'number', description: 'Age in years' },
            gender: { 
              type: 'string', 
              enum: ['male', 'female', 'other']
            },
            activityLevel: {
              type: 'string',
              enum: ['sedentary', 'light', 'moderate', 'active', 'very_active']
            },
            goal: {
              type: 'string',
              enum: ['maintain', 'lose_weight', 'gain_weight', 'build_muscle']
            }
          },
          required: ['userId']
        }
      } as Tool
    ],

    handlers: {
      get_user_profile: async (args: { userId: string }) => {
        const profile = await service.getUserProfile(args.userId);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(profile, null, 2)
          }]
        };
      },

      create_user_profile: async (args: CreateUserProfileDTO) => {
        const profile = await service.createUserProfile(args);
        return {
          content: [{
            type: 'text',
            text: `User profile created successfully: ${profile.id}`
          }]
        };
      },

      update_user_profile: async (args: { userId: string } & UpdateUserProfileDTO) => {
        const { userId, ...data } = args;
        const profile = await service.updateUserProfile(userId, data);
        return {
          content: [{
            type: 'text',
            text: `User profile updated successfully: ${profile.id}`
          }]
        };
      }
    }
  };
}
```

### Step 6: Create Tests

```typescript
// src/services/UserProfileService.test.ts

import { UserProfileService } from './UserProfileService';
import { UserProfileRepository } from '../repositories/UserProfileRepository';
import { ActivityLevel, HealthGoal } from '../types/user-profile.types';
import { AppError } from '../utils/errors';

describe('UserProfileService', () => {
  let service: UserProfileService;
  let repository: jest.Mocked<UserProfileRepository>;

  beforeEach(() => {
    // Create mock repository
    repository = {
      findByUserId: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      findAll: jest.fn()
    } as any;

    service = new UserProfileService(repository);
  });

  describe('getUserProfile', () => {
    it('should return user profile when found', async () => {
      const mockProfile = {
        id: '123',
        userId: 'user-1',
        age: 30,
        gender: 'male',
        activityLevel: ActivityLevel.MODERATE,
        goal: HealthGoal.MAINTAIN,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      repository.findByUserId.mockResolvedValue(mockProfile);

      const result = await service.getUserProfile('user-1');

      expect(result).toEqual(mockProfile);
      expect(repository.findByUserId).toHaveBeenCalledWith('user-1');
    });

    it('should throw AppError when profile not found', async () => {
      repository.findByUserId.mockResolvedValue(null);

      await expect(service.getUserProfile('user-1'))
        .rejects
        .toThrow(AppError);
      
      await expect(service.getUserProfile('user-1'))
        .rejects
        .toThrow('User profile not found');
    });
  });

  describe('createUserProfile', () => {
    it('should create new profile when none exists', async () => {
      const createData = {
        userId: 'user-1',
        age: 30,
        activityLevel: ActivityLevel.MODERATE,
        goal: HealthGoal.LOSE_WEIGHT
      };

      const createdProfile = {
        id: '123',
        ...createData,
        gender: undefined,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      repository.findByUserId.mockResolvedValue(null);
      repository.create.mockResolvedValue(createdProfile);

      const result = await service.createUserProfile(createData);

      expect(result).toEqual(createdProfile);
      expect(repository.findByUserId).toHaveBeenCalledWith('user-1');
      expect(repository.create).toHaveBeenCalledWith(createData);
    });

    it('should throw AppError when profile already exists', async () => {
      const existingProfile = {
        id: '123',
        userId: 'user-1',
        activityLevel: ActivityLevel.MODERATE,
        goal: HealthGoal.MAINTAIN,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      repository.findByUserId.mockResolvedValue(existingProfile);

      await expect(service.createUserProfile({
        userId: 'user-1',
        activityLevel: ActivityLevel.MODERATE,
        goal: HealthGoal.MAINTAIN
      }))
        .rejects
        .toThrow('User profile already exists');
    });
  });

  describe('updateUserProfile', () => {
    it('should update existing profile', async () => {
      const existingProfile = {
        id: '123',
        userId: 'user-1',
        age: 30,
        activityLevel: ActivityLevel.MODERATE,
        goal: HealthGoal.MAINTAIN,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      const updateData = {
        age: 31,
        goal: HealthGoal.LOSE_WEIGHT
      };

      const updatedProfile = {
        ...existingProfile,
        ...updateData
      };

      repository.findByUserId.mockResolvedValue(existingProfile);
      repository.update.mockResolvedValue(updatedProfile);

      const result = await service.updateUserProfile('user-1', updateData);

      expect(result).toEqual(updatedProfile);
      expect(repository.update).toHaveBeenCalledWith('123', updateData);
    });

    it('should throw AppError when profile not found', async () => {
      repository.findByUserId.mockResolvedValue(null);

      await expect(service.updateUserProfile('user-1', { age: 31 }))
        .rejects
        .toThrow('User profile not found');
    });
  });
});
```

## Best Practices

### 1. Strict TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

### 2. Use Proper Error Handling

```typescript
// Good - Custom error class
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Usage
throw new AppError('User not found', 404, 'USER_NOT_FOUND');

// Bad - Generic errors
throw new Error('Something went wrong');
```

### 3. Dependency Injection

```typescript
// Good - Constructor injection
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}
}

// Bad - Direct instantiation
export class UserService {
  private userRepository = new UserRepository();
  private emailService = new EmailService();
}
```

### 4. Proper Async/Await

```typescript
// Good
async function getUser(id: string): Promise<User> {
  try {
    const user = await userRepository.findById(id);
    if (!user) {
      throw new AppError('User not found', 404);
    }
    return user;
  } catch (error) {
    if (error instanceof AppError) throw error;
    throw new AppError('Failed to fetch user', 500);
  }
}

// Bad
function getUser(id: string): Promise<User> {
  return userRepository.findById(id)
    .then(user => {
      if (!user) throw new Error('Not found');
      return user;
    });
}
```

### 5. Comprehensive Testing

```typescript
// Good - Test all cases
describe('UserService', () => {
  describe('getUser', () => {
    it('should return user when found', ...);
    it('should throw 404 when not found', ...);
    it('should handle database errors', ...);
  });
});

// Bad - Only happy path
describe('UserService', () => {
  it('should get user', ...);
});
```

## Troubleshooting

### Module Not Found
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear TypeScript cache
rm -rf dist/
npm run build
```

### Type Errors
```bash
# Check types
npm run type-check

# Generate type declarations
npm run build

# Update @types packages
npm update @types/node @types/jest
```

### Test Failures
```bash
# Run with verbose output
npm test -- --verbose

# Run specific test
npm test -- UserService.test.ts

# Update snapshots
npm test -- -u

# Run with coverage
npm run test:coverage
```

### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres

# Run migrations
npm run migration:run

# Generate new migration
npm run migration:generate -- -n MigrationName
```

## References

- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
- **Jest Documentation**: https://jestjs.io/docs/getting-started
- **TypeORM Documentation**: https://typeorm.io/
- **MCP TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **ESLint Rules**: https://eslint.org/docs/latest/rules/

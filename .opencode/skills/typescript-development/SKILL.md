---
name: typescript-development
description: TypeScript development workflows and best practices for monorepo services (shared, assistant-mcp, api)
---

# TypeScript Development

TypeScript-Workflows für Monorepo-Services (shared, assistant-mcp, api).

## Quick Commands

### Setup
```bash
npm install                                      # Alle
npm install --workspace=cookidoo-assistant-mcp   # Spezifisch
```

### Tests
```bash
npm test                                         # Alle
npm test --workspace=cookidoo-assistant-mcp      # Spezifisch
npm run test:coverage --workspace=SERVICE        # Mit Coverage
npm run test:watch --workspace=SERVICE           # Watch
npm test --workspace=SERVICE -- file.test.ts     # Einzelne Datei
```

### Quality
```bash
npm run lint                                     # Alle
npm run lint:fix --workspace=SERVICE             # Auto-fix
npm run type-check --workspace=SERVICE           # Types
npm run lint && npm run type-check && npm test   # Full check
```

### Dev
```bash
npm run dev --workspace=SERVICE                  # Dev mode
npm run build --workspace=SERVICE                # Build
npm start --workspace=SERVICE                    # Start
```

## Feature-Struktur

### 1. Types (`src/types/feature.types.ts`)
```typescript
export interface UserProfile {
  id: string;
  userId: string;
  age?: number;
  activityLevel: ActivityLevel;
  goal: HealthGoal;
}

export enum ActivityLevel {
  SEDENTARY = 'sedentary',
  MODERATE = 'moderate',
  ACTIVE = 'active'
}

export interface CreateUserProfileDTO {
  userId: string;
  age?: number;
  activityLevel: ActivityLevel;
}
```

### 2. Entity (`src/models/Entity.ts`)
```typescript
import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity('user_profiles')
export class UserProfile {
  @PrimaryGeneratedColumn('uuid')
  id!: string;

  @Column({ unique: true })
  userId!: string;

  @Column({ nullable: true })
  age?: number;

  @Column({ type: 'enum', enum: ActivityLevel })
  activityLevel!: ActivityLevel;
}
```

### 3. Repository (`src/repositories/Repository.ts`)
```typescript
import { Repository, DataSource } from 'typeorm';

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
}
```

### 4. Service (`src/services/Service.ts`)
```typescript
import { AppError } from '../utils/errors';

export class UserProfileService {
  constructor(private repository: UserProfileRepository) {}

  async getUserProfile(userId: string): Promise<UserProfile> {
    const profile = await this.repository.findByUserId(userId);
    if (!profile) {
      throw new AppError(`Profile not found for ${userId}`, 404);
    }
    return profile;
  }

  async createUserProfile(data: CreateUserProfileDTO): Promise<UserProfile> {
    const existing = await this.repository.findByUserId(data.userId);
    if (existing) {
      throw new AppError(`Profile exists for ${data.userId}`, 409);
    }
    return this.repository.create(data);
  }
}
```

### 5. MCP Tool (`src/tools/feature.tools.ts`)
```typescript
import { Tool } from '@modelcontextprotocol/sdk/types.js';

export function createUserProfileTools(service: UserProfileService) {
  return {
    tools: [
      {
        name: 'get_user_profile',
        description: 'Get user health profile',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' }
          },
          required: ['userId']
        }
      } as Tool
    ],
    
    handlers: {
      get_user_profile: async (args: { userId: string }) => {
        const profile = await service.getUserProfile(args.userId);
        return {
          content: [{ type: 'text', text: JSON.stringify(profile, null, 2) }]
        };
      }
    }
  };
}
```

### 6. Tests (`src/services/Service.test.ts`)
```typescript
describe('UserProfileService', () => {
  let service: UserProfileService;
  let repository: jest.Mocked<UserProfileRepository>;

  beforeEach(() => {
    repository = {
      findByUserId: jest.fn(),
      create: jest.fn(),
      update: jest.fn()
    } as any;
    service = new UserProfileService(repository);
  });

  it('should return profile when found', async () => {
    const mock = { id: '123', userId: 'user-1' };
    repository.findByUserId.mockResolvedValue(mock);

    const result = await service.getUserProfile('user-1');
    expect(result).toEqual(mock);
  });

  it('should throw when not found', async () => {
    repository.findByUserId.mockResolvedValue(null);
    await expect(service.getUserProfile('user-1'))
      .rejects.toThrow(AppError);
  });
});
```

## Best Practices

### Error Handling
```typescript
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
throw new AppError('Not found', 404, 'USER_NOT_FOUND');
```

### Dependency Injection
```typescript
// Good
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}
}

// Bad
export class UserService {
  private userRepository = new UserRepository();
}
```

### Async/Await
```typescript
// Good
async function getUser(id: string): Promise<User> {
  try {
    const user = await userRepository.findById(id);
    if (!user) throw new AppError('Not found', 404);
    return user;
  } catch (error) {
    if (error instanceof AppError) throw error;
    throw new AppError('Failed to fetch', 500);
  }
}
```

## Troubleshooting

```bash
# Module not found
rm -rf node_modules package-lock.json && npm install

# Type errors
npm run type-check
npx tsc --noEmit --pretty

# Test failures
npm test -- --verbose
npm test -- --clearCache

# Database
docker-compose down -v && docker-compose up -d
npm run migration:run
```

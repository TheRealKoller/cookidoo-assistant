const isDbAvailable = process.env.DATABASE_AVAILABLE === 'true';

const coverageExclusions = [
  'src/**/*.d.ts',
  'src/**/__tests__/**',
  'src/**/index.ts',
  '!src/models/**', // Models are type definitions only
];

// Only exclude DB and repositories if database is NOT available
if (!isDbAvailable) {
  coverageExclusions.push(
    '!src/db/**',
    '!src/repositories/**',
  );
}

export default {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  transform: {
    '^.+\\.ts$': [
      'ts-jest',
      {
        useESM: false,
        diagnostics: {
          ignoreCodes: [151002],
        },
      },
    ],
  },
  moduleNameMapper: {
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  collectCoverageFrom: ['src/**/*.ts', ...coverageExclusions],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};

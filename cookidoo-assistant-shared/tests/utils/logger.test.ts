import { Logger } from '../../src/utils/logger';

describe('Logger', () => {
  let originalConsoleLog: typeof console.log;
  let originalConsoleWarn: typeof console.warn;
  let originalConsoleError: typeof console.error;
  let logOutput: string[];

  beforeEach(() => {
    logOutput = [];
    originalConsoleLog = console.log;
    originalConsoleWarn = console.warn;
    originalConsoleError = console.error;

    console.log = jest.fn((...args) => logOutput.push(args.join(' ')));
    console.warn = jest.fn((...args) => logOutput.push(args.join(' ')));
    console.error = jest.fn((...args) => logOutput.push(args.join(' ')));
  });

  afterEach(() => {
    console.log = originalConsoleLog;
    console.warn = originalConsoleWarn;
    console.error = originalConsoleError;
  });

  describe('log levels', () => {
    it('should log info messages when level is info', () => {
      const logger = new Logger('info');
      logger.info('Test message');
      expect(logOutput.length).toBe(1);
      expect(logOutput[0]).toContain('INFO: Test message');
    });

    it('should not log debug messages when level is info', () => {
      const logger = new Logger('info');
      logger.debug('Debug message');
      expect(logOutput.length).toBe(0);
    });

    it('should log debug messages when level is debug', () => {
      const logger = new Logger('debug');
      logger.debug('Debug message');
      expect(logOutput.length).toBe(1);
      expect(logOutput[0]).toContain('DEBUG: Debug message');
    });

    it('should log warn messages', () => {
      const logger = new Logger('info');
      logger.warn('Warning message');
      expect(logOutput.length).toBe(1);
      expect(logOutput[0]).toContain('WARN: Warning message');
    });

    it('should log error messages with error object', () => {
      const logger = new Logger('info');
      const error = new Error('Test error');
      logger.error('Error occurred', error);
      expect(logOutput.length).toBe(1);
      expect(logOutput[0]).toContain('ERROR: Error occurred');
      expect(logOutput[0]).toContain('Test error');
    });
  });

  describe('context logging', () => {
    it('should include context in log messages', () => {
      const logger = new Logger('info');
      logger.info('Message with context', { userId: '123', action: 'login' });
      expect(logOutput[0]).toContain('userId');
      expect(logOutput[0]).toContain('123');
      expect(logOutput[0]).toContain('action');
      expect(logOutput[0]).toContain('login');
    });
  });

  describe('setMinLevel', () => {
    it('should change log level dynamically', () => {
      const logger = new Logger('info');
      logger.debug('Should not appear');
      expect(logOutput.length).toBe(0);

      logger.setMinLevel('debug');
      logger.debug('Should appear');
      expect(logOutput.length).toBe(1);
    });
  });
});

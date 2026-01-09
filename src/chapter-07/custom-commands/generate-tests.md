# Custom Command: Generate Tests

Generate comprehensive tests for the specified file or function.

## Usage

```
/generate-tests <file-path> [function-name]
```

## Instructions

1. Read the target file and understand its functionality

2. Identify the testing framework from package.json (Jest, Mocha, Vitest, etc.)

3. Follow existing test patterns in the project

4. Generate tests covering:

   ### Happy Path
   - Normal inputs produce expected outputs
   - All main use cases work correctly

   ### Edge Cases
   - Empty inputs
   - Null/undefined values
   - Boundary values (0, -1, MAX_INT)
   - Very long strings
   - Special characters

   ### Error Conditions
   - Invalid inputs throw appropriate errors
   - Network failures are handled
   - Timeout scenarios
   - Permission errors

   ### Integration Points
   - Mock external dependencies
   - Verify API contracts
   - Test database operations with test data

5. Include test utilities:
   - Factory functions for test data
   - Helper functions for common assertions
   - Proper setup/teardown

## Template

```typescript
import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { functionUnderTest } from '../path/to/module';

describe('functionUnderTest', () => {
  // Setup
  beforeEach(() => {
    // Reset mocks, setup test data
  });

  afterEach(() => {
    // Cleanup
    jest.clearAllMocks();
  });

  describe('happy path', () => {
    it('should return expected result for valid input', () => {
      const result = functionUnderTest(validInput);
      expect(result).toEqual(expectedOutput);
    });
  });

  describe('edge cases', () => {
    it('should handle empty input', () => {
      const result = functionUnderTest('');
      expect(result).toBe(defaultValue);
    });

    it('should handle null input', () => {
      expect(() => functionUnderTest(null)).toThrow('Input required');
    });
  });

  describe('error handling', () => {
    it('should throw on invalid input', () => {
      expect(() => functionUnderTest(invalidInput)).toThrow(ExpectedError);
    });
  });
});
```

## Best Practices

1. **Descriptive names**: Test names should describe the scenario
2. **One assertion per test**: Each test should verify one thing
3. **AAA pattern**: Arrange, Act, Assert
4. **No logic in tests**: Tests should be straightforward
5. **Independent tests**: Tests shouldn't depend on each other

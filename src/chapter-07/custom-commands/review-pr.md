# Custom Command: Review PR

Review the current pull request for quality and issues.

## Instructions

1. Get the changed files:
   ```bash
   git diff origin/main...HEAD --name-only
   ```

2. For each changed file, analyze:
   - **Security**: Check for vulnerabilities, secrets, injection risks
   - **Performance**: Identify N+1 queries, memory leaks, inefficient algorithms
   - **Error Handling**: Verify try/catch, error propagation, logging
   - **Testing**: Check if changes have corresponding tests
   - **Style**: Ensure consistency with project conventions

3. Format findings as:

   ## Critical (Must Fix)
   Issues that block merge

   ## Major (Should Fix)
   Significant issues

   ## Minor (Nice to Have)
   Improvements

   ## Positive Feedback
   What was done well

4. For each issue, provide:
   - File and line number
   - Description of the problem
   - Why it matters
   - Suggested fix with code example

## Example Output

```markdown
## Critical (Must Fix)

### 1. SQL Injection in user query
**File**: src/services/user.ts:45
**Issue**: User input directly concatenated into SQL query
**Fix**:
```typescript
// Before
const query = `SELECT * FROM users WHERE id = ${userId}`;

// After (use parameterized query)
const query = `SELECT * FROM users WHERE id = $1`;
const result = await db.query(query, [userId]);
```

## Positive Feedback
- Good use of TypeScript generics in the response handlers
- Comprehensive test coverage for the new authentication flow
```

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0

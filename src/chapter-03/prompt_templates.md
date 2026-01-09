# Chapter 3: The Art of Prompting
## Prompt Templates for DevOps Engineers

This document contains reusable prompt templates for common DevOps tasks.

---

## The CRAFT Framework

Every good prompt should have these elements:

| Element | Description | Example |
|---------|-------------|---------|
| **C**ontext | Background information | "We're running a microservices architecture on Kubernetes" |
| **R**ole | Who should Claude be? | "Act as a senior SRE with 10 years of experience" |
| **A**ction | What to do | "Analyze these logs and identify the root cause" |
| **F**ormat | Output structure | "Provide your findings in a markdown table" |
| **T**one | Communication style | "Be concise and technical" |

---

## Template 1: Troubleshooting

```markdown
## Context
I'm a DevOps engineer troubleshooting [ISSUE TYPE] in our [ENVIRONMENT] environment.

## Current Situation
- **Service/System**: [SERVICE NAME]
- **Symptoms**: [WHAT'S HAPPENING]
- **Started**: [WHEN IT STARTED]
- **Impact**: [WHO/WHAT IS AFFECTED]

## What I've Tried
1. [ACTION 1] - [RESULT]
2. [ACTION 2] - [RESULT]
3. [ACTION 3] - [RESULT]

## Relevant Information
```
[PASTE LOGS, ERROR MESSAGES, CONFIGS]
```

## What I Need
Please help me:
1. Identify the most likely root cause
2. Suggest additional diagnostic steps
3. Recommend a fix with specific commands
4. Explain how to prevent this in the future
```

---

## Template 2: Code Review

```markdown
## Context
This is a [TYPE: PR/code change/new feature] for our [PROJECT DESCRIPTION].

## Files for Review
```[LANGUAGE]
[PASTE CODE]
```

## Review Focus Areas
Please review for:
- [ ] Security vulnerabilities (OWASP Top 10)
- [ ] Performance issues
- [ ] Error handling completeness
- [ ] Coding standards compliance
- [ ] Test coverage gaps

## Output Format
Provide findings as:
1. **Critical**: Must fix before merge
2. **Major**: Should fix before merge
3. **Minor**: Nice to have improvements
4. **Suggestions**: Optional enhancements

For each issue, provide:
- Line number/location
- Description of the problem
- Suggested fix with code example
```

---

## Template 3: Infrastructure Generation

```markdown
## Project Requirements
I need to create infrastructure for [PROJECT DESCRIPTION].

## Technical Specifications
- **Cloud Provider**: [AWS/GCP/Azure]
- **Environment**: [dev/staging/prod]
- **Scale**: [Expected load/users]
- **Budget**: [If applicable]

## Components Needed
- [ ] Compute: [EC2/EKS/Lambda/etc.]
- [ ] Database: [RDS/DynamoDB/etc.]
- [ ] Networking: [VPC/subnets/etc.]
- [ ] Security: [IAM/security groups/etc.]
- [ ] Monitoring: [CloudWatch/etc.]

## Requirements
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Constraints
- Must follow [COMPLIANCE FRAMEWORK]
- Must use [SPECIFIC TOOLS/VERSIONS]
- Must integrate with [EXISTING SYSTEMS]

## Output
Please provide:
1. Architecture overview (text description)
2. Terraform/CloudFormation code
3. Variable files for different environments
4. README with deployment instructions
```

---

## Template 4: Migration Planning

```markdown
## Migration Overview
We need to migrate from [SOURCE] to [TARGET].

## Current State
- **Technology**: [Current stack]
- **Scale**: [Data size, traffic, etc.]
- **Dependencies**: [Connected systems]
- **Timeline**: [Deadline if any]

## Target State
- **Technology**: [New stack]
- **Improvements**: [What we want to achieve]

## Constraints
- Maximum downtime: [TIME]
- Must maintain: [REQUIREMENTS]
- Cannot change: [LIMITATIONS]

## Risks
- [Known risk 1]
- [Known risk 2]

## Request
Please provide:
1. Migration strategy (big bang vs. gradual)
2. Detailed phase-by-phase plan
3. Rollback procedures for each phase
4. Testing/validation checkpoints
5. Risk mitigation strategies
```

---

## Template 5: Incident Response

```markdown
## Incident Summary
**Severity**: [P1/P2/P3/P4]
**Service**: [Affected service]
**Started**: [Time in UTC]
**Status**: [Investigating/Mitigating/Resolved]

## Symptoms
- [Symptom 1]
- [Symptom 2]

## Impact
- [User impact]
- [Business impact]

## Timeline
- HH:MM - [Event]
- HH:MM - [Event]

## Data Available
### Metrics
```
[Paste relevant metrics]
```

### Logs
```
[Paste relevant logs]
```

### Recent Changes
```
[Git log or deployment history]
```

## Analysis Requested
1. Correlate events to identify trigger
2. Determine root cause
3. Suggest immediate mitigation
4. Recommend permanent fix
5. Draft incident summary for stakeholders
```

---

## Template 6: Documentation Generation

```markdown
## Documentation Request
Generate [TYPE: runbook/README/API docs/architecture] for [SUBJECT].

## Context
- **Audience**: [Who will read this]
- **Technical Level**: [Beginner/Intermediate/Expert]
- **Purpose**: [Why this documentation is needed]

## Source Material
```
[Paste code, configs, or existing docs]
```

## Required Sections
1. [Section 1]
2. [Section 2]
3. [Section 3]

## Format Requirements
- Use [markdown/restructured text/etc.]
- Include code examples for [LANGUAGES]
- Add diagrams where helpful (describe in text)
- Maximum length: [PAGES/WORDS]
```

---

## Quick One-Liners

For quick tasks, use these concise templates:

```bash
# Explain an error
"Explain this error and how to fix it: [ERROR]"

# Optimize code
"Optimize this for [performance/readability/memory]: [CODE]"

# Generate tests
"Write unit tests for this function: [CODE]"

# Convert format
"Convert this from [FORMAT A] to [FORMAT B]: [CONTENT]"

# Security check
"Check this for security vulnerabilities: [CODE/CONFIG]"

# Best practices
"Review this against [AWS/K8s/Docker] best practices: [CONFIG]"
```

---

## Shell Helper Function

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
# AI prompt helper function
aiprompt() {
    local template="$1"
    case "$template" in
        troubleshoot)
            echo "Context: [ENVIRONMENT]
Issue: [DESCRIPTION]
Symptoms: [WHAT'S HAPPENING]
Tried: [WHAT YOU'VE TRIED]
Logs: [PASTE LOGS]

Help me identify root cause and fix."
            ;;
        review)
            echo "Review this code for security and performance issues:

\`\`\`
[PASTE CODE]
\`\`\`

Focus on: security, error handling, edge cases."
            ;;
        generate)
            echo "Generate [RESOURCE TYPE] for [PURPOSE]:

Requirements:
- [REQ 1]
- [REQ 2]

Constraints:
- [CONSTRAINT 1]

Follow [FRAMEWORK/BEST PRACTICES]."
            ;;
        *)
            echo "Available templates: troubleshoot, review, generate"
            ;;
    esac
}
```

Usage:
```bash
$ aiprompt troubleshoot
$ aiprompt review
$ aiprompt generate
```

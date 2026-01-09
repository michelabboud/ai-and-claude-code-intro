---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #eee
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  h1 {
    color: #00d4ff;
  }
  h2 {
    color: #7c3aed;
  }
  code {
    background-color: #2d2d44;
  }
  table {
    border-collapse: collapse;
    margin: 1em 0;
    width: 100%;
  }
  th {
    background-color: #7c3aed;
    color: #ffffff;
    font-weight: bold;
    padding: 12px 16px;
    text-align: left;
    border: 1px solid #5a2eb8;
  }
  td {
    background-color: #2d2d44;
    color: #eee;
    padding: 10px 16px;
    border: 1px solid #3d3d5c;
  }
  tr:nth-child(even) td {
    background-color: #363654;
  }
---

# AI for DevOps

## Chapter 10: Practical Applications

**Tips, Workflows, and Real-World Usage**

*By Michel Abboud | Created with Claude AI*
*© 2026 Michel Abboud | CC BY-NC 4.0*

---

# AI-Augmented Day

```
08:00 - Morning Check
> claude "Summarize overnight alerts"

09:00 - Code Review
> claude "Review PRs for security issues"

11:00 - Incident Response
> claude "Analyze these error logs"

14:00 - Infrastructure Work
> claude "Create Terraform for new service"

16:00 - Documentation
> claude "Update the runbook"
```

---

# Infrastructure as Code

## Terraform Generation

```bash
> Create Terraform for AWS with:
  - VPC across 3 AZs
  - ECS Fargate cluster
  - RDS PostgreSQL Multi-AZ
  - CloudFront distribution
  - All encrypted at rest
  - Cost allocation tags
```

---

# Kubernetes Manifests

```bash
> Create K8s manifests for user-service:
  - Rolling updates
  - HPA: 2-10 based on CPU 70%
  - Liveness/readiness probes
  - NetworkPolicy for api-gateway only
  - PodDisruptionBudget
  - Prometheus annotations
```

---

# CI/CD Pipelines

```bash
> Create GitHub Actions workflow:

  PR: Test and security scan

  Main branch:
  1. Test with coverage >80%
  2. Security scan (Bandit, Trivy)
  3. Build and push to ECR
  4. Deploy to staging
  5. Manual approval for prod
  6. Slack notifications
```

---

# Monitoring & Alerting

```bash
> Create Prometheus alerts for:
  - Service down (0 instances for 1min)
  - Error rate >5% for 5min
  - P99 latency >2s for 10min
  - CPU >80% for 10min
  - Pod restart loop

  Include runbook links and
  proper severity labels.
```

---

# Incident Response

```markdown
## Incident Template

> Analyze this incident:

Symptoms: Payment service 503 errors
Started: 14:32 UTC
Affected: 30% of requests

Logs: [paste]
Recent deploys: [paste]
Pod status: [paste]

1. What's the root cause?
2. Immediate mitigation?
3. Long-term fix?
```

---

# Security Automation

```bash
> Create security scanning pipeline:

  1. SAST: Semgrep
  2. SCA: Dependency vulnerabilities
  3. Secrets: gitleaks
  4. IaC: tfsec, Hadolint
  5. Containers: Trivy

  Block merge on critical issues.
```

---

# Documentation Generation

```bash
> From this codebase, generate:

  1. Architecture overview
  2. Service catalog
  3. Data flow diagram
  4. API documentation
  5. Runbook for operations

  Include ASCII diagrams.
```

---

# Shell Aliases

```bash
# Add to ~/.bashrc

alias ai='claude'
alias aireview='claude "Review: "'
alias aidebug='claude "Debug: "'

ai-review-pr() {
  git diff origin/main...HEAD | \
    claude "Review for security issues"
}

ai-logs() {
  tail -n 100 "$1" | \
    claude "Analyze for issues"
}
```

---

# Productivity Tips

## 1. Context is King
Include environment, versions, constraints

## 2. Iterate
Start simple, add requirements

## 3. Right Model
Haiku 4.5 for simple, Sonnet 4.5 for code, Opus 4.5 for complex

## 4. Verify
Always test AI-generated configs

---

# Common Patterns

```bash
# Explain then fix
> Explain this error, then fix it: [error]

# Review then implement
> Review this approach, then implement best solution

# Generate with constraints
> Create X that must use Y and must not use Z

# Compare options
> Compare options A vs B for [task]
```

---

# Building AI Culture

```
Phase 1: Introduction (2 weeks)
├── Demo sessions
├── Share resources
└── Set up access

Phase 2: Pilot (4 weeks)
├── Champions use daily
├── Document wins
└── Create team prompts

Phase 3: Expansion (4 weeks)
├── Full team rollout
├── Integrate into workflows
└── Measure improvements
```

---

# Metrics to Track

| Category | Metrics |
|----------|---------|
| Productivity | Incident resolution time |
| Quality | Issues caught by AI review |
| Adoption | API calls, active users |
| ROI | Time saved vs cost |

---

# The Future

- **Autonomous operations**: Self-healing infrastructure
- **Natural language infra**: "Deploy app for 10K users"
- **Continuous optimization**: AI-driven right-sizing
- **Predictive operations**: Issues detected before impact

---

# Your AI Journey

```
□ Set up Claude Code
□ Configure MCP servers
□ Create custom commands
□ Build prompt library
□ Measure improvements
□ Share with team

Your expertise + AI = Superpowers
```

---

# Key Takeaways

1. **AI transforms daily workflows**
2. **IaC generation saves hours**
3. **Automate code review & security**
4. **Build an AI-first culture**
5. **Measure and iterate**

---

# Quick Reference

```
┌─────────────────────────────────────────┐
│  Daily Tasks:                           │
│  • "Summarize overnight alerts"         │
│  • "Review PRs for security"            │
│  • "Analyze these logs"                 │
│                                         │
│  Infrastructure:                        │
│  • "Create Terraform for [X]"           │
│  • "Generate K8s manifests"             │
│  • "Write Ansible playbook"             │
│                                         │
│  CI/CD:                                 │
│  • "Create GitHub Actions for [X]"      │
│  • "Add security scanning"              │
│                                         │
│  Documentation:                         │
│  • "Create runbook for [service]"       │
│  • "Generate architecture docs"         │
└─────────────────────────────────────────┘
```

---

# Congratulations!

## You've Completed the Guide!

You now understand:
- AI and LLM fundamentals
- Effective prompting
- Claude and Claude Code
- MCP integrations
- Practical DevOps applications

**Go build amazing things!**

---

# Thank You!

## Resources

- Full chapter: [chapters/10-ai-for-devops.md](../chapters/10-ai-for-devops.md)
- All chapters: [chapters/](../chapters/)
- Claude: [claude.ai](https://claude.ai)
- MCP: [modelcontextprotocol.io](https://modelcontextprotocol.io)

---

# Credits

**Author:** Michel Abboud
**Created with:** Claude AI (Anthropic)

This entire guide and presentation series was created
with the assistance of AI - demonstrating the very
capabilities it teaches!

**License:** Creative Commons BY-NC 4.0
Free for personal and educational use.
Commercial use requires written permission.

© 2026 Michel Abboud

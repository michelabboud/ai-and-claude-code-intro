#!/usr/bin/env python3
"""
Chapter 16: Advanced Multi-Agent Workflows
Multi-Agent Code Review System

Deploys 5 specialist agents to comprehensively review pull requests:
1. Security Agent (Sonnet): OWASP vulnerabilities, secrets
2. Performance Agent (Sonnet): Algorithmic complexity, bottlenecks
3. Style Agent (Haiku): Code style, naming conventions
4. Test Coverage Agent (Haiku): Missing tests, test quality
5. Documentation Agent (Haiku): Missing/outdated documentation

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install anthropic PyGithub

Usage:
    python multi-agent-review.py \\
        --pr-number 123 \\
        --repo owner/repo-name \\
        --diff-file pr_diff.txt \\
        --changed-files changed_files.txt \\
        --output review_result.json
"""

import os
import asyncio
import json
import argparse
from datetime import datetime
from typing import Dict, List
from anthropic import AsyncAnthropic


class CodeReviewSwarm:
    """
    Multi-agent code review orchestrator.

    Deploys 5 specialist agents in parallel to review PR comprehensively.
    Aggregates findings and posts unified review comment.
    """

    def __init__(self, pr_number: int, repo: str, pr_diff: str, changed_files: List[str]):
        """
        Initialize code review swarm.

        Args:
            pr_number: Pull request number
            repo: Repository full name (owner/repo)
            pr_diff: Full PR diff content
            changed_files: List of changed file paths
        """
        self.pr_number = pr_number
        self.repo = repo
        self.pr_diff = pr_diff
        self.changed_files = changed_files
        self.client = AsyncAnthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        self.start_time = datetime.utcnow()

        print(f"🔍 Code Review Swarm initialized for PR #{pr_number}")
        print(f"📂 Repository: {repo}")
        print(f"📝 Files changed: {len(changed_files)}")

    async def review_with_swarm(self) -> Dict:
        """
        Deploy all 5 specialist agents in parallel.

        Returns:
            Dictionary containing aggregated review results
        """
        print(f"\n📡 Deploying 5 specialist agents in parallel...\\n")

        # Create tasks for parallel execution
        tasks = [
            self.security_review(self.pr_diff),
            self.performance_review(self.pr_diff),
            self.style_review(self.pr_diff),
            self.test_coverage_review(self.pr_diff, self.changed_files),
            self.documentation_review(self.pr_diff, self.changed_files)
        ]

        # Wait for all agents to complete
        results = await asyncio.gather(*tasks)

        # Calculate review time
        end_time = datetime.utcnow()
        review_duration = (end_time - self.start_time).total_seconds()

        print(f"\\n✅ All agents completed in {review_duration:.1f} seconds")

        # Aggregate findings
        aggregated = self.aggregate_findings(results, review_duration)

        return aggregated

    async def security_review(self, pr_diff: str) -> Dict:
        """
        Agent 1: Security vulnerability analysis with Sonnet.

        Checks for:
        - OWASP Top 10 vulnerabilities
        - Hardcoded secrets (API keys, passwords)
        - Authentication/authorization flaws
        - Input validation issues
        """
        print(f"🔒 [Security Agent] Starting analysis...")

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": f"""You are a security specialist reviewing this pull request for vulnerabilities.

PR Diff:
{pr_diff[:15000]}  # Limit to 15K chars

Analyze for:
1. **OWASP Top 10 vulnerabilities**:
   - SQL injection (string concatenation in queries)
   - XSS (unescaped user input in HTML)
   - CSRF (missing CSRF tokens)
   - Broken authentication (weak password checks, hardcoded credentials)
   - Security misconfiguration (debug mode enabled, verbose errors)

2. **Secrets detection**:
   - API keys (AWS, GCP, Azure keys)
   - Passwords or tokens in code
   - Private keys or certificates

3. **Authorization issues**:
   - Missing permission checks
   - Privilege escalation opportunities

Output JSON:
{{
  "severity": "critical|high|medium|low|none",
  "findings": [
    {{
      "severity": "critical",
      "type": "SQL Injection",
      "file": "api/users.py",
      "line": 45,
      "description": "User input concatenated directly into SQL query",
      "recommendation": "Use parameterized queries or ORM"
    }}
  ],
  "summary": "Brief executive summary"
}}

If no issues found, return {{"severity": "none", "findings": [], "summary": "No security issues detected"}}"""
                }]
            )

            result = {
                'agent': 'security',
                'model': 'sonnet',
                'status': 'completed',
                'findings': response.content[0].text,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

            print(f"✓ [Security Agent] Completed ({result['tokens_used']} tokens)")
            return result

        except Exception as e:
            print(f"✗ [Security Agent] Failed: {str(e)}")
            return {
                'agent': 'security',
                'model': 'sonnet',
                'status': 'failed',
                'error': str(e)
            }

    async def performance_review(self, pr_diff: str) -> Dict:
        """
        Agent 2: Performance analysis with Sonnet.

        Checks for:
        - Algorithmic complexity issues (O(n²) or worse)
        - N+1 query problems
        - Missing database indexes
        - Memory leaks
        """
        print(f"⚡ [Performance Agent] Starting analysis...")

        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": f"""You are a performance specialist reviewing this pull request for bottlenecks.

PR Diff:
{pr_diff[:15000]}

Analyze for:
1. **Algorithmic issues**:
   - Nested loops (potential O(n²))
   - Recursive algorithms without memoization
   - Linear search in large datasets

2. **Database anti-patterns**:
   - N+1 query problem
   - SELECT * instead of specific columns
   - Missing indexes on queried columns
   - Lack of pagination

3. **Memory issues**:
   - Large objects in memory
   - Memory leaks (unclosed connections)
   - String concatenation in loops

Output JSON:
{{
  "performance_score": 0-100,
  "bottlenecks": [
    {{
      "severity": "critical",
      "location": "function getUserOrders()",
      "file": "api/orders.py",
      "line": 123,
      "issue": "N+1 query problem",
      "current_performance": "2.5s for 100 orders",
      "potential_improvement": "250ms with single JOIN",
      "fix": "Use JOIN or eager loading"
    }}
  ],
  "quick_wins": ["Add index on user_id", "Enable query caching"]
}}

If no issues, return {{"performance_score": 95, "bottlenecks": [], "quick_wins": []}}"""
                }]
            )

            result = {
                'agent': 'performance',
                'model': 'sonnet',
                'status': 'completed',
                'findings': response.content[0].text,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

            print(f"✓ [Performance Agent] Completed ({result['tokens_used']} tokens)")
            return result

        except Exception as e:
            print(f"✗ [Performance Agent] Failed: {str(e)}")
            return {
                'agent': 'performance',
                'model': 'sonnet',
                'status': 'failed',
                'error': str(e)
            }

    async def style_review(self, pr_diff: str) -> Dict:
        """
        Agent 3: Code style analysis with Haiku.

        Checks for:
        - Naming conventions
        - Code formatting
        - Comment quality
        """
        print(f"🎨 [Style Agent] Starting analysis...")

        try:
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"""You are a code style reviewer checking this pull request.

PR Diff:
{pr_diff[:10000]}

Check for:
1. Naming conventions (camelCase, snake_case consistency)
2. Function/variable name clarity
3. Code formatting issues
4. Comment quality (outdated, missing, excessive)
5. Magic numbers (hardcoded values)

Output JSON with style issues found. Keep it concise.
If style is good, return {{"issues": [], "summary": "Code style follows conventions"}}"""
                }]
            )

            result = {
                'agent': 'style',
                'model': 'haiku',
                'status': 'completed',
                'findings': response.content[0].text,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

            print(f"✓ [Style Agent] Completed ({result['tokens_used']} tokens)")
            return result

        except Exception as e:
            print(f"✗ [Style Agent] Failed: {str(e)}")
            return {
                'agent': 'style',
                'model': 'haiku',
                'status': 'failed',
                'error': str(e)
            }

    async def test_coverage_review(self, pr_diff: str, changed_files: List[str]) -> Dict:
        """
        Agent 4: Test coverage analysis with Haiku.

        Checks for:
        - Missing tests for new functions
        - Test quality
        - Edge cases coverage
        """
        print(f"🧪 [Test Coverage Agent] Starting analysis...")

        try:
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"""You are a test coverage specialist reviewing this pull request.

PR Diff:
{pr_diff[:10000]}

Changed Files:
{', '.join(changed_files[:20])}

Check for:
1. New functions without tests
2. Missing edge case tests
3. Test quality (assertions, mocking)
4. Test file naming conventions

Output JSON listing missing tests.
If coverage is good, return {{"missing_tests": [], "summary": "Adequate test coverage"}}"""
                }]
            )

            result = {
                'agent': 'test_coverage',
                'model': 'haiku',
                'status': 'completed',
                'findings': response.content[0].text,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

            print(f"✓ [Test Coverage Agent] Completed ({result['tokens_used']} tokens)")
            return result

        except Exception as e:
            print(f"✗ [Test Coverage Agent] Failed: {str(e)}")
            return {
                'agent': 'test_coverage',
                'model': 'haiku',
                'status': 'failed',
                'error': str(e)
            }

    async def documentation_review(self, pr_diff: str, changed_files: List[str]) -> Dict:
        """
        Agent 5: Documentation analysis with Haiku.

        Checks for:
        - Missing docstrings
        - Outdated documentation
        - README updates needed
        """
        print(f"📚 [Documentation Agent] Starting analysis...")

        try:
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"""You are a documentation specialist reviewing this pull request.

PR Diff:
{pr_diff[:10000]}

Changed Files:
{', '.join(changed_files[:20])}

Check for:
1. Functions without docstrings
2. Outdated examples in comments
3. README updates needed (new features, API changes)
4. Missing API documentation

Output JSON listing documentation gaps.
If docs are complete, return {{"gaps": [], "summary": "Documentation is complete"}}"""
                }]
            )

            result = {
                'agent': 'documentation',
                'model': 'haiku',
                'status': 'completed',
                'findings': response.content[0].text,
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens
            }

            print(f"✓ [Documentation Agent] Completed ({result['tokens_used']} tokens)")
            return result

        except Exception as e:
            print(f"✗ [Documentation Agent] Failed: {str(e)}")
            return {
                'agent': 'documentation',
                'model': 'haiku',
                'status': 'failed',
                'error': str(e)
            }

    def aggregate_findings(self, all_findings: List[Dict], review_duration: float) -> Dict:
        """
        Aggregate findings from all agents into unified review.

        Args:
            all_findings: List of findings from all 5 agents
            review_duration: Total review time in seconds

        Returns:
            Aggregated review dictionary
        """
        # Parse agent findings
        critical_issues = []
        high_issues = []
        medium_issues = []
        low_issues = []

        for agent_result in all_findings:
            if agent_result['status'] != 'completed':
                continue

            try:
                findings = json.loads(agent_result['findings'])

                # Extract issues by severity
                agent_findings = findings.get('findings', findings.get('bottlenecks', findings.get('issues', [])))

                for issue in agent_findings:
                    severity = issue.get('severity', 'low')
                    issue['agent'] = agent_result['agent']

                    if severity == 'critical':
                        critical_issues.append(issue)
                    elif severity == 'high':
                        high_issues.append(issue)
                    elif severity == 'medium':
                        medium_issues.append(issue)
                    else:
                        low_issues.append(issue)

            except json.JSONDecodeError:
                print(f"Warning: Failed to parse findings from {agent_result['agent']}")

        # Generate summary
        summary = self.generate_review_summary(
            critical_issues,
            high_issues,
            medium_issues,
            low_issues,
            review_duration
        )

        return {
            'pr_number': self.pr_number,
            'repo': self.repo,
            'review_time_seconds': review_duration,
            'review_time_human': f"{review_duration:.1f}s",
            'critical_issues_count': len(critical_issues),
            'high_issues_count': len(high_issues),
            'medium_issues_count': len(medium_issues),
            'low_issues_count': len(low_issues),
            'critical_issues': critical_issues,
            'high_issues': high_issues,
            'medium_issues': medium_issues,
            'low_issues': low_issues,
            'summary': summary,
            'agent_details': all_findings,
            'total_tokens_used': sum(f.get('tokens_used', 0) for f in all_findings)
        }

    def generate_review_summary(
        self,
        critical: List,
        high: List,
        medium: List,
        low: List,
        duration: float
    ) -> str:
        """
        Generate markdown summary for GitHub comment.

        Args:
            critical/high/medium/low: Issue lists by severity
            duration: Review duration in seconds

        Returns:
            Markdown formatted summary
        """
        total_issues = len(critical) + len(high) + len(medium) + len(low)

        summary = f"""## 🤖 Multi-Agent Code Review

**Review completed in {duration:.1f}s** | **{total_issues} issues found**

"""

        if not total_issues:
            summary += "✅ **All checks passed!** No issues detected by any agent.\n\n"
            summary += "_Reviewed by: Security, Performance, Style, Test Coverage, Documentation agents_"
            return summary

        # Critical issues
        if critical:
            summary += f"### 🚨 Critical Issues ({len(critical)})\n\n"
            summary += "**These must be fixed before merging:**\n\n"
            for issue in critical:
                summary += f"- **[{issue['agent'].title()}]** {issue.get('type', 'Issue')} in `{issue.get('file', 'unknown')}`\n"
                summary += f"  - {issue.get('description', issue.get('issue', 'No description'))}\n"
                summary += f"  - 💡 Recommendation: {issue.get('recommendation', issue.get('fix', 'See details above'))}\n\n"

        # High issues
        if high:
            summary += f"### ⚠️  High Priority Issues ({len(high)})\n\n"
            for issue in high:
                summary += f"- **[{issue['agent'].title()}]** {issue.get('type', 'Issue')} in `{issue.get('file', 'unknown')}`\n"
                summary += f"  - {issue.get('description', issue.get('issue', 'No description'))}\n\n"

        # Medium/Low issues
        if medium or low:
            summary += f"<details>\n<summary>📝 Medium ({len(medium)}) and Low ({len(low)}) Priority Issues</summary>\n\n"

            for issue in medium + low:
                summary += f"- **[{issue['agent'].title()}]** {issue.get('type', 'Issue')} in `{issue.get('file', 'unknown')}`\n"

            summary += "\n</details>\n\n"

        summary += "---\n\n"
        summary += "_🤖 Generated by Multi-Agent Code Review System_\n"
        summary += "_Agents: Security (Sonnet), Performance (Sonnet), Style (Haiku), Tests (Haiku), Docs (Haiku)_"

        return summary


# CLI
async def main():
    parser = argparse.ArgumentParser(description='Multi-agent code review system')
    parser.add_argument('--pr-number', type=int, required=True, help='Pull request number')
    parser.add_argument('--repo', required=True, help='Repository (owner/repo)')
    parser.add_argument('--diff-file', required=True, help='Path to PR diff file')
    parser.add_argument('--changed-files', required=True, help='Path to changed files list')
    parser.add_argument('--output', required=True, help='Output JSON file path')

    args = parser.parse_args()

    # Read PR diff
    with open(args.diff_file, 'r') as f:
        pr_diff = f.read()

    # Read changed files
    with open(args.changed_files, 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]

    # Run review
    swarm = CodeReviewSwarm(args.pr_number, args.repo, pr_diff, changed_files)
    results = await swarm.review_with_swarm()

    # Write results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {args.output}")

    # Exit with error code if critical issues found
    if results['critical_issues_count'] > 0:
        print(f"\n❌ Found {results['critical_issues_count']} critical issues - blocking merge")
        exit(1)
    else:
        print(f"\n✅ Review complete - {results['total_tokens_used']} tokens used")
        exit(0)


if __name__ == '__main__':
    asyncio.run(main())

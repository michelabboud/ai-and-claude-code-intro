#!/usr/bin/env python3
"""
Scalable Log Analyzer with AI
Process millions of logs with AI-powered pattern extraction and natural language queries.

Part of Chapter 18: Advanced AIOps

Features:
- Batch processing for efficiency
- AI pattern extraction
- Natural language query interface
- Cost-optimized sampling
"""

import os
import json
import asyncio
import hashlib
from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict
import logging

import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LogAnalyzer:
    """
    Scalable log analyzer with AI-powered insights.

    Processes large volumes of logs efficiently using:
    - Batching to reduce API calls
    - Haiku model for cost optimization
    - Smart sampling for routine logs
    """

    def __init__(self, anthropic_api_key: Optional[str] = None):
        api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic(api_key=api_key)

        # Processing configuration
        self.batch_size = 50  # Process 50 logs per API call
        self.max_logs_per_analysis = 10000  # Safety limit

    async def analyze_logs(self, logs: List[str], log_level: str = 'ALL') -> Dict:
        """
        Analyze logs and extract patterns, errors, and anomalies.

        Args:
            logs: List of log strings
            log_level: Filter by level (ALL, ERROR, WARN, INFO)

        Returns:
            Dict with analysis results
        """
        logger.info(f"Analyzing {len(logs)} logs...")

        # Filter by level if specified
        if log_level != 'ALL':
            logs = [log for log in logs if log_level in log]
            logger.info(f"Filtered to {len(logs)} logs with level {log_level}")

        # Limit for safety
        if len(logs) > self.max_logs_per_analysis:
            logger.warning(f"Too many logs ({len(logs)}), sampling {self.max_logs_per_analysis}")
            logs = logs[:self.max_logs_per_analysis]

        # Process in batches
        all_patterns = []
        all_errors = []
        all_anomalies = []

        batch_count = (len(logs) + self.batch_size - 1) // self.batch_size

        for i in range(0, len(logs), self.batch_size):
            batch_num = i // self.batch_size + 1
            batch = logs[i:i + self.batch_size]

            logger.info(f"Processing batch {batch_num}/{batch_count} ({len(batch)} logs)")

            batch_analysis = await self._analyze_batch(batch)

            all_patterns.extend(batch_analysis.get('patterns', []))
            all_errors.extend(batch_analysis.get('errors', []))
            all_anomalies.extend(batch_analysis.get('anomalies', []))

        # Aggregate results
        result = {
            'total_logs': len(logs),
            'patterns': self._aggregate_patterns(all_patterns),
            'top_errors': self._get_top_errors(all_errors),
            'anomalies': all_anomalies,
            'summary': await self._generate_summary(logs, all_patterns, all_errors, all_anomalies)
        }

        logger.info(f"Analysis complete: {len(result['patterns'])} patterns, {len(result['top_errors'])} error types")

        return result

    async def _analyze_batch(self, batch: List[str]) -> Dict:
        """Analyze a batch of logs with AI"""

        prompt = f"""Analyze these log entries and extract patterns, errors, and anomalies.

Logs ({len(batch)} entries):
{chr(10).join(batch[:50])}  # Show first 50

Extract:
1. **Patterns**: Common log patterns (e.g., "Database query completed in Xms")
2. **Errors**: Distinct error types with example message
3. **Anomalies**: Unusual/unexpected log entries

Return JSON:
{{
  "patterns": [
    {{"pattern": "...", "count": X, "example": "..."}},
    ...
  ],
  "errors": [
    {{"error_type": "...", "message": "...", "severity": "critical|high|medium"}},
    ...
  ],
  "anomalies": [
    {{"log": "...", "reason": "why this is unusual"}},
    ...
  ]
}}

Be concise. Return ONLY JSON."""

        response = self.claude.messages.create(
            model="claude-3-haiku-20240307",  # Use Haiku for cost optimization
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            result = json.loads(response.content[0].text)
            return result
        except json.JSONDecodeError:
            logger.error("Failed to parse AI response as JSON")
            return {'patterns': [], 'errors': [], 'anomalies': []}

    def _aggregate_patterns(self, patterns: List[Dict]) -> List[Dict]:
        """Aggregate patterns across batches"""
        pattern_counts = defaultdict(int)
        pattern_examples = {}

        for p in patterns:
            pattern_key = p['pattern']
            pattern_counts[pattern_key] += p.get('count', 1)

            if pattern_key not in pattern_examples:
                pattern_examples[pattern_key] = p.get('example', '')

        # Convert to sorted list
        aggregated = [
            {
                'pattern': pattern,
                'count': count,
                'example': pattern_examples[pattern]
            }
            for pattern, count in pattern_counts.items()
        ]

        # Sort by count (descending)
        aggregated.sort(key=lambda x: x['count'], reverse=True)

        return aggregated[:20]  # Top 20 patterns

    def _get_top_errors(self, errors: List[Dict], top_n: int = 10) -> List[Dict]:
        """Get top N most common errors"""
        error_counts = defaultdict(int)
        error_details = {}

        for err in errors:
            error_type = err['error_type']
            error_counts[error_type] += 1

            if error_type not in error_details:
                error_details[error_type] = err

        # Convert to sorted list
        top_errors = [
            {
                'error_type': error_type,
                'count': count,
                'message': error_details[error_type]['message'],
                'severity': error_details[error_type].get('severity', 'medium')
            }
            for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        ]

        return top_errors

    async def _generate_summary(self, logs: List[str], patterns: List[Dict],
                                errors: List[Dict], anomalies: List[Dict]) -> str:
        """Generate natural language summary of analysis"""

        prompt = f"""Summarize this log analysis in 2-3 sentences.

Total logs: {len(logs)}
Patterns found: {len(patterns)}
Errors found: {len(errors)}
Anomalies found: {len(anomalies)}

Top patterns:
{json.dumps(patterns[:5], indent=2)}

Top errors:
{json.dumps(errors[:5], indent=2)}

Write a concise summary highlighting:
- Main activity observed
- Any concerning issues
- Recommended next steps (if issues found)

Keep it under 100 words."""

        response = self.claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    async def natural_language_query(self, logs: List[str], query: str) -> Dict:
        """
        Query logs using natural language.

        Args:
            logs: List of log strings
            query: Natural language query (e.g., "show me database errors")

        Returns:
            Dict with query results and AI summary
        """
        logger.info(f"Natural language query: '{query}'")

        # AI converts natural language to filter criteria
        filter_criteria = await self._nl_to_filter(query)

        # Filter logs based on criteria
        filtered_logs = self._apply_filter(logs, filter_criteria)

        logger.info(f"Query matched {len(filtered_logs)} logs")

        # AI summarizes results
        summary = await self._summarize_query_results(query, filtered_logs)

        return {
            'query': query,
            'filter_criteria': filter_criteria,
            'matched_logs': filtered_logs[:50],  # Return first 50
            'total_matches': len(filtered_logs),
            'ai_summary': summary
        }

    async def _nl_to_filter(self, query: str) -> Dict:
        """Convert natural language query to filter criteria"""

        prompt = f"""Convert this natural language log query to filter criteria.

Query: "{query}"

Extract filtering criteria:
- keywords: List of keywords to search for
- log_level: ERROR, WARN, INFO, or null (any level)
- time_related: true if query mentions time/date
- service: Service name if mentioned

Return JSON:
{{
  "keywords": ["keyword1", "keyword2"],
  "log_level": "ERROR|WARN|INFO|null",
  "time_related": true|false,
  "service": "service-name|null",
  "explanation": "Brief explanation of how you interpreted the query"
}}

Return ONLY JSON."""

        response = self.claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            criteria = json.loads(response.content[0].text)
            return criteria
        except json.JSONDecodeError:
            logger.error("Failed to parse filter criteria")
            return {'keywords': [], 'log_level': None}

    def _apply_filter(self, logs: List[str], criteria: Dict) -> List[str]:
        """Apply filter criteria to logs"""
        filtered = logs

        # Filter by keywords
        keywords = criteria.get('keywords', [])
        if keywords:
            filtered = [
                log for log in filtered
                if any(keyword.lower() in log.lower() for keyword in keywords)
            ]

        # Filter by log level
        log_level = criteria.get('log_level')
        if log_level:
            filtered = [log for log in filtered if log_level in log]

        # Filter by service
        service = criteria.get('service')
        if service:
            filtered = [log for log in filtered if service in log]

        return filtered

    async def _summarize_query_results(self, query: str, results: List[str]) -> str:
        """AI summarizes query results"""

        if not results:
            return "No matching logs found."

        prompt = f"""Summarize these log query results in plain English.

Original query: "{query}"

Results ({len(results)} total, showing first 20):
{chr(10).join(results[:20])}

Provide:
1. Direct answer to the query
2. Key patterns observed
3. Any concerning trends
4. Recommended next steps

Keep it concise (2-3 sentences)."""

        response = self.claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()


class IntelligentLogSampler:
    """
    AI-powered log sampling for cost optimization.

    Only indexes interesting logs, samples routine logs, stores AI summaries.
    """

    def __init__(self, anthropic_api_key: Optional[str] = None):
        api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic(api_key=api_key)

        # Sampling configuration
        self.routine_sample_rate = 0.10  # Index 10% of routine logs

    async def should_index(self, log_entry: Dict) -> bool:
        """
        Decide if a log should be indexed or discarded.

        Args:
            log_entry: Dict with 'level', 'message', etc.

        Returns:
            True if log should be indexed
        """
        # Always index critical logs
        if log_entry.get('level') in ['ERROR', 'CRITICAL', 'WARN']:
            return True

        # Always index security-related
        if 'auth' in log_entry.get('message', '').lower():
            return True

        if 'security' in log_entry.get('message', '').lower():
            return True

        # For INFO/DEBUG: sample + AI decision
        if random.random() < self.routine_sample_rate:
            return True

        # AI evaluates if log is interesting
        is_interesting = await self._ai_evaluate_interest(log_entry)
        return is_interesting

    async def _ai_evaluate_interest(self, log: Dict) -> bool:
        """Use AI to detect if log contains unusual patterns"""

        # Use cheap Haiku model
        prompt = f"""Is this log entry interesting/unusual? Answer YES or NO.

Log: {log.get('message', '')}

Interesting = unexpected errors, performance issues, security concerns, anomalies.
Not interesting = routine operations, health checks, standard requests.

Answer:"""

        response = self.claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.content[0].text.strip().upper()
        return answer == "YES"


async def demo_analysis():
    """Demo: Analyze sample logs"""
    analyzer = LogAnalyzer()

    # Sample logs
    sample_logs = [
        "[2026-01-11 10:15:23] INFO: User 1234 logged in successfully",
        "[2026-01-11 10:15:24] ERROR: Database connection timeout to db-primary after 5000ms",
        "[2026-01-11 10:15:25] WARN: High memory usage: 92%",
        "[2026-01-11 10:15:26] INFO: API request /users/1234 completed in 156ms",
        "[2026-01-11 10:15:27] ERROR: Failed to send email to user@example.com: SMTP error",
        "[2026-01-11 10:15:28] CRITICAL: Disk usage at 95% on server-3",
        "[2026-01-11 10:15:29] INFO: User 5678 logged out",
        "[2026-01-11 10:15:30] ERROR: Database connection timeout to db-primary after 5000ms",
    ] * 10  # Duplicate to simulate more logs

    print("=== Analyzing Logs ===")
    analysis = await analyzer.analyze_logs(sample_logs, log_level='ALL')

    print(json.dumps(analysis, indent=2))

    print("\n=== Natural Language Query ===")
    query_result = await analyzer.natural_language_query(
        sample_logs,
        "show me all database errors"
    )

    print(f"Query: {query_result['query']}")
    print(f"Matches: {query_result['total_matches']}")
    print(f"\nAI Summary:\n{query_result['ai_summary']}")


async def demo_batch_analysis():
    """Demo: Batch process 10,000 logs"""
    analyzer = LogAnalyzer()

    # Generate 10K sample logs
    import random
    from datetime import timedelta

    log_templates = [
        "INFO: User {user_id} logged in successfully",
        "ERROR: Database connection timeout to {db_host}",
        "WARN: High memory usage: {memory}%",
        "INFO: API request /users/{user_id} completed in {latency}ms",
        "ERROR: Failed to send email to {email}: SMTP error",
        "CRITICAL: Disk usage at {disk}% on {host}"
    ]

    start_time = datetime.now() - timedelta(hours=1)
    logs = []

    for i in range(10000):
        template = random.choice(log_templates)
        timestamp = start_time + timedelta(seconds=i*0.36)

        log = f"[{timestamp.isoformat()}] " + template.format(
            user_id=random.randint(1000, 9999),
            db_host=random.choice(['db-primary', 'db-replica-1', 'db-replica-2']),
            memory=random.randint(60, 95),
            latency=random.randint(10, 2000),
            email=f"user{random.randint(1,100)}@example.com",
            disk=random.randint(50, 95),
            host=f"server-{random.randint(1, 5)}"
        )

        logs.append(log)

    print(f"Generated {len(logs)} sample logs")

    start = datetime.now()
    analysis = await analyzer.analyze_logs(logs, log_level='ERROR')
    elapsed = (datetime.now() - start).total_seconds()

    print(f"\nProcessed {len(logs)} logs in {elapsed:.1f} seconds")
    print(f"Top errors: {len(analysis['top_errors'])}")
    print(f"\nSummary:\n{analysis['summary']}")


if __name__ == '__main__':
    import random

    print("=== Scalable Log Analyzer Demo ===\n")

    # Run demos
    asyncio.run(demo_analysis())
    print("\n" + "="*50 + "\n")
    asyncio.run(demo_batch_analysis())

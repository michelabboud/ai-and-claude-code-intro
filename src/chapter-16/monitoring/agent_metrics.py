#!/usr/bin/env python3
"""
Chapter 16: Advanced Multi-Agent Workflows
Agent Performance Metrics (Prometheus)

Tracks agent execution metrics for monitoring and alerting.
Exposes metrics via HTTP endpoint for Prometheus scraping.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install prometheus-client

Usage:
    # Start metrics server
    python agent_metrics.py --port 8000

    # In your agent code
    from agent_metrics import track_agent_execution

    @track_agent_execution('security-001', 'sonnet')
    def analyze_security(code):
        # Your analysis logic
        pass

    # Prometheus scrape config:
    # scrape_configs:
    #   - job_name: 'agent-metrics'
    #     static_configs:
    #       - targets: ['localhost:8000']
"""

import time
import functools
from typing import Callable
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Summary,
    start_http_server
)


# ============================================================================
# Metric Definitions
# ============================================================================

# Task execution metrics
agent_tasks_total = Counter(
    'agent_tasks_total',
    'Total number of tasks executed by agents',
    ['agent_id', 'model', 'status']  # status: success/failure
)

agent_task_duration_seconds = Histogram(
    'agent_task_duration_seconds',
    'Time taken to complete agent tasks',
    ['agent_id', 'model'],
    buckets=[1, 5, 10, 30, 60, 120, 300, 600, 1800]  # 1s to 30min
)

agent_task_duration_summary = Summary(
    'agent_task_duration_summary_seconds',
    'Summary statistics for agent task duration',
    ['agent_id', 'model']
)

# Token usage metrics
agent_tokens_used_total = Counter(
    'agent_tokens_used_total',
    'Total tokens consumed by agents',
    ['agent_id', 'model', 'type']  # type: input/output
)

agent_token_cost_dollars = Counter(
    'agent_token_cost_dollars_total',
    'Estimated cost in dollars for token usage',
    ['agent_id', 'model']
)

# Agent pool metrics
active_agents = Gauge(
    'active_agents',
    'Number of currently active (busy) agents',
    ['model']
)

idle_agents = Gauge(
    'idle_agents',
    'Number of idle agents in the pool',
    ['model']
)

queued_tasks = Gauge(
    'queued_tasks',
    'Number of tasks waiting in queue',
    []
)

# Error metrics
agent_errors_total = Counter(
    'agent_errors_total',
    'Total number of agent errors',
    ['agent_id', 'model', 'error_type']
)

agent_timeouts_total = Counter(
    'agent_timeouts_total',
    'Total number of agent timeouts',
    ['agent_id', 'model']
)

# Quality metrics
agent_findings_total = Counter(
    'agent_findings_total',
    'Total findings reported by agents',
    ['agent_id', 'severity']  # severity: critical/high/medium/low
)

agent_confidence_score = Histogram(
    'agent_confidence_score',
    'Confidence scores reported by agents',
    ['agent_id'],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)


# ============================================================================
# Helper Functions
# ============================================================================

def track_agent_execution(agent_id: str, model: str) -> Callable:
    """
    Decorator to automatically track agent execution metrics.

    Usage:
        @track_agent_execution('security-001', 'sonnet')
        def analyze_security(code):
            # Your logic here
            return result

    Args:
        agent_id: Unique identifier for the agent
        model: AI model being used (haiku, sonnet, opus)

    Returns:
        Decorated function with metric tracking
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Mark agent as active
            active_agents.labels(model=model).inc()

            start_time = time.time()
            success = False

            try:
                # Execute the function
                result = func(*args, **kwargs)
                success = True
                return result

            except TimeoutError:
                agent_timeouts_total.labels(agent_id=agent_id, model=model).inc()
                raise

            except Exception as e:
                error_type = type(e).__name__
                agent_errors_total.labels(
                    agent_id=agent_id,
                    model=model,
                    error_type=error_type
                ).inc()
                raise

            finally:
                # Record metrics
                duration = time.time() - start_time

                agent_tasks_total.labels(
                    agent_id=agent_id,
                    model=model,
                    status='success' if success else 'failure'
                ).inc()

                agent_task_duration_seconds.labels(
                    agent_id=agent_id,
                    model=model
                ).observe(duration)

                agent_task_duration_summary.labels(
                    agent_id=agent_id,
                    model=model
                ).observe(duration)

                # Mark agent as idle
                active_agents.labels(model=model).dec()

        return wrapper
    return decorator


def record_token_usage(agent_id: str, model: str, input_tokens: int, output_tokens: int):
    """
    Record token usage for an agent invocation.

    Args:
        agent_id: Agent identifier
        model: AI model used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    """
    agent_tokens_used_total.labels(
        agent_id=agent_id,
        model=model,
        type='input'
    ).inc(input_tokens)

    agent_tokens_used_total.labels(
        agent_id=agent_id,
        model=model,
        type='output'
    ).inc(output_tokens)

    # Estimate cost (2026 pricing)
    cost = calculate_cost(model, input_tokens, output_tokens)

    agent_token_cost_dollars.labels(
        agent_id=agent_id,
        model=model
    ).inc(cost)


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate estimated cost for token usage.

    Pricing (2026 rates per million tokens):
    - Haiku: $0.25 input, $1.25 output
    - Sonnet: $3 input, $15 output
    - Opus: $15 input, $75 output

    Args:
        model: AI model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Cost in dollars
    """
    pricing = {
        'haiku': {'input': 0.25, 'output': 1.25},
        'claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
        'sonnet': {'input': 3.0, 'output': 15.0},
        'claude-3-5-sonnet-20241022': {'input': 3.0, 'output': 15.0},
        'opus': {'input': 15.0, 'output': 75.0},
        'claude-opus-4-5-20251101': {'input': 15.0, 'output': 75.0},
    }

    # Default to sonnet pricing if model not found
    rates = pricing.get(model, pricing['sonnet'])

    input_cost = (input_tokens / 1_000_000) * rates['input']
    output_cost = (output_tokens / 1_000_000) * rates['output']

    return input_cost + output_cost


def record_finding(agent_id: str, severity: str, confidence: float):
    """
    Record an agent finding.

    Args:
        agent_id: Agent identifier
        severity: Severity level (critical, high, medium, low)
        confidence: Confidence score (0.0 to 1.0)
    """
    agent_findings_total.labels(
        agent_id=agent_id,
        severity=severity
    ).inc()

    agent_confidence_score.labels(
        agent_id=agent_id
    ).observe(confidence)


def update_pool_stats(model: str, active: int, idle: int, queued: int):
    """
    Update agent pool statistics.

    Args:
        model: AI model type
        active: Number of active agents
        idle: Number of idle agents
        queued: Number of queued tasks
    """
    active_agents.labels(model=model).set(active)
    idle_agents.labels(model=model).set(idle)
    queued_tasks.set(queued)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == '__main__':
    import argparse
    import random

    parser = argparse.ArgumentParser(description='Agent metrics exporter for Prometheus')
    parser.add_argument('--port', type=int, default=8000, help='HTTP server port')
    args = parser.parse_args()

    # Start Prometheus metrics server
    start_http_server(args.port)
    print(f"📊 Metrics server started on http://localhost:{args.port}/metrics")
    print("Available metrics:")
    print("  - agent_tasks_total")
    print("  - agent_task_duration_seconds")
    print("  - agent_tokens_used_total")
    print("  - agent_token_cost_dollars_total")
    print("  - active_agents")
    print("  - agent_errors_total")
    print("  - agent_findings_total")
    print("\\nPress Ctrl+C to stop\\n")

    # Simulate some agent activity for demo
    try:
        while True:
            # Simulate agent execution
            agent_id = random.choice(['security-001', 'performance-001', 'cost-001'])
            model = random.choice(['haiku', 'sonnet', 'opus'])

            # Simulate task
            active_agents.labels(model=model).inc()

            duration = random.uniform(1, 30)
            time.sleep(0.1)  # Simulate work

            success = random.random() > 0.1  # 90% success rate

            agent_tasks_total.labels(
                agent_id=agent_id,
                model=model,
                status='success' if success else 'failure'
            ).inc()

            agent_task_duration_seconds.labels(
                agent_id=agent_id,
                model=model
            ).observe(duration)

            # Simulate token usage
            input_tokens = random.randint(1000, 10000)
            output_tokens = random.randint(500, 5000)
            record_token_usage(agent_id, model, input_tokens, output_tokens)

            # Simulate findings
            if random.random() > 0.7:  # 30% chance of finding
                severity = random.choice(['critical', 'high', 'medium', 'low'])
                confidence = random.uniform(0.5, 1.0)
                record_finding(agent_id, severity, confidence)

            active_agents.labels(model=model).dec()

            # Update pool stats
            update_pool_stats(
                model='sonnet',
                active=random.randint(0, 5),
                idle=random.randint(0, 5),
                queued=random.randint(0, 10)
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\\n\\nShutting down metrics server...")

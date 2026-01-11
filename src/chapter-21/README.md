# Chapter 21: Resilience Patterns for Agents

This directory contains production-ready implementations of core resilience patterns for building robust AI agents.

## Overview

**Chapter 21 (Part 1 of 2)** teaches the **core resilience patterns** for preventing Ralph Wiggum loops, complementing Chapter 20's loop detection techniques. Chapter 22 covers advanced patterns (exponential backoff, graceful degradation, self-healing).

### Resilience Patterns Implemented (Chapter 21)

| Pattern | Purpose | File |
|---------|---------|------|
| **Circuit Breaker** | Prevent cascading failures | `src/circuit_breaker.py` |
| **Idempotency** | Safe retries without duplicates | Chapter 21 content |
| **Checkpointing** | Crash recovery | Chapter 21 content |

**Note**: Exponential Backoff, Graceful Degradation, and Self-Healing are covered in Chapter 22: Production Deployment.

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

```bash
# Navigate to chapter directory
cd src/chapter-21

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Circuit Breaker Pattern

Protect external service calls from cascading failures:

```python
from src.circuit_breaker import CircuitBreaker, CircuitBreakerConfig

# Configure circuit breaker
breaker = CircuitBreaker(
    config=CircuitBreakerConfig(
        failure_threshold=5,  # Open after 5 failures
        timeout=60.0          # Try recovery after 60 seconds
    )
)

# Use with async functions
result = await breaker.call(external_api_call, arg1, arg2)
```

**Run the demo:**

```bash
python src/circuit_breaker.py
```

### 2. Complete Production Example

See the full incident response agent combining all 6 patterns:

```python
# See examples/ directory for complete implementation
# Demonstrates real-world usage of all resilience patterns together
```

## Running Examples

### Circuit Breaker Demo

```bash
python src/circuit_breaker.py
```

**Expected output:**
- Shows circuit transitioning through CLOSED → OPEN → HALF_OPEN → CLOSED states
- Demonstrates fail-fast behavior when circuit is open
- Shows recovery testing in half-open state

## Testing

Run the test suite to verify all patterns work correctly:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_circuit_breaker.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Directory Structure

```
chapter-21/
├── src/                         # Main pattern implementations
│   ├── circuit_breaker.py      # Circuit breaker pattern
│   └── __init__.py
├── examples/                    # Complete working examples
│   └── production_incident_agent.py  # Full production example
├── tests/                       # Unit tests
│   └── test_circuit_breaker.py
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

## Key Concepts

### Defense in Depth

Combine multiple patterns for comprehensive resilience:

```python
# Example: Combining patterns
circuit_breaker = CircuitBreaker()
retry_strategy = RetryStrategy()
idempotent_agent = IdempotentAgent()

# Result: Resilient system at multiple levels
```

### When to Use Each Pattern

| Situation | Recommended Pattern |
|-----------|-------------------|
| External API call | Circuit Breaker |
| Transient network failure | Exponential Backoff |
| Database update | Idempotency |
| Long workflow | Checkpointing |
| Multi-service system | Graceful Degradation |
| Production deployment | Self-Healing |

## Production Considerations

### Circuit Breaker Tuning

- **failure_threshold**: Start with 3-5 failures
- **timeout**: Start with 30-60 seconds
- **success_threshold**: Usually 1-2 successes

### Monitoring

Add metrics for all resilience patterns:

```python
# Track circuit breaker state
prometheus_metrics.gauge('circuit_breaker_state', breaker.state.value)

# Track retry attempts
prometheus_metrics.counter('retry_attempts_total')

# Track degradation level
prometheus_metrics.gauge('system_degradation_level')
```

### Logging

Log all resilience actions for debugging:

```python
logger.info(f"Circuit opened after {threshold} failures")
logger.warning(f"Degraded mode: using cached data")
logger.info(f"Self-heal successful: cleared caches")
```

## Troubleshooting

### Circuit Breaker Stuck Open

**Problem**: Circuit never closes even after service recovers

**Solution**:
- Check `timeout` value (may be too long)
- Verify `success_threshold` is achievable
- Ensure service health checks are accurate

### Excessive Retries

**Problem**: System retries too aggressively

**Solution**:
- Add exponential backoff
- Set `max_retries` limit
- Implement retry budgets

### Stale Cached Data

**Problem**: Graceful degradation serving old data

**Solution**:
- Set appropriate cache TTL
- Display "cached data" warnings to users
- Implement cache invalidation

## Learn More

- **Chapter 20**: Loop Detection & Prevention Fundamentals
- **Chapter 21**: Resilience Patterns for Agents (this chapter)
- **Chapter 22**: Production Deployment of Agentic Systems
- Related reading: *Release It!* by Michael Nygard, *Site Reliability Engineering* by Google

## Additional Resources

- [Netflix Hystrix Documentation](https://github.com/Netflix/Hystrix/wiki)
- [AWS Architecture Blog: Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/)

## Support

For questions or issues:
1. Review the chapter content in `chapters/21-resilience-patterns.md`
2. See Chapter 22 for advanced patterns: `chapters/22-production-deployment.md`
3. Check the hands-on exercise for practical implementation guidance
4. Review the production example for complete reference implementation

---

**Chapter 21 Code** | Resilience Patterns for Agents | © 2026 Michel Abboud

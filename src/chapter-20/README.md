# Chapter 20: Agent Loop Detection Code Examples

This directory contains working code examples for Chapter 20: Agent Loop Detection & Prevention Fundamentals.

## Directory Structure

```
chapter-20/
├── src/                     # Core modules
│   ├── loop_detector.py     # Basic loop detection
│   ├── monitored_agent.py   # Agent with Prometheus metrics
│   ├── secure_agent.py      # Security-hardened agent
│   ├── secrets_manager.py   # Vault secrets management
│   └── compliance_logger.py # Audit logging
├── examples/                # Demonstration scripts
│   ├── basic_loop.py        # Intentional loop (broken)
│   ├── fixed_loop.py        # Same logic with detection
│   └── db_agent.py          # Database connection agent
├── tests/                   # Unit tests
│   └── test_loop_detector.py
└── README.md               # This file
```

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running Examples

### Basic Loop Detection

```bash
# Run broken agent (will loop forever - press Ctrl+C to stop)
python examples/basic_loop.py

# Run fixed agent (with loop detection)
python examples/fixed_loop.py
```

### Monitored Agent with Prometheus

```bash
# Start agent with metrics server
python src/monitored_agent.py

# View metrics in browser
open http://localhost:8000/metrics
```

### Security-Hardened Agent

```bash
# Test DoW protection
python src/secure_agent.py
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Monitoring Setup

### Prometheus + Grafana (Docker Compose)

```bash
# Start monitoring stack
cd monitoring
docker-compose up -d

# Access services
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### Kubernetes Deployment

```bash
# Deploy agent
kubectl apply -f k8s/deployment.yaml

# Port-forward metrics
kubectl port-forward deployment/agent-loop-detection 8000:8000
```

## Key Learnings

This code demonstrates:

1. **Loop Detection**: Simple repetition tracking and max iteration limits
2. **State Fingerprinting**: Detect when agent returns to same state
3. **Prometheus Metrics**: Production-grade observability
4. **DoW Protection**: Rate limiting and cost budgets
5. **Secrets Management**: HashiCorp Vault integration
6. **Compliance Logging**: SOC 2 / GDPR audit trails

## Next Steps

After completing these examples, move to Chapter 21 to learn:
- Circuit breaker pattern
- Idempotency and checkpointing
- Advanced retry strategies
- Self-healing architectures

## Support

- Questions? Open an issue on GitHub
- Found a bug? Submit a PR
- Need help? Join our Discord #loop-detection channel

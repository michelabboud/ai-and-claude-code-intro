# Chapter 18: Advanced AIOps - Code Examples

This directory contains production-ready code examples from Chapter 18: Advanced AIOps.

## Files

### 1. `auto_remediation_engine.py` (527 lines)

Production-ready auto-remediation engine with:
- Safe/risky/forbidden action classifications
- Human approval workflow for risky actions
- Circuit breaker to prevent runaway automation
- Comprehensive audit logging
- Rollback capability

**Dependencies:**
```bash
pip install anthropic kubernetes
```

**Usage:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python auto_remediation_engine.py
```

**Key Features:**
- Classifies actions as SAFE, REQUIRES_APPROVAL, or FORBIDDEN
- Circuit breaker opens at 30% failure rate
- AI diagnosis with confidence thresholds
- Full audit trail for compliance
- Kubernetes integration for pod/deployment operations

---

### 2. `self_healing_operator.py` (442 lines)

Kubernetes operator that automatically detects and heals unhealthy pods using AI.

**Dependencies:**
```bash
pip install kopf kubernetes anthropic
```

**Usage:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python self_healing_operator.py
```

**Key Features:**
- Real-time pod health monitoring
- AI-powered failure diagnosis (OOMKilled, CrashLoopBackOff, etc.)
- Automatic remediation: restart pods, increase memory/CPU, rollback deployments
- Confidence threshold (80%) for automatic vs. human escalation
- Kubernetes operator framework (kopf)

**Remediations Supported:**
- Restart failed pods
- Increase memory limits (OOMKilled)
- Increase CPU limits (throttled)
- Rollback bad deployments
- Escalate complex issues to humans

---

### 3. `scalable_log_analyzer.py` (486 lines)

Process millions of logs with AI-powered pattern extraction and natural language queries.

**Dependencies:**
```bash
pip install anthropic
```

**Usage:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python scalable_log_analyzer.py
```

**Key Features:**
- Batch processing (50 logs per API call)
- Uses Haiku model for cost optimization
- Pattern extraction and error classification
- Natural language query interface
- Smart sampling for routine logs

**Example Queries:**
```python
analyzer = LogAnalyzer()

# Analyze all logs
analysis = await analyzer.analyze_logs(logs, log_level='ERROR')

# Natural language query
result = await analyzer.natural_language_query(
    logs,
    "show me all database connection errors in the last hour"
)
```

---

### 4. `trace_analyzer.py` (444 lines)

Analyze Jaeger/Zipkin distributed traces to find bottlenecks and suggest optimizations.

**Dependencies:**
```bash
pip install anthropic requests
```

**Usage:**
```bash
export ANTHROPIC_API_KEY="your-api-key"

# Requires running Jaeger instance
# Start Jaeger all-in-one: docker run -d --name jaeger -p 16686:16686 jaegertracing/all-in-one:latest

python trace_analyzer.py
```

**Key Features:**
- Fetch slow traces from Jaeger API
- AI identifies performance bottlenecks
- Suggests specific code optimizations (with examples)
- Maps service dependencies automatically
- Detects architectural issues (circular deps, chatty services, etc.)

**Example Analysis:**
```python
analyzer = TraceAnalyzer(jaeger_host='localhost:16686')

# Find slow traces
analysis = await analyzer.analyze_slow_traces('api-server', min_duration_ms=1000)

# Get code-level suggestions
suggestions = await analyzer.suggest_code_optimizations(trace_id='abc123')
```

---

### 5. `chaos_experiment.yaml` (246 lines)

Chaos Mesh experiments for validating self-healing systems.

**Prerequisites:**
```bash
# Install Chaos Mesh
kubectl create ns chaos-mesh
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh --version 2.6.0
```

**Usage:**
```bash
kubectl apply -f chaos_experiment.yaml
```

**Experiments Included:**

1. **Pod Failure** - Kill 20% of pods (tests pod restart)
2. **Memory Stress** - Trigger OOMKills (tests memory increase)
3. **Network Latency** - Add 500ms delays (tests performance detection)
4. **CPU Stress** - Max out CPU (tests autoscaling)
5. **Bad Deployment** - Deploy crashloop image (tests rollback)
6. **Network Partition** - Simulate network split (tests resilience)
7. **Disk Fill** - Fill disk space (tests cleanup)
8. **HTTP Abort** - Inject 500 errors (tests circuit breakers)

**Success Criteria:**
- Self-healing operator detects failures within 30 seconds
- 80%+ auto-healing rate
- <5% incorrect remediations
- MTTR < 2 minutes

---

## Integration Example

Complete workflow using all components together:

```python
import asyncio
from auto_remediation_engine import AutoRemediationEngine
from self_healing_operator import SelfHealingOperator
from scalable_log_analyzer import LogAnalyzer
from trace_analyzer import TraceAnalyzer

async def full_aiops_pipeline():
    """Complete AIOps pipeline"""

    # 1. Monitor with self-healing operator (runs continuously)
    operator = SelfHealingOperator()
    # operator runs as Kubernetes operator

    # 2. Analyze logs for patterns
    log_analyzer = LogAnalyzer()
    logs = fetch_recent_logs()  # From Elasticsearch
    log_analysis = await log_analyzer.analyze_logs(logs)

    # 3. Analyze traces for bottlenecks
    trace_analyzer = TraceAnalyzer()
    trace_analysis = await trace_analyzer.analyze_slow_traces('api-server')

    # 4. Handle alerts with auto-remediation
    engine = AutoRemediationEngine()
    alert = {
        'alertname': 'HighDatabaseConnections',
        'severity': 'critical'
    }
    remediation_result = await engine.handle_alert(alert)

    print(f"Log patterns: {len(log_analysis['patterns'])}")
    print(f"Trace bottlenecks: {trace_analysis['analysis']['bottleneck_service']}")
    print(f"Remediation: {remediation_result['status']}")

# Run pipeline
asyncio.run(full_aiops_pipeline())
```

---

## Testing

### Unit Tests

Each module includes demo functions for testing:

```bash
# Test auto-remediation
python auto_remediation_engine.py

# Test self-healing (requires Kubernetes cluster)
python self_healing_operator.py

# Test log analysis
python scalable_log_analyzer.py

# Test trace analysis (requires Jaeger)
python trace_analyzer.py
```

### Chaos Engineering Validation

```bash
# Apply chaos experiments
kubectl apply -f chaos_experiment.yaml

# Watch pod health
kubectl get pods -w -n production

# Check operator logs
kubectl logs -f deployment/self-healing-operator -n kube-system

# Validate success criteria
kubectl get podchaos,stresschaos,networkchaos -n production
```

---

## Production Deployment

### 1. Deploy Self-Healing Operator

```bash
# Build Docker image
docker build -t self-healing-operator:v1 .

# Deploy to Kubernetes
kubectl create namespace aiops
kubectl create secret generic anthropic-api-key \
  --from-literal=ANTHROPIC_API_KEY="your-key" \
  -n aiops

kubectl apply -f kubernetes/operator-deployment.yaml
```

### 2. Configure Auto-Remediation Webhook

```bash
# Deploy webhook receiver
kubectl apply -f kubernetes/auto-remediation-webhook.yaml

# Configure Prometheus AlertManager
# alertmanager.yml:
# receivers:
#   - name: 'auto-remediation'
#     webhook_configs:
#       - url: 'http://auto-remediation-service.aiops.svc.cluster.local/webhook'
```

### 3. Deploy Log Analyzer

```bash
# Deploy as CronJob (hourly analysis)
kubectl apply -f kubernetes/log-analyzer-cronjob.yaml

# Or as streaming processor with Kafka
kubectl apply -f kubernetes/log-analyzer-stream.yaml
```

---

## Cost Estimates

Based on production usage:

**Auto-Remediation Engine:**
- 4 incidents/week × $0.07/incident = $1.12/week
- **Monthly: ~$5**

**Log Analyzer (10K logs/day):**
- Haiku: 200 API calls/day × $0.001 = $0.20/day
- **Monthly: ~$6**

**Trace Analyzer (100 traces/day):**
- Sonnet: 10 API calls/day × $0.03 = $0.30/day
- **Monthly: ~$9**

**Total Monthly AI Costs: ~$20**

Compare to:
- Manual incident response: ~$3,600/month (20 hours × $180/hr)
- **ROI: 180× return**

---

## Troubleshooting

### Common Issues

**1. "Failed to load kubeconfig"**
```bash
# Set KUBECONFIG environment variable
export KUBECONFIG=~/.kube/config

# Or run from within Kubernetes cluster (uses service account)
```

**2. "Circuit breaker is OPEN"**
```bash
# Wait 15 minutes for automatic reset, or restart operator
kubectl rollout restart deployment/auto-remediation-engine -n aiops
```

**3. "AI confidence too low"**
```bash
# Check logs for diagnosis details
# May need to:
# - Gather more context (metrics, logs)
# - Use Opus model for complex scenarios
# - Escalate to human operator
```

**4. "Chaos experiment not working"**
```bash
# Verify Chaos Mesh is running
kubectl get pods -n chaos-mesh

# Check experiment status
kubectl describe podchaos pod-failure-test -n production

# View Chaos Mesh dashboard
kubectl port-forward -n chaos-mesh svc/chaos-dashboard 2333:2333
# Open http://localhost:2333
```

---

## References

- **Chapter 18**: Advanced AIOps (full guide in `/chapters/18-aiops-advanced.md`)
- **Anthropic Claude API**: https://docs.anthropic.com
- **Kubernetes Python Client**: https://github.com/kubernetes-client/python
- **Kopf (Kubernetes Operators)**: https://kopf.readthedocs.io
- **Chaos Mesh**: https://chaos-mesh.org
- **Jaeger**: https://www.jaegertracing.io

---

## License

Part of "AI and Claude Code: A Comprehensive Guide for DevOps Engineers"

Author: Michel Abboud
License: CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial)

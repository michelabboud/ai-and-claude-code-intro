"""
Production agent with Prometheus metrics.

This agent exposes metrics for monitoring loop detection,
execution times, token usage, and costs in real-time.
"""

import time
import asyncio
from typing import Dict, Optional
from prometheus_client import Counter, Histogram, Gauge, Info, start_http_server

from loop_detector import LoopDetector, LoopDetectionConfig, LoopDetected


# Define Prometheus metrics
# =========================

# Counter: Monotonically increasing values
agent_executions_total = Counter(
    'agent_executions_total',
    'Total number of agent executions',
    ['status', 'agent_type']  # Labels for filtering
)

agent_loops_detected_total = Counter(
    'agent_loops_detected_total',
    'Total loops detected and prevented',
    ['loop_type', 'agent_type']
)

agent_token_usage_total = Counter(
    'agent_tokens_used_total',
    'Total tokens consumed',
    ['model', 'token_type']  # token_type: input/output
)

agent_cost_dollars_total = Counter(
    'agent_cost_dollars_total',
    'Total estimated cost in USD',
    ['model']
)

# Histogram: Track distribution of values
agent_execution_duration_seconds = Histogram(
    'agent_execution_duration_seconds',
    'Time spent executing agent tasks',
    ['agent_type'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 120.0]
)

agent_iteration_count = Histogram(
    'agent_iteration_count',
    'Number of iterations before completion or loop detection',
    ['agent_type'],
    buckets=[1, 3, 5, 10, 15, 20, 30, 50, 100]
)

# Gauge: Values that can go up or down
agent_active_count = Gauge(
    'agent_active_count',
    'Number of currently active agents',
    ['agent_type']
)

agent_queue_length = Gauge(
    'agent_queue_length',
    'Number of tasks waiting in queue'
)

# Info: Metadata about the agent
agent_info = Info(
    'agent_version',
    'Agent version and configuration'
)

# Set agent info once at startup
agent_info.info({
    'version': '1.0.0',
    'python': '3.11',
    'loop_detection': 'enabled'
})


class MonitoredAgent:
    """
    Production agent with comprehensive Prometheus monitoring.

    Tracks:
    - Execution times and counts
    - Loop detection events
    - Token usage and costs
    - Active agent count
    """

    def __init__(
        self,
        agent_type: str = "pod_fixer",
        model: str = "claude-3-5-sonnet-20241022"
    ):
        self.agent_type = agent_type
        self.model = model
        self.loop_detector = LoopDetector(
            config=LoopDetectionConfig(
                max_action_repetitions=3,
                max_total_iterations=20,
                debug=False  # Disable debug in production
            )
        )

        # Token pricing (as of 2024)
        self.token_prices = {
            'claude-3-5-sonnet-20241022': {
                'input': 3.00 / 1_000_000,   # $3 per 1M tokens
                'output': 15.00 / 1_000_000   # $15 per 1M tokens
            },
            'claude-3-opus-20240229': {
                'input': 15.00 / 1_000_000,
                'output': 75.00 / 1_000_000
            }
        }

    async def execute(self, task: str, **kwargs) -> Dict:
        """
        Execute agent task with full monitoring.

        Args:
            task: Task to perform (e.g., "fix_pod", "analyze_logs")
            **kwargs: Task-specific parameters

        Returns:
            Result dictionary with status and details
        """
        # Track active agents
        agent_active_count.labels(agent_type=self.agent_type).inc()

        # Start execution timer
        start_time = time.time()

        try:
            # Execute task
            result = await self._execute_task(task, **kwargs)

            # Record success
            agent_executions_total.labels(
                status='success',
                agent_type=self.agent_type
            ).inc()

            # Record token usage and cost
            if 'tokens' in result:
                self._record_tokens(result['tokens'])

            return result

        except LoopDetected as e:
            # Record loop detection
            agent_loops_detected_total.labels(
                loop_type='action_repetition',
                agent_type=self.agent_type
            ).inc()

            agent_executions_total.labels(
                status='loop_detected',
                agent_type=self.agent_type
            ).inc()

            # Re-raise for handling upstream
            raise

        except Exception as e:
            # Record failure
            agent_executions_total.labels(
                status='error',
                agent_type=self.agent_type
            ).inc()

            raise

        finally:
            # Record execution time
            duration = time.time() - start_time
            agent_execution_duration_seconds.labels(
                agent_type=self.agent_type
            ).observe(duration)

            # Record iteration count
            agent_iteration_count.labels(
                agent_type=self.agent_type
            ).observe(self.loop_detector.iteration_count)

            # Track active agents
            agent_active_count.labels(agent_type=self.agent_type).dec()

    async def _execute_task(self, task: str, **kwargs) -> Dict:
        """
        Internal task execution logic.

        This is where your actual agent logic goes.
        """
        if task == "fix_pod":
            return await self._fix_pod(kwargs.get('pod_name'))
        elif task == "analyze_logs":
            return await self._analyze_logs(kwargs.get('log_file'))
        else:
            raise ValueError(f"Unknown task: {task}")

    async def _fix_pod(self, pod_name: str) -> Dict:
        """Example task: Fix failing pod"""
        iteration = 0
        max_iterations = 10

        while iteration < max_iterations:
            iteration += 1

            # Check action before performing
            self.loop_detector.check_action("check_pod_status")

            # Simulate checking pod
            status = await self._check_pod_status(pod_name)

            if status == "Running":
                return {
                    'status': 'success',
                    'message': f'Pod {pod_name} is running',
                    'iterations': iteration,
                    'tokens': {'input': 1000, 'output': 500}
                }

            # Check action before performing
            self.loop_detector.check_action("restart_pod")

            # Simulate restart
            await self._restart_pod(pod_name)
            await asyncio.sleep(2)

        return {
            'status': 'failed',
            'message': f'Could not fix pod after {max_iterations} attempts',
            'iterations': iteration
        }

    async def _check_pod_status(self, pod_name: str) -> str:
        """Simulate Kubernetes API call"""
        await asyncio.sleep(0.1)
        # In real implementation, call K8s API
        return "CrashLoopBackOff"  # Always failing for demo

    async def _restart_pod(self, pod_name: str) -> None:
        """Simulate pod restart"""
        await asyncio.sleep(0.5)
        # In real implementation, kubectl delete pod

    async def _analyze_logs(self, log_file: str) -> Dict:
        """Example task: Analyze logs"""
        # Implementation here
        pass

    def _record_tokens(self, tokens: Dict[str, int]):
        """Record token usage and cost"""
        input_tokens = tokens.get('input', 0)
        output_tokens = tokens.get('output', 0)

        # Record token counts
        agent_token_usage_total.labels(
            model=self.model,
            token_type='input'
        ).inc(input_tokens)

        agent_token_usage_total.labels(
            model=self.model,
            token_type='output'
        ).inc(output_tokens)

        # Calculate and record cost
        if self.model in self.token_prices:
            prices = self.token_prices[self.model]
            cost = (
                input_tokens * prices['input'] +
                output_tokens * prices['output']
            )

            agent_cost_dollars_total.labels(model=self.model).inc(cost)


# Main application
async def main():
    """Run agent with Prometheus metrics server"""

    # Start Prometheus metrics HTTP server
    # Metrics will be available at http://localhost:8000/metrics
    start_http_server(8000)
    print("✅ Prometheus metrics server started on http://localhost:8000/metrics")

    # Create agent
    agent = MonitoredAgent(agent_type="pod_fixer")

    # Simulate work
    print("\nSimulating agent work...")
    for i in range(5):
        print(f"\n--- Task {i+1} ---")
        try:
            result = await agent.execute("fix_pod", pod_name=f"my-app-{i}")
            print(f"Result: {result['status']}")
        except LoopDetected as e:
            print(f"❌ Loop detected: {e}")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(1)

    # Keep server running for scraping
    print("\n✅ Agent work complete. Metrics server still running...")
    print("   View metrics: http://localhost:8000/metrics")
    print("   Press Ctrl+C to stop")

    try:
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\n\nShutting down...")


if __name__ == "__main__":
    asyncio.run(main())

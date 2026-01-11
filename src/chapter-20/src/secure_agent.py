"""
Security-hardened agent with DoW protection.
"""

import time
import asyncio
import zlib
from typing import Dict, Optional
from prometheus_client import Counter

# Security metrics
dow_attempts_blocked = Counter(
    'dow_attempts_blocked_total',
    'Denial of Wallet attempts blocked'
)

rate_limit_exceeded = Counter(
    'rate_limit_exceeded_total',
    'Rate limit exceeded events'
)


class RateLimiter:
    """
    Token bucket rate limiter to prevent DoW attacks.

    Limits both requests per second and total cost per hour.
    """

    def __init__(
        self,
        max_requests_per_minute: int = 60,
        max_cost_per_hour: float = 10.0
    ):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_cost_per_hour = max_cost_per_hour

        # Sliding window for requests
        self.request_timestamps = []

        # Cost tracking
        self.hourly_costs = []

    def allow_request(self) -> bool:
        """Check if request is allowed under rate limit"""
        current_time = time.time()

        # Clean old requests (older than 1 minute)
        cutoff = current_time - 60
        self.request_timestamps = [
            ts for ts in self.request_timestamps if ts > cutoff
        ]

        # Check rate limit
        if len(self.request_timestamps) >= self.max_requests_per_minute:
            rate_limit_exceeded.inc()
            return False

        # Allow request
        self.request_timestamps.append(current_time)
        return True

    def record_cost(self, cost: float):
        """Record API cost"""
        current_time = time.time()

        # Clean old costs (older than 1 hour)
        cutoff = current_time - 3600
        self.hourly_costs = [
            (ts, c) for ts, c in self.hourly_costs if ts > cutoff
        ]

        # Add new cost
        self.hourly_costs.append((current_time, cost))

    def get_hourly_cost(self) -> float:
        """Get total cost in last hour"""
        return sum(cost for _, cost in self.hourly_costs)

    def allow_cost(self, estimated_cost: float) -> bool:
        """Check if cost is allowed"""
        current_hourly_cost = self.get_hourly_cost()

        if current_hourly_cost + estimated_cost > self.max_cost_per_hour:
            dow_attempts_blocked.inc()
            return False

        return True


class SecureAgent:
    """
    Security-hardened agent with DoW protection,
    rate limiting, and audit logging.
    """

    def __init__(self):
        self.rate_limiter = RateLimiter(
            max_requests_per_minute=60,  # 1 req/sec average
            max_cost_per_hour=10.0        # $10/hour max
        )
        self.audit_log = []

    async def execute(self, task: str, **kwargs) -> Dict:
        """Execute task with security checks"""

        # Security check 1: Rate limiting
        if not self.rate_limiter.allow_request():
            self._audit_log('rate_limit_exceeded', task, kwargs)
            raise RateLimitExceeded(
                f"Rate limit exceeded: {self.rate_limiter.max_requests_per_minute} req/min"
            )

        # Security check 2: Cost budget
        estimated_cost = self._estimate_cost(task, kwargs)
        if not self.rate_limiter.allow_cost(estimated_cost):
            self._audit_log('cost_limit_exceeded', task, kwargs)
            raise CostLimitExceeded(
                f"Cost limit exceeded: ${self.rate_limiter.max_cost_per_hour}/hour"
            )

        # Security check 3: Input validation
        self._validate_input(task, kwargs)

        # Execute task
        try:
            result = await self._execute_task(task, **kwargs)

            # Record actual cost
            actual_cost = result.get('cost', estimated_cost)
            self.rate_limiter.record_cost(actual_cost)

            self._audit_log('success', task, kwargs, result)
            return result

        except Exception as e:
            self._audit_log('error', task, kwargs, error=str(e))
            raise

    def _estimate_cost(self, task: str, kwargs: Dict) -> float:
        """
        Estimate API cost before execution.

        Prevents expensive operations from starting if budget exhausted.
        """
        # Estimate tokens based on input size
        input_size = len(str(kwargs))
        estimated_input_tokens = input_size * 0.75  # Rough estimate

        # Assume 2:1 output ratio
        estimated_output_tokens = estimated_input_tokens * 2

        # Claude 3.5 Sonnet pricing
        cost = (
            estimated_input_tokens * (3.00 / 1_000_000) +
            estimated_output_tokens * (15.00 / 1_000_000)
        )

        return cost

    def _validate_input(self, task: str, kwargs: Dict):
        """
        Validate input to prevent injection attacks and DoW.
        """
        # Check 1: Input size limit (prevent massive token usage)
        input_str = str(kwargs)
        if len(input_str) > 100_000:  # 100KB limit
            raise InputTooLarge(f"Input size {len(input_str)} exceeds 100KB limit")

        # Check 2: Detect repetitive patterns (DoW indicator)
        if self._is_repetitive(input_str):
            dow_attempts_blocked.inc()
            raise SuspiciousInput("Input contains repetitive patterns (possible DoW attack)")

        # Check 3: Task whitelist
        allowed_tasks = ['fix_pod', 'analyze_logs', 'check_metrics']
        if task not in allowed_tasks:
            raise UnauthorizedTask(f"Task '{task}' not in whitelist")

    def _is_repetitive(self, text: str, threshold: float = 0.8) -> bool:
        """
        Detect if text is suspiciously repetitive.

        Uses simple compression ratio heuristic:
        If zlib compresses text by >80%, it's highly repetitive.
        """
        if len(text) < 100:  # Skip check for small inputs
            return False

        compressed = zlib.compress(text.encode())
        compression_ratio = len(compressed) / len(text.encode())

        return compression_ratio < (1 - threshold)

    def _audit_log(self, event: str, task: str, kwargs: Dict, result: Optional[Dict] = None, error: Optional[str] = None):
        """
        Audit log for security compliance (SOC 2, GDPR, etc.)
        """
        log_entry = {
            'timestamp': time.time(),
            'event': event,
            'task': task,
            'input_size': len(str(kwargs)),
            'result': result,
            'error': error
        }

        self.audit_log.append(log_entry)

        # In production, send to logging system (Splunk, ELK, etc.)
        print(f"[AUDIT] {event}: {task}")

    async def _execute_task(self, task: str, **kwargs) -> Dict:
        """Execute the actual task"""
        # Simulated implementation
        await asyncio.sleep(0.1)
        return {'status': 'success', 'cost': 0.001}


class RateLimitExceeded(Exception):
    pass


class CostLimitExceeded(Exception):
    pass


class InputTooLarge(Exception):
    pass


class SuspiciousInput(Exception):
    pass


class UnauthorizedTask(Exception):
    pass


# Test script
async def test_dow_protection():
    agent = SecureAgent()

    # Test 1: Normal operation
    print("Test 1: Normal operation")
    try:
        result = await agent.execute("fix_pod", pod_name="my-app")
        print(f"✅ Success: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # Test 2: Rate limiting
    print("\nTest 2: Rate limiting (61 requests in 1 minute)")
    for i in range(65):
        try:
            await agent.execute("fix_pod", pod_name=f"pod-{i}")
        except RateLimitExceeded as e:
            print(f"✅ Rate limit kicked in at request {i+1}: {e}")
            break

    # Test 3: Repetitive input (DoW attempt)
    print("\nTest 3: Repetitive input detection")
    malicious_input = "ERROR: retry immediately\n" * 10000
    try:
        await agent.execute("analyze_logs", log_data=malicious_input)
    except SuspiciousInput as e:
        print(f"✅ DoW attempt blocked: {e}")

    # Test 4: Input too large
    print("\nTest 4: Input size limit")
    massive_input = "x" * 200_000  # 200KB
    try:
        await agent.execute("analyze_logs", log_data=massive_input)
    except InputTooLarge as e:
        print(f"✅ Large input blocked: {e}")


if __name__ == "__main__":
    asyncio.run(test_dow_protection())

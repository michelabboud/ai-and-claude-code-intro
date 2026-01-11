"""
Circuit Breaker Pattern for resilient agentic systems.

This module implements the Circuit Breaker pattern to prevent cascading
failures when calling external services or downstream dependencies.

Installation:
    pip install asyncio

Usage:
    from circuit_breaker import CircuitBreaker, CircuitBreakerConfig

    breaker = CircuitBreaker(config=CircuitBreakerConfig(failure_threshold=3))
    result = await breaker.call(my_async_function, arg1, arg2)
"""

import asyncio
from typing import Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation, requests pass through
    OPEN = "open"          # Failing fast, requests rejected immediately
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior"""
    failure_threshold: int = 5  # Failures before opening circuit
    success_threshold: int = 2   # Successes before closing from half-open
    timeout: float = 60.0        # Seconds before trying half-open from open
    expected_exception: type = Exception  # Which exceptions trigger the breaker


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


class CircuitBreaker:
    """
    Circuit Breaker implementation based on Netflix Hystrix patterns.

    Prevents cascading failures by:
    1. Tracking failure rates
    2. Opening circuit after threshold failures
    3. Testing recovery in half-open state
    4. Closing circuit when service recovers
    """

    def __init__(self, config: Optional[CircuitBreakerConfig] = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.last_state_change: datetime = datetime.now()

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to try half-open"""
        if self.last_failure_time is None:
            return False

        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.config.timeout

    def _time_until_retry(self) -> float:
        """Calculate seconds until half-open attempt"""
        if self.last_failure_time is None:
            return 0.0

        elapsed = datetime.now() - self.last_failure_time
        remaining = self.config.timeout - elapsed.total_seconds()
        return max(0.0, remaining)

    def _transition_to_half_open(self):
        """Transition from OPEN to HALF_OPEN"""
        logger.info("🔌 Circuit breaker transitioning to HALF_OPEN (testing recovery)")
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.last_state_change = datetime.now()

    def _on_success(self):
        """Handle successful call"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1

            if self.success_count >= self.config.success_threshold:
                logger.info("✓ Circuit breaker CLOSING (service recovered)")
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                self.last_state_change = datetime.now()

        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            # Failed in half-open, go back to open
            logger.warning("⚠️ Circuit breaker OPENING (service still failing)")
            self.state = CircuitState.OPEN
            self.failure_count = 0
            self.success_count = 0
            self.last_state_change = datetime.now()

        elif self.state == CircuitState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                logger.warning(f"⚠️ Circuit breaker OPENING ({self.failure_count} failures)")
                self.state = CircuitState.OPEN
                self.success_count = 0
                self.last_state_change = datetime.now()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call function with circuit breaker protection.

        Args:
            func: Async function to call
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            CircuitOpenError: If circuit is open
            Exception: Any exception from func
        """

        # Check if circuit is open
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                raise CircuitOpenError(
                    f"Circuit breaker is OPEN. Retry in {self._time_until_retry():.0f} seconds"
                )

        # Attempt call
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except self.config.expected_exception as e:
            self._on_failure()
            raise

    def get_state(self) -> dict:
        """Get current circuit breaker state"""
        return {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'last_state_change': self.last_state_change.isoformat(),
            'time_until_retry': self._time_until_retry() if self.state == CircuitState.OPEN else 0
        }


# ============================================================
# DEMONSTRATION
# ============================================================

# Simulated flaky service
class FlakyService:
    """Simulates an unreliable external service"""

    def __init__(self, failure_count: int = 5):
        self.calls = 0
        self.failure_count = failure_count

    async def call(self) -> str:
        """Simulate API call that fails N times then succeeds"""
        self.calls += 1

        if self.calls <= self.failure_count:
            raise ConnectionError(f"Service unavailable (call {self.calls})")

        return f"Success! (call {self.calls})"


async def demo_circuit_breaker():
    """Demonstrate circuit breaker protecting against failures"""

    print("=" * 70)
    print("CIRCUIT BREAKER DEMONSTRATION")
    print("=" * 70)
    print()

    service = FlakyService(failure_count=5)
    breaker = CircuitBreaker(
        config=CircuitBreakerConfig(
            failure_threshold=3,
            timeout=5.0
        )
    )

    # Make multiple calls to see circuit breaker in action
    for i in range(10):
        print(f"\nAttempt {i + 1}:")

        try:
            result = await breaker.call(service.call)
            print(f"✓ {result}")

        except CircuitOpenError as e:
            print(f"🔌 {e}")

        except ConnectionError as e:
            print(f"❌ {e}")

        state = breaker.get_state()
        print(f"   State: {state['state'].upper()}, Failures: {state['failure_count']}")

        # Small delay between attempts
        if i < 9:
            await asyncio.sleep(0.5)

    print("\n" + "=" * 70)
    print("Circuit breaker prevented unnecessary calls after failure threshold!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo_circuit_breaker())

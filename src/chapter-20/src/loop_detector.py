"""
Basic loop detection for AI agents.

This module provides simple loop detection mechanisms suitable for
development and testing. For production use, see Chapter 21.
"""

import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class LoopDetectionConfig:
    """Configuration for loop detection behavior"""

    # Maximum times same action can repeat
    max_action_repetitions: int = 3

    # Maximum total iterations before forced stop
    max_total_iterations: int = 20

    # Time window for action repetition (seconds)
    repetition_window: int = 60

    # Enable debug output
    debug: bool = False


@dataclass
class ActionRecord:
    """Record of a single agent action"""

    action: str
    timestamp: float
    metadata: Dict = field(default_factory=dict)


class LoopDetector:
    """
    Simple loop detector for development and debugging.

    Tracks agent actions and raises exceptions when loops are detected.

    Usage:
        detector = LoopDetector(debug=True)

        for action in agent_actions:
            detector.check_action(action)  # Raises LoopDetected if loop found
            perform_action(action)
    """

    def __init__(self, config: Optional[LoopDetectionConfig] = None):
        self.config = config or LoopDetectionConfig()
        self.action_history: List[ActionRecord] = []
        self.iteration_count = 0

    def check_action(self, action: str, metadata: Optional[Dict] = None) -> None:
        """
        Check if action would create a loop.

        Args:
            action: Name of action to perform
            metadata: Optional context (pod name, service, etc.)

        Raises:
            LoopDetected: If action would create a loop
            MaxIterationsExceeded: If too many total iterations
        """
        self.iteration_count += 1
        current_time = time.time()

        # Check 1: Max iterations
        if self.iteration_count > self.config.max_total_iterations:
            raise MaxIterationsExceeded(
                f"Exceeded {self.config.max_total_iterations} total iterations"
            )

        # Check 2: Action repetition
        self._check_repetition(action, current_time)

        # Record action
        record = ActionRecord(
            action=action,
            timestamp=current_time,
            metadata=metadata or {}
        )
        self.action_history.append(record)

        if self.config.debug:
            print(f"[LoopDetector] Action {self.iteration_count}: {action}")
            print(f"[LoopDetector] Recent history: {self._get_recent_actions(5)}")

    def _check_repetition(self, action: str, current_time: float) -> None:
        """Check if action repeats too many times"""
        # Get recent actions within time window
        cutoff_time = current_time - self.config.repetition_window
        recent_actions = [
            record for record in self.action_history
            if record.timestamp >= cutoff_time
        ]

        # Count how many times this action appears
        repetition_count = sum(
            1 for record in recent_actions
            if record.action == action
        )

        if repetition_count >= self.config.max_action_repetitions:
            raise LoopDetected(
                f"Action '{action}' repeated {repetition_count} times "
                f"within {self.config.repetition_window}s window"
            )

    def _get_recent_actions(self, count: int) -> List[str]:
        """Get last N actions for debugging"""
        recent = self.action_history[-count:] if len(self.action_history) >= count else self.action_history
        return [record.action for record in recent]

    def reset(self) -> None:
        """Reset detector state (useful for testing)"""
        self.action_history.clear()
        self.iteration_count = 0

    def get_stats(self) -> Dict:
        """Get detection statistics"""
        return {
            'total_iterations': self.iteration_count,
            'unique_actions': len(set(r.action for r in self.action_history)),
            'total_actions': len(self.action_history),
            'recent_actions': self._get_recent_actions(10)
        }


class LoopDetected(Exception):
    """Raised when a loop is detected"""
    pass


class MaxIterationsExceeded(Exception):
    """Raised when iteration limit is reached"""
    pass


# Example usage
if __name__ == "__main__":
    # Create detector with debug mode
    detector = LoopDetector(
        config=LoopDetectionConfig(
            max_action_repetitions=3,
            max_total_iterations=10,
            debug=True
        )
    )

    try:
        # Simulate agent actions
        detector.check_action("check_logs")
        detector.check_action("check_metrics")
        detector.check_action("restart_pod")
        detector.check_action("check_logs")
        detector.check_action("restart_pod")
        detector.check_action("restart_pod")
        detector.check_action("restart_pod")  # This will raise LoopDetected

    except LoopDetected as e:
        print(f"\n❌ Loop detected: {e}")
        print(f"Stats: {detector.get_stats()}")

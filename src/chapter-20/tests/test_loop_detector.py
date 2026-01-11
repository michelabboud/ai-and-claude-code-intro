"""
Unit tests for loop detector.
"""

import pytest
import time
from src.loop_detector import (
    LoopDetector,
    LoopDetectionConfig,
    LoopDetected,
    MaxIterationsExceeded
)


def test_detects_exact_repetition():
    """Test that detector raises after max repetitions"""
    detector = LoopDetector(
        config=LoopDetectionConfig(max_action_repetitions=3)
    )

    detector.check_action("restart_pod")
    detector.check_action("restart_pod")

    with pytest.raises(LoopDetected):
        detector.check_action("restart_pod")  # 3rd time should raise


def test_allows_different_actions():
    """Test that different actions don't trigger detection"""
    detector = LoopDetector()

    detector.check_action("check_logs")
    detector.check_action("check_metrics")
    detector.check_action("restart_pod")

    # Should not raise - all different actions
    assert detector.iteration_count == 3


def test_max_iterations_exceeded():
    """Test that max iterations limit works"""
    detector = LoopDetector(
        config=LoopDetectionConfig(max_total_iterations=5)
    )

    for i in range(5):
        detector.check_action(f"action_{i}")

    with pytest.raises(MaxIterationsExceeded):
        detector.check_action("action_6")


def test_time_window():
    """Test that repetition window works"""
    detector = LoopDetector(
        config=LoopDetectionConfig(
            max_action_repetitions=3,
            repetition_window=1  # 1 second window
        )
    )

    # First 2 within window
    detector.check_action("restart_pod")
    detector.check_action("restart_pod")

    # Wait for window to expire
    time.sleep(1.1)

    # This should be OK (old actions expired)
    detector.check_action("restart_pod")
    detector.check_action("restart_pod")


def test_get_stats():
    """Test statistics tracking"""
    detector = LoopDetector()

    detector.check_action("action_a")
    detector.check_action("action_b")
    detector.check_action("action_a")

    stats = detector.get_stats()

    assert stats['total_iterations'] == 3
    assert stats['unique_actions'] == 2
    assert stats['total_actions'] == 3
    assert 'action_a' in stats['recent_actions']
    assert 'action_b' in stats['recent_actions']


def test_reset():
    """Test that reset clears state"""
    detector = LoopDetector()

    detector.check_action("action_a")
    detector.check_action("action_b")

    detector.reset()

    assert detector.iteration_count == 0
    assert len(detector.action_history) == 0


def test_metadata_tracking():
    """Test that metadata is stored"""
    detector = LoopDetector()

    metadata = {'pod': 'my-app', 'namespace': 'production'}
    detector.check_action("restart_pod", metadata=metadata)

    assert len(detector.action_history) == 1
    assert detector.action_history[0].metadata == metadata


def test_debug_mode():
    """Test debug output (visual check)"""
    detector = LoopDetector(
        config=LoopDetectionConfig(debug=True)
    )

    print("\n--- Debug Mode Test ---")
    detector.check_action("test_action_1")
    detector.check_action("test_action_2")
    print("--- End Debug Mode Test ---\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Example of the same agent WITH loop detection.
This demonstrates proper safeguards.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.loop_detector import LoopDetector, LoopDetectionConfig, LoopDetected, MaxIterationsExceeded


async def check_pod_status(pod_name: str) -> str:
    """Simulate checking pod status"""
    await asyncio.sleep(0.1)
    return "CrashLoopBackOff"


async def restart_pod(pod_name: str) -> None:
    """Simulate pod restart"""
    print(f"🔄 Restarting pod: {pod_name}")
    await asyncio.sleep(0.5)


async def alert_humans(message: str, context: dict) -> None:
    """Simulate alerting on-call engineer"""
    print(f"\n🚨 ALERT TO HUMANS: {message}")
    print(f"   Context: {context}")


async def fix_pod_with_detection(pod_name: str):
    """
    ✅ GOOD: Same logic but with loop detection.

    Agent will detect it's stuck and escalate to humans instead
    of running indefinitely.
    """
    print(f"Starting agent for pod: {pod_name}\n")

    # Create loop detector
    detector = LoopDetector(
        config=LoopDetectionConfig(
            max_action_repetitions=3,
            max_total_iterations=10,
            debug=True
        )
    )

    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\nIteration {iteration}")

            # Check action BEFORE performing it
            detector.check_action("check_pod_status", metadata={'pod': pod_name})
            status = await check_pod_status(pod_name)
            print(f"  Status: {status}")

            if status == "CrashLoopBackOff":
                # Check action BEFORE performing it
                detector.check_action("restart_pod", metadata={'pod': pod_name})
                await restart_pod(pod_name)
                await asyncio.sleep(2)

                # Check again
                detector.check_action("check_pod_status", metadata={'pod': pod_name})
                new_status = await check_pod_status(pod_name)

                if new_status == "Running":
                    print("✅ Pod is now running!")
                    break
                else:
                    print("  Still failing, will retry...")

            elif status == "Running":
                print("✅ Pod is running!")
                break

    except LoopDetected as e:
        print(f"\n❌ Loop detected: {e}")
        print(f"\nAgent stats: {detector.get_stats()}")

        # Escalate to humans instead of continuing
        await alert_humans(
            "Agent stuck in loop while fixing pod",
            {
                'pod': pod_name,
                'stats': detector.get_stats(),
                'error': str(e)
            }
        )

        print("\n✅ Agent stopped safely and alerted humans")

    except MaxIterationsExceeded as e:
        print(f"\n⚠️  Max iterations exceeded: {e}")
        print(f"\nAgent stats: {detector.get_stats()}")

        await alert_humans(
            "Agent exceeded max iterations",
            {
                'pod': pod_name,
                'stats': detector.get_stats()
            }
        )

        print("\n✅ Agent stopped safely after iteration limit")


if __name__ == "__main__":
    print("="*60)
    print("DEMO: Agent WITH loop detection")
    print("="*60 + "\n")

    asyncio.run(fix_pod_with_detection("my-app-pod"))

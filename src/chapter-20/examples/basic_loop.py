"""
Example of an agent with an infinite loop (for educational purposes).
This demonstrates what NOT to do.
"""

import asyncio


async def check_pod_status(pod_name: str) -> str:
    """Simulate checking pod status"""
    await asyncio.sleep(0.1)
    # Always return failing status (simulates unfixable issue)
    return "CrashLoopBackOff"


async def restart_pod(pod_name: str) -> None:
    """Simulate pod restart"""
    print(f"🔄 Restarting pod: {pod_name}")
    await asyncio.sleep(0.5)


async def fix_pod_without_detection(pod_name: str):
    """
    ❌ BAD: This will loop forever!

    Problem: Pod is crashing due to missing ConfigMap, which restart
    cannot fix. Agent will retry indefinitely.
    """
    print(f"Starting agent for pod: {pod_name}\n")

    iteration = 0
    while True:
        iteration += 1
        print(f"Iteration {iteration}")

        status = await check_pod_status(pod_name)
        print(f"  Status: {status}")

        if status == "CrashLoopBackOff":
            await restart_pod(pod_name)
            await asyncio.sleep(2)

            # Check again
            new_status = await check_pod_status(pod_name)
            if new_status == "Running":
                print("✅ Pod is now running!")
                break
            else:
                print("  Still failing, retrying...\n")
                # Infinite loop! No escape condition!


if __name__ == "__main__":
    print("="*60)
    print("DEMO: Agent without loop detection (will run forever)")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")

    try:
        asyncio.run(fix_pod_without_detection("my-app-pod"))
    except KeyboardInterrupt:
        print("\n\n⚠️  Agent stopped manually. In production, this would run")
        print("   indefinitely, racking up costs!")

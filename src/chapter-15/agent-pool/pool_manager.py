#!/usr/bin/env python3
"""
Chapter 15: Multi-Agent Orchestration - Fundamentals
Agent Pool Management

Demonstrates task delegation and load balancing across agent pools.
Manages agent lifecycle, task queuing, and performance tracking.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Usage:
    from pool_manager import AgentPool, Agent

    # Create pool with max 10 agents
    pool = AgentPool(max_agents=10)

    # Assign tasks
    task = {'id': 'task-001', 'type': 'security_audit', 'required_model': 'sonnet'}
    agent = pool.assign_task(task)

    # Complete task
    pool.complete_task(agent.id, task_time=5.2)

    # Get pool statistics
    stats = pool.get_statistics()
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import time
from datetime import datetime


class AgentStatus(Enum):
    """Agent operational status."""
    IDLE = "idle"
    BUSY = "busy"
    FAILED = "failed"


@dataclass
class Agent:
    """
    Represents a single agent in the pool.

    Attributes:
        id: Unique agent identifier
        model: AI model type (haiku, sonnet, opus)
        status: Current status (idle, busy, failed)
        current_task: ID of task currently being processed
        tasks_completed: Total number of completed tasks
        tasks_failed: Total number of failed tasks
        avg_task_time: Rolling average task completion time (seconds)
        created_at: Timestamp when agent was spawned
    """
    id: str
    model: str
    status: AgentStatus
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_task_time: float = 0.0
    created_at: float = field(default_factory=time.time)

    def __repr__(self):
        return f"Agent({self.id}, {self.model}, {self.status.value}, completed={self.tasks_completed})"


class AgentPool:
    """
    Manages a pool of AI agents for task processing.

    Features:
    - Dynamic agent spawning up to max limit
    - Task queueing when all agents busy
    - Load balancing based on agent performance
    - Performance tracking (completion time, success rate)
    - Automatic agent cleanup (failed agents)
    """

    def __init__(self, max_agents: int = 10):
        """
        Initialize agent pool.

        Args:
            max_agents: Maximum number of concurrent agents
        """
        self.max_agents = max_agents
        self.agents: List[Agent] = []
        self.task_queue: List[Dict] = []
        self.completed_tasks: int = 0
        self.failed_tasks: int = 0

    def get_idle_agent(self, required_model: str = "sonnet") -> Optional[Agent]:
        """
        Get an idle agent of specified model type.

        Args:
            required_model: Preferred AI model (haiku, sonnet, opus)

        Returns:
            Idle agent or None if none available
        """
        for agent in self.agents:
            if agent.status == AgentStatus.IDLE and agent.model == required_model:
                return agent
        return None

    def spawn_agent(self, model: str = "sonnet") -> Optional[Agent]:
        """
        Spawn a new agent if under pool limit.

        Args:
            model: AI model type for the new agent

        Returns:
            Newly created agent or None if pool is full
        """
        if len(self.agents) >= self.max_agents:
            print(f"[AgentPool] Cannot spawn agent: pool at maximum ({self.max_agents})")
            return None

        agent = Agent(
            id=f"agent-{len(self.agents):03d}",
            model=model,
            status=AgentStatus.IDLE
        )

        self.agents.append(agent)
        print(f"[AgentPool] Spawned {agent.id} (model: {model})")

        return agent

    def assign_task(self, task: Dict) -> Optional[Agent]:
        """
        Assign task to an available agent or queue it.

        Decision logic:
        1. Try to get idle agent of required model
        2. If none available, try to spawn new agent
        3. If pool is full, queue the task

        Args:
            task: Task dictionary with 'id', 'type', 'required_model'

        Returns:
            Agent assigned to task, or None if task was queued
        """
        required_model = task.get('required_model', 'sonnet')

        # Try to get idle agent
        agent = self.get_idle_agent(required_model)

        if agent:
            agent.status = AgentStatus.BUSY
            agent.current_task = task['id']
            print(f"[AgentPool] Assigned {task['id']} to {agent.id}")
            return agent

        # Try to spawn new agent
        if len(self.agents) < self.max_agents:
            agent = self.spawn_agent(required_model)
            if agent:
                agent.status = AgentStatus.BUSY
                agent.current_task = task['id']
                print(f"[AgentPool] Assigned {task['id']} to new {agent.id}")
                return agent

        # Queue the task
        self.task_queue.append(task)
        print(f"[AgentPool] Queued {task['id']} (pool busy)")
        return None

    def complete_task(self, agent_id: str, task_time: float, success: bool = True):
        """
        Mark agent's current task as completed.

        Args:
            agent_id: ID of agent that completed the task
            task_time: Time taken to complete task (seconds)
            success: Whether task succeeded or failed
        """
        for agent in self.agents:
            if agent.id == agent_id:
                # Update agent stats
                if success:
                    agent.tasks_completed += 1
                    self.completed_tasks += 1

                    # Update rolling average task time
                    agent.avg_task_time = (
                        (agent.avg_task_time * (agent.tasks_completed - 1) + task_time)
                        / agent.tasks_completed
                    )

                    print(f"[AgentPool] {agent_id} completed task in {task_time:.1f}s "
                          f"(avg: {agent.avg_task_time:.1f}s)")
                else:
                    agent.tasks_failed += 1
                    self.failed_tasks += 1
                    print(f"[AgentPool] {agent_id} failed task")

                # Mark agent as idle
                agent.status = AgentStatus.IDLE
                agent.current_task = None

                # Process queued tasks
                if self.task_queue:
                    next_task = self.task_queue.pop(0)
                    self.assign_task(next_task)
                    print(f"[AgentPool] Assigned queued task {next_task['id']} to {agent_id}")

                break

    def fail_agent(self, agent_id: str):
        """
        Mark agent as failed and remove from pool.

        Args:
            agent_id: ID of failed agent
        """
        self.agents = [a for a in self.agents if a.id != agent_id]
        print(f"[AgentPool] Removed failed agent {agent_id}")

        # Try to spawn replacement
        if self.task_queue:
            next_task = self.task_queue.pop(0)
            self.assign_task(next_task)

    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """
        Get agent by ID.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent or None if not found
        """
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None

    def get_statistics(self) -> Dict:
        """
        Get pool performance statistics.

        Returns:
            Dictionary with pool metrics
        """
        idle_agents = [a for a in self.agents if a.status == AgentStatus.IDLE]
        busy_agents = [a for a in self.agents if a.status == AgentStatus.BUSY]
        failed_agents = [a for a in self.agents if a.status == AgentStatus.FAILED]

        total_tasks = self.completed_tasks + self.failed_tasks
        success_rate = (
            (self.completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        )

        return {
            'total_agents': len(self.agents),
            'idle_agents': len(idle_agents),
            'busy_agents': len(busy_agents),
            'failed_agents': len(failed_agents),
            'queued_tasks': len(self.task_queue),
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'success_rate': f"{success_rate:.1f}%",
            'avg_task_time': sum(a.avg_task_time for a in self.agents) / len(self.agents) if self.agents else 0
        }

    def print_status(self):
        """Print current pool status."""
        stats = self.get_statistics()

        print("\n=== Agent Pool Status ===")
        print(f"Agents: {stats['total_agents']}/{self.max_agents}")
        print(f"  Idle: {stats['idle_agents']}")
        print(f"  Busy: {stats['busy_agents']}")
        print(f"  Failed: {stats['failed_agents']}")
        print(f"Queued tasks: {stats['queued_tasks']}")
        print(f"Completed: {stats['completed_tasks']}")
        print(f"Failed: {stats['failed_tasks']}")
        print(f"Success rate: {stats['success_rate']}")
        print(f"Avg task time: {stats['avg_task_time']:.1f}s")
        print()


def smart_load_balance(tasks: List[Dict], agent_pool: AgentPool) -> List[tuple]:
    """
    Distribute tasks based on agent performance history.

    Strategy:
    - Sort agents by average task time (fastest first)
    - Assign tasks to fastest agents first
    - Queue remaining tasks

    Args:
        tasks: List of task dictionaries
        agent_pool: AgentPool instance

    Returns:
        List of (task_id, agent_id) tuples for assignments
    """
    # Get available idle agents
    available_agents = [
        a for a in agent_pool.agents
        if a.status == AgentStatus.IDLE
    ]

    # Sort by performance (fastest first)
    available_agents.sort(key=lambda a: a.avg_task_time if a.avg_task_time > 0 else float('inf'))

    assignments = []

    # Assign tasks to fastest agents first
    for task, agent in zip(tasks, available_agents):
        agent_pool.assign_task(task)
        assignments.append((task['id'], agent.id))

    # Queue remaining tasks
    for task in tasks[len(available_agents):]:
        agent_pool.task_queue.append(task)
        print(f"[LoadBalancer] Queued {task['id']} (no agents available)")

    return assignments


# Example usage
if __name__ == '__main__':
    import random

    # Create pool
    pool = AgentPool(max_agents=5)

    # Create sample tasks
    tasks = [
        {'id': f'task-{i:03d}', 'type': 'security_audit', 'required_model': 'sonnet'}
        for i in range(10)
    ]

    print("[Demo] Assigning 10 tasks to pool with max 5 agents...\n")

    # Assign all tasks
    for task in tasks:
        pool.assign_task(task)

    pool.print_status()

    # Simulate task completion
    print("[Demo] Simulating task completion...\n")

    for i in range(10):
        # Random agent completes task
        busy_agents = [a for a in pool.agents if a.status == AgentStatus.BUSY]

        if busy_agents:
            agent = random.choice(busy_agents)
            task_time = random.uniform(1.0, 5.0)
            success = random.random() > 0.1  # 90% success rate

            pool.complete_task(agent.id, task_time, success)
            time.sleep(0.5)

    pool.print_status()

    print("[Demo] Load balancing example:\n")

    # Create more tasks
    new_tasks = [
        {'id': f'task-{i:03d}', 'type': 'performance_check', 'required_model': 'haiku'}
        for i in range(20, 25)
    ]

    assignments = smart_load_balance(new_tasks, pool)

    print(f"\nAssignments: {assignments}")
    pool.print_status()

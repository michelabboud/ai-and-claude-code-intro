#!/usr/bin/env python3
"""
Chapter 15: Multi-Agent Orchestration - Fundamentals
File-Based Agent Coordination

Demonstrates how agents coordinate via JSON files on shared filesystem.
Simple, lightweight approach suitable for local development and CI/CD pipelines.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Usage:
    # Terminal 1: Coordinator creates tasks
    python file_coordinator.py --mode coordinator --task-count 5

    # Terminal 2-4: Agents claim and process tasks
    python file_coordinator.py --mode agent --agent-id security-001
    python file_coordinator.py --mode agent --agent-id performance-001
    python file_coordinator.py --mode agent --agent-id cost-001
"""

import os
import json
import time
import argparse
import fcntl
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List


class FileCoordinator:
    """
    File-based multi-agent coordinator.

    Uses JSON files on shared filesystem for coordination.
    Suitable for:
    - Local development
    - CI/CD pipelines (GitHub Actions, GitLab CI)
    - Docker Compose environments
    - Simple deployments without database

    File structure:
        findings_dir/
        ├── tasks/
        │   ├── task-001.json (pending/in_progress/completed)
        │   └── task-002.json
        ├── findings/
        │   ├── security-001.json
        │   └── performance-001.json
        └── .locks/
            └── task-001.lock (file lock for atomic claims)
    """

    def __init__(self, findings_dir: str = '/tmp/agent-findings'):
        """
        Initialize file coordinator.

        Args:
            findings_dir: Root directory for coordination files
        """
        self.findings_dir = Path(findings_dir)
        self.tasks_dir = self.findings_dir / 'tasks'
        self.findings_subdir = self.findings_dir / 'findings'
        self.locks_dir = self.findings_dir / '.locks'

        # Create directories
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.findings_subdir.mkdir(parents=True, exist_ok=True)
        self.locks_dir.mkdir(parents=True, exist_ok=True)

    def create_task(self, task_id: str, task_type: str, task_data: Dict) -> bool:
        """
        Create a new task file.

        Args:
            task_id: Unique identifier for this task
            task_type: Type of task (e.g., "security_audit")
            task_data: Dictionary containing task details

        Returns:
            True if task created successfully
        """
        task_file = self.tasks_dir / f"{task_id}.json"

        # Don't overwrite existing tasks
        if task_file.exists():
            print(f"[Coordinator] Task already exists: {task_id}")
            return False

        task = {
            'task_id': task_id,
            'task_type': task_type,
            'status': 'pending',
            'task_data': task_data,
            'created_at': datetime.utcnow().isoformat(),
            'assigned_to': None,
            'claimed_at': None,
            'completed_at': None,
            'result': None
        }

        try:
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

            print(f"[Coordinator] Created task: {task_id} ({task_type})")
            return True

        except Exception as e:
            print(f"[Coordinator] Failed to create task: {str(e)}")
            return False

    def claim_task(self, agent_id: str, task_types: List[str] = None) -> Optional[Dict]:
        """
        Agent claims an available task (atomic using file locking).

        Args:
            agent_id: Unique identifier for the claiming agent
            task_types: Optional list of task types this agent can handle

        Returns:
            Task dictionary if successfully claimed, None otherwise
        """
        # Get all pending tasks
        for task_file in sorted(self.tasks_dir.glob('*.json')):
            lock_file = self.locks_dir / f"{task_file.stem}.lock"

            try:
                # Try to acquire exclusive lock
                with open(lock_file, 'w') as lock_f:
                    fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

                    # Read task
                    with open(task_file, 'r') as f:
                        task = json.load(f)

                    # Check if task is claimable
                    if task['status'] != 'pending':
                        continue

                    if task_types and task['task_type'] not in task_types:
                        continue

                    # Claim the task
                    task['status'] = 'in_progress'
                    task['assigned_to'] = agent_id
                    task['claimed_at'] = datetime.utcnow().isoformat()

                    # Write back
                    with open(task_file, 'w') as f:
                        json.dump(task, f, indent=2)

                    print(f"[{agent_id}] Claimed task: {task['task_id']}")
                    return task

            except (BlockingIOError, IOError):
                # Lock is held by another agent, try next task
                continue
            except Exception as e:
                print(f"[{agent_id}] Error claiming task: {str(e)}")
                continue

        return None

    def submit_finding(self, task_id: str, agent_id: str, finding: Dict) -> bool:
        """
        Agent submits a finding to its findings file.

        Args:
            task_id: ID of the task this finding relates to
            agent_id: ID of the agent submitting the finding
            finding: Dictionary containing finding details

        Returns:
            True if finding submitted successfully
        """
        findings_file = self.findings_subdir / f"{agent_id}.json"

        # Load existing findings or create new
        if findings_file.exists():
            with open(findings_file, 'r') as f:
                data = json.load(f)
        else:
            data = {
                'agent_id': agent_id,
                'findings': []
            }

        # Add new finding
        finding_entry = {
            'task_id': task_id,
            'timestamp': datetime.utcnow().isoformat(),
            **finding
        }

        data['findings'].append(finding_entry)

        try:
            with open(findings_file, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"[{agent_id}] Submitted finding: {finding['title']}")
            return True

        except Exception as e:
            print(f"[{agent_id}] Failed to submit finding: {str(e)}")
            return False

    def complete_task(self, task_id: str, agent_id: str, result: Dict) -> bool:
        """
        Mark task as completed.

        Args:
            task_id: ID of the task being completed
            agent_id: ID of the agent completing the task
            result: Dictionary containing task results

        Returns:
            True if task marked as completed successfully
        """
        task_file = self.tasks_dir / f"{task_id}.json"

        if not task_file.exists():
            print(f"[{agent_id}] Task not found: {task_id}")
            return False

        try:
            with open(task_file, 'r') as f:
                task = json.load(f)

            # Verify agent owns this task
            if task['assigned_to'] != agent_id:
                print(f"[{agent_id}] Not assigned to this task: {task_id}")
                return False

            # Mark complete
            task['status'] = 'completed'
            task['result'] = result
            task['completed_at'] = datetime.utcnow().isoformat()

            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)

            print(f"[{agent_id}] Completed task: {task_id}")
            return True

        except Exception as e:
            print(f"[{agent_id}] Failed to complete task: {str(e)}")
            return False

    def get_all_findings(self, task_id: str = None) -> List[Dict]:
        """
        Read all agent findings.

        Args:
            task_id: Optional task ID to filter by

        Returns:
            List of all findings from all agents
        """
        all_findings = []

        for findings_file in self.findings_subdir.glob('*.json'):
            try:
                with open(findings_file, 'r') as f:
                    data = json.load(f)

                for finding in data.get('findings', []):
                    if task_id and finding.get('task_id') != task_id:
                        continue
                    all_findings.append({
                        'agent_id': data['agent_id'],
                        **finding
                    })

            except Exception as e:
                print(f"Warning: Failed to read {findings_file}: {str(e)}")

        return all_findings

    def wait_for_agents(self, expected_agents: set, timeout: int = 300) -> bool:
        """
        Wait for all expected agents to report findings.

        Args:
            expected_agents: Set of agent IDs to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            True if all agents reported, False if timeout
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            completed = {
                f.stem for f in self.findings_subdir.glob('*.json')
            }

            if expected_agents.issubset(completed):
                return True

            time.sleep(1)

        return False

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        Get current status of a task.

        Args:
            task_id: Task ID to check

        Returns:
            Task dictionary or None if not found
        """
        task_file = self.tasks_dir / f"{task_id}.json"

        if not task_file.exists():
            return None

        try:
            with open(task_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading task: {str(e)}")
            return None

    def get_all_tasks(self, status: str = None) -> List[Dict]:
        """
        Get all tasks, optionally filtered by status.

        Args:
            status: Optional status filter (pending/in_progress/completed)

        Returns:
            List of task dictionaries
        """
        tasks = []

        for task_file in self.tasks_dir.glob('*.json'):
            try:
                with open(task_file, 'r') as f:
                    task = json.load(f)

                if status and task['status'] != status:
                    continue

                tasks.append(task)

            except Exception as e:
                print(f"Warning: Failed to read {task_file}: {str(e)}")

        return tasks

    def cleanup(self):
        """Remove all coordination files (for testing)."""
        import shutil
        if self.findings_dir.exists():
            shutil.rmtree(self.findings_dir)
        print(f"Cleaned up {self.findings_dir}")


# Example: Coordinator Mode
def run_coordinator(findings_dir: str, task_count: int = 5):
    """
    Coordinator creates tasks and waits for agents to complete them.
    """
    coordinator = FileCoordinator(findings_dir)

    # Clean up any old files
    coordinator.cleanup()
    coordinator.__init__(findings_dir)

    print(f"\n[Coordinator] Creating {task_count} tasks...\n")

    task_types = ['security_audit', 'performance_check', 'cost_analysis']

    for i in range(task_count):
        task_id = f"task-{i+1:03d}"
        task_type = task_types[i % len(task_types)]

        coordinator.create_task(task_id, task_type, {
            'target': f'service-{i+1}',
            'priority': 'high' if i < 2 else 'medium',
            'deadline': '2026-01-11T18:00:00Z'
        })

    # Wait for all tasks to complete
    print(f"\n[Coordinator] Waiting for agents to complete tasks...\n")

    timeout = 60
    start_time = time.time()

    while time.time() - start_time < timeout:
        tasks = coordinator.get_all_tasks()
        completed = sum(1 for t in tasks if t['status'] == 'completed')

        if completed == task_count:
            break

        time.sleep(2)

    # Display results
    print(f"\n[Coordinator] === RESULTS ===")

    tasks = coordinator.get_all_tasks()
    completed = sum(1 for t in tasks if t['status'] == 'completed')

    print(f"Tasks completed: {completed}/{task_count}")

    # Get all findings
    findings = coordinator.get_all_findings()

    by_severity = {}
    for finding in findings:
        sev = finding.get('severity', 'unknown')
        by_severity[sev] = by_severity.get(sev, 0) + 1

    print(f"Total findings: {len(findings)}")
    print(f"By severity: {by_severity}")


# Example: Agent Mode
def run_agent(findings_dir: str, agent_id: str):
    """
    Agent claims and processes tasks.
    """
    coordinator = FileCoordinator(findings_dir)

    print(f"[{agent_id}] Started, waiting for tasks...\n")

    tasks_processed = 0
    max_tasks = 5
    timeout = 30
    start_time = time.time()

    while tasks_processed < max_tasks and (time.time() - start_time) < timeout:
        # Try to claim a task
        task = coordinator.claim_task(agent_id)

        if task:
            # Simulate analysis work
            time.sleep(2)

            # Submit findings
            coordinator.submit_finding(task['task_id'], agent_id, {
                'type': f"{task['task_type']}_result",
                'severity': 'medium',
                'title': f"Analysis of {task['task_data']['target']}",
                'description': f"Agent {agent_id} analyzed the target",
                'metadata': {
                    'processing_time': 2.0,
                    'confidence': 0.85
                }
            })

            # Mark task complete
            coordinator.complete_task(task['task_id'], agent_id, {
                'status': 'success',
                'findings_count': 1
            })

            tasks_processed += 1
        else:
            # No tasks available, wait a bit
            time.sleep(1)

    print(f"\n[{agent_id}] Processed {tasks_processed} tasks, shutting down")


def main():
    """Main entry point with mode selection."""
    parser = argparse.ArgumentParser(
        description='File-based multi-agent coordination demo'
    )
    parser.add_argument(
        '--mode',
        choices=['coordinator', 'agent'],
        required=True,
        help='Coordinator creates tasks, agents process them'
    )
    parser.add_argument(
        '--agent-id',
        help='Agent identifier (required for agent mode)',
        default='agent-001'
    )
    parser.add_argument(
        '--task-count',
        type=int,
        default=5,
        help='Number of tasks to create (coordinator mode)'
    )
    parser.add_argument(
        '--findings-dir',
        default='/tmp/agent-findings',
        help='Directory for coordination files'
    )

    args = parser.parse_args()

    if args.mode == 'coordinator':
        run_coordinator(args.findings_dir, args.task_count)
    elif args.mode == 'agent':
        run_agent(args.findings_dir, args.agent_id)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Chapter 15: Multi-Agent Orchestration - Fundamentals
Database-Backed Agent Coordination

Demonstrates how agents coordinate via shared PostgreSQL database.
Agents claim tasks, submit findings, and coordinator synthesizes results.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Requirements:
    pip install psycopg2-binary

Setup:
    # Create database
    createdb agent_coordination

    # Initialize schema
    python database_coordinator.py --init-db

Usage:
    # Terminal 1: Coordinator creates tasks
    python database_coordinator.py --mode coordinator --task-count 5

    # Terminal 2-4: Agents claim and process tasks
    python database_coordinator.py --mode agent --agent-id security-001
    python database_coordinator.py --mode agent --agent-id performance-001
    python database_coordinator.py --mode agent --agent-id cost-001
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Optional, List


class DatabaseCoordinator:
    """
    Database-backed multi-agent coordinator.
    Uses PostgreSQL for task queuing and finding storage.
    """

    def __init__(self, db_config: Dict):
        """
        Initialize database connection pool.

        Args:
            db_config: PostgreSQL connection parameters
        """
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            host=db_config.get('host', 'localhost'),
            port=db_config.get('port', 5432),
            database=db_config.get('database', 'agent_coordination'),
            user=db_config.get('user', 'postgres'),
            password=db_config.get('password', '')
        )

    def get_connection(self):
        """Get connection from pool."""
        return self.connection_pool.getconn()

    def return_connection(self, conn):
        """Return connection to pool."""
        self.connection_pool.putconn(conn)

    def init_schema(self):
        """
        Initialize database schema for agent coordination.
        Creates agent_tasks and agent_findings tables.
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Agent tasks table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS agent_tasks (
                        id SERIAL PRIMARY KEY,
                        task_id VARCHAR(100) UNIQUE NOT NULL,
                        task_type VARCHAR(50) NOT NULL,
                        assigned_to VARCHAR(100),
                        status VARCHAR(20) DEFAULT 'pending',
                        task_data JSONB NOT NULL,
                        result JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        claimed_at TIMESTAMP,
                        completed_at TIMESTAMP,
                        INDEX idx_status (status),
                        INDEX idx_created (created_at DESC)
                    )
                """)

                # Agent findings table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS agent_findings (
                        id SERIAL PRIMARY KEY,
                        task_id VARCHAR(100) NOT NULL,
                        agent_id VARCHAR(100) NOT NULL,
                        finding_type VARCHAR(50) NOT NULL,
                        severity VARCHAR(20) NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_task_findings (task_id),
                        INDEX idx_severity (severity),
                        INDEX idx_created (created_at DESC),
                        FOREIGN KEY (task_id) REFERENCES agent_tasks(task_id)
                    )
                """)

                conn.commit()
                print("✓ Database schema initialized")

        except Exception as e:
            conn.rollback()
            print(f"✗ Schema initialization failed: {str(e)}")
            raise
        finally:
            self.return_connection(conn)

    def create_task(self, task_id: str, task_type: str, task_data: Dict) -> bool:
        """
        Create a new task for agents to pick up.

        Args:
            task_id: Unique identifier for this task
            task_type: Type of task (e.g., "security_audit", "performance_check")
            task_data: Dictionary containing task details

        Returns:
            True if task created successfully
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO agent_tasks (task_id, task_type, task_data)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (task_id) DO NOTHING
                """, (task_id, task_type, json.dumps(task_data)))

                conn.commit()
                print(f"[Coordinator] Created task: {task_id} ({task_type})")
                return True

        except Exception as e:
            conn.rollback()
            print(f"[Coordinator] Failed to create task: {str(e)}")
            return False
        finally:
            self.return_connection(conn)

    def claim_task(self, agent_id: str, task_types: List[str] = None) -> Optional[Dict]:
        """
        Agent claims an available task (atomic operation using SELECT FOR UPDATE SKIP LOCKED).

        Args:
            agent_id: Unique identifier for the claiming agent
            task_types: Optional list of task types this agent can handle

        Returns:
            Task dictionary if successfully claimed, None otherwise
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Build WHERE clause
                where_clause = "WHERE status = 'pending'"
                params = [agent_id]

                if task_types:
                    where_clause += " AND task_type = ANY(%s)"
                    params.append(task_types)

                cur.execute(f"""
                    UPDATE agent_tasks
                    SET assigned_to = %s,
                        status = 'in_progress',
                        claimed_at = CURRENT_TIMESTAMP
                    WHERE id = (
                        SELECT id FROM agent_tasks
                        {where_clause}
                        ORDER BY created_at ASC
                        LIMIT 1
                        FOR UPDATE SKIP LOCKED
                    )
                    RETURNING *
                """, params)

                task = cur.fetchone()
                conn.commit()

                if task:
                    task_dict = dict(task)
                    print(f"[{agent_id}] Claimed task: {task_dict['task_id']}")
                    return task_dict
                else:
                    return None

        except Exception as e:
            conn.rollback()
            print(f"[{agent_id}] Failed to claim task: {str(e)}")
            return None
        finally:
            self.return_connection(conn)

    def submit_finding(self, task_id: str, agent_id: str, finding: Dict) -> bool:
        """
        Agent submits an analysis finding.

        Args:
            task_id: ID of the task this finding relates to
            agent_id: ID of the agent submitting the finding
            finding: Dictionary containing finding details

        Returns:
            True if finding submitted successfully
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO agent_findings
                    (task_id, agent_id, finding_type, severity, title, description, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    task_id,
                    agent_id,
                    finding['type'],
                    finding['severity'],
                    finding['title'],
                    finding.get('description', ''),
                    json.dumps(finding.get('metadata', {}))
                ))

                conn.commit()
                print(f"[{agent_id}] Submitted finding: {finding['title']}")
                return True

        except Exception as e:
            conn.rollback()
            print(f"[{agent_id}] Failed to submit finding: {str(e)}")
            return False
        finally:
            self.return_connection(conn)

    def complete_task(self, task_id: str, agent_id: str, result: Dict) -> bool:
        """
        Mark task as completed with results.

        Args:
            task_id: ID of the task being completed
            agent_id: ID of the agent completing the task
            result: Dictionary containing task results

        Returns:
            True if task marked as completed successfully
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE agent_tasks
                    SET status = 'completed',
                        result = %s,
                        completed_at = CURRENT_TIMESTAMP
                    WHERE task_id = %s AND assigned_to = %s
                """, (json.dumps(result), task_id, agent_id))

                conn.commit()
                print(f"[{agent_id}] Completed task: {task_id}")
                return True

        except Exception as e:
            conn.rollback()
            print(f"[{agent_id}] Failed to complete task: {str(e)}")
            return False
        finally:
            self.return_connection(conn)

    def get_all_findings(self, task_id: str = None) -> List[Dict]:
        """
        Retrieve all findings, optionally filtered by task_id.

        Args:
            task_id: Optional task ID to filter by

        Returns:
            List of finding dictionaries
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if task_id:
                    cur.execute("""
                        SELECT * FROM agent_findings
                        WHERE task_id = %s
                        ORDER BY created_at DESC
                    """, (task_id,))
                else:
                    cur.execute("""
                        SELECT * FROM agent_findings
                        ORDER BY created_at DESC
                    """)

                return [dict(row) for row in cur.fetchall()]

        finally:
            self.return_connection(conn)

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        Get current status of a task.

        Args:
            task_id: Task ID to check

        Returns:
            Task status dictionary or None if not found
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM agent_tasks WHERE task_id = %s
                """, (task_id,))

                row = cur.fetchone()
                return dict(row) if row else None

        finally:
            self.return_connection(conn)


# Example: Coordinator Mode
def run_coordinator(db_config: Dict, task_count: int = 5):
    """
    Coordinator creates tasks and waits for agents to complete them.
    """
    coordinator = DatabaseCoordinator(db_config)

    # Create sample tasks
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

    completed = 0
    timeout = 60  # seconds
    start_time = time.time()

    while completed < task_count and (time.time() - start_time) < timeout:
        # Check completion status
        conn = coordinator.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM agent_tasks WHERE status = 'completed'
                """)
                completed = cur.fetchone()[0]
        finally:
            coordinator.return_connection(conn)

        if completed < task_count:
            time.sleep(2)

    # Display results
    print(f"\n[Coordinator] === RESULTS ===")
    print(f"Tasks completed: {completed}/{task_count}")

    # Get all findings
    findings = coordinator.get_all_findings()

    by_severity = {}
    for finding in findings:
        sev = finding['severity']
        by_severity[sev] = by_severity.get(sev, 0) + 1

    print(f"Total findings: {len(findings)}")
    print(f"By severity: {by_severity}")


# Example: Agent Mode
def run_agent(db_config: Dict, agent_id: str):
    """
    Agent claims and processes tasks.
    """
    coordinator = DatabaseCoordinator(db_config)

    print(f"[{agent_id}] Started, waiting for tasks...\n")

    # Agent processes up to 5 tasks or waits 30 seconds
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
        description='Database-backed multi-agent coordination demo'
    )
    parser.add_argument(
        '--mode',
        choices=['coordinator', 'agent', 'init'],
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
        '--init-db',
        action='store_true',
        help='Initialize database schema'
    )

    args = parser.parse_args()

    # Database configuration
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'agent_coordination',
        'user': 'postgres',
        'password': ''
    }

    coordinator = DatabaseCoordinator(db_config)

    if args.init_db or args.mode == 'init':
        coordinator.init_schema()
        return

    if args.mode == 'coordinator':
        run_coordinator(db_config, args.task_count)
    elif args.mode == 'agent':
        run_agent(db_config, args.agent_id)


if __name__ == '__main__':
    main()

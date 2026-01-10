#!/usr/bin/env python3
"""
Simple Flask API that connects to PostgreSQL
Intentionally has a configuration bug causing crashes

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0
"""

import os
import sys
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# BUG: App looks for DATABASE_URL but docker-compose sets DB_URL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set!", file=sys.stderr)
    print("Cannot connect to database. Exiting...", file=sys.stderr)
    sys.exit(1)  # This causes the crash!

# Test database connection on startup
try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.close()
    print("✅ Database connection successful")
except Exception as e:
    print(f"ERROR: Cannot connect to database: {e}", file=sys.stderr)
    sys.exit(1)


@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Flask API!",
        "status": "running"
    })


@app.route('/health')
def health():
    try:
        # Check database connection
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route('/data')
def get_data():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Database query successful",
            "postgres_version": db_version[0]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask API on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)

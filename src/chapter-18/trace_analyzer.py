#!/usr/bin/env python3
"""
Distributed Trace Analyzer with AI
Analyze Jaeger/Zipkin traces to find performance bottlenecks and suggest optimizations.

Part of Chapter 18: Advanced AIOps
"""

import os
import json
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import logging

import anthropic
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TraceAnalyzer:
    """
    AI-powered distributed trace analyzer for microservices.

    Features:
    - Find performance bottlenecks automatically
    - Suggest specific code optimizations
    - Map service dependencies
    - Detect architectural issues
    """

    def __init__(self, jaeger_host: str = 'localhost:16686',
                 anthropic_api_key: Optional[str] = None):
        self.jaeger_host = jaeger_host

        api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic(api_key=api_key)

    def fetch_traces(self, service: str, min_duration_ms: int = 1000,
                    lookback_hours: int = 1, limit: int = 100) -> List[Dict]:
        """
        Fetch slow traces from Jaeger.

        Args:
            service: Service name to query
            min_duration_ms: Minimum trace duration in milliseconds
            lookback_hours: How far back to search
            limit: Maximum traces to fetch

        Returns:
            List of trace dictionaries
        """
        logger.info(f"Fetching traces for {service} (min duration: {min_duration_ms}ms)")

        # Jaeger query API
        params = {
            'service': service,
            'limit': limit,
            'lookback': f'{lookback_hours}h',
            'minDuration': f"{min_duration_ms}ms"
        }

        try:
            response = requests.get(
                f"http://{self.jaeger_host}/api/traces",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            traces = data.get('data', [])

            logger.info(f"Fetched {len(traces)} traces")
            return traces

        except requests.RequestException as e:
            logger.error(f"Failed to fetch traces: {e}")
            return []

    async def analyze_slow_traces(self, service: str, min_duration_ms: int = 1000) -> Dict:
        """
        Analyze slow traces and identify bottlenecks.

        Args:
            service: Service name
            min_duration_ms: Threshold for "slow" traces

        Returns:
            Dict with analysis and recommendations
        """
        # Fetch traces
        traces = self.fetch_traces(service, min_duration_ms)

        if not traces:
            return {
                'message': 'No slow traces found',
                'service': service
            }

        # Extract performance data
        trace_data = self._extract_trace_data(traces[:10])  # Analyze top 10

        # AI analysis
        analysis = await self._ai_analyze_traces(trace_data)

        return {
            'service': service,
            'slow_traces_count': len(traces),
            'analyzed_sample_size': len(trace_data),
            'analysis': analysis
        }

    def _extract_trace_data(self, traces: List[Dict]) -> List[Dict]:
        """Extract key performance data from traces"""
        trace_data = []

        for trace in traces:
            trace_id = trace.get('traceID')
            spans = trace.get('spans', [])

            # Calculate total duration
            total_duration_us = trace.get('duration', 0)

            # Extract span data
            span_data = []
            for span in spans:
                span_data.append({
                    'service': span.get('process', {}).get('serviceName', 'unknown'),
                    'operation': span.get('operationName', 'unknown'),
                    'duration_ms': span.get('duration', 0) / 1000,  # microseconds to ms
                    'tags': span.get('tags', [])
                })

            trace_data.append({
                'trace_id': trace_id,
                'total_duration_ms': total_duration_us / 1000,
                'spans': span_data
            })

        return trace_data

    async def _ai_analyze_traces(self, traces: List[Dict]) -> Dict:
        """Have AI analyze traces for bottlenecks"""

        prompt = f"""Analyze these slow distributed traces and identify performance bottlenecks.

Traces (showing service call chains and durations):
{json.dumps(traces, indent=2)}

Provide detailed analysis:

1. **Bottleneck Service**: Which service is the primary bottleneck?
2. **Bottleneck Operation**: Which specific operation is slow?
3. **Time Wasted**: How much time (ms) is wasted on average?
4. **Root Cause**: Why is this operation slow? (e.g., N+1 queries, sequential calls, missing cache)
5. **Optimization Suggestions**: List of specific, actionable fixes
6. **Confidence**: High/Medium/Low

Return JSON:
{{
  "bottleneck_service": "...",
  "bottleneck_operation": "...",
  "average_time_wasted_ms": ...,
  "root_cause": "...",
  "optimization_suggestions": [
    "Specific suggestion 1",
    "Specific suggestion 2"
  ],
  "confidence": "High|Medium|Low",
  "evidence": "Brief explanation of evidence"
}}

Be specific and actionable. Return ONLY JSON."""

        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1536,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            analysis = json.loads(response.content[0].text)
            return analysis
        except json.JSONDecodeError:
            logger.error("Failed to parse AI analysis as JSON")
            return {}

    async def suggest_code_optimizations(self, trace_id: str) -> Dict:
        """
        Analyze a specific trace and suggest specific code changes.

        Args:
            trace_id: Jaeger trace ID

        Returns:
            Dict with code-level optimization suggestions
        """
        # Fetch trace detail
        trace = self._fetch_trace_detail(trace_id)

        if not trace:
            return {'error': 'Trace not found'}

        # Extract performance data
        trace_data = self._extract_trace_data([trace])[0]

        # AI generates specific optimization suggestions
        suggestions = await self._generate_code_optimizations(trace_data)

        return {
            'trace_id': trace_id,
            'total_duration_ms': trace_data['total_duration_ms'],
            'optimizations': suggestions
        }

    def _fetch_trace_detail(self, trace_id: str) -> Optional[Dict]:
        """Fetch detailed trace by ID"""
        try:
            response = requests.get(
                f"http://{self.jaeger_host}/api/traces/{trace_id}",
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            traces = data.get('data', [])

            return traces[0] if traces else None

        except requests.RequestException as e:
            logger.error(f"Failed to fetch trace {trace_id}: {e}")
            return None

    async def _generate_code_optimizations(self, trace_data: Dict) -> List[Dict]:
        """AI generates specific, actionable code optimizations"""

        prompt = f"""Analyze this trace and suggest specific code optimizations.

Trace data:
{json.dumps(trace_data, indent=2)}

For EACH bottleneck you find, provide:
1. **Problem**: What's slow and why (be specific)
2. **Specific Fix**: Exact code pattern to implement (with before/after examples)
3. **Expected Improvement**: How much faster (ms or %)
4. **Effort**: Easy/Medium/Hard to implement
5. **Confidence**: High/Medium/Low

Focus on:
- N+1 query problems
- Sequential API calls (that could be parallel)
- Missing caching
- Database query optimization
- Inefficient algorithms

Return JSON array:
[
  {{
    "problem": "...",
    "specific_fix": "... (with code examples)",
    "expected_improvement": "...",
    "effort": "Easy|Medium|Hard",
    "confidence": "High|Medium|Low"
  }},
  ...
]

Be very specific with code examples. Return ONLY JSON array."""

        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            suggestions = json.loads(response.content[0].text)
            return suggestions
        except json.JSONDecodeError:
            logger.error("Failed to parse optimization suggestions")
            return []


class DependencyMapper:
    """
    Auto-discover microservice dependencies from distributed traces.
    """

    def __init__(self, jaeger_host: str = 'localhost:16686',
                 anthropic_api_key: Optional[str] = None):
        self.jaeger_host = jaeger_host

        api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic(api_key=api_key)

    async def map_dependencies(self, service_name: str, lookback_hours: int = 24) -> Dict:
        """
        Build dependency graph for a service.

        Args:
            service_name: Service to analyze
            lookback_hours: How far back to analyze

        Returns:
            Dict with dependency graph and AI analysis
        """
        logger.info(f"Mapping dependencies for {service_name}")

        # Fetch traces
        traces = self._fetch_traces(service_name, lookback_hours)

        if not traces:
            return {
                'service': service_name,
                'error': 'No traces found'
            }

        # Build call graph
        call_graph = self._build_call_graph(traces)

        # AI analyzes dependency graph for issues
        analysis = await self._analyze_dependencies(call_graph)

        return {
            'service': service_name,
            'dependency_graph': call_graph,
            'ai_analysis': analysis
        }

    def _fetch_traces(self, service: str, lookback_hours: int) -> List[Dict]:
        """Fetch traces for dependency analysis"""
        params = {
            'service': service,
            'limit': 200,
            'lookback': f'{lookback_hours}h'
        }

        try:
            response = requests.get(
                f"http://{self.jaeger_host}/api/traces",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            return data.get('data', [])

        except requests.RequestException as e:
            logger.error(f"Failed to fetch traces: {e}")
            return []

    def _build_call_graph(self, traces: List[Dict]) -> Dict:
        """Extract service-to-service call graph from traces"""
        call_graph = {}

        for trace in traces:
            spans = trace.get('spans', [])

            # Build span parent-child relationships
            span_by_id = {span['spanID']: span for span in spans}

            for span in spans:
                service = span.get('process', {}).get('serviceName', 'unknown')

                # Find child spans (dependencies)
                span_id = span['spanID']
                children = [
                    s for s in spans
                    if s.get('references', [{}])[0].get('spanID') == span_id
                ]

                for child in children:
                    child_service = child.get('process', {}).get('serviceName', 'unknown')

                    if service not in call_graph:
                        call_graph[service] = {}

                    if child_service not in call_graph[service]:
                        call_graph[service][child_service] = 0

                    call_graph[service][child_service] += 1

        return call_graph

    async def _analyze_dependencies(self, graph: Dict) -> Dict:
        """AI identifies problematic dependency patterns"""

        prompt = f"""Analyze this microservice dependency graph for architectural issues.

Dependency graph (service -> [dependencies with call counts]):
{json.dumps(graph, indent=2)}

Look for:
1. **Circular dependencies** (A -> B -> A): Services calling each other
2. **Chatty services**: Too many calls between services (>100)
3. **Single points of failure**: One service many others depend on
4. **Excessive fanout**: One service calls too many others (>5)
5. **Unused dependencies**: Services with very few calls (<5)

Provide analysis:
{{
  "issues_found": [
    {{
      "type": "circular_dependencies|chatty_services|single_point_of_failure|excessive_fanout",
      "services": ["service1", "service2"],
      "severity": "critical|high|medium|low",
      "call_count": ...,  # if applicable
      "recommendation": "Specific fix"
    }},
    ...
  ],
  "health_score": 0-100,
  "summary": "Brief overall assessment"
}}

Return ONLY JSON."""

        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1536,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            analysis = json.loads(response.content[0].text)
            return analysis
        except json.JSONDecodeError:
            logger.error("Failed to parse dependency analysis")
            return {}


async def demo_trace_analysis():
    """Demo: Analyze slow traces"""
    # Note: This requires a running Jaeger instance
    # For demo purposes, we'll use mock data

    print("=== Trace Analyzer Demo ===\n")

    analyzer = TraceAnalyzer(jaeger_host='localhost:16686')

    # Mock trace data (since we don't have real Jaeger)
    mock_traces = [{
        'traceID': 'abc123',
        'duration': 3500000,  # 3.5 seconds in microseconds
        'spans': [
            {
                'spanID': '1',
                'process': {'serviceName': 'api-gateway'},
                'operationName': 'GET /recommendations',
                'duration': 3500000,
                'tags': []
            },
            {
                'spanID': '2',
                'process': {'serviceName': 'recommendation-engine'},
                'operationName': 'fetch_recommendations',
                'duration': 3200000,
                'tags': []
            },
            {
                'spanID': '3',
                'process': {'serviceName': 'product-catalog'},
                'operationName': 'get_product',
                'duration': 200000,
                'tags': []
            }
        ]
    }]

    trace_data = analyzer._extract_trace_data(mock_traces)
    analysis = await analyzer._ai_analyze_traces(trace_data)

    print("Analysis:")
    print(json.dumps(analysis, indent=2))


async def demo_dependency_mapping():
    """Demo: Map service dependencies"""
    print("\n=== Dependency Mapper Demo ===\n")

    mapper = DependencyMapper(jaeger_host='localhost:16686')

    # Mock dependency graph
    mock_graph = {
        'api-gateway': {
            'user-service': 150,
            'recommendation-engine': 120,
            'auth-service': 145
        },
        'recommendation-engine': {
            'product-catalog': 480,
            'user-service': 120
        },
        'user-service': {
            'database': 270
        }
    }

    analysis = await mapper._analyze_dependencies(mock_graph)

    print("Dependency Analysis:")
    print(json.dumps(analysis, indent=2))


if __name__ == '__main__':
    print("=== Distributed Trace Analyzer ===\n")

    # Run demos
    asyncio.run(demo_trace_analysis())
    asyncio.run(demo_dependency_mapping())

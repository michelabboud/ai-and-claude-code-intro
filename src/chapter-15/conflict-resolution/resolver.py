#!/usr/bin/env python3
"""
Chapter 15: Multi-Agent Orchestration - Fundamentals
Conflict Resolution Algorithms

Demonstrates how to resolve disagreements between multiple agents.
Implements voting systems, consensus mechanisms, and human escalation.

Part of: AI and Claude Code - A Comprehensive Guide for DevOps Engineers
Created by: Michel Abboud with Claude Sonnet 4.5 (Anthropic)
Copyright: © 2026 Michel Abboud. All rights reserved.
License: CC BY-NC 4.0

Usage:
    from resolver import ConflictResolver

    # Create resolver
    resolver = ConflictResolver()

    # Register agent votes
    resolver.register_vote('security-001', 'Recommendation A', confidence=0.85)
    resolver.register_vote('performance-001', 'Recommendation B', confidence=0.75)
    resolver.register_vote('cost-001', 'Recommendation A', confidence=0.60)

    # Resolve by highest confidence
    result = resolver.resolve_by_confidence()

    # Or require consensus
    result = resolver.resolve_by_consensus(threshold=0.66)
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class ConflictResolutionMethod(Enum):
    """Methods for resolving agent conflicts."""
    CONFIDENCE = "confidence"
    CONSENSUS = "consensus"
    WEIGHTED_VOTE = "weighted_vote"
    HUMAN_ESCALATION = "human_escalation"


@dataclass
class Vote:
    """
    Represents an agent's vote for a recommendation.

    Attributes:
        agent_id: Unique identifier of the voting agent
        recommendation: The recommended solution
        confidence: Confidence score (0.0 to 1.0)
        reasoning: Optional explanation of the vote
        metadata: Additional context (expertise area, evidence quality, etc.)
    """
    agent_id: str
    recommendation: str
    confidence: float
    reasoning: str = ""
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

        # Validate confidence score
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")


class ConflictResolver:
    """
    Resolves conflicts when multiple agents propose different solutions.

    Supports multiple resolution strategies:
    1. Confidence-based: Choose the recommendation with highest confidence
    2. Consensus-based: Require majority agreement (e.g., 2/3 threshold)
    3. Weighted voting: Weight votes by agent expertise/track record
    4. Human escalation: Defer to human when no clear winner
    """

    def __init__(self):
        """Initialize conflict resolver."""
        self.votes: Dict[str, Vote] = {}

    def register_vote(
        self,
        agent_id: str,
        recommendation: str,
        confidence: float,
        reasoning: str = "",
        metadata: Dict = None
    ):
        """
        Register an agent's vote.

        Args:
            agent_id: Unique identifier for the voting agent
            recommendation: The proposed solution
            confidence: Confidence score (0.0 to 1.0)
            reasoning: Optional explanation
            metadata: Optional additional context
        """
        vote = Vote(
            agent_id=agent_id,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            metadata=metadata or {}
        )

        self.votes[agent_id] = vote
        print(f"[ConflictResolver] Registered vote from {agent_id}: "
              f"{recommendation} (confidence: {confidence:.2f})")

    def resolve_by_confidence(self) -> Optional[Dict]:
        """
        Choose recommendation with highest confidence score.

        Returns:
            Dictionary with chosen recommendation and metadata
        """
        if not self.votes:
            return None

        # Find vote with highest confidence
        best_vote = max(self.votes.values(), key=lambda v: v.confidence)

        result = {
            'method': ConflictResolutionMethod.CONFIDENCE.value,
            'chosen_recommendation': best_vote.recommendation,
            'deciding_agent': best_vote.agent_id,
            'confidence': best_vote.confidence,
            'reasoning': best_vote.reasoning,
            'all_votes': {
                agent_id: {
                    'recommendation': vote.recommendation,
                    'confidence': vote.confidence
                }
                for agent_id, vote in self.votes.items()
            }
        }

        print(f"\n[ConflictResolver] Resolved by confidence: "
              f"{result['chosen_recommendation']} "
              f"(agent: {result['deciding_agent']}, confidence: {result['confidence']:.2f})")

        return result

    def resolve_by_consensus(self, threshold: float = 0.66) -> Dict:
        """
        Require majority agreement (e.g., 2/3 of agents).

        Args:
            threshold: Fraction of agents that must agree (default: 0.66 = 2/3)

        Returns:
            Dictionary with resolution result (may be None if no consensus)
        """
        if not self.votes:
            return {
                'method': ConflictResolutionMethod.CONSENSUS.value,
                'chosen_recommendation': None,
                'reason': 'No votes registered'
            }

        # Count votes for each recommendation
        vote_counts: Dict[str, List[str]] = {}
        for agent_id, vote in self.votes.items():
            if vote.recommendation not in vote_counts:
                vote_counts[vote.recommendation] = []
            vote_counts[vote.recommendation].append(agent_id)

        total_votes = len(self.votes)

        # Check if any recommendation meets threshold
        for recommendation, supporters in vote_counts.items():
            support_ratio = len(supporters) / total_votes

            if support_ratio >= threshold:
                result = {
                    'method': ConflictResolutionMethod.CONSENSUS.value,
                    'chosen_recommendation': recommendation,
                    'support_ratio': support_ratio,
                    'supporters': supporters,
                    'threshold_required': threshold
                }

                print(f"\n[ConflictResolver] Consensus reached: {recommendation} "
                      f"({len(supporters)}/{total_votes} agents, "
                      f"{support_ratio:.1%} support)")

                return result

        # No consensus
        result = {
            'method': ConflictResolutionMethod.CONSENSUS.value,
            'chosen_recommendation': None,
            'reason': f'No recommendation reached {threshold:.1%} threshold',
            'vote_distribution': {
                rec: len(supporters) for rec, supporters in vote_counts.items()
            }
        }

        print(f"\n[ConflictResolver] No consensus (threshold: {threshold:.1%})")
        print(f"Vote distribution: {result['vote_distribution']}")

        return result

    def resolve_by_weighted_vote(self, agent_weights: Dict[str, float]) -> Optional[Dict]:
        """
        Weight votes by agent expertise or track record.

        Args:
            agent_weights: Dictionary mapping agent_id to weight (0.0 to 1.0)

        Returns:
            Dictionary with chosen recommendation and weighted score
        """
        if not self.votes:
            return None

        # Calculate weighted scores for each recommendation
        recommendation_scores: Dict[str, float] = {}

        for agent_id, vote in self.votes.items():
            weight = agent_weights.get(agent_id, 0.5)  # Default weight 0.5
            weighted_score = vote.confidence * weight

            rec = vote.recommendation
            recommendation_scores[rec] = recommendation_scores.get(rec, 0) + weighted_score

        # Choose recommendation with highest weighted score
        best_recommendation = max(recommendation_scores.items(), key=lambda x: x[1])

        result = {
            'method': ConflictResolutionMethod.WEIGHTED_VOTE.value,
            'chosen_recommendation': best_recommendation[0],
            'weighted_score': best_recommendation[1],
            'all_scores': recommendation_scores,
            'agent_weights': agent_weights
        }

        print(f"\n[ConflictResolver] Resolved by weighted vote: "
              f"{result['chosen_recommendation']} "
              f"(score: {result['weighted_score']:.2f})")

        return result

    def should_escalate_to_human(
        self,
        min_confidence_threshold: float = 0.5,
        consensus_threshold: float = 0.66
    ) -> tuple[bool, str]:
        """
        Determine if conflict should be escalated to human decision-maker.

        Escalation criteria:
        1. All confidence scores are low (< threshold)
        2. Votes are evenly split (no clear winner)
        3. Recommendations are contradictory

        Args:
            min_confidence_threshold: Minimum acceptable confidence
            consensus_threshold: Required agreement ratio

        Returns:
            Tuple of (should_escalate: bool, reason: str)
        """
        if not self.votes:
            return True, "No votes registered"

        # Check 1: Low confidence across all agents
        max_confidence = max(v.confidence for v in self.votes.values())
        if max_confidence < min_confidence_threshold:
            return True, f"Low confidence (max: {max_confidence:.2f}, threshold: {min_confidence_threshold})"

        # Check 2: No consensus
        consensus_result = self.resolve_by_consensus(consensus_threshold)
        if consensus_result['chosen_recommendation'] is None:
            return True, "No consensus reached among agents"

        # Check 3: Contradictory recommendations
        # (This would require domain-specific logic to detect contradictions)
        # For now, we consider recommendations with similar vote counts as potential contradictions
        vote_counts = {}
        for vote in self.votes.values():
            vote_counts[vote.recommendation] = vote_counts.get(vote.recommendation, 0) + 1

        if len(vote_counts) > 1:
            max_votes = max(vote_counts.values())
            close_votes = [count for count in vote_counts.values() if count >= max_votes * 0.8]

            if len(close_votes) > 1:
                return True, "Votes are evenly split between multiple recommendations"

        return False, "Clear resolution possible without human intervention"

    def resolve_with_escalation(
        self,
        min_confidence_threshold: float = 0.5,
        consensus_threshold: float = 0.66
    ) -> Dict:
        """
        Attempt automatic resolution, escalate to human if necessary.

        Args:
            min_confidence_threshold: Minimum acceptable confidence
            consensus_threshold: Required agreement ratio

        Returns:
            Dictionary with resolution or escalation details
        """
        should_escalate, reason = self.should_escalate_to_human(
            min_confidence_threshold,
            consensus_threshold
        )

        if should_escalate:
            result = {
                'action': 'escalate_to_human',
                'reason': reason,
                'votes': {
                    agent_id: {
                        'recommendation': vote.recommendation,
                        'confidence': vote.confidence,
                        'reasoning': vote.reasoning
                    }
                    for agent_id, vote in self.votes.items()
                }
            }

            print(f"\n[ConflictResolver] ⚠️  Escalating to human: {reason}")
            return result

        # Try consensus first
        consensus_result = self.resolve_by_consensus(consensus_threshold)
        if consensus_result['chosen_recommendation']:
            return consensus_result

        # Fall back to confidence-based
        confidence_result = self.resolve_by_confidence()
        return confidence_result

    def get_summary(self) -> Dict:
        """
        Get summary of all votes and recommendations.

        Returns:
            Dictionary with vote statistics
        """
        if not self.votes:
            return {'total_votes': 0}

        recommendations = {}
        for vote in self.votes.values():
            rec = vote.recommendation
            if rec not in recommendations:
                recommendations[rec] = {
                    'supporters': [],
                    'avg_confidence': 0,
                    'confidences': []
                }

            recommendations[rec]['supporters'].append(vote.agent_id)
            recommendations[rec]['confidences'].append(vote.confidence)

        # Calculate averages
        for rec_data in recommendations.values():
            rec_data['avg_confidence'] = sum(rec_data['confidences']) / len(rec_data['confidences'])

        return {
            'total_votes': len(self.votes),
            'unique_recommendations': len(recommendations),
            'recommendations': recommendations,
            'highest_confidence': max(v.confidence for v in self.votes.values()),
            'lowest_confidence': min(v.confidence for v in self.votes.values()),
            'avg_confidence': sum(v.confidence for v in self.votes.values()) / len(self.votes)
        }


# Example usage
if __name__ == '__main__':
    print("=== Conflict Resolution Demo ===\n")

    # Scenario: 3 agents analyze production incident
    # Security agent: "SQL injection is root cause"
    # Performance agent: "Database overload is root cause"
    # Infrastructure agent: "SQL injection caused overload" (agrees with security)

    resolver = ConflictResolver()

    resolver.register_vote(
        'security-001',
        'SQL injection vulnerability in /api/users',
        confidence=0.85,
        reasoning='Found evidence of malicious queries in logs'
    )

    resolver.register_vote(
        'performance-001',
        'Database connection pool exhaustion',
        confidence=0.75,
        reasoning='Database connections maxed out at incident time'
    )

    resolver.register_vote(
        'infrastructure-001',
        'SQL injection vulnerability in /api/users',
        confidence=0.70,
        reasoning='SQL injection caused excessive database load'
    )

    print("\n--- Method 1: Confidence-based ---")
    result1 = resolver.resolve_by_confidence()

    print("\n--- Method 2: Consensus (66% threshold) ---")
    result2 = resolver.resolve_by_consensus(threshold=0.66)

    print("\n--- Method 3: Weighted vote ---")
    # Weight security agent higher for security issues
    agent_weights = {
        'security-001': 1.0,      # Security expert
        'performance-001': 0.7,   # Less relevant for security
        'infrastructure-001': 0.8  # Infrastructure knowledge relevant
    }
    result3 = resolver.resolve_by_weighted_vote(agent_weights)

    print("\n--- Method 4: Automatic with escalation ---")
    result4 = resolver.resolve_with_escalation(
        min_confidence_threshold=0.5,
        consensus_threshold=0.66
    )

    print("\n--- Vote Summary ---")
    summary = resolver.get_summary()
    print(f"Total votes: {summary['total_votes']}")
    print(f"Unique recommendations: {summary['unique_recommendations']}")
    print(f"Average confidence: {summary['avg_confidence']:.2f}")

    print("\n\n=== Low Confidence Escalation Demo ===\n")

    # Scenario: All agents have low confidence
    resolver2 = ConflictResolver()

    resolver2.register_vote('agent-1', 'Recommendation A', confidence=0.30)
    resolver2.register_vote('agent-2', 'Recommendation B', confidence=0.35)
    resolver2.register_vote('agent-3', 'Recommendation C', confidence=0.25)

    result = resolver2.resolve_with_escalation(min_confidence_threshold=0.5)

    if result['action'] == 'escalate_to_human':
        print(f"\n✓ Correctly escalated: {result['reason']}")

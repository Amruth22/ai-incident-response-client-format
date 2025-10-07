"""
Coordinator Agent

Agent responsible for aggregating results from all analysis agents.
"""

from typing import Dict, Any
from .base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """Agent for coordinating and aggregating analysis results"""
    
    def __init__(self):
        """Initialize coordinator agent"""
        super().__init__("coordinator")
        self.log("Coordinator agent initialized")
    
    def analyze(self, log_results: Dict[str, Any],
                knowledge_results: Dict[str, Any],
                root_cause_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate and coordinate results from all analysis agents
        
        Args:
            log_results: Results from log analysis agent
            knowledge_results: Results from knowledge lookup agent
            root_cause_results: Results from root cause agent
        
        Returns:
            Dictionary with coordination summary
        """
        self.log("Coordinating results from all analysis agents")
        
        # Collect completion status
        analyses_completed = []
        if log_results:
            analyses_completed.append("log_analysis")
        if knowledge_results:
            analyses_completed.append("knowledge_lookup")
        if root_cause_results:
            analyses_completed.append("root_cause")
        
        self.log(f"Analyses completed: {', '.join(analyses_completed)}")
        
        # Calculate summary metrics
        summary = {
            "analyses_completed": analyses_completed,
            "anomalies_found": log_results.get('anomalies_found', False),
            "similar_incidents_count": knowledge_results.get('total_matches', 0),
            "root_cause_confidence": root_cause_results.get('confidence', 0.0),
            "has_historical_guidance": knowledge_results.get('total_matches', 0) > 0
        }
        
        self.log(f"Coordination complete - {len(analyses_completed)} analyses aggregated")
        
        return {
            "coordination_summary": summary
        }

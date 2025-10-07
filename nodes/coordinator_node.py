"""
Coordinator Node - Simplified Wrapper

Calls CoordinatorAgent to aggregate all analysis results.
"""

from state import IncidentState
from agents.coordinator_agent import CoordinatorAgent

# Create agent instance
agent = CoordinatorAgent()


def coordinator_node(state: IncidentState) -> IncidentState:
    """
    Coordinate and aggregate all analysis results
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with coordination summary
    """
    result = agent.analyze(
        state.log_analysis_results,
        state.knowledge_lookup_results,
        state.root_cause_results
    )
    
    state.coordination_summary = result.get("coordination_summary", {})
    return state

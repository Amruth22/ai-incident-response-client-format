"""
Root Cause Node - Simplified Wrapper

Calls RootCauseAgent to perform AI-powered root cause analysis.
"""

from state import IncidentState
from agents.root_cause_agent import RootCauseAgent

# Create agent instance
agent = RootCauseAgent()


def root_cause_node(state: IncidentState) -> IncidentState:
    """
    Perform AI-powered root cause analysis
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with root cause results
    """
    result = agent.analyze(
        state.service,
        state.description,
        state.log_analysis_results,
        state.knowledge_lookup_results
    )
    state.root_cause_results = result
    return state

"""
Log Analysis Node - Simplified Wrapper

Calls LogAnalysisAgent to analyze system logs.
"""

from state import IncidentState
from agents.log_analysis_agent import LogAnalysisAgent

# Create agent instance
agent = LogAnalysisAgent()


def log_analysis_node(state: IncidentState) -> IncidentState:
    """
    Analyze system logs for anomalies
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with log analysis results
    """
    result = agent.analyze(state.service, state.description)
    state.log_analysis_results = result
    return state

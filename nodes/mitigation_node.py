"""
Mitigation Node - Simplified Wrapper

Calls MitigationAgent to execute automated mitigation (if decision is auto_mitigation).
"""

from state import IncidentState
from agents.mitigation_agent import MitigationAgent

# Create agent instance
agent = MitigationAgent()


def mitigation_node(state: IncidentState) -> IncidentState:
    """
    Execute automated mitigation actions
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with mitigation results
    """
    # Only execute if decision is auto_mitigation
    if state.decision == "auto_mitigation":
        result = agent.analyze(
            state.service,
            state.root_cause_results.get("root_cause", ""),
            state.root_cause_results.get("recommended_solution", ""),
            state.incident_id
        )
        state.mitigation_results = result
    
    return state

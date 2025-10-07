"""
Incident Trigger Node - Simplified Wrapper

Calls IncidentTriggerAgent to parse alert and initialize response.
"""

from state import IncidentState
from agents.incident_trigger_agent import IncidentTriggerAgent

# Create agent instance
agent = IncidentTriggerAgent()


def incident_trigger_node(state: IncidentState) -> IncidentState:
    """
    Parse incident alert and initialize response
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with parsed incident data
    """
    result = agent.analyze(state.raw_alert, state.incident_id)
    
    state.service = result.get("service", "")
    state.severity = result.get("severity", "")
    state.description = result.get("description", "")
    
    return state

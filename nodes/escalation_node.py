"""
Escalation Node - Simplified Wrapper

Calls EscalationAgent to escalate to humans (if decision is escalation).
"""

from state import IncidentState
from agents.escalation_agent import EscalationAgent

# Create agent instance
agent = EscalationAgent()


def escalation_node(state: IncidentState) -> IncidentState:
    """
    Escalate incident to human operators
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with escalation results
    """
    # Only execute if decision is escalation
    if state.decision == "escalation":
        result = agent.analyze(
            state.service,
            state.escalation_reason,
            state.incident_id,
            state.decision_metrics
        )
        state.escalation_results = result
    
    return state

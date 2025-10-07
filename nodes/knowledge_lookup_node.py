"""
Knowledge Lookup Node - Simplified Wrapper

Calls KnowledgeLookupAgent to search historical incidents.
"""

from state import IncidentState
from agents.knowledge_lookup_agent import KnowledgeLookupAgent

# Create agent instance
agent = KnowledgeLookupAgent()


def knowledge_lookup_node(state: IncidentState) -> IncidentState:
    """
    Search for similar historical incidents
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with knowledge lookup results
    """
    result = agent.analyze(state.service, state.description)
    state.knowledge_lookup_results = result
    return state

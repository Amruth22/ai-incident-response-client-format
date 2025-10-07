"""
Incident Workflow Builder

Defines the staged incident response pipeline with parallel and sequential nodes.
"""

from graph import IncidentGraph
from nodes import (
    incident_trigger_node,
    log_analysis_node,
    knowledge_lookup_node,
    root_cause_node,
    coordinator_node,
    decision_node,
    mitigation_node,
    escalation_node,
    communicator_node
)


def build_incident_workflow(max_workers: int = 3) -> IncidentGraph:
    """
    Build the incident response workflow with parallel execution
    
    Stages:
    1. Incident trigger (parse alert)
    2. Parallel analyses (log, knowledge, root cause)
    3. Coordinator (aggregate results)
    4. Decision (auto-mitigation or escalation)
    5. Action (mitigation OR escalation)
    6. Communicator (final report)
    
    Args:
        max_workers: Maximum number of parallel workers (default: 3)
    
    Returns:
        Compiled IncidentGraph ready for execution
    """
    stages = [
        # Stage 1: Incident trigger
        [incident_trigger_node],
        
        # Stage 2: Parallel analyses (all 3 run simultaneously)
        [log_analysis_node, knowledge_lookup_node, root_cause_node],
        
        # Stage 3: Coordinator
        [coordinator_node],
        
        # Stage 4: Decision
        [decision_node],
        
        # Stage 5: Action (mitigation OR escalation - handled by decision routing)
        # Note: In this simplified version, both run but only one takes effect
        [mitigation_node, escalation_node],
        
        # Stage 6: Communicator
        [communicator_node]
    ]
    
    return IncidentGraph(stages=stages, max_workers=max_workers, raise_on_error=False)

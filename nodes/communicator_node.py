"""
Communicator Node - Business Logic

Generates final report and summary.
"""

import logging
from datetime import datetime
from state import IncidentState

logger = logging.getLogger("communicator_node")


def communicator_node(state: IncidentState) -> IncidentState:
    """
    Generate final report
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with final report
    """
    logger.info("Generating final report")
    
    # Build final report
    report = {
        "incident_id": state.incident_id,
        "service": state.service,
        "severity": state.severity,
        "decision": state.decision,
        "status": "RESOLVED" if state.decision == "auto_mitigation" else "ESCALATED",
        "metrics": state.decision_metrics,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add mitigation or escalation details
    if state.decision == "auto_mitigation":
        report["actions_taken"] = state.mitigation_results.get("actions_taken", [])
        report["automated_resolution"] = True
    else:
        report["escalation_reason"] = state.escalation_reason
        report["ticket_id"] = state.escalation_results.get("ticket_id", "")
        report["requires_human_intervention"] = True
    
    logger.info(f"Final report generated: {report['status']}")
    
    # Update state
    state.final_report = report
    state.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return state

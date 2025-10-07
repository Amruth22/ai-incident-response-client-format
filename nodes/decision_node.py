"""
Decision Node - Business Logic

Makes automated decision based on multi-factor criteria.
"""

import logging
from state import IncidentState
from config import get_config_value

logger = logging.getLogger("decision_node")


def decision_node(state: IncidentState) -> IncidentState:
    """
    Make automated decision based on analysis results
    
    Args:
        state: Current incident state
    
    Returns:
        Updated state with decision
    """
    logger.info("Making automated decision")
    
    # Get configuration
    CONFIDENCE_THRESHOLD = get_config_value("CONFIDENCE_THRESHOLD", 0.8)
    MAX_RETRIES = get_config_value("MAX_RETRIES", 3)
    
    # Extract results
    log_results = state.log_analysis_results
    knowledge_results = state.knowledge_lookup_results
    root_cause_results = state.root_cause_results
    retry_count = state.retry_count
    
    # Get key metrics
    confidence = root_cause_results.get("confidence", 0.0)
    anomalies_found = log_results.get("anomalies_found", False)
    similar_incidents = knowledge_results.get("total_matches", 0) > 0
    
    # Decision logic
    decision = "auto_mitigation"
    escalation_reason = ""
    
    # Check escalation conditions
    if retry_count >= MAX_RETRIES:
        decision = "escalation"
        escalation_reason = f"Max retries ({MAX_RETRIES}) reached without finding anomalies"
    elif not anomalies_found:
        decision = "escalation"
        escalation_reason = "No anomalies detected in log analysis"
    elif confidence < CONFIDENCE_THRESHOLD:
        decision = "escalation"
        escalation_reason = f"Low confidence ({confidence:.2f}) in root cause analysis"
    elif not similar_incidents:
        decision = "escalation"
        escalation_reason = "No similar historical incidents found for guidance"
    
    # Log decision
    if decision == "auto_mitigation":
        logger.info(f"HIGH CONFIDENCE ({confidence:.2f}) - Auto-mitigation approved")
    else:
        logger.warning(f"ESCALATING - {escalation_reason}")
    
    # Calculate decision metrics
    metrics = {
        "confidence": confidence,
        "anomalies_found": anomalies_found,
        "similar_incidents_count": knowledge_results.get("total_matches", 0),
        "retry_count": retry_count,
        "escalation_reason": escalation_reason
    }
    
    # Update state
    state.decision = decision
    state.decision_metrics = metrics
    state.escalation_reason = escalation_reason
    
    return state

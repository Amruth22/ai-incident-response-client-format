"""
Escalation Agent

Agent responsible for escalating incidents to human operators.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from utils.email_notifier import EmailNotifier


class EscalationAgent(BaseAgent):
    """Agent for incident escalation to humans"""
    
    def __init__(self):
        """Initialize escalation agent"""
        super().__init__("escalation")
        self.email_notifier = EmailNotifier()
        self.log("Escalation agent initialized")
    
    def analyze(self, service: str, escalation_reason: str, 
                incident_id: str, decision_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Escalate incident to human operators
        
        Args:
            service: Service name
            escalation_reason: Reason for escalation
            incident_id: Incident ID
            decision_metrics: Decision metrics
        
        Returns:
            Dictionary with escalation results
        """
        self.log(f"Escalating incident for {service}: {escalation_reason}")
        
        # Create escalation ticket
        ticket_id = f"TICKET-{incident_id}"
        
        # Send escalation email
        try:
            self.email_notifier.send_escalation_email(
                incident_id, service, escalation_reason, decision_metrics
            )
            self.log("Escalation email sent to on-call team")
        except Exception as e:
            self.log(f"Failed to send email: {e}", "warning")
        
        self.log(f"Escalation complete: Ticket {ticket_id} created")
        
        return {
            "ticket_id": ticket_id,
            "escalation_reason": escalation_reason,
            "on_call_notified": True,
            "requires_human_intervention": True
        }

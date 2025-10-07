"""
Incident Trigger Agent

Agent responsible for parsing incident alerts and initializing response.
Uses AIAnalyzer for alert parsing and EmailNotifier for notifications.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ai_analyzer import AIAnalyzer
from utils.email_notifier import EmailNotifier


class IncidentTriggerAgent(BaseAgent):
    """Agent for parsing and triggering incident response"""
    
    def __init__(self):
        """Initialize incident trigger agent"""
        super().__init__("incident_trigger")
        self.ai_analyzer = AIAnalyzer()
        self.email_notifier = EmailNotifier()
        self.log("Incident Trigger agent initialized")
    
    def analyze(self, raw_alert: str, incident_id: str) -> Dict[str, Any]:
        """
        Parse incident alert and initialize response
        
        Args:
            raw_alert: Raw alert text
            incident_id: Incident ID
        
        Returns:
            Dictionary with parsed incident data
        """
        self.log(f"Parsing incident alert: {incident_id}")
        
        # Use AI analyzer to parse alert
        parsed = self.ai_analyzer.parse_incident_alert(raw_alert)
        
        service = parsed.get('service', 'Unknown Service')
        severity = parsed.get('severity', 'MEDIUM')
        description = parsed.get('description', raw_alert[:100])
        
        self.log(f"Parsed - Service: {service}, Severity: {severity}")
        
        # Send initial alert email
        try:
            self.email_notifier.send_incident_alert(incident_id, service, severity, description)
            self.log("Initial alert email sent")
        except Exception as e:
            self.log(f"Failed to send email: {e}", "warning")
        
        return {
            "service": service,
            "severity": severity,
            "description": description
        }

"""
Log Analysis Agent

Agent responsible for coordinating log analysis.
Uses LogAnalyzer as a tool for anomaly detection.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.log_analyzer import LogAnalyzer


class LogAnalysisAgent(BaseAgent):
    """Agent for log analysis and anomaly detection"""
    
    def __init__(self):
        """Initialize log analysis agent with analyzer"""
        super().__init__("log_analysis")
        self.analyzer = LogAnalyzer()
        self.log("Log Analysis agent initialized")
    
    def analyze(self, service: str, description: str) -> Dict[str, Any]:
        """
        Analyze system logs for anomalies
        
        Args:
            service: Service name
            description: Incident description
        
        Returns:
            Dictionary with log analysis results
        """
        self.log(f"Analyzing logs for {service}")
        
        # Use analyzer tool for actual analysis
        results = self.analyzer.analyze_logs(service, description)
        
        anomalies_found = results.get('anomalies_found', False)
        anomaly_count = len(results.get('anomalies', []))
        
        self.log(f"Log analysis complete: {anomaly_count} anomalies found")
        
        return results

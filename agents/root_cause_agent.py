"""
Root Cause Agent

Agent responsible for AI-powered root cause analysis.
Uses AIAnalyzer as a tool for determining root cause.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.ai_analyzer import AIAnalyzer


class RootCauseAgent(BaseAgent):
    """Agent for AI-powered root cause analysis"""
    
    def __init__(self):
        """Initialize root cause agent with AI analyzer"""
        super().__init__("root_cause")
        self.ai_analyzer = AIAnalyzer()
        self.log("Root Cause agent initialized")
    
    def analyze(self, service: str, description: str,
                log_results: Dict[str, Any],
                knowledge_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform AI-powered root cause analysis
        
        Args:
            service: Service name
            description: Incident description
            log_results: Results from log analysis
            knowledge_results: Results from knowledge lookup
        
        Returns:
            Dictionary with root cause analysis results
        """
        self.log(f"Analyzing root cause for {service}")
        
        # Use AI analyzer for root cause determination
        results = self.ai_analyzer.analyze_root_cause(
            service, description, log_results, knowledge_results
        )
        
        confidence = results.get('confidence', 0.0)
        root_cause = results.get('root_cause', 'Unknown')
        
        self.log(f"Root cause analysis complete: {root_cause} (confidence: {confidence:.2f})")
        
        return results

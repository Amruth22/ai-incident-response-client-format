"""
Knowledge Lookup Agent

Agent responsible for searching historical incidents.
Uses KnowledgeSearcher as a tool for finding similar incidents.
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from analyzers.knowledge_searcher import KnowledgeSearcher


class KnowledgeLookupAgent(BaseAgent):
    """Agent for knowledge base search and historical incident lookup"""
    
    def __init__(self):
        """Initialize knowledge lookup agent with searcher"""
        super().__init__("knowledge_lookup")
        self.searcher = KnowledgeSearcher()
        self.log("Knowledge Lookup agent initialized")
    
    def analyze(self, service: str, description: str) -> Dict[str, Any]:
        """
        Search for similar historical incidents
        
        Args:
            service: Service name
            description: Incident description
        
        Returns:
            Dictionary with knowledge lookup results
        """
        self.log(f"Searching knowledge base for {service}")
        
        # Use searcher tool for actual search
        results = self.searcher.search_similar_incidents(service, description)
        
        match_count = results.get('total_matches', 0)
        self.log(f"Knowledge search complete: {match_count} similar incidents found")
        
        return results

"""
Incident State - Shared State for Incident Response Pipeline

Dataclass-based state management with clone and merge capabilities.
This is ONLY a data structure - NO business logic, NO orchestration logic.
"""

from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List, Dict, Any, Optional
import copy


@dataclass
class IncidentState:
    """
    Shared state for multi-agent incident response pipeline
    
    This is a pure data structure with helper methods for state management.
    All business logic lives in agents/ and nodes/
    All orchestration logic lives in graph.py and workflows/
    """
    
    # Basic incident information
    incident_id: str = ""
    raw_alert: str = ""
    timestamp: str = ""
    
    # Parsed incident details
    service: str = ""
    severity: str = ""
    description: str = ""
    
    # Analysis results (populated by agents)
    log_analysis_results: Dict[str, Any] = field(default_factory=dict)
    knowledge_lookup_results: Dict[str, Any] = field(default_factory=dict)
    root_cause_results: Dict[str, Any] = field(default_factory=dict)
    
    # Action results
    mitigation_results: Dict[str, Any] = field(default_factory=dict)
    escalation_results: Dict[str, Any] = field(default_factory=dict)
    
    # Coordination data
    coordination_summary: Dict[str, Any] = field(default_factory=dict)
    
    # Decision results
    decision: str = ""
    decision_metrics: Dict[str, Any] = field(default_factory=dict)
    escalation_reason: str = ""
    
    # Final report
    final_report: Dict[str, Any] = field(default_factory=dict)
    
    # Workflow metadata
    retry_count: int = 0
    emails_sent: List[Dict[str, Any]] = field(default_factory=list)
    error: str = ""
    workflow_complete: bool = False
    updated_at: str = ""
    
    # Extra metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def clone(self) -> "IncidentState":
        """
        Deep copy for safe parallel execution
        
        Returns:
            Deep copy of the current state
        """
        return copy.deepcopy(self)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state to dictionary
        
        Returns:
            Dictionary representation of state
        """
        return asdict(self)
    
    def merge_from(self, other: Any, overwrite_scalars: bool = True) -> None:
        """
        Merge another IncidentState or dict into this state
        
        SMART MERGE LOGIC:
        - Initial data fields: REPLACE (don't extend)
        - Result fields: EXTEND or MERGE (accumulate from parallel agents)
        - Dicts: Shallow merge
        - Scalars: Overwrite if allowed
        
        Args:
            other: Another IncidentState instance or dictionary to merge from
            overwrite_scalars: Whether to overwrite scalar values (default: True)
        """
        if other is None:
            return
        
        # Convert to dict if it's a dataclass
        if is_dataclass(other):
            other_dict = asdict(other)
        elif isinstance(other, dict):
            other_dict = other
        else:
            return
        
        # Fields that should be REPLACED, not extended (initial data)
        REPLACE_FIELDS = {'emails_sent'}
        
        # Result fields are dicts, so they'll be merged automatically
        
        for key, val in other_dict.items():
            if val is None:
                continue
            
            if not hasattr(self, key):
                # Store unknown keys in metadata
                self.metadata.setdefault("extra", {})[key] = val
                continue
            
            current = getattr(self, key)
            
            # Handle lists with smart logic
            if isinstance(current, list) and isinstance(val, list):
                if key in REPLACE_FIELDS:
                    # REPLACE for initial data (prevent duplicates)
                    setattr(self, key, val)
                else:
                    # EXTEND for other lists (accumulate)
                    current.extend(val)
                    setattr(self, key, current)
                continue
            
            # Merge dicts by updating
            if isinstance(current, dict) and isinstance(val, dict):
                # MERGE dicts (for result fields)
                merged = current.copy()
                merged.update(val)
                setattr(self, key, merged)
                continue
            
            # Merge scalars by overwriting (if allowed and value is not empty)
            if overwrite_scalars and val not in (None, "", [], {}):
                setattr(self, key, val)

"""
Workflows Package

Contains workflow builder functions that define the execution flow.
"""

from .incident_workflow import build_incident_workflow

__all__ = ['build_incident_workflow']

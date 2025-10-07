"""
AI-Powered Incident Response System - Client Format
Main application entry point
"""

import sys
import argparse
from datetime import datetime
import uuid

from config import validate_config, get_config_value
from state import IncidentState
from workflows.incident_workflow import build_incident_workflow
from utils.logging_utils import setup_logging


def main():
    """Main application entry point"""
    # Setup logging
    log_file = get_config_value("LOG_FILE", "logs/incident_response.log")
    log_level = get_config_value("LOG_LEVEL", "INFO")
    setup_logging(log_level, log_file)
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="AI-Powered Incident Response - Client Format Multi-Agent System"
    )
    
    parser.add_argument("alert", nargs='?', help="Incident alert description")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--max-workers", type=int, default=3, help="Maximum parallel workers")
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        validate_config()
        
        # Handle commands
        if args.demo:
            run_demo(args.max_workers)
        elif args.alert:
            process_incident(args.alert, args.max_workers)
        else:
            interactive_mode()
    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def process_incident(raw_alert: str, max_workers: int = 3):
    """
    Process an incident alert
    
    Args:
        raw_alert: Raw incident alert text
        max_workers: Maximum parallel workers
    """
    print(f"\\n{'='*70}")
    print(f"AI-POWERED INCIDENT RESPONSE - CLIENT FORMAT")
    print(f"{'='*70}")
    print(f"Alert: {raw_alert[:60]}...")
    print(f"Max Workers: {max_workers}")
    print(f"{'='*70}\\n")
    
    # Create initial state
    incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    initial_state = IncidentState(
        incident_id=incident_id,
        raw_alert=raw_alert,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    print(f"Incident ID: {incident_id}")
    print(f"Starting workflow execution...\\n")
    
    # Build and execute workflow
    workflow = build_incident_workflow(max_workers=max_workers)
    final_state = workflow.run(initial_state)
    
    # Display results
    display_results(final_state)


def display_results(state: IncidentState):
    """Display workflow results"""
    print(f"\\n{'='*70}")
    print("INCIDENT RESPONSE COMPLETE")
    print(f"{'='*70}")
    print(f"Incident ID: {state.incident_id}")
    print(f"Service: {state.service}")
    print(f"Decision: {state.decision.upper()}")
    
    if state.decision == "auto_mitigation":
        print(f"\\n[OK] SUCCESS: Incident automatically resolved")
        if state.mitigation_results:
            actions = state.mitigation_results.get("actions_taken", [])
            if actions:
                print(f"\\nActions Taken:")
                for action in actions:
                    print(f"  - {action}")
    else:
        print(f"\\n[!] ESCALATED: {state.escalation_reason}")
        if state.escalation_results:
            ticket_id = state.escalation_results.get("ticket_id", "")
            print(f"\\nTicket ID: {ticket_id}")
    
    # Display metrics
    if state.decision_metrics:
        print(f"\\n{'='*70}")
        print("DECISION METRICS")
        print(f"{'='*70}")
        metrics = state.decision_metrics
        print(f"Confidence:        {metrics.get('confidence', 0):.2f}")
        print(f"Anomalies Found:   {metrics.get('anomalies_found', False)}")
        print(f"Similar Incidents: {metrics.get('similar_incidents_count', 0)}")
        print(f"Retry Count:       {metrics.get('retry_count', 0)}")
    
    print(f"\\n{'='*70}")
    print("Email notifications sent to configured recipient")
    print(f"{'='*70}\\n")


def run_demo(max_workers: int = 3):
    """Run demo with sample incidents"""
    print(f"\\n{'='*70}")
    print("DEMO MODE - AI-Powered Incident Response")
    print(f"{'='*70}")
    print("\\nSelect a demo scenario:")
    print("1. Database Timeout (high confidence → auto-resolve)")
    print("2. Memory Leak (medium confidence → may escalate)")
    print("3. Network Issues (complex → likely escalation)")
    print("4. Unknown Service (low confidence → escalation)")
    
    choice = input("\\nSelect scenario (1-4): ").strip()
    
    scenarios = {
        "1": "Payment API experiencing database connection timeouts",
        "2": "Auth Service showing memory leak symptoms",
        "3": "Load Balancer having network connectivity issues",
        "4": "Unknown service reporting critical errors"
    }
    
    alert = scenarios.get(choice, scenarios["1"])
    print(f"\\nProcessing: {alert}\\n")
    
    process_incident(alert, max_workers)


def interactive_mode():
    """Interactive mode for incident response"""
    print(f"\\n{'='*70}")
    print("AI-Powered Incident Response - Client Format Multi-Agent System")
    print(f"{'='*70}")
    print("\\n1. Process Incident Alert")
    print("2. Run Demo")
    print("0. Exit")
    
    choice = input("\\nSelect option (0-2): ").strip()
    
    if choice == "0":
        print("Goodbye!")
        return
    
    elif choice == "1":
        alert = input("Enter incident alert: ").strip()
        max_workers_str = input("Enter max workers (default 3): ").strip()
        
        try:
            max_workers = int(max_workers_str) if max_workers_str else 3
            process_incident(alert, max_workers)
        except ValueError:
            print("ERROR: Invalid input")
    
    elif choice == "2":
        max_workers_str = input("Enter max workers (default 3): ").strip()
        max_workers = int(max_workers_str) if max_workers_str else 3
        run_demo(max_workers)
    
    else:
        print("ERROR: Invalid choice")


if __name__ == "__main__":
    main()

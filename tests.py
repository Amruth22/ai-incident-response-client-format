#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI-Powered Incident Response - Client Format

Tests all major components: agents, analyzers, nodes, workflow, graph, and state.

Run with: python tests.py
Or with pytest: pytest tests.py -v
"""

import os
import sys
import unittest
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("tests")

# Import the required modules
try:
    from config import get_config, get_config_value
    from state import IncidentState
    from graph import IncidentGraph
    from workflows.incident_workflow import build_incident_workflow
    
    # Import agents
    from agents.base_agent import BaseAgent
    from agents.incident_trigger_agent import IncidentTriggerAgent
    from agents.log_analysis_agent import LogAnalysisAgent
    from agents.knowledge_lookup_agent import KnowledgeLookupAgent
    from agents.root_cause_agent import RootCauseAgent
    from agents.coordinator_agent import CoordinatorAgent
    from agents.mitigation_agent import MitigationAgent
    from agents.escalation_agent import EscalationAgent
    
    # Import analyzers
    from analyzers.log_analyzer import LogAnalyzer
    from analyzers.knowledge_searcher import KnowledgeSearcher
    from analyzers.ai_analyzer import AIAnalyzer
    
    # Import nodes
    from nodes.incident_trigger_node import incident_trigger_node
    from nodes.log_analysis_node import log_analysis_node
    from nodes.knowledge_lookup_node import knowledge_lookup_node
    from nodes.root_cause_node import root_cause_node
    from nodes.coordinator_node import coordinator_node
    from nodes.decision_node import decision_node
    from nodes.mitigation_node import mitigation_node
    from nodes.escalation_node import escalation_node
    from nodes.communicator_node import communicator_node
    
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure you're running this test from the project root directory")
    sys.exit(1)


class TestIncidentResponseClientFormat(unittest.TestCase):
    """Test suite for Incident Response Client Format Architecture"""
    
    def setUp(self):
        """Setup test environment"""
        self.sample_alert = "Payment API experiencing database connection timeouts"
        self.incident_id = "TEST-INC-001"
    
    # ========================================================================
    # CONFIGURATION TESTS
    # ========================================================================
    
    def test_configuration(self):
        """Test configuration management"""
        logger.info("Testing configuration management...")
        
        config = get_config()
        self.assertIsNotNone(config, "Config should not be None")
        
        # Test getting specific values with defaults
        gemini_key = get_config_value("GEMINI_API_KEY", "default")
        self.assertIsNotNone(gemini_key, "GEMINI_API_KEY should not be None")
        
        # Test default value
        test_value = get_config_value("NON_EXISTENT_VALUE", "default_value")
        self.assertEqual(test_value, "default_value", "Default value should be returned")
        
        # Test thresholds
        confidence_threshold = get_config_value("CONFIDENCE_THRESHOLD", 0.0)
        self.assertGreaterEqual(confidence_threshold, 0.0, "CONFIDENCE_THRESHOLD should be >= 0.0")
        
        max_retries = get_config_value("MAX_RETRIES", 0)
        self.assertGreaterEqual(max_retries, 0, "MAX_RETRIES should be >= 0")
        
        logger.info("✓ Configuration tests passed")
    
    # ========================================================================
    # STATE TESTS
    # ========================================================================
    
    def test_state_creation(self):
        """Test IncidentState dataclass creation"""
        logger.info("Testing IncidentState creation...")
        
        state = IncidentState(
            incident_id="TEST-123",
            raw_alert=self.sample_alert,
            service="Payment API"
        )
        
        self.assertIsNotNone(state, "State should not be None")
        self.assertEqual(state.incident_id, "TEST-123", "Incident ID should be set")
        self.assertEqual(state.raw_alert, self.sample_alert, "Raw alert should be set")
        self.assertEqual(state.service, "Payment API", "Service should be set")
        
        logger.info("✓ State creation tests passed")
    
    def test_state_clone(self):
        """Test IncidentState clone method"""
        logger.info("Testing IncidentState clone...")
        
        state = IncidentState(incident_id="TEST-123", service="Payment API")
        state.log_analysis_results = {"test": "data"}
        
        cloned = state.clone()
        
        self.assertIsNotNone(cloned, "Cloned state should not be None")
        self.assertEqual(cloned.incident_id, state.incident_id, "Incident ID should match")
        self.assertIsNot(cloned, state, "Cloned state should be a different object")
        self.assertIsNot(cloned.log_analysis_results, state.log_analysis_results, "Dicts should be deep copied")
        
        logger.info("✓ State clone tests passed")
    
    def test_state_merge(self):
        """Test IncidentState merge_from method"""
        logger.info("Testing IncidentState merge...")
        
        state1 = IncidentState(incident_id="TEST-123")
        state2 = IncidentState(service="Payment API")
        
        state1.merge_from(state2)
        
        self.assertEqual(state1.service, "Payment API", "Service should be merged")
        
        logger.info("✓ State merge tests passed")
    
    # ========================================================================
    # ANALYZER TESTS (Pure Tools)
    # ========================================================================
    
    def test_log_analyzer(self):
        """Test LogAnalyzer (pure tool)"""
        logger.info("Testing LogAnalyzer...")
        
        analyzer = LogAnalyzer()
        results = analyzer.analyze_logs("Payment API", "database timeout")
        
        self.assertIsNotNone(results, "Log analysis results should not be None")
        self.assertIn("anomalies", results, "Results should contain anomalies")
        self.assertIn("anomalies_found", results, "Results should contain anomalies_found")
        self.assertTrue(results["anomalies_found"], "Should find anomalies for database timeout")
        
        logger.info("✓ LogAnalyzer tests passed")
    
    def test_knowledge_searcher(self):
        """Test KnowledgeSearcher (pure tool)"""
        logger.info("Testing KnowledgeSearcher...")
        
        searcher = KnowledgeSearcher()
        results = searcher.search_similar_incidents("Payment API", "database timeout")
        
        self.assertIsNotNone(results, "Knowledge search results should not be None")
        self.assertIn("similar_incidents", results, "Results should contain similar_incidents")
        self.assertIn("total_matches", results, "Results should contain total_matches")
        self.assertGreater(results["total_matches"], 0, "Should find similar incidents")
        
        logger.info("✓ KnowledgeSearcher tests passed")
    
    def test_ai_analyzer(self):
        """Test AIAnalyzer (pure tool)"""
        logger.info("Testing AIAnalyzer...")
        
        analyzer = AIAnalyzer()
        
        # Test alert parsing
        parsed = analyzer.parse_incident_alert(self.sample_alert)
        
        self.assertIsNotNone(parsed, "Parsed result should not be None")
        self.assertIn("service", parsed, "Result should contain service")
        self.assertIn("severity", parsed, "Result should contain severity")
        self.assertIn("description", parsed, "Result should contain description")
        
        logger.info("✓ AIAnalyzer tests passed")
    
    # ========================================================================
    # AGENT TESTS (Coordinators)
    # ========================================================================
    
    def test_base_agent(self):
        """Test BaseAgent class"""
        logger.info("Testing BaseAgent...")
        
        agent = BaseAgent("test_agent")
        
        self.assertEqual(agent.name, "test_agent", "Agent name should be set")
        self.assertIsNotNone(agent.logger, "Agent should have a logger")
        
        with self.assertRaises(NotImplementedError):
            agent.analyze()
        
        logger.info("✓ BaseAgent tests passed")
    
    def test_log_analysis_agent(self):
        """Test LogAnalysisAgent (coordinator)"""
        logger.info("Testing LogAnalysisAgent...")
        
        agent = LogAnalysisAgent()
        results = agent.analyze("Payment API", "database timeout")
        
        self.assertIsNotNone(results, "Log analysis agent results should not be None")
        self.assertIn("anomalies_found", results, "Result should contain anomalies_found")
        
        logger.info("✓ LogAnalysisAgent tests passed")
    
    def test_knowledge_lookup_agent(self):
        """Test KnowledgeLookupAgent (coordinator)"""
        logger.info("Testing KnowledgeLookupAgent...")
        
        agent = KnowledgeLookupAgent()
        results = agent.analyze("Payment API", "database timeout")
        
        self.assertIsNotNone(results, "Knowledge lookup agent results should not be None")
        self.assertIn("total_matches", results, "Result should contain total_matches")
        
        logger.info("✓ KnowledgeLookupAgent tests passed")
    
    def test_coordinator_agent(self):
        """Test CoordinatorAgent"""
        logger.info("Testing CoordinatorAgent...")
        
        # Create mock results
        log_results = {"anomalies_found": True}
        knowledge_results = {"total_matches": 2}
        root_cause_results = {"confidence": 0.85}
        
        agent = CoordinatorAgent()
        result = agent.analyze(log_results, knowledge_results, root_cause_results)
        
        self.assertIsNotNone(result, "Coordinator result should not be None")
        self.assertIn("coordination_summary", result, "Result should contain coordination_summary")
        
        summary = result["coordination_summary"]
        self.assertEqual(len(summary["analyses_completed"]), 3, "Should have 3 completed analyses")
        
        logger.info("✓ CoordinatorAgent tests passed")
    
    def test_mitigation_agent(self):
        """Test MitigationAgent"""
        logger.info("Testing MitigationAgent...")
        
        agent = MitigationAgent()
        result = agent.analyze("Payment API", "Database timeout", "Restart connection pool", "TEST-INC-001")
        
        self.assertIsNotNone(result, "Mitigation result should not be None")
        self.assertIn("actions_taken", result, "Result should contain actions_taken")
        self.assertGreater(len(result["actions_taken"]), 0, "Should have actions")
        
        logger.info("✓ MitigationAgent tests passed")
    
    def test_escalation_agent(self):
        """Test EscalationAgent"""
        logger.info("Testing EscalationAgent...")
        
        agent = EscalationAgent()
        result = agent.analyze("Payment API", "Low confidence", "TEST-INC-001", {"confidence": 0.5})
        
        self.assertIsNotNone(result, "Escalation result should not be None")
        self.assertIn("ticket_id", result, "Result should contain ticket_id")
        self.assertIn("requires_human_intervention", result, "Result should contain requires_human_intervention")
        
        logger.info("✓ EscalationAgent tests passed")
    
    # ========================================================================
    # NODE TESTS (Thin Wrappers)
    # ========================================================================
    
    def test_log_analysis_node(self):
        """Test log_analysis_node (thin wrapper)"""
        logger.info("Testing log_analysis_node...")
        
        state = IncidentState(
            incident_id="TEST-INC",
            service="Payment API",
            description="database timeout"
        )
        
        result = log_analysis_node(state)
        
        self.assertIsNotNone(result, "Log analysis node result should not be None")
        self.assertIsInstance(result, IncidentState, "Result should be IncidentState")
        self.assertIsNotNone(result.log_analysis_results, "Should have log analysis results")
        
        logger.info("✓ log_analysis_node tests passed")
    
    def test_decision_node(self):
        """Test decision_node logic"""
        logger.info("Testing decision_node...")
        
        # Create mock state with high confidence (should auto-mitigate)
        state = IncidentState(
            incident_id="TEST-INC",
            service="Payment API",
            log_analysis_results={"anomalies_found": True, "anomalies": [{"type": "timeout"}]},
            knowledge_lookup_results={"total_matches": 2},
            root_cause_results={"confidence": 0.9}
        )
        
        result = decision_node(state)
        
        self.assertIsNotNone(result, "Decision result should not be None")
        self.assertIsInstance(result, IncidentState, "Result should be IncidentState")
        self.assertIn(result.decision, ["auto_mitigation", "escalation"], "Decision should be valid")
        self.assertEqual(result.decision, "auto_mitigation", "High confidence should auto-mitigate")
        
        logger.info("✓ decision_node tests passed")
    
    def test_decision_node_escalation(self):
        """Test decision_node escalation logic"""
        logger.info("Testing decision_node escalation...")
        
        # Create mock state with low confidence (should escalate)
        state = IncidentState(
            incident_id="TEST-INC",
            service="Payment API",
            log_analysis_results={"anomalies_found": True},
            knowledge_lookup_results={"total_matches": 1},
            root_cause_results={"confidence": 0.5}
        )
        
        result = decision_node(state)
        
        self.assertEqual(result.decision, "escalation", "Low confidence should escalate")
        self.assertIn("confidence", result.escalation_reason.lower(), "Should mention confidence")
        
        logger.info("✓ decision_node escalation tests passed")
    
    # ========================================================================
    # GRAPH TESTS
    # ========================================================================
    
    def test_incident_graph_creation(self):
        """Test IncidentGraph class creation"""
        logger.info("Testing IncidentGraph creation...")
        
        def dummy_node(state):
            return state
        
        stages = [[dummy_node]]
        graph = IncidentGraph(stages=stages, max_workers=2)
        
        self.assertIsNotNone(graph, "Graph should not be None")
        self.assertEqual(len(graph.stages), 1, "Should have 1 stage")
        self.assertEqual(graph.max_workers, 2, "Max workers should be 2")
        
        logger.info("✓ IncidentGraph creation tests passed")
    
    def test_incident_graph_execution(self):
        """Test IncidentGraph execution"""
        logger.info("Testing IncidentGraph execution...")
        
        def test_node(state):
            state.metadata["test"] = "executed"
            return state
        
        stages = [[test_node]]
        graph = IncidentGraph(stages=stages, max_workers=1)
        
        initial_state = IncidentState(incident_id="TEST-123", raw_alert="Test alert")
        final_state = graph.run(initial_state)
        
        self.assertIsNotNone(final_state, "Final state should not be None")
        self.assertTrue(final_state.workflow_complete, "Workflow should be marked complete")
        self.assertEqual(final_state.metadata.get("test"), "executed", "Node should have executed")
        
        logger.info("✓ IncidentGraph execution tests passed")
    
    # ========================================================================
    # WORKFLOW TESTS
    # ========================================================================
    
    def test_workflow_builder(self):
        """Test workflow builder function"""
        logger.info("Testing workflow builder...")
        
        workflow = build_incident_workflow(max_workers=2)
        
        self.assertIsNotNone(workflow, "Workflow should not be None")
        self.assertIsInstance(workflow, IncidentGraph, "Workflow should be IncidentGraph instance")
        self.assertEqual(workflow.max_workers, 2, "Max workers should be 2")
        self.assertGreater(len(workflow.stages), 0, "Should have stages")
        
        logger.info("✓ Workflow builder tests passed")
    
    # ========================================================================
    # INTEGRATION TESTS
    # ========================================================================
    
    def test_full_pipeline(self):
        """Test the full pipeline"""
        logger.info("Testing full pipeline execution...")
        
        # Create state
        state = IncidentState(
            incident_id="TEST-PIPELINE",
            raw_alert=self.sample_alert,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Execute trigger node
        trigger_result = incident_trigger_node(state)
        self.assertIsNotNone(trigger_result.service, "Should have service")
        self.assertIsNotNone(trigger_result.severity, "Should have severity")
        
        # Execute analysis nodes
        log_result = log_analysis_node(trigger_result)
        knowledge_result = knowledge_lookup_node(trigger_result)
        root_cause_result = root_cause_node(trigger_result)
        
        # Verify results
        self.assertIsNotNone(log_result.log_analysis_results, "Should have log results")
        self.assertIsNotNone(knowledge_result.knowledge_lookup_results, "Should have knowledge results")
        self.assertIsNotNone(root_cause_result.root_cause_results, "Should have root cause results")
        
        # Execute coordinator
        coord_result = coordinator_node(root_cause_result)
        self.assertIsNotNone(coord_result.coordination_summary, "Should have coordination summary")
        
        # Execute decision
        decision_result = decision_node(coord_result)
        self.assertIsNotNone(decision_result.decision, "Should have a decision")
        self.assertIn(decision_result.decision, ["auto_mitigation", "escalation"], "Decision should be valid")
        
        logger.info(f"Pipeline decision: {decision_result.decision}")
        logger.info("✓ Full pipeline tests passed")
    
    # ========================================================================
    # ARCHITECTURE COMPLIANCE TESTS
    # ========================================================================
    
    def test_agent_analyzer_separation(self):
        """Test that agents and analyzers are properly separated"""
        logger.info("Testing agent/analyzer separation...")
        
        # Agents should use analyzers
        log_agent = LogAnalysisAgent()
        self.assertIsNotNone(log_agent.analyzer, "LogAnalysisAgent should have an analyzer")
        self.assertIsInstance(log_agent.analyzer, LogAnalyzer, "Should use LogAnalyzer")
        
        knowledge_agent = KnowledgeLookupAgent()
        self.assertIsNotNone(knowledge_agent.searcher, "KnowledgeLookupAgent should have a searcher")
        self.assertIsInstance(knowledge_agent.searcher, KnowledgeSearcher, "Should use KnowledgeSearcher")
        
        logger.info("✓ Agent/Analyzer separation tests passed")
    
    def test_node_purity(self):
        """Test that nodes are pure wrappers (no orchestration)"""
        logger.info("Testing node purity...")
        
        state = IncidentState(
            incident_id="TEST-INC",
            service="Payment API",
            description="test"
        )
        
        # Test that nodes return IncidentState (not dict)
        result = log_analysis_node(state)
        self.assertIsInstance(result, IncidentState, "Node should return IncidentState")
        
        result = knowledge_lookup_node(state)
        self.assertIsInstance(result, IncidentState, "Node should return IncidentState")
        
        logger.info("✓ Node purity tests passed")
    
    def test_smart_merge_logic(self):
        """Test that smart merge prevents duplicates"""
        logger.info("Testing smart merge logic...")
        
        state1 = IncidentState(incident_id="TEST-123")
        state1.emails_sent = [{"email": "test1"}]
        
        state2 = IncidentState()
        state2.emails_sent = [{"email": "test2"}]
        
        # Merge - emails_sent should be REPLACED, not extended
        state1.merge_from(state2)
        
        # Since emails_sent is in REPLACE_FIELDS, it should be replaced
        self.assertEqual(len(state1.emails_sent), 1, "Should replace, not extend")
        self.assertEqual(state1.emails_sent[0]["email"], "test2", "Should have new value")
        
        logger.info("✓ Smart merge logic tests passed")


def run_tests():
    """Run all tests"""
    logger.info("=" * 70)
    logger.info("AI-Powered Incident Response - Client Format Test Suite")
    logger.info("=" * 70)
    
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()

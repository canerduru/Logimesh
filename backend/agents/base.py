from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
import logging
import os
import json
from datetime import datetime

try:
    from backend.models.agent_state import AgentState
    from backend.utils.mock_llm import mock_claude_response
except ImportError:
    # Handle relative imports for different execution contexts
    try:
        from models.agent_state import AgentState
        from utils.mock_llm import mock_claude_response
    except ImportError:
        pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent:
    """
    Base class for all LogisticsMesh agents.
    Provides common infrastructure for LangGraph workflow creation and state management.
    """
    def __init__(self, company_id: str, agent_type: str, system_prompt: str = ""):
        self.company_id = company_id
        self.agent_type = agent_type
        self.system_prompt = system_prompt
        self.workflow = StateGraph(AgentState)
        self.dry_run = os.getenv("DRY_RUN", "false").lower() == "true"

        # Initialize the graph structure
        self._setup_graph()

    def _setup_graph(self):
        """
        Sets up the state machine graph with standard nodes.
        Subclasses can override or extend this.
        """
        # Define standard nodes
        self.workflow.add_node("IDLE", self.idle_node)
        self.workflow.add_node("SCANNING", self.scanning_node)
        self.workflow.add_node("NEGOTIATING", self.negotiating_node)
        self.workflow.add_node("EXECUTING", self.executing_node)
        self.workflow.add_node("COMPLETED", self.completed_node)

        # Define entry point
        self.workflow.set_entry_point("IDLE")

        # Define transitions
        self.workflow.add_conditional_edges(
            "IDLE",
            self.decide_next_step,
            {
                "SCANNING": "SCANNING",
                "NEGOTIATING": "NEGOTIATING",
                "EXECUTING": "EXECUTING",
                "COMPLETED": "COMPLETED",
                "IDLE": "IDLE"  # Loop back if nothing to do
            }
        )

        self.workflow.add_edge("SCANNING", "IDLE")
        self.workflow.add_edge("NEGOTIATING", "IDLE")
        self.workflow.add_edge("EXECUTING", "IDLE")
        self.workflow.add_edge("COMPLETED", END)

    def decide_next_step(self, state: AgentState) -> str:
        """
        Determines the next state based on current context.
        """
        # Default implementation: return the state's next field or IDLE
        if isinstance(state, dict):
            return state.get("next", "IDLE")
        return getattr(state, "next", "IDLE")

    # --- Node Implementations (to be overridden) ---

    async def idle_node(self, state: AgentState) -> Dict[str, Any]:
        """Default IDLE node implementation."""
        self.log_action("Agent is IDLE")
        # Logic to check for new tasks or messages could go here
        return {"current_status": "IDLE"}

    async def scanning_node(self, state: AgentState) -> Dict[str, Any]:
        """Default SCANNING node implementation."""
        self.log_action("Agent is SCANNING")
        return {"current_status": "SCANNING", "next": "IDLE"}

    async def negotiating_node(self, state: AgentState) -> Dict[str, Any]:
        """Default NEGOTIATING node implementation."""
        self.log_action("Agent is NEGOTIATING")
        return {"current_status": "NEGOTIATING", "next": "IDLE"}

    async def executing_node(self, state: AgentState) -> Dict[str, Any]:
        """Default EXECUTING node implementation."""
        self.log_action("Agent is EXECUTING")
        return {"current_status": "EXECUTING", "next": "IDLE"}

    async def completed_node(self, state: AgentState) -> Dict[str, Any]:
        """Default COMPLETED node implementation."""
        self.log_action("Agent task COMPLETED")
        return {"current_status": "COMPLETED"}

    # --- Helper Methods ---

    def transition_to(self, state_name: str, state_data: Dict[str, Any]):
        """Helper to transition to a new state."""
        state_data["next"] = state_name
        return state_data

    def log_action(self, action: str):
        """Logs an action to console and/or database."""
        timestamp = datetime.now().isoformat()
        log_message = f"[{timestamp}] [{self.agent_type}] [{self.company_id}] {action}"
        logger.info(log_message)
        # If not dry run, could log to DB
        if not self.dry_run:
            pass # TODO: Implement DB logging

    async def save_state_to_db(self, state: AgentState):
        """Persists the current state to the agent_states table."""
        if self.dry_run:
            self.log_action("Checking point state (DRY RUN)")
            return

        # TODO: Implement actual DB write using Supabase client
        # table('agent_states').upsert(...)
        pass

    def compile(self):
        """Compiles the workflow into an executable application."""
        return self.workflow.compile()

    async def invoke(self, inputs: Dict[str, Any]):
        """Runs the agent workflow with the given inputs."""
        app = self.compile()

        # Ensure required fields are in inputs
        if "company_id" not in inputs:
            inputs["company_id"] = self.company_id
        if "agent_type" not in inputs:
            inputs["agent_type"] = self.agent_type
        if "messages" not in inputs:
            inputs["messages"] = []

        return await app.ainvoke(inputs)

    def mock_decision(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Wrapper for the mock LLM call using this agent's system prompt."""
        return mock_claude_response(self.system_prompt, prompt, context)

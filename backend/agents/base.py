from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor

try:
    from backend.models.state import AgentState
    from backend.utils.mock_llm import mock_claude_response
except ImportError:
    # Handle relative imports for different execution contexts
    try:
        from models.state import AgentState
        from utils.mock_llm import mock_claude_response
    except ImportError:
        pass

class BaseAgent:
    """
    Base class for all LogisticsMesh agents.
    Provides common infrastructure for LangGraph workflow creation.
    """
    def __init__(self, company_id: str, agent_type: str):
        self.company_id = company_id
        self.agent_type = agent_type
        self.workflow = StateGraph(AgentState)
        self.system_prompt = ""

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

    def add_node(self, name: str, function):
        """Adds a node to the LangGraph workflow."""
        self.workflow.add_node(name, function)

    def set_entry_point(self, name: str):
        """Sets the entry point for the workflow."""
        self.workflow.set_entry_point(name)

    def add_edge(self, start: str, end: str):
        """Adds a direct edge between nodes."""
        self.workflow.add_edge(start, end)

    def add_conditional_edges(self, start: str, function, mapping: Dict[str, str]):
        """Adds conditional edges based on function output."""
        self.workflow.add_conditional_edges(start, function, mapping)

    def compile(self):
        """Compiles the workflow into an executable application."""
        return self.workflow.compile()

    async def invoke(self, inputs: Dict[str, Any]):
        """Runs the agent workflow with the given inputs."""
        app = self.compile()
        # Ensure company_id and agent_type are in the inputs
        if "company_id" not in inputs:
            inputs["company_id"] = self.company_id
        if "agent_type" not in inputs:
            inputs["agent_type"] = self.agent_type

        return await app.ainvoke(inputs)

    def mock_decision(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Wrapper for the mock LLM call using this agent's system prompt."""
        return mock_claude_response(self.system_prompt, prompt, context)

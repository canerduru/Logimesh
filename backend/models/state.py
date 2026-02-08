from typing import TypedDict, Annotated, List, Dict, Any, Union
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    Represents the state of an agent in the LangGraph workflow.
    """
    # The history of messages in the conversation
    messages: Annotated[List[BaseMessage], operator.add]

    # The next step/node to execute
    next: str

    # Contextual data (e.g., current load_id being negotiated, fleet status)
    context: Dict[str, Any]

    # The company this agent belongs to
    company_id: str

    # The type of agent (FLEET, LOAD, ROUTE, ORCHESTRATOR)
    agent_type: str

    # Internal memory for decision making
    memory: Dict[str, Any]

from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
import operator

class AgentState(BaseModel):
    """
    Represents the state of an agent in the LangGraph workflow.
    """
    messages: Annotated[List[BaseMessage], operator.add] = Field(default_factory=list)
    next: str = Field(default="IDLE")
    context: Dict[str, Any] = Field(default_factory=dict)
    company_id: str
    agent_type: str
    memory: Dict[str, Any] = Field(default_factory=dict)
    current_status: str = Field(default="IDLE", description="Current status of the agent (IDLE, SCANNING, etc.)")

    class Config:
        arbitrary_types_allowed = True

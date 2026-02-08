import pytest
from unittest.mock import AsyncMock, patch
from backend.agents.master_orchestrator import MasterOrchestrator
from backend.models.message import MessageType, AgentMessage

@pytest.mark.asyncio
async def test_orchestrator_initialization():
    agent = MasterOrchestrator()
    assert agent.agent_type == "ORCHESTRATOR"
    assert agent.active_negotiations == {}

@pytest.mark.asyncio
async def test_monitor_negotiation_start():
    """Test tracking a new negotiation."""
    agent = MasterOrchestrator()
    message = {
        "message_type": MessageType.NEGOTIATION_START,
        "conversation_id": "conv-1",
        "sender_id": "comp-A"
    }

    await agent.monitor_network_message(message)

    assert "conv-1" in agent.active_negotiations
    assert agent.active_negotiations["conv-1"]["status"] == "ACTIVE"
    assert agent.active_negotiations["conv-1"]["rounds"] == 0

@pytest.mark.asyncio
async def test_monitor_negotiation_round():
    """Test updating round count."""
    agent = MasterOrchestrator()
    agent.active_negotiations["conv-1"] = {"rounds": 0, "status": "ACTIVE", "last_update": None}

    message = {
        "message_type": MessageType.COUNTER_OFFER,
        "conversation_id": "conv-1",
        "sender_id": "comp-B"
    }

    await agent.monitor_network_message(message)

    assert agent.active_negotiations["conv-1"]["rounds"] == 1

@pytest.mark.asyncio
async def test_monitor_negotiation_complete():
    """Test completing a negotiation."""
    agent = MasterOrchestrator()
    agent.active_negotiations["conv-1"] = {"rounds": 2, "status": "ACTIVE"}

    message = {
        "message_type": MessageType.ACCEPT,
        "conversation_id": "conv-1",
        "sender_id": "comp-B"
    }

    await agent.monitor_network_message(message)

    assert agent.active_negotiations["conv-1"]["status"] == "COMPLETED"

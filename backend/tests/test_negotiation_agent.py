import pytest
from unittest.mock import AsyncMock, patch
from backend.agents.negotiation_agent import NegotiationAgent
from backend.models.message import AgentMessage, MessageType, NegotiationStartPayload, CounterOfferPayload

@pytest.mark.asyncio
async def test_negotiation_agent_initialization():
    agent = NegotiationAgent("comp-1")
    assert agent.agent_type == "NEGOTIATION_AGENT"

@pytest.mark.asyncio
async def test_initiate_negotiation(mocker):
    """Test initiating negotiation sends a message."""
    agent = NegotiationAgent("comp-1")
    mock_send = mocker.patch("backend.agents.negotiation_agent.send_message", new_callable=AsyncMock)

    conversation_id = await agent.initiate_negotiation(
        load_id="load-1",
        fleet_id="fleet-1",
        initial_price=1000.0
    )

    assert conversation_id is not None
    mock_send.assert_called_once()

    call_args = mock_send.call_args[0][0]
    assert call_args.message_type == MessageType.NEGOTIATION_START
    assert call_args.payload["initial_price"] == 1000.0

@pytest.mark.asyncio
async def test_process_negotiation_start(mocker):
    """Test processing an initial offer triggers a counter-offer."""
    agent = NegotiationAgent("comp-1")
    mock_send = mocker.patch("backend.agents.negotiation_agent.send_message", new_callable=AsyncMock)

    # Mock LLM to return COUNTER
    with patch.object(agent, "mock_decision", return_value={
        "decision": "COUNTER_OFFER",
        "counter_price": 1100.0,
        "reason": "Too low"
    }):
        message = AgentMessage(
            sender_id="comp-2",
            sender_agent_type="NEGOTIATION_AGENT",
            receiver_agent_type="NEGOTIATION_AGENT",
            message_type=MessageType.NEGOTIATION_START,
            payload={"load_id": "l1", "fleet_id": "f1", "initial_price": 1000.0},
            conversation_id="conv-1"
        )

        await agent.process_negotiation_message(message)

        mock_send.assert_called_once()
        response = mock_send.call_args[0][0]
        assert response.message_type == MessageType.COUNTER_OFFER
        assert response.payload["price"] == 1100.0

@pytest.mark.asyncio
async def test_process_agreement(mocker):
    """Test processing an ACCEPT decision."""
    agent = NegotiationAgent("comp-1")
    mock_send = mocker.patch("backend.agents.negotiation_agent.send_message", new_callable=AsyncMock)

    # Mock LLM to return ACCEPT
    with patch.object(agent, "mock_decision", return_value={
        "decision": "ACCEPT",
        "reason": "Good price"
    }):
        message = AgentMessage(
            sender_id="comp-2",
            sender_agent_type="NEGOTIATION_AGENT",
            receiver_agent_type="NEGOTIATION_AGENT",
            message_type=MessageType.COUNTER_OFFER,
            payload={"original_message_id": "orig", "price": 1000.0, "round_number": 2},
            conversation_id="conv-1"
        )

        await agent.process_negotiation_message(message)

        mock_send.assert_called_once()
        response = mock_send.call_args[0][0]
        assert response.message_type == MessageType.ACCEPT

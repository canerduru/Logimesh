import pytest
from unittest.mock import AsyncMock, patch
from backend.agents.fleet_agent import FleetAgent
from backend.models.core import Fleet, Load

@pytest.mark.asyncio
async def test_fleet_agent_initialization():
    agent = FleetAgent("comp-1")
    assert agent.company_id == "comp-1"
    assert agent.agent_type == "FLEET_AGENT"
    assert agent.dry_run is True

@pytest.mark.asyncio
async def test_scan_available_fleet_dry_run(mocker):
    """Test scanning fleets in DRY_RUN mode."""
    agent = FleetAgent("comp-1")
    fleets = await agent.scan_available_fleet()

    assert isinstance(fleets, list)
    assert len(fleets) > 0
    assert isinstance(fleets[0], Fleet)
    assert fleets[0].status == "IDLE"

@pytest.mark.asyncio
async def test_broadcast_capacity(mocker):
    """Test broadcasting capacity sends a message."""
    agent = FleetAgent("comp-1")
    fleet = Fleet(
        company_id="comp-1",
        vehicle_type="TestTruck",
        capacity_tons=10.0,
        current_location_lat=0.0,
        current_location_lng=0.0
    )

    # Mock send_message
    mock_send = mocker.patch("backend.agents.fleet_agent.send_message", new_callable=AsyncMock)
    mock_send.return_value = "msg-123"

    msg_id = await agent.broadcast_capacity(fleet)

    assert msg_id == "msg-123"
    mock_send.assert_called_once()

    # Check payload of the sent message
    call_args = mock_send.call_args[0][0] # First arg is the AgentMessage object
    assert call_args.sender_id == "comp-1"
    assert call_args.message_type == "CAPACITY_OFFER"
    assert call_args.payload["fleet_id"] == fleet.id

@pytest.mark.asyncio
async def test_evaluate_load_offers_accept(mocker):
    """Test evaluating a good load offer."""
    agent = FleetAgent("comp-1")

    offer = {
        "load_id": "load-1",
        "origin": "A",
        "destination": "B",
        "price_offered": 2000.0,
        "weight_tons": 10.0
    }

    # Mock mock_decision to return ACCEPT
    with patch.object(agent, "mock_decision", return_value={"decision": "ACCEPT", "reason": "Good price"}) as mock_dec:
        decision = await agent.evaluate_load_offers(offer)

        assert decision["decision"] == "ACCEPT"
        mock_dec.assert_called_once()
        # Verify context passed to mock_decision
        args, kwargs = mock_dec.call_args
        context = args[1] if len(args) > 1 else kwargs.get("context") # context is 2nd arg or kwarg
        assert context["load"] == offer

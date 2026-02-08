import pytest
from unittest.mock import AsyncMock, patch
from backend.agents.load_agent import LoadAgent
from backend.models.core import Load

@pytest.mark.asyncio
async def test_load_agent_initialization():
    agent = LoadAgent("comp-1")
    assert agent.company_id == "comp-1"
    assert agent.agent_type == "LOAD_AGENT"
    assert agent.dry_run is True

@pytest.mark.asyncio
async def test_scan_pending_loads_dry_run(mocker):
    """Test scanning loads in DRY_RUN mode."""
    agent = LoadAgent("comp-1")
    loads = await agent.scan_pending_loads()

    assert isinstance(loads, list)
    assert len(loads) > 0
    assert isinstance(loads[0], Load)
    assert loads[0].status == "PENDING"

@pytest.mark.asyncio
async def test_broadcast_load_request(mocker):
    """Test broadcasting load request sends a message."""
    agent = LoadAgent("comp-1")
    load = Load(
        company_id="comp-1",
        origin_lat=0.0,
        origin_lng=0.0,
        destination_lat=10.0,
        destination_lng=10.0,
        weight_tons=10.0,
        deadline="2023-12-31T23:59:59",
        price_offered=1000.0
    )

    # Mock send_message
    mock_send = mocker.patch("backend.agents.load_agent.send_message", new_callable=AsyncMock)
    mock_send.return_value = "msg-456"

    msg_id = await agent.broadcast_load_request(load)

    assert msg_id == "msg-456"
    mock_send.assert_called_once()

    # Check payload
    call_args = mock_send.call_args[0][0]
    assert call_args.sender_id == "comp-1"
    assert call_args.message_type == "LOAD_REQUEST"
    assert call_args.payload["load_id"] == load.id

@pytest.mark.asyncio
async def test_evaluate_fleet_offers(mocker):
    """Test evaluating fleet offers."""
    agent = LoadAgent("comp-1")

    offers = [
        {"fleet_id": "f1", "price": 1000},
        {"fleet_id": "f2", "price": 1200}
    ]

    # Mock mock_decision
    with patch.object(agent, "mock_decision", return_value={"ranked_carriers": ["f1", "f2"], "reason": "Price"}) as mock_dec:
        decision = await agent.evaluate_fleet_offers(offers)

        assert decision["ranked_carriers"] == ["f1", "f2"]
        mock_dec.assert_called_once()
        # Verify context
        args, kwargs = mock_dec.call_args
        context = args[1] if len(args) > 1 else kwargs.get("context")
        assert context["offers"] == offers

from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime

try:
    from backend.agents.base import BaseAgent
    from backend.models.core import Fleet, Load
    from backend.models.message import AgentMessage, MessageType, CapacityOfferPayload
    from backend.utils.message_router import send_message, subscribe_to_messages
    from backend.models.agent_state import AgentState
except ImportError:
    from agents.base import BaseAgent
    from models.core import Fleet, Load
    from models.message import AgentMessage, MessageType, CapacityOfferPayload
    from utils.message_router import send_message, subscribe_to_messages
    from models.agent_state import AgentState

class FleetAgent(BaseAgent):
    """
    Fleet Agent responsible for managing vehicle capacity and responding to load offers.
    """
    def __init__(self, company_id: str, system_prompt: str = ""):
        super().__init__(company_id=company_id, agent_type="FLEET_AGENT", system_prompt=system_prompt)

    async def scan_available_fleet(self) -> List[Fleet]:
        """
        Scans for idle trucks in the fleet.
        In DRY_RUN mode, returns mock data.
        """
        self.log_action("Scanning for available fleet...")

        if self.dry_run:
            # Return mock fleets
            mock_fleets = [
                Fleet(
                    company_id=self.company_id,
                    vehicle_type="Tautliner",
                    capacity_tons=24.0,
                    current_location_lat=52.5200, # Berlin
                    current_location_lng=13.4050,
                    status="IDLE"
                ),
                Fleet(
                    company_id=self.company_id,
                    vehicle_type="Refrigerated",
                    capacity_tons=20.0,
                    current_location_lat=48.1351, # Munich
                    current_location_lng=11.5820,
                    status="IDLE"
                )
            ]
            self.log_action(f"Found {len(mock_fleets)} mock idle trucks.")
            return mock_fleets

        # TODO: Implement Supabase query
        # data = supabase.table("fleets").select("*").eq("company_id", self.company_id).eq("status", "IDLE").execute()
        return []

    async def broadcast_capacity(self, fleet: Fleet) -> str:
        """
        Broadcasts available capacity to the network.
        """
        payload = CapacityOfferPayload(
            fleet_id=fleet.id,
            vehicle_type=fleet.vehicle_type,
            capacity_tons=fleet.capacity_tons,
            current_location={"lat": fleet.current_location_lat, "lng": fleet.current_location_lng},
            available_from=fleet.available_from.isoformat(),
            status=fleet.status
        )

        message = AgentMessage(
            sender_id=self.company_id,
            sender_agent_type=self.agent_type,
            receiver_agent_type="LOAD_AGENT", # Broadcast to all load agents? Or specific channel?
            message_type=MessageType.CAPACITY_OFFER,
            payload=payload.model_dump()
        )

        msg_id = await send_message(message)
        self.log_action(f"Broadcasted capacity for fleet {fleet.id} (Msg ID: {msg_id})")
        return msg_id

    async def evaluate_load_offers(self, offer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates an incoming load offer using the LLM.
        """
        # Construct context for the LLM
        context = {
            "load": offer,
            "fleet": {
                "capacity_tons": 24.0, # Using a generic fleet capacity for evaluation if specific fleet not matched yet
                # ideally we match against a specific fleet, but for now generic evaluation
            }
        }

        prompt = f"Evaluate load offer: Origin {offer.get('origin')}, Dest {offer.get('destination')}, Price {offer.get('price_offered')}"
        decision = self.mock_decision(prompt, context)

        self.log_action(f"Evaluated offer: {decision['decision']} - {decision.get('reason')}")
        return decision

    # --- Node Overrides ---

    async def scanning_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Override SCANNING node to scan fleets and broadcast.
        """
        self.log_action("Executing SCANNING logic...")
        fleets = await self.scan_available_fleet()

        # Broadcast all found fleets
        for fleet in fleets:
            await self.broadcast_capacity(fleet)

        return {"current_status": "SCANNING", "next": "IDLE"}

    async def idle_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Override IDLE node to listen for messages (simulated).
        """
        self.log_action("Fleet Agent IDLE - Listening for offers...")
        # In a real agent, this might wait for an event.
        # For LangGraph, we just return status.
        return {"current_status": "IDLE"}

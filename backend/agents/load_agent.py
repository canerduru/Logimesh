from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime

try:
    from backend.agents.base import BaseAgent
    from backend.models.core import Fleet, Load
    from backend.models.message import AgentMessage, MessageType, LoadRequestPayload
    from backend.utils.message_router import send_message, subscribe_to_messages
    from backend.models.agent_state import AgentState
except ImportError:
    from agents.base import BaseAgent
    from models.core import Fleet, Load
    from models.message import AgentMessage, MessageType, LoadRequestPayload
    from utils.message_router import send_message, subscribe_to_messages
    from models.agent_state import AgentState

class LoadAgent(BaseAgent):
    """
    Load Agent responsible for managing pending shipments and finding suitable carriers.
    """
    def __init__(self, company_id: str, system_prompt: str = ""):
        super().__init__(company_id=company_id, agent_type="LOAD_AGENT", system_prompt=system_prompt)

    async def scan_pending_loads(self) -> List[Load]:
        """
        Scans for pending loads.
        In DRY_RUN mode, returns mock data.
        """
        self.log_action("Scanning for pending loads...")

        if self.dry_run:
            mock_loads = [
                Load(
                    company_id=self.company_id,
                    origin_lat=52.5200, # Berlin
                    origin_lng=13.4050,
                    destination_lat=48.8566, # Paris
                    destination_lng=2.3522,
                    weight_tons=18.5,
                    deadline=datetime.now(),
                    status="PENDING",
                    price_offered=1200.0
                )
            ]
            self.log_action(f"Found {len(mock_loads)} mock pending loads.")
            return mock_loads

        # TODO: Implement Supabase query
        return []

    async def broadcast_load_request(self, load: Load) -> str:
        """
        Broadcasts a load request to the network.
        """
        payload = LoadRequestPayload(
            load_id=load.id,
            origin={"lat": load.origin_lat, "lng": load.origin_lng},
            destination={"lat": load.destination_lat, "lng": load.destination_lng},
            weight_tons=load.weight_tons,
            deadline=load.deadline.isoformat(),
            price_offered=load.price_offered
        )

        message = AgentMessage(
            sender_id=self.company_id,
            sender_agent_type=self.agent_type,
            receiver_agent_type="FLEET_AGENT", # Broadcast to fleet agents
            message_type=MessageType.LOAD_REQUEST,
            payload=payload.model_dump()
        )

        msg_id = await send_message(message)
        self.log_action(f"Broadcasted request for load {load.id} (Msg ID: {msg_id})")
        return msg_id

    async def evaluate_fleet_offers(self, offers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates incoming fleet capacity offers.
        """
        context = {
            "offers": offers
        }

        prompt = f"Evaluate {len(offers)} fleet offers and rank carriers."
        decision = self.mock_decision(prompt, context)

        self.log_action(f"Ranked carriers: {decision.get('ranked_carriers')}")
        return decision

    # --- Node Overrides ---

    async def scanning_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Override SCANNING node to scan loads and broadcast.
        """
        self.log_action("Executing SCANNING logic...")
        loads = await self.scan_pending_loads()

        for load in loads:
            await self.broadcast_load_request(load)

        return {"current_status": "SCANNING", "next": "IDLE"}

    async def idle_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Override IDLE node.
        """
        self.log_action("Load Agent IDLE - Waiting for capacity offers...")
        return {"current_status": "IDLE"}

import asyncio
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from backend.agents.base import BaseAgent
    from backend.models.message import AgentMessage, MessageType, NegotiationStartPayload, CounterOfferPayload
    from backend.utils.message_router import send_message
    from backend.models.agent_state import AgentState
except ImportError:
    from agents.base import BaseAgent
    from models.message import AgentMessage, MessageType, NegotiationStartPayload, CounterOfferPayload
    from utils.message_router import send_message
    from models.agent_state import AgentState

class NegotiationAgent(BaseAgent):
    """
    Agent responsible for negotiating price and terms.
    It manages the conversation flow, generates counter-offers, and decides when to accept or walk away.
    """
    def __init__(self, company_id: str, system_prompt: str = ""):
        super().__init__(company_id=company_id, agent_type="NEGOTIATION_AGENT", system_prompt=system_prompt)
        # In a real implementation, we might track active negotiations here or in DB
        self.active_negotiations = {}

    async def initiate_negotiation(self, load_id: str, fleet_id: str, initial_price: float, receiver_agent_type: str = "NEGOTIATION_AGENT"):
        """
        Starts a new negotiation thread.
        """
        conversation_id = str(uuid.uuid4())
        self.log_action(f"Initiating negotiation for load {load_id} with fleet {fleet_id} at {initial_price}")

        payload = NegotiationStartPayload(
            load_id=load_id,
            fleet_id=fleet_id,
            initial_price=initial_price,
            terms="Standard Terms"
        )

        message = AgentMessage(
            sender_id=self.company_id,
            sender_agent_type=self.agent_type,
            receiver_agent_type=receiver_agent_type,
            message_type=MessageType.NEGOTIATION_START,
            payload=payload.model_dump(),
            conversation_id=conversation_id
        )

        await send_message(message)
        return conversation_id

    async def generate_counter_offer(self, incoming_offer: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a counter-offer or decision (ACCEPT/REJECT) using the LLM.
        """
        # Context for LLM
        prompt = (
            f"You are negotiating for load {context.get('load_id')}. "
            f"Current offer is {incoming_offer.get('price')}. "
            f"Your target price is {context.get('target_price')}. "
            f"This is round {context.get('round', 1)} of 5. "
            "Decide to ACCEPT, REJECT, or COUNTER."
        )

        # Mock LLM decision
        decision = self.mock_decision(prompt, {
            "current_price": incoming_offer.get('price'),
            "target_price": context.get('target_price'),
            "round": context.get('round', 1)
        })

        self.log_action(f"Generated negotiation response: {decision['decision']}")
        return decision

    async def process_negotiation_message(self, message: Any):
        """
        Main handler for incoming negotiation messages.
        """
        # Handle dict input (from local router)
        if isinstance(message, dict):
            try:
                message = AgentMessage(**message)
            except Exception as e:
                self.log_action(f"Failed to parse message: {e}")
                return

        msg_type = message.message_type
        payload = message.payload
        conversation_id = message.conversation_id

        self.log_action(f"Processing {msg_type} for conversation {conversation_id}")

        if msg_type == MessageType.NEGOTIATION_START:
            # Received an initial offer, decide how to respond
            initial_price = payload.get("initial_price")
            # For demo, let's assume we are the seller (Fleet) and want 10% more
            target_price = initial_price * 1.10

            decision = await self.generate_counter_offer(
                {"price": initial_price},
                {"target_price": target_price, "round": 1, "load_id": payload.get("load_id")}
            )

            await self._send_response(decision, message, round_number=1)

        elif msg_type == MessageType.COUNTER_OFFER:
            # Received a counter-offer
            current_price = payload.get("price")
            round_number = payload.get("round_number", 1)

            # Use mock logic to decide response
            # Strategy: if price is close enough (within 5%), accept. Else counter.
            # Unless round > 5, then force decision.

            target_price = current_price * 0.95 # Buyer wants lower

            decision = await self.generate_counter_offer(
                {"price": current_price},
                {"target_price": target_price, "round": round_number + 1, "load_id": "unknown"}
            )

            await self._send_response(decision, message, round_number=round_number + 1)

        elif msg_type == MessageType.ACCEPT:
             self.log_action(f"Negotiation {conversation_id} SUCCESS: Deal accepted!")
             # Trigger transaction finalization (in Phase 3.4)

        elif msg_type == MessageType.REJECT:
             self.log_action(f"Negotiation {conversation_id} FAILED: Offer rejected.")

    async def _send_response(self, decision: Dict[str, Any], original_message: AgentMessage, round_number: int):
        """Helper to send the decision back."""

        response_type = MessageType.COUNTER_OFFER
        payload = {}

        if decision["decision"] == "ACCEPT":
            response_type = MessageType.ACCEPT
            payload = {"original_message_id": original_message.id, "reason": decision.get("reason")}

        elif decision["decision"] == "REJECT":
            response_type = MessageType.REJECT
            payload = {"original_message_id": original_message.id, "reason": decision.get("reason")}

        else: # COUNTER_OFFER
            response_type = MessageType.COUNTER_OFFER
            payload = {
                "original_message_id": original_message.id,
                "price": decision.get("counter_price"),
                "reason": decision.get("reason"),
                "round_number": round_number
            }

        msg = AgentMessage(
            sender_id=self.company_id,
            sender_agent_type=self.agent_type,
            receiver_agent_type=original_message.sender_agent_type, # Reply to sender
            message_type=response_type,
            payload=payload,
            conversation_id=original_message.conversation_id
        )

        await send_message(msg)

    # --- Node Overrides ---

    async def negotiating_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Active negotiation state.
        """
        # In a real implementation, this might poll for active threads needing attention
        self.log_action("Negotiation Agent active - monitoring threads...")
        return {"current_status": "NEGOTIATING", "next": "IDLE"}

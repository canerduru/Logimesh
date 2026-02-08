import asyncio
from typing import Dict, Any, List
from datetime import datetime

try:
    from backend.agents.base import BaseAgent
    from backend.models.agent_state import AgentState
    from backend.models.message import MessageType, AgentMessage
except ImportError:
    from agents.base import BaseAgent
    from models.agent_state import AgentState
    from models.message import MessageType, AgentMessage

class MasterOrchestrator(BaseAgent):
    """
    System-level agent responsible for network optimization and deadlock resolution.
    """
    def __init__(self, company_id: str = "SYSTEM", system_prompt: str = ""):
        super().__init__(company_id=company_id, agent_type="ORCHESTRATOR", system_prompt=system_prompt)
        self.active_negotiations = {} # conversation_id -> {start_time, last_update, rounds}

    async def monitor_network_message(self, message: Dict[str, Any]):
        """
        Callback for listening to all network traffic.
        """
        msg_type = message.get("message_type")
        conversation_id = message.get("conversation_id")

        if not conversation_id:
            return

        # Track negotiation progress
        if msg_type == MessageType.NEGOTIATION_START:
            self.active_negotiations[conversation_id] = {
                "start_time": datetime.now(),
                "last_update": datetime.now(),
                "rounds": 0,
                "status": "ACTIVE"
            }
            self.log_action(f"Tracking new negotiation {conversation_id}")

        elif msg_type in [MessageType.COUNTER_OFFER, MessageType.NEGOTIATION_ROUND]:
            if conversation_id in self.active_negotiations:
                self.active_negotiations[conversation_id]["rounds"] += 1
                self.active_negotiations[conversation_id]["last_update"] = datetime.now()

                # Check for deadlock (e.g., > 10 rounds)
                if self.active_negotiations[conversation_id]["rounds"] > 10:
                    await self.force_resolution(conversation_id)

        elif msg_type in [MessageType.AGREEMENT_REACHED, MessageType.NEGOTIATION_FAILED, MessageType.ACCEPT, MessageType.REJECT]:
            if conversation_id in self.active_negotiations:
                self.active_negotiations[conversation_id]["status"] = "COMPLETED"
                self.log_action(f"Negotiation {conversation_id} completed.")

    async def detect_deadlocks(self):
        """
        Periodically checks for stuck negotiations.
        """
        self.log_action("Scanning for deadlocks...")
        now = datetime.now()

        for conv_id, data in self.active_negotiations.items():
            if data["status"] != "ACTIVE":
                continue

            # If idle for > 5 minutes (mock: > 5 seconds for demo)
            time_diff = (now - data["last_update"]).total_seconds()
            if time_diff > 300: # 5 minutes real time
                self.log_action(f"Deadlock detected in {conv_id} (Idle {time_diff}s)")
                # In real system, trigger intervention

    async def force_resolution(self, conversation_id: str):
        """
        Intervenes in a stuck negotiation.
        """
        self.log_action(f"Forcing resolution for {conversation_id}")
        # Logic to send a SYSTEM_OVERRIDE message or similar
        pass

    # --- Node Overrides ---

    async def executing_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Orchestrator periodic tasks.
        """
        await self.detect_deadlocks()
        return {"current_status": "EXECUTING", "next": "IDLE"}

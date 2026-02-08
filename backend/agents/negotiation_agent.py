from typing import Dict, Any
try:
    from backend.agents.base import BaseAgent
except ImportError:
    from agents.base import BaseAgent

class NegotiationAgent(BaseAgent):
    """
    Agent responsible for negotiating price and terms.
    """
    def __init__(self, company_id: str, system_prompt: str = ""):
        super().__init__(company_id=company_id, agent_type="NEGOTIATION_AGENT", system_prompt=system_prompt)

    async def initiate_negotiation(self, load_id: str, fleet_id: str):
        self.log_action(f"Initiating negotiation for load {load_id} with fleet {fleet_id}")
        pass

    async def generate_counter_offer(self, offer: Dict[str, Any]):
        pass

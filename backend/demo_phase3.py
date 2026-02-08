import asyncio
import os
import logging
import json
from datetime import datetime

# Set DRY_RUN to true for the demo
os.environ["DRY_RUN"] = "true"

try:
    from backend.agents.fleet_agent import FleetAgent
    from backend.agents.load_agent import LoadAgent
    from backend.agents.negotiation_agent import NegotiationAgent
    from backend.agents.master_orchestrator import MasterOrchestrator
    from backend.utils.message_router import subscribe_to_messages
    from backend.models.message import MessageType
    from backend.utils.transaction_manager import create_transaction, finalize_transaction
except ImportError:
    from agents.fleet_agent import FleetAgent
    from agents.load_agent import LoadAgent
    from agents.negotiation_agent import NegotiationAgent
    from agents.master_orchestrator import MasterOrchestrator
    from utils.message_router import subscribe_to_messages
    from models.message import MessageType
    from utils.transaction_manager import create_transaction, finalize_transaction

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("DEMO_P3")

async def run_demo():
    print("\n" + "="*50)
    print("LOGISTICSMESH PHASE 3 DEMO: NEGOTIATION & ORCHESTRATION")
    print("="*50 + "\n")

    # 1. Initialize Agents
    logger.info("Initializing Agents...")
    fleet_agent = FleetAgent(company_id="comp-A", system_prompt="You are a Fleet Manager for Company A.")
    load_agent = LoadAgent(company_id="comp-B", system_prompt="You are a Logistics Manager for Company B.")

    # Negotiation agents (one for each party, or a shared mediator?
    # Plan says 'Negotiation Agent' (singular class), but logically each company has one.
    # For simplicity, we'll instantiate one for the Buyer (Load) side to negotiate with the Seller (Fleet).
    # Wait, the plan implies a dedicated agent type. Let's assume the Load Agent hands off to a Negotiation Agent.

    negotiation_agent_B = NegotiationAgent(company_id="comp-B", system_prompt="Negotiate best price for load.")
    negotiation_agent_A = NegotiationAgent(company_id="comp-A", system_prompt="Get best price for fleet.")

    orchestrator = MasterOrchestrator()

    # Shared state for demo flow control
    demo_state = {"load_id": "load-123", "fleet_id": "fleet-456", "transaction_id": None}

    # 2. Setup Message Handling

    async def handle_negotiation_messages(message: dict):
        """Callback for negotiation messages."""
        msg_type = message.get("message_type")
        sender = message.get("sender_id")
        receiver = message.get("receiver_id")
        payload = message.get("payload")

        # Log for Orchestrator
        await orchestrator.monitor_network_message(message)

        # Simulate Agent Responses
        if msg_type == MessageType.NEGOTIATION_START:
            logger.info(f"[NEGOTIATION START] {sender} proposed {payload.get('initial_price')}")
            # Seller (A) receives offer from Buyer (B)
            # Agent A processes it
            await negotiation_agent_A.process_negotiation_message(message) # This will trigger COUNTER or ACCEPT

        elif msg_type == MessageType.COUNTER_OFFER:
            price = payload.get("price")
            logger.info(f"[COUNTER OFFER] {sender} counters with {price}")

            # If A sent counter, B processes it. If B sent counter, A processes it.
            if sender == "comp-A":
                await negotiation_agent_B.process_negotiation_message(message)
            else:
                await negotiation_agent_A.process_negotiation_message(message)

        elif msg_type == MessageType.ACCEPT:
            logger.info(f"[AGREEMENT] {sender} ACCEPTED the offer!")
            # Trigger Transaction
            tx_id = await create_transaction(
                load_id=demo_state["load_id"],
                fleet_id=demo_state["fleet_id"],
                final_price=1500.0, # Mock price
                carrier_id="comp-A",
                shipper_id="comp-B"
            )
            demo_state["transaction_id"] = tx_id
            await finalize_transaction(tx_id, success=True)

        elif msg_type == MessageType.REJECT:
            logger.info(f"[FAILURE] {sender} REJECTED the offer.")

    # Subscribe agents
    subscribe_to_messages("NEGOTIATION_AGENT", handle_negotiation_messages)
    # Orchestrator subscribes to everything (simulated via manual call in callback above)

    # 3. Start Scenario
    print("\n--- STEP 1: INITIATE NEGOTIATION ---\n")

    # Load Agent (comp-B) has found a fleet (comp-A) and wants to negotiate.
    # It delegates to its Negotiation Agent.

    initial_price = 1000.0
    await negotiation_agent_B.initiate_negotiation(
        load_id=demo_state["load_id"],
        fleet_id=demo_state["fleet_id"],
        initial_price=initial_price,
        receiver_agent_type="NEGOTIATION_AGENT" # Targeting Agent A's negotiator
    )

    # The message loop is async. In this script, we need to let the event loop process.
    # Since we are using a local in-memory router (utils/message_router.py) which awaits callbacks,
    # the 'initiate_negotiation' call will trigger the chain reaction if properly wired.
    # However, 'process_negotiation_message' is async and calls 'send_message'.

    # Let's wait a bit to ensure potential async tasks complete
    await asyncio.sleep(2)

    print("\n" + "="*50)
    print("DEMO COMPLETE")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(run_demo())

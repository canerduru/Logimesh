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
    from backend.utils.message_router import subscribe_to_messages
    from backend.models.message import MessageType
except ImportError:
    from agents.fleet_agent import FleetAgent
    from agents.load_agent import LoadAgent
    from utils.message_router import subscribe_to_messages
    from models.message import MessageType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("DEMO")

async def run_demo():
    print("\n" + "="*50)
    print("LOGISTICSMESH PHASE 2 DEMO: AGENT-TO-AGENT COMMUNICATION")
    print("="*50 + "\n")

    # 1. Initialize Agents
    logger.info("Initializing Agents...")
    fleet_agent = FleetAgent(company_id="comp-A", system_prompt="You are a Fleet Manager for Company A.")
    load_agent = LoadAgent(company_id="comp-B", system_prompt="You are a Logistics Manager for Company B.")

    # 2. Setup Message Handling
    async def handle_fleet_message(message: dict):
        """Callback for messages sent TO Fleet Agent."""
        msg_type = message.get("message_type")
        sender = message.get("sender_id")
        logger.info(f"FleetAgent received {msg_type} from {sender}")

        if msg_type == MessageType.LOAD_REQUEST:
            logger.info("FleetAgent evaluating load request...")
            # Extract payload (Load details)
            payload = message.get("payload")
            # In real scenario, payload needs to be mapped to what evaluate expects
            # evaluate_load_offers expects 'offer' dict
            decision = await fleet_agent.evaluate_load_offers(payload)
            print(f"\n[FLEET DECISION] {decision}\n")

    async def handle_load_message(message: dict):
        """Callback for messages sent TO Load Agent."""
        msg_type = message.get("message_type")
        sender = message.get("sender_id")
        logger.info(f"LoadAgent received {msg_type} from {sender}")

        if msg_type == MessageType.CAPACITY_OFFER:
            logger.info("LoadAgent evaluating capacity offer...")
            payload = message.get("payload")
            # evaluate_fleet_offers expects list of offers
            decision = await load_agent.evaluate_fleet_offers([payload])
            print(f"\n[LOAD AGENT DECISION] {decision}\n")

    # Subscribe agents to the message bus
    subscribe_to_messages("FLEET_AGENT", handle_fleet_message)
    subscribe_to_messages("LOAD_AGENT", handle_load_message)

    # 3. Scenario 1: Fleet Agent Broadcasts Capacity
    print("\n--- SCENARIO 1: FLEET BROADCAST ---\n")
    # Trigger Fleet Agent to scan and broadcast
    # We can invoke the graph or call method directly. Calling method directly for clarity in demo.
    await fleet_agent.scan_available_fleet()
    # Note: scan_available_fleet in implementation calls broadcast_capacity if invoked via node,
    # but the method itself just returns fleets.
    # Wait, let's check fleet_agent.py.
    # scan_available_fleet returns fleets. scanning_node calls broadcast_capacity.
    # So let's invoke the agent via graph or call the node logic manually.

    # Let's call scanning_node manually for the demo to trigger the broadcast
    await fleet_agent.scanning_node({})

    # 4. Scenario 2: Load Agent Broadcasts Request
    print("\n--- SCENARIO 2: LOAD REQUEST ---\n")
    # Similarly, call scanning_node on load agent
    await load_agent.scanning_node({})

    print("\n" + "="*50)
    print("DEMO COMPLETE")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(run_demo())

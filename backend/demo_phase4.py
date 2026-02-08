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
    from backend.agents.route_simulation_agent import RouteSimulationAgent
except ImportError:
    from agents.fleet_agent import FleetAgent
    from agents.load_agent import LoadAgent
    from agents.route_simulation_agent import RouteSimulationAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("DEMO_P4")

async def run_demo():
    print("\n" + "="*50)
    print("LOGISTICSMESH PHASE 4 DEMO: ROUTE SIMULATION & RISK ANALYSIS")
    print("="*50 + "\n")

    # 1. Initialize Agents
    logger.info("Initializing Agents...")
    fleet_agent = FleetAgent(company_id="comp-A", system_prompt="You are a data-driven Fleet Manager.")

    # 2. Define Scenarios
    scenarios = [
        {
            "name": "High Profit / Low Risk Route",
            "load": {
                "load_id": "L-001",
                "origin": "Berlin",
                "destination": "Munich", # Popular route
                "price_offered": 2500.0,
                "weight_tons": 18.0
            }
        },
        {
            "name": "Low Profit / High Risk Route",
            "load": {
                "load_id": "L-002",
                "origin": "Berlin",
                "destination": "Remote_Village_In_Mountains", # Unlikely return load
                "price_offered": 800.0, # Low price
                "weight_tons": 10.0
            }
        }
    ]

    # 3. Run Simulations
    for scenario in scenarios:
        print(f"\n--- SCENARIO: {scenario['name']} ---")
        load_offer = scenario["load"]

        logger.info(f"Fleet Agent evaluating offer: {load_offer['origin']} -> {load_offer['destination']} @ {load_offer['price_offered']} EUR")

        # This call will internally trigger the RouteSimulationAgent
        decision = await fleet_agent.evaluate_load_offers(load_offer)

        print(f"\n[FLEET DECISION] {decision['decision']}")
        print(f"[REASONING] {decision.get('reason')}")
        if 'confidence' in decision:
            print(f"[CONFIDENCE] {decision['confidence']}")

        print("-" * 30)

    print("\n" + "="*50)
    print("DEMO COMPLETE")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(run_demo())

import asyncio
import random
import math
from typing import Dict, Any, List
from datetime import datetime

try:
    from backend.agents.base import BaseAgent
    from backend.models.core import RouteSimulation
except ImportError:
    from agents.base import BaseAgent
    from models.core import RouteSimulation

class RouteSimulationAgent(BaseAgent):
    """
    Agent responsible for simulating route profitability and risk.
    Uses Monte Carlo simulation to estimate outcomes under uncertainty.
    """
    def __init__(self, company_id: str, system_prompt: str = ""):
        super().__init__(company_id=company_id, agent_type="ROUTE_AGENT", system_prompt=system_prompt)

    async def simulate_route(self, origin: str, destination: str, offered_price: float, vehicle_type: str = "Tautliner") -> RouteSimulation:
        """
        Runs a simulation for a specific route and offered price.
        """
        self.log_action(f"Simulating route: {origin} -> {destination} for {offered_price} EUR")

        # 1. Determine Base Metrics (Mock distance calculation for now)
        # In real implementation, call Google Maps API
        # Mock: Assume distance based on string length hash or random for demo consistency
        random.seed(origin + destination) # Deterministic for same route
        distance_km = random.randint(300, 1200)
        duration_hours = distance_km / 70.0 # Avg speed 70km/h

        # 2. Base Costs
        fuel_consumption_per_km = 0.30 if vehicle_type == "Tautliner" else 0.35
        fuel_price_per_liter = 1.70
        toll_per_km = 0.18
        driver_wage_per_hour = 25.0

        base_fuel_cost = distance_km * fuel_consumption_per_km * fuel_price_per_liter
        base_toll_cost = distance_km * toll_per_km
        base_driver_cost = duration_hours * driver_wage_per_hour

        # 3. Monte Carlo Simulation (1000 iterations)
        # Variables: Fuel Price (+/- 10%), Traffic/Duration (+/- 20%), Return Load Prob (0-100%)
        profits = []
        return_load_probs = []

        for _ in range(1000):
            # Randomized factors
            sim_fuel_price = fuel_price_per_liter * random.uniform(0.9, 1.1)
            sim_duration = duration_hours * random.uniform(0.8, 1.2)

            # Simulated Costs
            sim_fuel_cost = distance_km * fuel_consumption_per_km * sim_fuel_price
            sim_driver_cost = sim_duration * driver_wage_per_hour
            sim_total_cost = sim_fuel_cost + base_toll_cost + sim_driver_cost

            # Return Load Logic:
            # If we find a return load, we allocate costs differently or assume extra profit.
            # Simplified: If return load found (prob based on destination "popularity"), profit increases.

            # Destination popularity mock
            dest_score = random.random() # 0.0 to 1.0
            return_load_found = dest_score > 0.4 # 60% chance of return load
            return_load_probs.append(1 if return_load_found else 0)

            revenue = offered_price
            if return_load_found:
                # Assume return load covers return trip costs + 10% margin
                revenue += (sim_total_cost * 1.1)
                # But we also incur return trip costs
                sim_total_cost *= 2
            else:
                # Empty return - cost doubles (round trip)
                sim_total_cost *= 2

            profit = revenue - sim_total_cost
            profits.append(profit)

        # 4. Analysis
        avg_profit = sum(profits) / len(profits)
        avg_return_prob = sum(return_load_probs) / len(return_load_probs)

        # Risk Score: Calculate standard deviation of profit relative to average
        # Higher variance = Higher Risk. Also low return prob = High Risk.

        variance = sum((p - avg_profit) ** 2 for p in profits) / len(profits)
        std_dev = math.sqrt(variance)

        # Normalize risk 0-100
        # If std_dev is high compared to profit, risky.
        # If profit is negative, extremely risky (100).

        if avg_profit <= 0:
            risk_score = 95.0
        else:
            risk_ratio = std_dev / avg_profit
            risk_score = min(100.0, risk_ratio * 50 + (1 - avg_return_prob) * 30)

        # Create Result Object
        simulation = RouteSimulation(
            origin=origin,
            destination=destination,
            distance_km=distance_km,
            estimated_duration_hours=duration_hours,
            fuel_cost=base_fuel_cost,
            toll_cost=base_toll_cost,
            driver_cost=base_driver_cost,
            total_cost=base_fuel_cost + base_toll_cost + base_driver_cost,
            expected_revenue=offered_price,
            projected_profit=avg_profit, # This is the Monte Carlo average
            profit_margin=(avg_profit / offered_price) * 100 if offered_price > 0 else 0,
            risk_score=risk_score,
            return_load_probability=avg_return_prob,
            scenarios_run=1000
        )

        self.log_action(f"Simulation complete. Profit: {avg_profit:.2f}, Risk: {risk_score:.2f}")
        return simulation

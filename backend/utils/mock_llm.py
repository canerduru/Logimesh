import json
import random
from typing import Dict, Any, List

def mock_claude_response(system_prompt: str, user_prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Simulates a structured response from Anthropic Claude.
    """

    # Analyze prompt keywords to return context-aware mock responses
    prompt_lower = user_prompt.lower()

    # Negotiation Logic (Phase 3)
    if "negotiate" in prompt_lower or "round" in prompt_lower:
        return _mock_negotiation_logic(context)

    # Fleet Decision Logic (Phase 4 Update: Accept/Reject based on Simulation)
    if "evaluate load offer" in prompt_lower or "capacity" in prompt_lower:
        return _mock_fleet_decision(context)

    # Load Decision Logic (Select carrier)
    elif "evaluate fleet offers" in prompt_lower or "rank carriers" in prompt_lower:
        return _mock_load_decision(context)

    # Route Simulation NARRATIVE Logic (Phase 4)
    elif "simulation" in prompt_lower or "report" in prompt_lower:
        return _mock_simulation_narrative(context)

    # Route Simulation Data Logic (Phase 4 - Risk Analysis)
    elif "route" in prompt_lower or "simulate" in prompt_lower:
        # If this is called by Route Agent directly (though Route Agent logic is mostly Python now)
        return {
            "profitability_score": round(random.uniform(0.6, 0.95), 2),
            "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "recommendation": random.choice(["OPEN", "WAIT", "REJECT"]),
            "reasoning": "Fuel costs are stable, but return load probability is low."
        }

    # Default fallback
    return {
        "action": "UNKNOWN",
        "message": "I understood the request but have no specific mock logic for it."
    }

def _mock_simulation_narrative(context: Dict[str, Any]) -> Dict[str, Any]:
    """Generates a text summary of the route simulation."""
    if not context:
        return {"summary": "No context provided."}

    profit = context.get("projected_profit", 0)
    risk = context.get("risk_score", 50)

    if profit > 500 and risk < 30:
        return {
            "summary": "This route is highly profitable with low risk. Return loads are likely.",
            "recommendation": "PRIORITY_ACCEPT"
        }
    elif profit > 0 and risk < 60:
        return {
            "summary": "Profit margins are acceptable but risk is moderate due to potential empty returns.",
            "recommendation": "ACCEPT"
        }
    else:
        return {
            "summary": "High risk detected. Expected profit is negative or too volatile.",
            "recommendation": "REJECT"
        }

def _mock_negotiation_logic(context: Dict[str, Any]) -> Dict[str, Any]:
    current_price = context.get("current_price", 1000)
    target_price = context.get("target_price", 1000)
    round_num = context.get("round", 1)

    diff = abs(current_price - target_price)
    percentage_diff = diff / target_price if target_price > 0 else 0

    if round_num >= 3:
        return {"decision": "ACCEPT", "reason": "Max rounds reached.", "final_price": current_price}

    if percentage_diff <= 0.05:
        return {"decision": "ACCEPT", "reason": "Price is within acceptable range.", "final_price": current_price}

    step = (target_price - current_price) * 0.5
    counter_price = current_price + step

    return {"decision": "COUNTER_OFFER", "reason": "Countering based on market rates.", "counter_price": round(counter_price, 2)}

def _mock_fleet_decision(context: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates a Fleet Agent deciding on a load offer."""
    if not context:
        return {"decision": "REJECT", "reason": "No context provided", "confidence": 0.0}

    load = context.get("load", {})
    fleet = context.get("fleet", {})

    # Phase 4: Use Simulation Data if available
    simulation = context.get("simulation")
    if simulation:
        profit = simulation.get("projected_profit", 0)
        risk = simulation.get("risk_score", 50)

        if profit < 0 or risk > 80:
            return {
                "decision": "REJECT",
                "reason": f"Simulation indicates high risk ({risk:.1f}) and low/negative profit ({profit:.1f}).",
                "confidence": 0.95
            }
        elif profit > 300 and risk < 40:
            return {
                "decision": "ACCEPT",
                "reason": f"Simulation confirms profitability ({profit:.1f}) with low risk.",
                "confidence": 0.9
            }
        else:
            # Borderline case - maybe negotiate?
            return {
                "decision": "COUNTER_OFFER", # Or NEGOTIATE
                "reason": f"Profit ({profit:.1f}) is marginal. Need higher price to offset risk.",
                "confidence": 0.7
            }

    # Fallback to simple logic if no simulation
    if load.get("weight_tons", 0) > fleet.get("capacity_tons", 0):
        return {"decision": "REJECT", "reason": "Load too heavy", "confidence": 1.0}

    if random.random() < 0.85:
        return {"decision": "ACCEPT", "reason": "Standard acceptance logic.", "confidence": 0.9}
    else:
        return {"decision": "REJECT", "reason": "Schedule conflict.", "confidence": 0.7}

def _mock_load_decision(context: Dict[str, Any]) -> Dict[str, Any]:
    offers = context.get("offers", [])
    if not offers: return {"ranked_carriers": [], "reasoning": "No offers"}
    ranked = sorted(offers, key=lambda x: x.get("price", 0) or 0)
    return {"ranked_carriers": ranked, "reasoning": "Selected best price."}

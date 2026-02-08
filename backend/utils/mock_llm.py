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

    # Fleet Decision Logic (ACCEPT/REJECT load)
    if "evaluate load offer" in prompt_lower or "capacity" in prompt_lower:
        return _mock_fleet_decision(context)

    # Load Decision Logic (Select carrier)
    elif "evaluate fleet offers" in prompt_lower or "rank carriers" in prompt_lower:
        return _mock_load_decision(context)

    # Route Simulation Logic
    elif "route" in prompt_lower or "simulate" in prompt_lower:
        return {
            "profitability_score": round(random.uniform(0.6, 0.95), 2),
            "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "estimated_cost": round(random.uniform(1200, 1800), 2),
            "recommendation": random.choice(["OPEN", "WAIT", "REJECT"]),
            "reasoning": "Fuel costs are stable, but return load probability is low."
        }

    # Default fallback
    return {
        "action": "UNKNOWN",
        "message": "I understood the request but have no specific mock logic for it."
    }

def _mock_negotiation_logic(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates a negotiation turn.
    Logic:
    - If round > 3, force agreement (for demo purposes).
    - If current_price is within 5% of target, ACCEPT.
    - Else, COUNTER with a step towards target.
    """
    current_price = context.get("current_price", 1000)
    target_price = context.get("target_price", 1000)
    round_num = context.get("round", 1)

    diff = abs(current_price - target_price)
    percentage_diff = diff / target_price if target_price > 0 else 0

    # Force agreement after 3 rounds
    if round_num >= 3:
        return {
            "decision": "ACCEPT",
            "reason": "Max rounds reached, accepting best offer.",
            "final_price": current_price
        }

    # Accept if close enough
    if percentage_diff <= 0.05:
        return {
            "decision": "ACCEPT",
            "reason": "Price is within acceptable range (5%).",
            "final_price": current_price
        }

    # Counter offer
    # Move 50% towards the target
    step = (target_price - current_price) * 0.5
    counter_price = current_price + step

    return {
        "decision": "COUNTER_OFFER",
        "reason": f"Market average is closer to {target_price}. Countering.",
        "counter_price": round(counter_price, 2)
    }

def _mock_fleet_decision(context: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates a Fleet Agent deciding on a load offer."""
    if not context:
        return {"decision": "REJECT", "reason": "No context provided", "confidence": 0.0}

    load = context.get("load", {})
    fleet = context.get("fleet", {})

    # Simple logic:
    # 1. Check capacity
    if load.get("weight_tons", 0) > fleet.get("capacity_tons", 0):
        return {
            "decision": "REJECT",
            "reason": f"Load too heavy ({load.get('weight_tons')} > {fleet.get('capacity_tons')})",
            "confidence": 1.0
        }

    # 85% chance to accept valid loads
    if random.random() < 0.85:
        return {
            "decision": "ACCEPT",
            "reason": "Load fits capacity and schedule. Price is acceptable.",
            "confidence": 0.9
        }
    else:
        return {
            "decision": "REJECT",
            "reason": "Schedule conflict or better offer available.",
            "confidence": 0.7
        }

def _mock_load_decision(context: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates a Load Agent ranking carrier offers."""
    if not context:
        return {"ranked_carriers": [], "reasoning": "No context provided"}

    offers = context.get("offers", [])
    if not offers:
        return {"ranked_carriers": [], "reasoning": "No offers to evaluate"}

    ranked = sorted(offers, key=lambda x: x.get("price", 0) or 0) # Sort by price (mock)

    return {
        "ranked_carriers": ranked,
        "reasoning": f"Evaluated {len(offers)} offers. Selected top candidate based on price and reputation."
    }

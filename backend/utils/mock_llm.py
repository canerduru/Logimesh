import json
import random
from typing import Dict, Any, List

def mock_claude_response(system_prompt: str, user_prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Simulates a structured response from Anthropic Claude.

    In a real implementation, this would call:
    client.messages.create(
        model="claude-3-sonnet-20240229",
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    """

    # Analyze prompt keywords to return context-aware mock responses
    prompt_lower = user_prompt.lower()

    # Fleet Decision Logic (ACCEPT/REJECT load)
    if "evaluate load offer" in prompt_lower or "capacity" in prompt_lower:
        return _mock_fleet_decision(context)

    # Load Decision Logic (Select carrier)
    elif "evaluate fleet offers" in prompt_lower or "rank carriers" in prompt_lower:
        return _mock_load_decision(context)

    # Negotiation Logic
    elif "negotiate" in prompt_lower or "offer" in prompt_lower:
        base_price = context.get('current_price', 2000) if context else 2000

        # 50% chance to accept, 30% counter, 20% reject
        rand = random.random()
        if rand < 0.5:
            return {
                "decision": "ACCEPT",
                "reason": "The price is within our target range.",
                "final_price": base_price
            }
        elif rand < 0.8:
            counter_price = int(base_price * 1.05)
            return {
                "decision": "COUNTER_OFFER",
                "reason": "Market rates are slightly higher for this route.",
                "counter_price": counter_price
            }
        else:
            return {
                "decision": "REJECT",
                "reason": "Price is too low for the distance and weight."
            }

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

    # 2. Check price (mock logic: if price per km is low)
    # We don't have distance readily available in simple mock, so let's use random chance weighted by reputation

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

    # Rank by a simple score: (reputation * 0.4) + (price factor * 0.6)
    # Since we might not have all data, we'll just sort randomly or by available fields

    ranked = sorted(offers, key=lambda x: x.get("price", 0) or 0) # Sort by price (mock)

    # Add reasoning
    return {
        "ranked_carriers": ranked,
        "reasoning": f"Evaluated {len(offers)} offers. Selected top candidate based on price and reputation."
    }

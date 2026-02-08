import json
import random
from typing import Dict, Any

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

    # Negotiation Logic
    if "negotiate" in prompt_lower or "offer" in prompt_lower:
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

    # Load Matching Logic
    elif "match" in prompt_lower:
        return {
            "match_score": round(random.uniform(70, 99), 1),
            "suitability": "HIGH",
            "reason": "Truck location and capacity are perfect match."
        }

    # Default fallback
    return {
        "action": "UNKNOWN",
        "message": "I understood the request but have no specific mock logic for it."
    }

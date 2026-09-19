import re
from typing import Dict, Any, List

def calculate_risk(agent_id: str, tool_name: str, parameters: Dict[str, Any], agent_risk_level: str, tool_base_score: int) -> Dict[str, Any]:
    score = tool_base_score
    reasons = []

    # Agent privilege modifier
    if agent_risk_level == "HIGH":
        score += 20
        reasons.append("High privilege agent")
    elif agent_risk_level == "MEDIUM":
        score += 10
        reasons.append("Medium privilege agent")

    # Financial transaction modifier
    if "amount" in parameters:
        amount = parameters.get("amount", 0)
        try:
            amount = float(amount)
            if amount > 0:
                score += 15
                reasons.append("Financial transaction")
            if amount > 5000:
                score += 10
                reasons.append("Large financial transaction (>5000)")
            if amount > 25000:
                score += 20
                reasons.append("Very large financial transaction (>25000)")
        except (ValueError, TypeError):
            pass

    # Basic PII modifier
    pii_fields = ["email", "phone", "ssn", "credit_card", "password"]
    for field in pii_fields:
        if field in parameters:
            score += 20
            reasons.append(f"PII involved ({field})")
            break # Apply once

    # Threshold evaluation
    if score >= 70:
        level = "HIGH"
        decision = "BLOCK"
    elif score >= 40:
        level = "MEDIUM"
        decision = "REQUIRE_APPROVAL"
    else:
        level = "LOW"
        decision = "ALLOW"

    return {
        "risk_score": min(score, 100),
        "risk_level": level,
        "decision": decision,
        "reasons": reasons
    }

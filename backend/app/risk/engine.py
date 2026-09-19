import re
import json
import logging
from typing import Dict, Any, List
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

def evaluate_with_llm(agent_id: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    try:
        from groq import Groq
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        prompt = f"""
        You are an AI Security and Risk Engine evaluating an action proposed by an autonomous agent.
        
        Agent ID: {agent_id}
        Tool Requested: {tool_name}
        Parameters: {json.dumps(parameters)}
        
        Evaluate the risk of this action. Output a raw JSON object with the following structure:
        {{
            "risk_score": <int 0-100>,
            "risk_level": <"LOW", "MEDIUM", "HIGH", or "CRITICAL">,
            "decision": <"ALLOW", "REQUIRE_APPROVAL", or "BLOCK">,
            "reasons": [<list of string reasons for the decision>]
        }}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a strict security policy engine. Always output pure valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        response = completion.choices[0].message.content
        return json.loads(response)
    except Exception as e:
        logger.error(f"LLM Evaluation failed: {e}")
        return None

def calculate_risk(agent_id: str, tool_name: str, parameters: Dict[str, Any], agent_risk_level: str, tool_base_score: int) -> Dict[str, Any]:
    # Try LLM if configured
    if settings.GROQ_API_KEY and settings.LLM_PROVIDER.lower() == "groq":
        llm_result = evaluate_with_llm(agent_id, tool_name, parameters)
        if llm_result:
            return llm_result

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

from typing import Dict, Any, List, Optional
from app.models import Policy

def evaluate_policies(policies: List[Policy], tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    results = []
    decision_override = None # BLOCK > REQUIRE_APPROVAL > ALLOW

    for policy in policies:
        if not policy.enabled:
            continue
        
        rules = policy.rules
        
        # Evaluate Financial Policy
        if policy.category == "FINANCE" and "amount" in parameters and tool_name in ["issue_refund", "update_payment"]:
            try:
                amount = float(parameters["amount"])
                auto_max = rules.get("refunds", {}).get("auto_approve_max", 5000)
                human_max = rules.get("refunds", {}).get("human_approval_max", 25000)
                
                if amount > human_max:
                    results.append({"policy_id": policy.id, "name": policy.name, "violation": True, "reason": f"Amount {amount} exceeds hard limit {human_max}"})
                    decision_override = "BLOCK"
                elif amount > auto_max:
                    results.append({"policy_id": policy.id, "name": policy.name, "violation": True, "reason": f"Amount {amount} requires approval (> {auto_max})"})
                    if decision_override != "BLOCK":
                        decision_override = "REQUIRE_APPROVAL"
                else:
                    results.append({"policy_id": policy.id, "name": policy.name, "violation": False, "reason": f"Amount {amount} within auto-approve limit"})
            except:
                pass
                
        # Evaluate Database Policy
        if policy.category == "DATABASE" and "customer" in tool_name:
            operation = "SELECT"
            if "update" in tool_name:
                operation = "UPDATE"
            elif "delete" in tool_name:
                operation = "DELETE"
            elif "insert" in tool_name or "create" in tool_name:
                operation = "INSERT"
                
            rule_decision = rules.get("operations", {}).get(operation, "ALLOW")
            
            if rule_decision == "BLOCK":
                results.append({"policy_id": policy.id, "name": policy.name, "violation": True, "reason": f"Operation {operation} is blocked"})
                decision_override = "BLOCK"
            elif rule_decision == "REQUIRE_APPROVAL":
                results.append({"policy_id": policy.id, "name": policy.name, "violation": True, "reason": f"Operation {operation} requires approval"})
                if decision_override != "BLOCK":
                    decision_override = "REQUIRE_APPROVAL"
                    
    return {
        "results": results,
        "decision_override": decision_override
    }

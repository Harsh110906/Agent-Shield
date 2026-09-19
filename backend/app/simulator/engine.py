from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.schemas import ActionProposal
from app.gateway.action_gateway import ActionGateway

class SimulatorEngine:
    def __init__(self, db: Session):
        self.db = db
        # We use the real gateway but could wrap it in a transaction that rolls back
        self.gateway = ActionGateway(db)
        
    def simulate_sequence(self, proposals: List[ActionProposal]) -> Dict[str, Any]:
        """
        Runs a sequence of proposals through the gateway without executing the actual tools.
        Because we want this to be safe, we'll run it normally through the gateway, 
        but we won't call the actual tools. The gateway already saves evaluation records,
        which is fine for the hackathon (it acts as a log of the simulation).
        """
        results = []
        stats = {
            "total": len(proposals),
            "ALLOW": 0,
            "REQUIRE_APPROVAL": 0,
            "BLOCK": 0,
            "financial_exposure": 0.0,
            "policy_violations": 0,
            "highest_risk": 0
        }
        
        for p in proposals:
            res = self.gateway.evaluate(p)
            decision = res["evaluation"]["decision"]
            stats[decision] += 1
            
            risk = res["evaluation"]["risk_score"]
            if risk > stats["highest_risk"]:
                stats["highest_risk"] = risk
                
            if "amount" in p.parameters:
                try:
                    stats["financial_exposure"] += float(p.parameters["amount"])
                except:
                    pass
                    
            stats["policy_violations"] += len([v for v in res["evaluation"]["policy_results"] if v.get("violation")])
            
            results.append(res)
            
        return {
            "results": results,
            "stats": stats
        }

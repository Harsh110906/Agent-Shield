from sqlalchemy.orm import Session
from app.models import Agent, Tool, AgentTool, Policy, Action, ActionEvaluation, Approval, AuditLog, SecurityEvent
from app.schemas import ActionProposal
from app.risk.engine import calculate_risk
from app.policies.engine import evaluate_policies
from app.security.sensitive_data import detect_sensitive_data
from app.security.prompt_injection import detect_prompt_injection

class ActionGateway:
    def __init__(self, db: Session):
        self.db = db

    def evaluate(self, proposal: ActionProposal) -> dict:
        # 1. Fetch Agent
        agent = self.db.query(Agent).filter(Agent.id == proposal.agent_id).first()
        if not agent:
            return self._fast_fail(proposal, "BLOCK", "Agent not found")

        # 2. Fetch Tool & Permissions
        tool = self.db.query(Tool).filter(Tool.name == proposal.tool_name).first()
        if not tool:
            return self._fast_fail(proposal, "BLOCK", f"Unknown tool {proposal.tool_name}", agent_id=agent.id)

        permission = self.db.query(AgentTool).filter(
            AgentTool.agent_id == agent.id, 
            AgentTool.tool_id == tool.id
        ).first()

        if not permission or permission.permission == "blocked":
            return self._fast_fail(proposal, "BLOCK", f"Agent not permitted to use {tool.name}", agent_id=agent.id, tool_id=tool.id)

        # 3. Save Action
        action = Action(
            agent_id=agent.id,
            tool_name=tool.name,
            parameters=proposal.parameters,
            context=proposal.context,
            status="PENDING"
        )
        self.db.add(action)
        self.db.commit()

        # 4. Security Scans
        sensitive = detect_sensitive_data(proposal.parameters)
        injection = detect_prompt_injection(proposal.parameters)
        security_findings = sensitive + injection
        
        for finding in security_findings:
            sec_event = SecurityEvent(
                action_id=action.id,
                agent_id=agent.id,
                severity=finding["severity"],
                event_type=finding["type"],
                description=finding["description"]
            )
            self.db.add(sec_event)

        # 5. Policies
        policies = self.db.query(Policy).all()
        policy_eval = evaluate_policies(policies, tool.name, proposal.parameters)

        # 6. Risk Calculation
        risk_calc = calculate_risk(
            agent_id=agent.id,
            tool_name=tool.name,
            parameters=proposal.parameters,
            agent_risk_level=agent.risk_level,
            tool_base_score=tool.risk_base_score
        )

        # 7. Final Decision Logic
        decision = risk_calc["decision"]
        
        # Override with permission if stricter
        if permission.permission == "approval" and decision == "ALLOW":
            decision = "REQUIRE_APPROVAL"
            
        # Override with policy if stricter
        if policy_eval["decision_override"]:
            pol_dec = policy_eval["decision_override"]
            if pol_dec == "BLOCK" or (pol_dec == "REQUIRE_APPROVAL" and decision == "ALLOW"):
                decision = pol_dec

        # Override with security if findings exist
        if len(security_findings) > 0:
            decision = "BLOCK"
            risk_calc["reasons"].append("Critical security findings detected")

        # 8. Save Evaluation
        evaluation = ActionEvaluation(
            action_id=action.id,
            risk_score=risk_calc["risk_score"],
            risk_level=risk_calc["risk_level"],
            decision=decision,
            reasons=risk_calc["reasons"],
            policy_results=policy_eval["results"],
            security_findings=security_findings
        )
        self.db.add(evaluation)
        
        # 9. Handle Status Updates & Approvals
        if decision == "BLOCK":
            action.status = "BLOCKED"
        elif decision == "ALLOW":
            action.status = "EXECUTED" # We assume immediate execution next
        elif decision == "REQUIRE_APPROVAL":
            action.status = "PENDING"
            approval = Approval(action_id=action.id)
            self.db.add(approval)
            
        # 10. Audit Log
        audit = AuditLog(
            action_id=action.id,
            agent_id=agent.id,
            tool_name=tool.name,
            decision=decision,
            risk_score=risk_calc["risk_score"],
            details={"reasons": risk_calc["reasons"]}
        )
        self.db.add(audit)
        
        self.db.commit()
        
        return {
            "action_id": action.id,
            "evaluation": {
                "risk_score": evaluation.risk_score,
                "risk_level": evaluation.risk_level,
                "decision": evaluation.decision,
                "reasons": evaluation.reasons,
                "policy_results": evaluation.policy_results,
                "security_findings": evaluation.security_findings
            },
            "status": action.status
        }

    def _fast_fail(self, proposal: ActionProposal, decision: str, reason: str, agent_id=None, tool_id=None):
        return {
            "action_id": "fast-fail-no-id",
            "evaluation": {
                "risk_score": 100 if decision == "BLOCK" else 0,
                "risk_level": "CRITICAL" if decision == "BLOCK" else "LOW",
                "decision": decision,
                "reasons": [reason],
                "policy_results": [],
                "security_findings": []
            },
            "status": "BLOCKED"
        }

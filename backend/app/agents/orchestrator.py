from app.schemas import ActionProposal
from app.gateway.action_gateway import ActionGateway
from app.tools import execute_tool
from sqlalchemy.orm import Session
from app.models import Action

class AgentOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.gateway = ActionGateway(db)
        
    def execute_action(self, proposal: ActionProposal) -> dict:
        """
        Takes an action proposed by an agent, passes it through the gateway,
        and executes it if ALLOWED.
        """
        # 1. Gateway Evaluation
        gateway_response = self.gateway.evaluate(proposal)
        
        # 2. Execution if allowed
        if gateway_response["status"] == "EXECUTED":
            try:
                result = execute_tool(proposal.tool_name, proposal.parameters)
                gateway_response["result"] = result
                
                # Update action record with success
                action = self.db.query(Action).filter(Action.id == gateway_response["action_id"]).first()
                if action:
                    action.context["result"] = result
                    self.db.commit()
            except Exception as e:
                gateway_response["status"] = "FAILED"
                gateway_response["error"] = str(e)
                
                action = self.db.query(Action).filter(Action.id == gateway_response["action_id"]).first()
                if action:
                    action.status = "FAILED"
                    action.context["error"] = str(e)
                    self.db.commit()
                    
        return gateway_response

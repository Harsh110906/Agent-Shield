from app.tools.base import MockTool
from typing import Dict, Any

class SendEmailTool(MockTool):
    name = "send_email"
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Email sent successfully",
            "to": parameters.get("to", "unknown@example.com"),
            "subject": parameters.get("subject", "No Subject")
        }

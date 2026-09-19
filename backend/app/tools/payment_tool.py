from app.tools.base import MockTool
from typing import Dict, Any
import uuid

class GetInvoiceTool(MockTool):
    name = "get_invoice"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "invoice": {
                "id": parameters.get("invoice_id", "INV-100"),
                "amount": 18500,
                "status": "paid"
            }
        }

class IssueRefundTool(MockTool):
    name = "issue_refund"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "refund_id": f"REF-{str(uuid.uuid4())[:8]}",
            "amount": parameters.get("amount"),
            "customer_id": parameters.get("customer_id")
        }

class UpdatePaymentTool(MockTool):
    name = "update_payment"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "updated": True,
            "method": parameters.get("method", "credit_card")
        }

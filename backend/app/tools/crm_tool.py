from app.tools.base import MockTool
from typing import Dict, Any
import uuid

class GetCustomerTool(MockTool):
    name = "get_customer"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        cust_id = parameters.get("customer_id", "CUST-UNKNOWN")
        return {
            "success": True,
            "customer": {
                "id": cust_id,
                "name": "Jane Doe",
                "email": "jane@example.com",
                "status": "active"
            }
        }

class GetOrderTool(MockTool):
    name = "get_order"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        order_id = parameters.get("order_id", "ORD-UNKNOWN")
        return {
            "success": True,
            "order": {
                "id": order_id,
                "customer_id": "CUST-1023",
                "total": 12500,
                "status": "processing"
            }
        }

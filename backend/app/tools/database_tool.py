from app.tools.base import MockTool
from typing import Dict, Any

class ReadCustomerTool(MockTool):
    name = "read_customer"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "data": {"id": parameters.get("id"), "db_record": True}}

class UpdateCustomerTool(MockTool):
    name = "update_customer"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "updated": True, "fields": list(parameters.keys())}

class DeleteCustomerTool(MockTool):
    name = "delete_customer"
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "deleted": True, "id": parameters.get("id")}

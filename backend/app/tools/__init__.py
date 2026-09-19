from app.tools.base import MockTool
from app.tools.email_tool import SendEmailTool
from app.tools.crm_tool import GetCustomerTool, GetOrderTool
from app.tools.database_tool import ReadCustomerTool, UpdateCustomerTool, DeleteCustomerTool
from app.tools.payment_tool import GetInvoiceTool, IssueRefundTool, UpdatePaymentTool

AVAILABLE_TOOLS = {
    "send_email": SendEmailTool(),
    "get_customer": GetCustomerTool(),
    "get_order": GetOrderTool(),
    "read_customer": ReadCustomerTool(),
    "update_customer": UpdateCustomerTool(),
    "delete_customer": DeleteCustomerTool(),
    "get_invoice": GetInvoiceTool(),
    "issue_refund": IssueRefundTool(),
    "update_payment": UpdatePaymentTool(),
}

def execute_tool(tool_name: str, parameters: dict) -> dict:
    if tool_name not in AVAILABLE_TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")
    return AVAILABLE_TOOLS[tool_name].execute(parameters)

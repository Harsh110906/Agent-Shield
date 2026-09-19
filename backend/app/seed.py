from sqlalchemy.orm import Session
from app.models import Agent, Tool, AgentTool, Policy
from app.database import engine, Base, SessionLocal

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if seeded
    if db.query(Agent).first():
        print("Database already seeded.")
        return

    # Create Agents
    customer_agent = Agent(id="agent-customer-support", name="CustomerSupportAgent", type="SUPPORT", description="Handles customer queries, order lookups, and emails.", risk_level="LOW")
    finance_agent = Agent(id="agent-finance", name="FinanceAgent", type="FINANCE", description="Processes invoices, refunds, and payments.", risk_level="MEDIUM")
    database_agent = Agent(id="agent-database", name="DatabaseAgent", type="SYSTEM", description="Direct database operations on records.", risk_level="HIGH")
    
    db.add_all([customer_agent, finance_agent, database_agent])
    
    # Create Tools
    tools = [
        Tool(id="tool-get-customer", name="get_customer", category="CRM", description="Look up customer details", risk_base_score=5),
        Tool(id="tool-get-order", name="get_order", category="CRM", description="Look up order details", risk_base_score=5),
        Tool(id="tool-send-email", name="send_email", category="COMMUNICATION", description="Send email to customer", risk_base_score=15),
        Tool(id="tool-get-invoice", name="get_invoice", category="FINANCE", description="Get invoice details", risk_base_score=10),
        Tool(id="tool-issue-refund", name="issue_refund", category="FINANCE", description="Issue a refund", risk_base_score=30),
        Tool(id="tool-update-payment", name="update_payment", category="FINANCE", description="Update payment details", risk_base_score=30),
        Tool(id="tool-read-customer", name="read_customer", category="DATABASE", description="Read customer record", risk_base_score=10),
        Tool(id="tool-update-customer", name="update_customer", category="DATABASE", description="Update customer record", risk_base_score=25),
        Tool(id="tool-delete-customer", name="delete_customer", category="DATABASE", description="Delete customer record", risk_base_score=50),
    ]
    db.add_all(tools)
    db.commit()

    # Link Agents and Tools
    agent_tools = [
        # Customer Agent
        AgentTool(agent_id=customer_agent.id, tool_id="tool-get-customer", permission="allowed"),
        AgentTool(agent_id=customer_agent.id, tool_id="tool-get-order", permission="allowed"),
        AgentTool(agent_id=customer_agent.id, tool_id="tool-send-email", permission="allowed"),
        AgentTool(agent_id=customer_agent.id, tool_id="tool-issue-refund", permission="blocked"),
        
        # Finance Agent
        AgentTool(agent_id=finance_agent.id, tool_id="tool-get-invoice", permission="allowed"),
        AgentTool(agent_id=finance_agent.id, tool_id="tool-issue-refund", permission="allowed"),
        AgentTool(agent_id=finance_agent.id, tool_id="tool-update-payment", permission="approval"),
        
        # Database Agent
        AgentTool(agent_id=database_agent.id, tool_id="tool-read-customer", permission="allowed"),
        AgentTool(agent_id=database_agent.id, tool_id="tool-update-customer", permission="approval"),
        AgentTool(agent_id=database_agent.id, tool_id="tool-delete-customer", permission="blocked"),
    ]
    db.add_all(agent_tools)

    # Create Policies
    policies = [
        Policy(
            id="pol-finance-01",
            name="Financial Policy",
            category="FINANCE",
            description="Rules for refunds and payments.",
            rules={
                "refunds": {
                    "auto_approve_max": 5000,
                    "human_approval_max": 25000,
                }
            }
        ),
        Policy(
            id="pol-db-01",
            name="Database Policy",
            category="DATABASE",
            description="Rules for database operations.",
            rules={
                "operations": {
                    "SELECT": "ALLOW",
                    "INSERT": "ALLOW",
                    "UPDATE": "REQUIRE_APPROVAL",
                    "DELETE": "BLOCK"
                }
            }
        ),
        Policy(
            id="pol-data-01",
            name="Data Policy",
            category="DATA",
            description="PII and Sensitive Data Policy",
            rules={
                "pii_export": "REQUIRE_APPROVAL",
                "pii_external": "BLOCK"
            }
        )
    ]
    db.add_all(policies)

    db.commit()
    print("Database seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed_database()

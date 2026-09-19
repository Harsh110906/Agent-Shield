# API Reference

AgentShield provides a REST API for evaluating actions, querying agents, and managing policies.

## Actions

### `POST /api/actions/evaluate`
Evaluate an action proposal without executing it immediately.

**Request Body:**
```json
{
  "agent_id": "agent-finance",
  "tool_name": "issue_refund",
  "parameters": {
    "customer_id": "CUST-2938",
    "amount": 18500
  },
  "context": {}
}
```

**Response:**
```json
{
  "action_id": "...",
  "evaluation": {
    "risk_score": 67,
    "risk_level": "MEDIUM",
    "decision": "REQUIRE_APPROVAL",
    "reasons": [
        "Financial transaction",
        "Large financial transaction"
    ],
    "policy_results": [...],
    "security_findings": []
  },
  "status": "PENDING"
}
```

## Approvals

### `GET /api/approvals`
List all pending, approved, and rejected approvals.

### `POST /api/approvals/{id}/approve`
Approve a pending action and execute it.

### `POST /api/approvals/{id}/reject`
Reject a pending action.

## Agents

### `GET /api/agents`
List all registered agents and their risk profiles.

### `GET /api/agents/{id}`
Get detailed information about an agent, including its permitted tools.

## Policies

### `GET /api/policies`
List all configured policies.

### `POST /api/policies`
Create a new policy.

## Metrics & Auditing

### `GET /api/metrics`
Get high-level statistics for the dashboard (e.g., active agents, actions today, average risk).

### `GET /api/audit-logs`
Retrieve a history of all executed and blocked actions.

### `GET /api/security-events`
Retrieve a history of all detected security events (e.g., prompt injection attempts).

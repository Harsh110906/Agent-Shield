# AgentShield

AgentShield is the runtime security & governance layer for autonomous AI agents. 
It intercepts agent actions before they reach their tools, evaluating them for risk, policy violations, sensitive data, and prompt injection, acting as a control plane for AI systems.

## Key Features

- **Action Gateway**: The central hub that evaluates all agent actions.
- **Risk Engine**: Deterministic risk scoring based on financial values, agent privilege, and data sensitivity.
- **Policy Engine**: Configurable rules for what actions are allowed, blocked, or require approval.
- **Security Engine**: Detects sensitive data leaks and prompt injection attempts.
- **Human-in-the-Loop**: A dedicated inbox for approving medium-risk actions.
- **Observability**: Complete audit logging and dashboard metrics.
- **Simulator**: Dry-run actions to see their predicted risk without executing them.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite (swappable to PostgreSQL)
- **Frontend**: Next.js 14, Tailwind CSS, shadcn/ui, React Flow, Recharts
- **Infrastructure**: Docker Compose

## Getting Started

### Demo Mode (Zero Configuration)
The project runs out-of-the-box using deterministic mock agents. No API keys are required.

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/api`

### Demo Scenarios
Four built-in scenarios are available from the UI's Demo panel:
1. **Safe Action (Allow)**: A simple customer lookup.
2. **Financial Action (Approval)**: A ₹18,500 refund that triggers human review.
3. **Destructive Action (Block)**: An attempt to delete all customers, bypassing instructions.
4. **Data Leak (Block)**: An attempt to email an API key.

## Architecture
See `docs/architecture.md` for a complete system diagram.

# System Architecture

## Overview
AgentShield uses a gateway pattern to intercept and evaluate all agent actions.

```mermaid
graph TD
    A[AI Agent / Planner] -->|Proposes Action| G[Action Gateway]
    
    subgraph AgentShield
        G --> P1[Permission Validation]
        P1 --> S[Security Scanners]
        S --> P2[Policy Engine]
        P2 --> R[Risk Engine]
        R --> D{Decision}
    end
    
    D -->|ALLOW| T[Execute Tool]
    D -->|BLOCK| B[Return Blocked Error]
    D -->|REQUIRE_APPROVAL| H[Human Approval Inbox]
    
    H -->|Approved| T
    H -->|Rejected| B
    
    T --> ALog[Audit Log]
    B --> ALog
```

## Components
- **Action Gateway**: The core evaluation pipeline.
- **Risk Engine**: Calculates a 0-100 score based on parameters.
- **Policy Engine**: Evaluates rule-based constraints.
- **Security Scanners**: Detects API keys, PII, and prompt injection patterns.

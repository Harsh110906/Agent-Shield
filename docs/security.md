# Security Model

## Fail-Closed Principle
If AgentShield encounters an error while evaluating an action, the default fallback is to BLOCK the action.

## Deterministic Evaluation
While LLMs may be used to generate actions, the evaluation of those actions is entirely deterministic. Risk scores, policy violations, and permission checks rely on hard-coded rules and thresholds, not LLM inference.

## Security Scanners
AgentShield includes two main scanners:
1. **Sensitive Data Detection**: Uses regex patterns to identify API keys, passwords, and credit card numbers in action parameters, blocking them before they leave the gateway.
2. **Prompt Injection Detection**: Scans parameters for common injection patterns like "ignore previous instructions" to prevent agents from being manipulated into unauthorized actions.

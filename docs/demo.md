# Demo Guide

To demonstrate AgentShield's capabilities, we have prepared 4 built-in scenarios that highlight different security features.

## Scenario 1: Safe Customer Support (ALLOW)
- **Action**: Look up a customer record.
- **Expected Outcome**: Allowed (Low Risk)
- **Why**: The CustomerSupportAgent has permission to use `get_customer`, and no policies are violated.

## Scenario 2: Financial Transaction (APPROVAL)
- **Action**: Issue a ₹18,500 refund.
- **Expected Outcome**: Requires Human Approval (Medium Risk)
- **Why**: The Finance Policy requires human approval for refunds between ₹5,000 and ₹25,000. The risk score increases due to the financial amount.

## Scenario 3: Destructive Attack (BLOCK)
- **Action**: Delete all customer records.
- **Expected Outcome**: Blocked (High Risk / Policy Violation)
- **Why**: The Database Policy explicitly blocks `DELETE` operations. Additionally, prompt injection patterns may be detected.

## Scenario 4: Secret Leakage (BLOCK)
- **Action**: Email an API key.
- **Expected Outcome**: Blocked (High Risk / Security Event)
- **Why**: The Sensitive Data Scanner detects an API key in the email body, immediately halting execution and logging a security event.

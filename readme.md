# ParcelPilot AI Support Agent

An AI-assisted customer support decision system for ParcelPilot that combines deterministic business logic, document retrieval, and LLM-based response generation.

The system is designed around an important principle:

> **Business and policy decisions are deterministic; the LLM is used only for generating the final customer-facing response.**

This makes the system more reliable, traceable, and resistant to hallucinated policy decisions.

---

## 1. Project Overview

ParcelPilot Support Agent analyzes customer support tickets and produces an actionable support decision.

For each ticket, the system can determine:

- Ticket severity
- Applicable SLA
- SLA response target
- SLA deadline
- SLA breach status
- Escalation requirement
- Relevant known issues
- Recommended actions
- Cancellation eligibility
- Service-credit eligibility
- Final customer-facing response

The system uses customer-specific agreements and current support policies stored in the document knowledge base.

An LLM is then used to convert the deterministic decision into a professional customer response.

If the LLM is unavailable, rate-limited, or produces a response that fails validation, the system falls back to a deterministic response.

---

## 2. Architecture

```text
                         ┌─────────────────────┐
                         │    Support Ticket   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Ticket / Account  │
                         │       Retrieval     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │   Deterministic Decision     │
                    │           Engine             │
                    ├──────────────────────────────┤
                    │ Severity Classification      │
                    │ SLA Retrieval & Parsing      │
                    │ SLA Deadline Calculation    │
                    │ SLA Breach Detection        │
                    │ Escalation Decision          │
                    │ Known Issue Retrieval        │
                    │ Recommendations              │
                    │ Cancellation Evaluation      │
                    │ Service Credit Evaluation    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │   Support Decision  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    LLM Response    │
                         │      Generator      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Response Validator  │
                         └──────────┬──────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                 Valid Response           Invalid / Failed
                       │                         │
                       ▼                         ▼
                Customer Response      Deterministic Fallback
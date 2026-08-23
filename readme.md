# 📦 ParcelPilot Support Assistant

AI-assisted customer support agent built for the ParcelPilot AI Agent Assessment.

The application helps answer support questions involving:

- Customer accounts
- Orders and shipments
- Support tickets
- SLAs
- Cancellation policies
- Service credits
- Product documentation
- Known issues
- Support escalations

The system combines deterministic business logic, document retrieval, structured-data tools, and LLM-based response generation.

## Core Design Principle

> **Deterministic systems make business decisions; the LLM handles response wording.**

The LLM does not determine:

- SLA values
- SLA breaches
- Cancellation fees
- Service-credit eligibility
- Ticket severity
- Escalation requirements

These decisions are calculated by deterministic application logic.

The generated response is then validated. If the LLM is unavailable or produces an invalid response, the system uses a deterministic fallback response.

---

## Architecture

```text
Streamlit UI
     │
     ▼
Chat Router
     │
     ├───────────────┬────────────────┐
     ▼               ▼                ▼
Document Search   Data Tools      Action Tools
     │               │                │
     ▼               ▼                ▼
Policies          SQLite          Escalation
Agreements        Accounts        Confirmation
SOPs              Orders
Known Issues      Tickets
     │               │
     └───────────────┤
                     ▼
             Deterministic
             Decision Layer
                     │
                     ▼
              LLM Response
                 Generation
                     │
                     ▼
              Response Validator
                     │
               ┌─────┴─────┐
               ▼           ▼
             Valid       Invalid
               │           │
               ▼           ▼
             LLM       Deterministic
           Response       Fallback
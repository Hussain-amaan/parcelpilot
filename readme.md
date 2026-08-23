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


```

# Folder Structure :

## Project Structure

```text
parcelpilot/
├── app/
│   ├── agent/          # Chat routing, LLM response generation and validation
│   ├── data/           # SQLite database access and queries
│   ├── policy/         # Deterministic policy evaluation
│   ├── retrieval/      # PDF processing and vector search
│   ├── tickets/        # SLA, ticket analysis and service-credit logic
│   ├── tools/          # Document, data and state-changing tools
│               
│
├── data/
│   ├── raw/            # Structured CSV data
│   ├── chroma/         # Vector store
│   ├── parcelpilot.db  # SQLite operational database
│   └── escalations.json # Mock escalation state
│
├── documents/          # Supplied ParcelPilot PDF knowledge base
├── docs/
│   ├── ARCHITECTURE.md
│   └── PRODUCT_NOTE.md
│
├── tests/
│   ├── agents/
│   └── tickets/
├── streamlit_app     # ui made with streamlit
├── README.md
└── requirements.txt


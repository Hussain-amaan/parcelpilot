# ParcelPilot Support Assistant — Architecture

## Overview

ParcelPilot Support Assistant is a Streamlit-based customer support chatbot that combines deterministic business logic, document retrieval, structured data, and LLM-based response generation.

The main design principle is:

> Business decisions are handled deterministically; the LLM is used primarily for natural-language responses.

## Architecture

```text
User
 │
 ▼
Streamlit Chat Interface
 │
 ▼
Chat Router
 │
 ├── Document Search
 │      └── Policies / Agreements / SOPs / Known Issues
 │
 ├── Structured Data Tools
 │      └── SQLite: Accounts / Orders / Tickets
 │
 ├── Business Logic
 │      ├── SLA
 │      ├── Cancellation
 │      └── Service Credit
 │
 └── Action Tools
        └── Escalation
              │
              ▼
        User Confirmation
```

```
For responses requiring natural-language generation:

Deterministic Decision
        │
        ▼
   LLM Response
        │
        ▼
 Response Validator
        │
   ┌────┴────┐
   │         │
 Valid     Invalid
   │         │
   ▼         ▼
Response   Deterministic
           Fallback
```


# Tool Design

The chatbot provides three main tool categories:

## 1. Document Search

Retrieves relevant information from the supplied ParcelPilot documents, including policies, customer agreements, SOPs, and known issues.

## 2. Structured Data

Uses controlled functions to access account, order, and ticket information from the SQLite database.

Business rules such as cancellation, SLA, and service-credit evaluation are handled by deterministic Python functions.

## 3. State-Changing Action

The application provides a mock escalation action.

An escalation is prepared first and requires explicit user confirmation before it is created.

# Data Handling

Structured operational data is stored in SQLite.

The document knowledge base is handled separately through the retrieval layer.

Customer account context is used to prevent access to data belonging to other accounts.

# Source Reliability

The system does not treat every source as equally authoritative.

Customer-specific agreements and current policies take precedence over deprecated policies or historical ticket information.

Historical ticket resolutions are treated as context only because they may contain incorrect guidance.

# Technical Trade-offs

A hybrid architecture was chosen instead of allowing the LLM to make all business decisions.

This provides:

More predictable policy decisions
Easier testing
Safer handling of SLA and contractual rules
Reduced risk of hallucinated business decisions

The LLM is therefore used mainly to make deterministic results more natural and customer-friendly.

# Reliability

If the LLM is unavailable or produces a response that fails validation, the system falls back to a deterministic response generator.

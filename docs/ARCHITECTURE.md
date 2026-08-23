# ParcelPilot Support Assistant — Architecture Note

## 1. Overview

ParcelPilot Support Assistant is a hybrid AI customer-support system designed to answer customer questions about accounts, orders, tickets, SLAs, cancellation policies, service credits, product documentation, known issues, and escalations.

The architecture deliberately separates **business decision-making** from **natural-language generation**.

The core principle is:

> **Deterministic application logic makes business decisions; the LLM is responsible only for generating customer-facing language.**

This reduces the risk of hallucinated contractual or policy decisions while still providing a natural conversational experience.

---

## 2. High-Level Architecture

```text
                    ┌──────────────────────┐
                    │      Streamlit UI    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Chat Router      │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
     ┌──────────────┐  ┌──────────────┐  ┌────────────────┐
     │ Document     │  │ Structured   │  │ Action Tools   │
     │ Search Tool  │  │ Data Tools   │  │                │
     └──────┬───────┘  └──────┬───────┘  └───────┬────────┘
            │                 │                  │
            ▼                 ▼                  ▼
     Policies, SOPs,     SQLite Database      Escalation
     Agreements,         Accounts, Orders,    Workflow
     Known Issues        Tickets
            │                 │
            └─────────────────┼─────────────────┘
                              ▼
                  ┌─────────────────────────┐
                  │ Deterministic Decision  │
                  │ Layer                   │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ LLM Response Generator  │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ Response Validator      │
                  └────────────┬────────────┘
                               │
                     ┌─────────┴─────────┐
                     │                   │
                  Valid              Invalid
                     │                   │
                     ▼                   ▼
                 LLM Response      Deterministic
                                   Fallback
```

### 3. Agent Design

The agent uses a routing-based architecture.

Natural-language requests are classified into workflows such as:

Cancellation
Service credit
Ticket/SLA lookup
Document search
Escalation

The router then invokes the appropriate tools and deterministic business logic.

For example:

User:
Can Northstar cancel ORD-1001 without a cancellation fee?

        ↓

Chat Router

        ↓

Order Lookup
        +
Account Lookup
        +
Cancellation Policy

        ↓

Deterministic Decision

        ↓

Customer Response

The system does not require the LLM to independently determine the cancellation policy.

### 4. Deterministic Decision Layer

Business-critical decisions are handled by deterministic Python modules.

The decision layer evaluates information from the structured database and supplied policy/document data.

Important decisions include:

SLA

The system determines:

Ticket severity
Applicable SLA
SLA target value
SLA target unit
Coverage
Deadline
Whether the SLA has been breached
Whether escalation is required
Cancellation

The system determines:

Whether an order can be cancelled
Applicable cancellation fee
Reason for the decision
Service Credit

The system determines:

Whether the customer is eligible
Credit amount
Reason for eligibility or non-eligibility

The LLM is not responsible for making these decisions.

5. Tool Design

The assessment requires at least three distinct tool categories. The application implements all three.

5.1 Document Search Tool

The document search tool searches the supplied ParcelPilot knowledge base.

It can retrieve information from:

Current support policies
Deprecated policies
Customer agreements
Cancellation/service-credit SOPs
Product operations documentation
Known issues

The main tool is:

search_parcelpilot_documents()

The tool is read-only.

5.2 Structured-Data Tools

Structured operational information is stored in SQLite.

The application exposes controlled data functions including:

lookup_ticket()
lookup_account()
lookup_orders()
check_cancellation()
check_service_credit()

These functions provide controlled access to:

Accounts
Orders
Tickets
Cancellation decisions
Service-credit decisions

The LLM does not receive unrestricted direct database access.

5.3 State-Changing Action Tool

The application provides a mock escalation action:

create_escalation()

The action creates an escalation record in:

data/escalations.json

An escalation contains information such as:

Escalation ID
Ticket ID
Account ID
Reason
Priority
Status
Creation timestamp

This demonstrates a state-changing workflow without requiring a production ticketing system.

6. Confirmation Before State-Changing Actions

State-changing actions require explicit confirmation.

The escalation workflow is:

User requests escalation
        ↓
Ticket is analysed
        ↓
System determines whether escalation is required
        ↓
Escalation action is prepared
        ↓
User confirmation requested
        ↓
User confirms
        ↓
Escalation is created

The preparation step does not modify application state.

For example:

Ticket TKT-501 requires escalation.

Reason:
P1 incident with an SLA breach.

Do you want me to create the escalation?

Only after explicit confirmation is the action executed.

This prevents accidental state changes.

7. Access Control and Data Privacy

The application uses account context to scope customer-facing data access.

Customer information is not intended to be exposed solely because the LLM was instructed not to reveal it.

Instead, access is enforced in the application/data layer.

For example, if a customer associated with one account attempts to access an order belonging to another account, the system returns an access-denied result instead of passing the unauthorized order information to the response generator.

Example:

You are not authorised to access this order.

This approach reduces the risk of exposing another customer's information through prompt manipulation or model behaviour.

Authentication is mocked for the assessment environment.

A production implementation would replace the mocked account context with a proper identity and authorization system.

8. Document and Source Handling

The source base contains documents with different authority, freshness, and reliability.

The system distinguishes between:

Current policies
Deprecated policies
Customer-specific agreements
Product documentation
Known issues
Historical support information

Customer-specific agreements are considered for account-specific decisions.

Deprecated policies should not automatically override current policies.

Historical ticket resolutions are treated as contextual information rather than authoritative policy because the assessment explicitly states that historical resolutions may contain incorrect guidance.

9. Source Reliability and Conflict Handling

The system follows a source-aware approach rather than treating every retrieved document as equally authoritative.

The general decision hierarchy is:

Customer-specific active agreement
              ↓
Current applicable policy / SOP
              ↓
Current product documentation
              ↓
Known issues / operational information
              ↓
Historical ticket resolutions

When information is uncertain or insufficient to make a reliable business decision, the system should avoid inventing a policy exception.

Where appropriate, the request should be escalated for human review.

This is particularly important for:

Contractual terms
SLA interpretation
Service-credit eligibility
Unsupported exceptions
Conflicting information
10. Multi-Step Requests

The system supports requests that require multiple tools or sources.

For example:

Can Northstar cancel ORD-1001 without a cancellation fee?

can involve:

Account Context
      ↓
Order Lookup
      ↓
Account Lookup
      ↓
Applicable Cancellation Rules
      ↓
Customer-Specific Agreement
      ↓
Deterministic Decision
      ↓
Customer Response

Another example:

What is the SLA for TKT-501?

can involve:

Ticket Lookup
      ↓
Account / Plan
      ↓
Applicable Agreement or Policy
      ↓
SLA Rule
      ↓
SLA Calculation
      ↓
Breach Determination
      ↓
Response

This allows the application to combine structured data and document-derived information rather than relying on a single source.

11. LLM Response Generation

The LLM is used after the deterministic decision has been produced.

The LLM receives the decision and is instructed to rewrite it into a professional customer-facing response.

The prompt explicitly instructs the model not to:

Invent facts
Change severity
Change SLA values
Change SLA units
Invent service credits
Invent policy exceptions
Make new policy decisions
Contradict the deterministic decision

The LLM therefore acts primarily as a response writer, rather than the policy engine.

12. Response Validation

LLM responses are validated against the deterministic decision before being returned.

The validator checks important decision facts, including:

Severity
SLA value
SLA unit
SLA breach status
Escalation requirement
Relevant recommendations
Service-credit information where applicable

For example, if the deterministic decision states:

Severity: P1
SLA: 15 minutes
Breached: True
Escalation: Required

but the LLM produces a response that does not communicate the SLA breach, the response can be rejected.

13. Deterministic Fallback

External LLM APIs can fail because of:

Rate limits
Temporary API failures
Model availability
Network problems

The application therefore includes a deterministic response generator.

The workflow is:

                    LLM Request
                         │
                 ┌───────┴────────┐
                 │                │
              Success           Failure
                 │                │
                 ▼                ▼
           Validate LLM      Deterministic
              Response         Fallback
                 │
          ┌──────┴──────┐
          │             │
        Valid         Invalid
          │             │
          ▼             ▼
       LLM Response   Deterministic
                       Fallback

This prevents an external LLM service from becoming a complete single point of failure for the support workflow.

14. Interface

The application is exposed through a Streamlit chat interface.

The interface allows users to submit natural-language support requests.

Examples include:

Can Northstar cancel ORD-1001 without a cancellation fee?

What is the SLA for TKT-501?

What is the current CSV upload policy?

Escalate TKT-501

The interface can also expose agent/tool information to make the workflow easier to understand.

15. Data Architecture

Structured operational data is stored in SQLite.

The current database provides tables for entities such as:

accounts
orders
tickets

Raw structured data is maintained separately under:

data/raw/

The document retrieval system uses the supplied ParcelPilot documents and a local vector-store/retrieval layer.

State-changing mock escalation records are stored in:

data/escalations.json

This keeps structured data, retrieved documents, and action state logically separated.

16. Major Technical Trade-offs
Deterministic Logic vs Fully LLM-Based Agent

A fully autonomous LLM agent could make the architecture simpler from a coding perspective.

However, allowing an LLM to independently determine:

Contractual terms
SLA breaches
Cancellation fees
Service-credit eligibility

would introduce unnecessary reliability risks.

The deterministic approach was therefore selected for business-critical decisions.

SQLite vs Production Database

SQLite was selected because the assessment dataset is relatively small and the application needs to remain easy to run locally.

Advantages include:

Simple setup
No external database server
Deterministic queries
Easy reproducibility

A production deployment would likely use PostgreSQL or another managed relational database.

API LLM vs Local LLM

The application uses Groq for LLM-based response generation.

The benefit is simple integration and fast inference.

The trade-off is dependency on external API availability and rate limits.

The deterministic fallback was therefore implemented to maintain basic functionality when the LLM cannot be reached.

Mocked Actions vs Production Integrations

The escalation action is intentionally mocked.

Instead of modifying a real support platform, it writes an escalation record to:

data/escalations.json

This demonstrates the complete action/confirmation workflow without requiring access to ParcelPilot's production systems.

17. Security Considerations

The current assessment implementation includes:

Account-scoped data access
Controlled database functions
Confirmation before state-changing actions
Separation of decision logic and LLM generation
No reliance on LLM instructions alone for authorization
Environment variables for API credentials

The following would be required for production:

Proper authentication
Role-based access control
Secrets management
Audit logging
Encryption
Rate limiting
Production database permissions
Detailed action authorization
Monitoring and alerting
18. Reliability Strategy

The system uses multiple layers of protection:

                 Source Data
                     ↓
              Controlled Tools
                     ↓
          Deterministic Decisions
                     ↓
             LLM Generation
                     ↓
             Response Validator
                     ↓
        ┌────────────┴────────────┐
        │                         │
      Valid                    Invalid
        │                         │
        ▼                         ▼
   LLM Response             Deterministic
                              Fallback

The goal is not to make the LLM perfect.

The goal is to ensure that an imperfect LLM cannot silently change important business decisions.

19. Example End-to-End Flow

Consider:

A user asks:

"What is the SLA for TKT-501?"

The system performs:

1. Identify ticket request
2. Retrieve TKT-501
3. Identify account and plan
4. Determine applicable SLA
5. Calculate SLA deadline
6. Determine whether the SLA was breached
7. Determine escalation requirement
8. Build deterministic decision
9. Generate customer-facing response
10. Validate response
11. Return validated response

If the LLM is unavailable:

LLM unavailable
      ↓
Deterministic response generator
      ↓
Final response
20. Summary

The architecture is intentionally designed around a hybrid model:

Natural Language
       ↓
     Router
       ↓
     Tools
       ↓
Deterministic Decisions
       ↓
      LLM
       ↓
   Validation
       ↓
Fallback when required

The main architectural trade-off is choosing controlled, deterministic business logic over fully autonomous LLM decision-making.

This makes the system better suited to a support environment where incorrect SLA, contractual, cancellation, or service-credit decisions could have significant consequences.

The architecture can later be extended with production authentication, proactive issue detection, audit logging, real ticketing integrations, carrier APIs, and a managed database without fundamentally changing the core decision-and-validation model.

# ParcelPilot Support Assistant — Product Note

## 1. Additional Client Problem

### Trust and Reliability

I chose to focus on the **Trust and Reliability** problem.

Support decisions can depend on different sources such as customer agreements, current policies, product documentation, and historical ticket information. These sources may not always agree or have the same level of authority.

The system addresses this by:

- Using deterministic logic for important business decisions such as SLA, cancellation, and service-credit evaluation.
- Giving customer-specific agreements appropriate priority.
- Treating historical ticket resolutions as context rather than authoritative policy.
- Validating LLM-generated responses against the deterministic decision.
- Falling back to a deterministic response when the LLM is unavailable or produces an invalid response.

This reduces the risk of confidently providing an incorrect support answer.

## 2. What I Would Build Next

If development continued, I would prioritise:

1. **Production authentication and role-based access control**
   - Replace the current mocked account context with proper authentication.

2. **Real ticketing integration**
   - Replace the local escalation action with integration into a support/ticketing platform.

3. **Proactive issue detection**
   - Identify recurring issues, SLA risks, high-severity tickets, and problems affecting multiple customers.

4. **Monitoring and audit logs**
   - Track tool usage, decisions, escalations, validation failures, and system errors.

## 3. What I Intentionally Left Out

For this assessment, I intentionally kept the system focused on the core support workflow.

I did not implement:

- Production authentication
- A real ticketing-system integration
- Production infrastructure
- Real customer communication channels
- A full proactive-issue dashboard
- Production-grade monitoring and auditing

These would be appropriate next steps for a production version.

## 4. Success Metric

The primary metric I would use is:

**Support resolution accuracy rate**

> Percentage of support requests where the system's final answer is correct and consistent with the applicable source data and business rules.

This metric is more important than response speed alone because incorrect support decisions could directly affect customers and contractual obligations.

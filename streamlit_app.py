import streamlit as st

from app.agent.chat_router import handle_chat_query
from app.agent.action_manager import confirm_escalation


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="ParcelPilot Support Assistant",
    page_icon="📦",
    layout="wide",
)


# ==================================================
# PAGE HEADER
# ==================================================

st.title("📦 ParcelPilot Support Assistant")

st.caption(
    "AI-assisted customer support for policies, orders, "
    "tickets, SLAs, service credits, and escalations."
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("Support Context")

    account_id = st.text_input(
        "Account ID",
        value="ACCT-001",
        help=(
            "Mock authenticated account context. "
            "Customer data is restricted to this account."
        ),
    )

    st.divider()

    st.subheader("Example queries")

    st.markdown(
        """
**Cancellation**

Can Northstar cancel ORD-1001 without a cancellation fee?

**Service credit**

A pickup is 3 hours late because of carrier fault.
Should I get a service credit for ORD-2001?

**Ticket / SLA**

What is the SLA for TKT-501?

**Escalation**

Escalate TKT-501

**Document search**

What is the current CSV upload policy?
"""
    )

    st.divider()

    st.info(
        "State-changing actions require explicit confirmation."
    )


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_escalation" not in st.session_state:
    st.session_state.pending_escalation = None

if "action_result" not in st.session_state:
    st.session_state.action_result = None


# ==================================================
# RESULT FORMATTER
# ==================================================

def format_result(result):
    """
    Convert router output into a clean response
    for the Streamlit chat interface.
    """

    status = result.get("status")
    intent = result.get("intent")

    # ------------------------------------------------
    # ACCESS DENIED
    # ------------------------------------------------

    if status == "access_denied":

        return result.get(
            "message",
            "You are not authorised to access this information.",
        )

    # ------------------------------------------------
    # NEEDS INFORMATION
    # ------------------------------------------------

    if status == "needs_information":

        return result.get(
            "message",
            "Additional information is required.",
        )

    # ------------------------------------------------
    # NOT FOUND
    # ------------------------------------------------

    if status == "not_found":

        return result.get(
            "message",
            "The requested record could not be found.",
        )

    # ------------------------------------------------
    # ERROR
    # ------------------------------------------------

    if status == "error":

        return result.get(
            "message",
            "An error occurred while processing the request.",
        )

    # ------------------------------------------------
    # CANCELLATION
    # ------------------------------------------------

    if intent == "cancellation":

        cancellation = result["result"]
        order_id = result["order_id"]

        if cancellation["can_cancel"]:

            fee = cancellation["fee_inr"]

            if fee == 0:

                return (
                    "### Cancellation result\n\n"
                    f"Yes. **{order_id}** can be cancelled "
                    "with **no cancellation fee**.\n\n"
                    f"**Reason:** {cancellation['reason']}"
                )

            return (
                "### Cancellation result\n\n"
                f"Yes. **{order_id}** can be cancelled "
                f"with a **₹{fee} cancellation fee**.\n\n"
                f"**Reason:** {cancellation['reason']}"
            )

        return (
            "### Cancellation result\n\n"
            f"**{order_id} cannot be cancelled.**\n\n"
            f"**Reason:** {cancellation['reason']}"
        )

    # ------------------------------------------------
    # SERVICE CREDIT
    # ------------------------------------------------

    if intent == "service_credit":

        credit = result["result"]
        order_id = result["order_id"]

        if credit["eligible"]:

            return (
                "### Service credit result\n\n"
                f"Order **{order_id}** is eligible for "
                f"a **₹{credit['credit_inr']} service credit**.\n\n"
                f"**Reason:** {credit['reason']}"
            )

        return (
            "### Service credit result\n\n"
            f"Order **{order_id}** is not eligible "
            "for a service credit based on the supplied "
            "information.\n\n"
            f"**Reason:** {credit['reason']}"
        )

    # ------------------------------------------------
    # TICKET / SLA
    # ------------------------------------------------

    if intent == "ticket":

        decision = result["decision"]

        sla = decision["sla"]
        sla_result = decision["sla_result"]

        if sla_result["breached"]:

            breach_text = (
                "The SLA **has been breached**."
            )

        else:

            breach_text = (
                "The SLA **has not been breached**."
            )

        if decision["escalation_required"]:

            escalation_text = (
                "Escalation is **required**."
            )

        else:

            escalation_text = (
                "Escalation is **not currently required**."
            )

        response = (
            f"### Ticket {decision['ticket_id']}\n\n"
            f"**Account:** {decision['account']}\n\n"
            f"**Plan:** {decision['plan']}\n\n"
            f"**Severity:** {decision['severity']}\n\n"
            f"**SLA:** {sla['target_value']} "
            f"{sla['target_unit']} "
            f"({sla['coverage']})\n\n"
            f"**Deadline:** {sla_result['deadline']}\n\n"
            f"{breach_text}\n\n"
            f"{escalation_text}"
        )

        # --------------------------------------------
        # Known issues
        # --------------------------------------------

        if decision.get("known_issues"):

            response += (
                "\n\n### Known issues\n\n"
            )

            for issue in decision["known_issues"]:

                if isinstance(issue, dict):

                    issue_id = issue.get(
                        "issue_id",
                        issue.get("id", "Known issue"),
                    )

                    response += (
                        f"- {issue_id}\n"
                    )

                else:

                    response += (
                        f"- {issue}\n"
                    )

        # --------------------------------------------
        # Recommendations
        # --------------------------------------------

        if decision.get("recommendations"):

            response += (
                "\n\n### Recommended action\n\n"
            )

            for recommendation in decision["recommendations"]:

                if isinstance(
                    recommendation,
                    dict,
                ):

                    action = recommendation.get(
                        "action",
                        recommendation.get(
                            "recommendation",
                            str(recommendation),
                        ),
                    )

                    response += (
                        f"{action}\n"
                    )

                else:

                    response += (
                        f"{recommendation}\n"
                    )

        # --------------------------------------------
        # Service credit
        # --------------------------------------------

        service_credit = decision.get(
            "service_credit"
        )

        if service_credit is not None:

            response += (
                "\n\n### Service credit\n\n"
            )

            if service_credit.get("eligible"):

                response += (
                    f"Eligible for "
                    f"₹{service_credit.get('credit_inr', 0)} "
                    "service credit.\n\n"
                )

            response += (
                f"{service_credit.get('reason', '')}"
            )

        return response

    # ------------------------------------------------
    # DOCUMENT SEARCH
    # ------------------------------------------------

    if intent == "document_search":

        results = result.get(
            "results",
            [],
        )

        if not results:

            return (
                "I could not find relevant information "
                "in the supplied ParcelPilot documents."
            )

        response = (
            "### Relevant ParcelPilot documentation\n\n"
        )

        for index, item in enumerate(
            results,
            start=1,
        ):

            metadata = item.get(
                "metadata",
                {},
            )

            source = metadata.get(
                "source",
                "Unknown source",
            )

            text = item.get(
                "text",
                item.get(
                    "content",
                    "",
                ),
            )

            response += (
                f"**{index}. {source}**\n\n"
                f"{text}\n\n"
            )

        return response

    # ------------------------------------------------
    # UNKNOWN
    # ------------------------------------------------

    return result.get(
        "message",
        "I could not determine how to handle that request.",
    )


# ==================================================
# DISPLAY PREVIOUS CHAT MESSAGES
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message.get("metadata"):

            with st.expander(
                "Agent details"
            ):

                st.json(
                    message["metadata"]
                )


# ==================================================
# DISPLAY PENDING ESCALATION
# ==================================================

pending = st.session_state.pending_escalation

if pending is not None:

    st.divider()

    st.warning(
        "⚠️ A state-changing escalation is waiting for confirmation."
    )

    action = pending["action"]

    st.markdown(
        f"""
### Escalation Request

**Ticket:** `{action['ticket_id']}`

**Account:** {action['account']}

**Priority:** `{action['priority']}`

**Reason:** {action['reason']}
"""
    )

    st.info(
        action["message"]
    )

    # ----------------------------------------------
    # CONFIRM / CANCEL BUTTONS
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        confirm = st.button(
            "✅ Confirm escalation",
            key="confirm_pending_escalation",
            type="primary",
            use_container_width=True,
        )

    with col2:

        cancel = st.button(
            "❌ Cancel",
            key="cancel_pending_escalation",
            use_container_width=True,
        )

    # ----------------------------------------------
    # CONFIRM ESCALATION
    # ----------------------------------------------

    if confirm:

        try:

            confirmation_result = confirm_escalation(
                pending["decision"],
                confirmed=True,
            )

            if confirmation_result["executed"]:

                st.session_state.action_result = {
                    "type": "success",
                    "message": confirmation_result[
                        "message"
                    ],
                    "escalation": confirmation_result.get(
                        "escalation"
                    ),
                }

            else:

                st.session_state.action_result = {
                    "type": "error",
                    "message": confirmation_result[
                        "message"
                    ],
                }

            # Remove pending action
            st.session_state.pending_escalation = None

            # Rerun so the result appears cleanly
            st.rerun()

        except Exception as exc:

            st.session_state.action_result = {
                "type": "error",
                "message": (
                    f"Could not create escalation: {exc}"
                ),
            }

            st.session_state.pending_escalation = None

            st.rerun()

    # ----------------------------------------------
    # CANCEL ESCALATION
    # ----------------------------------------------

    if cancel:

        confirmation_result = confirm_escalation(
            pending["decision"],
            confirmed=False,
        )

        st.session_state.action_result = {
            "type": "cancelled",
            "message": confirmation_result[
                "message"
            ],
        }

        st.session_state.pending_escalation = None

        st.rerun()


# ==================================================
# DISPLAY ACTION RESULT
# ==================================================

if st.session_state.action_result is not None:

    action_result = (
        st.session_state.action_result
    )

    if action_result["type"] == "success":

        st.success(
            action_result["message"]
        )

        escalation = action_result.get(
            "escalation"
        )

        if escalation:

            with st.expander(
                "Escalation details"
            ):

                st.json(
                    escalation
                )

    elif action_result["type"] == "cancelled":

        st.info(
            action_result["message"]
        )

    elif action_result["type"] == "error":

        st.error(
            action_result["message"]
        )

    # Clear after rendering
    st.session_state.action_result = None


# ==================================================
# CHAT INPUT
# ==================================================

query = st.chat_input(
    "Ask ParcelPilot Support a question..."
)


# ==================================================
# PROCESS NEW QUERY
# ==================================================

if query:

    # ----------------------------------------------
    # Save user message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            query
        )

    # ----------------------------------------------
    # Run agent
    # ----------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Investigating..."
        ):

            try:

                result = handle_chat_query(
                    query=query,
                    account_id=account_id or None,
                )

            except Exception as exc:

                result = {
                    "status": "error",
                    "message": (
                        "I encountered an internal error "
                        "while processing your request."
                    ),
                    "error": str(exc),
                }

        # ------------------------------------------
        # ACTION PENDING
        # ------------------------------------------

        if result.get(
            "status"
        ) == "action_pending":

            action = result["action"]

            # --------------------------------------
            # Store pending action
            # --------------------------------------

            st.session_state.pending_escalation = {
                "decision": result["decision"],
                "action": action,
            }

            answer = (
                f"Escalation for "
                f"**{action['ticket_id']}** "
                "is prepared and waiting for "
                "your confirmation."
            )

        else:

            answer = format_result(
                result
            )

        # ------------------------------------------
        # Display answer
        # ------------------------------------------

        st.markdown(
            answer
        )

        # ------------------------------------------
        # Agent details
        # ------------------------------------------

        with st.expander(
            "🔎 Agent details"
        ):

            st.json(
                result
            )

    # ----------------------------------------------
    # Save assistant message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "metadata": result,
        }
    )

    # ----------------------------------------------
    # IMPORTANT
    #
    # If an action is pending, rerun the application.
    # This causes the pending escalation block above
    # to render the confirmation buttons.
    # ----------------------------------------------

    if result.get(
        "status"
    ) == "action_pending":

        st.rerun()
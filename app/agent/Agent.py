from app.tickets.decision import analyze_ticket_decision
from app.agent.llm_response import generate_llm_response
from app.agent.response_generator import generate_deterministic_response
from app.agent.validator import validate_response


def run_support_agent(ticket_id, assessment_time):
    """
    Run the complete ParcelPilot support-agent pipeline.

    Deterministic modules make all policy decisions.

    The LLM is used only to generate the final response.

    If the LLM is unavailable or produces a response that
    contradicts the deterministic decision, the system falls
    back to a deterministic response.
    """

    # --------------------------------------------------
    # 1. Deterministic ticket analysis
    # --------------------------------------------------

    decision = analyze_ticket_decision(
        ticket_id=ticket_id,
        assessment_time=assessment_time,
    )

    # --------------------------------------------------
    # 2. Try LLM response generation
    # --------------------------------------------------

    try:

        response = generate_llm_response(
            decision
        )

        response_source = "llm"

    except Exception as exc:

        print(
            "LLM unavailable. "
            "Using deterministic fallback."
        )

        print(
            f"Reason: {exc}"
        )

        response = generate_deterministic_response(
            decision
        )

        return {
            "decision": decision,
            "response": response,
            "response_source": "deterministic_fallback",
            "validation": None,
        }

    # --------------------------------------------------
    # 3. Validate LLM response
    # --------------------------------------------------

    validation = validate_response(
        response,
        decision
    )

    # --------------------------------------------------
    # 4. If validation fails, use deterministic fallback
    # --------------------------------------------------

    if not validation["valid"]:

        print(
            "LLM response failed validation."
        )

        for error in validation["errors"]:

            print(
                f"- {error}"
            )

        response = generate_deterministic_response(
            decision
        )

        response_source = "deterministic_fallback"

    # --------------------------------------------------
    # 5. Return complete result
    # --------------------------------------------------

    return {
        "decision": decision,
        "response": response,
        "response_source": response_source,
        "validation": validation,
    }
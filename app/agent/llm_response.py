import os
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


def generate_llm_response(decision):
    """
    Convert a deterministic ParcelPilot decision
    into a professional customer-facing response.

    The LLM is only responsible for wording.
    It must not make policy decisions.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    llm = ChatGroq(
        model="groq/compound",
        temperature=0.1,
        max_tokens=150,
        api_key=api_key,
    )

    prompt = f"""
Write a concise customer-support response using ONLY the
deterministic ParcelPilot decision below.

Account: {decision["account"]}
Plan: {decision["plan"]}
Severity: {decision["severity"]}
SLA: {decision["sla"]}
SLA Result: {decision["sla_result"]}
Known Issues: {decision.get("known_issues", [])}
Recommendations: {decision.get("recommendations", [])}
Service Credit: {decision.get("service_credit")}
Escalation Required: {decision["escalation_required"]}

RULES:
- Do not invent facts.
- Do not change the severity.
- Do not change the SLA.
- Do not invent policy exceptions.
- Do not invent service credits.
- Do not make new policy decisions.
- Use only information supplied above.
- Preserve uncertainty when information is uncertain.
- If Service Credit is None, do not mention service credits.
- Only mention a service credit when an explicit result is provided.
- If escalation is required, clearly communicate escalation.
- Keep the response concise and professional.
- Do not mention internal implementation details.
- Do not mention the source filenames.
- Do not expose internal reasoning.
- Output only the final customer-facing response.
"""

    messages = [
        SystemMessage(
            content=(
                "You are a careful ParcelPilot customer-support "
                "response writer. The supplied decision is authoritative."
            )
        ),
        HumanMessage(content=prompt),
    ]

    # Retry a few times if Groq temporarily rate-limits the request.
    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = llm.invoke(messages)

            return response.content.strip()

        except Exception as exc:

            error_text = str(exc)

            # Retry only for rate-limit errors.
            if "429" not in error_text and "rate_limit" not in error_text:
                raise

            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** attempt

            print(
                f"Groq rate limit reached. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)
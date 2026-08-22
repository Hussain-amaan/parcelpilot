import re


def validate_response(response, decision):
    """
    Validate an LLM-generated response against the
    authoritative deterministic decision.

    The validator checks for contradictions rather than
    requiring the LLM to repeat every decision field.
    """

    errors = []

    response_lower = response.lower()

    # --------------------------------------------------
    # 1. Severity
    # --------------------------------------------------

    severity = decision["severity"].lower()

    mentioned_severities = re.findall(
        r"\bp[123]\b",
        response_lower
    )

    for mentioned in mentioned_severities:

        if mentioned != severity:

            errors.append(
                f"Response contains incorrect severity. "
                f"Expected {severity.upper()}."
            )

            break

    # --------------------------------------------------
    # 2. SLA numerical contradiction
    # --------------------------------------------------

    sla = decision["sla"]

    expected_value = str(
        sla["target_value"]
    )

    expected_unit = (
        sla["target_unit"]
        .replace("_", " ")
        .lower()
    )

    # Only validate SLA numbers if the response
    # actually talks about an SLA/response target.

    sla_context_terms = [
        "sla",
        "response target",
        "response time",
        "support target",
    ]

    talks_about_sla = any(
        term in response_lower
        for term in sla_context_terms
    )

    if talks_about_sla:

        # Look for common number + time expressions.
        sla_numbers = re.findall(
            r"\b\d+\s*(?:minute|minutes|hour|hours|day|days)\b",
            response_lower
        )

        if sla_numbers:

            expected_phrase = (
                f"{expected_value} "
                f"{expected_unit}"
            )

            # Normalize plural/singular forms
            normalized_response = response_lower.replace(
                "minutes",
                "minute"
            ).replace(
                "hours",
                "hour"
            ).replace(
                "days",
                "day"
            )

            normalized_expected = expected_phrase.replace(
                "minutes",
                "minute"
            ).replace(
                "hours",
                "hour"
            ).replace(
                "days",
                "day"
            )

            if normalized_expected not in normalized_response:

                errors.append(
                    f"Response may contain an incorrect "
                    f"SLA target. Expected "
                    f"{expected_phrase}."
                )

    # --------------------------------------------------
    # 3. SLA breach contradiction
    # --------------------------------------------------

    breached = decision[
        "sla_result"
    ]["breached"]

    breach_terms = [
        "sla was breached",
        "sla has been breached",
        "sla breach",
        "breached the sla",
        "deadline was missed",
        "response target was missed",
        "response target has been missed",
        "sla was missed",
        "sla has been missed",
        "outside the sla",
        "past the sla deadline",
    ]

    no_breach_terms = [
        "sla has not been breached",
        "sla was not breached",
        "no sla breach",
        "within the sla",
        "within the response window",
        "response window has not been exceeded",
        "sla is being met",
        "sla remains within",
        "sla is currently being met",
        "within the applicable response target",
    ]

    breach_detected = any(
        term in response_lower
        for term in breach_terms
    )

    no_breach_detected = any(
        term in response_lower
        for term in no_breach_terms
    )

    if breached:

        if no_breach_detected:

            errors.append(
                "Decision says the SLA is breached, "
                "but the response says it is within SLA."
            )

    else:

        if breach_detected:

            errors.append(
                "Decision says the SLA is not breached, "
                "but the response claims a breach."
            )

    # --------------------------------------------------
    # 4. Escalation contradiction
    # --------------------------------------------------

    escalation_required = decision[
        "escalation_required"
    ]

    escalation_terms = [
        "escalation is required",
        "requires escalation",
        "we are escalating",
        "we're escalating",
        "being escalated",
        "escalate this",
        "escalated",
    ]

    escalation_detected = any(
        term in response_lower
        for term in escalation_terms
    )

    no_escalation_terms = [
        "no escalation is required",
        "escalation is not required",
        "does not require escalation",
        "no need to escalate",
        "no escalation needed",
    ]

    no_escalation_detected = any(
        term in response_lower
        for term in no_escalation_terms
    )

    if escalation_required:

        if no_escalation_detected:

            errors.append(
                "Escalation is required, but the "
                "response says escalation is not required."
            )

    else:

        if escalation_detected:

            errors.append(
                "Escalation is not required, but the "
                "response says escalation is required."
            )

    # --------------------------------------------------
    # 5. Service-credit contradiction
    # --------------------------------------------------

    service_credit = decision.get(
        "service_credit"
    )

    if service_credit is not None:

        eligible = service_credit.get(
            "eligible"
        )

        credit = service_credit.get(
            "credit_inr"
        )

        if eligible:

            # If an explicit credit exists, the response
            # must not state a different amount.

            if credit is not None:

                credit_pattern = re.compile(
                    r"(?:inr|₹)\s*([0-9]+(?:\.[0-9]+)?)",
                    re.IGNORECASE
                )

                amounts = credit_pattern.findall(
                    response
                )

                for amount in amounts:

                    if float(amount) != float(credit):

                        errors.append(
                            f"Response mentions an incorrect "
                            f"service credit. Expected INR {credit}."
                        )

                        break

        else:

            # If customer is not eligible, reject claims
            # that a credit has been granted.

            positive_credit_terms = [
                "eligible for a service credit",
                "eligible for service credit",
                "credit has been issued",
                "credit has been applied",
                "we will issue a credit",
                "we have issued a credit",
            ]

            if any(
                term in response_lower
                for term in positive_credit_terms
            ):

                errors.append(
                    "Response claims service-credit eligibility "
                    "although the deterministic decision says "
                    "the customer is not eligible."
                )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }
def generate_deterministic_response(decision):
    """
    Generate a safe customer-facing response directly from
    the deterministic support decision.

    This function does not use an LLM.
    """

    account = decision["account"]
    severity = decision["severity"]

    sla = decision["sla"]
    sla_result = decision["sla_result"]

    response = []

    # Greeting
    response.append(
        f"Hello {account},"
    )

    response.append("")

    # Severity
    response.append(
        f"We have classified your support request as {severity}."
    )

    # SLA
    target_value = sla["target_value"]
    target_unit = sla["target_unit"]

    if sla_result["breached"]:

        response.append(
            f"The applicable {severity} response target is "
            f"{target_value} {target_unit.replace('_', ' ')}."
        )

        response.append(
            "The applicable SLA has been breached, and this issue "
            "requires escalation."
        )

    else:

        response.append(
            f"The applicable {severity} response target is "
            f"{target_value} {target_unit.replace('_', ' ')}."
        )

        response.append(
            "The applicable SLA has not been breached."
        )

    # Known issues
    known_issues = decision.get("known_issues", [])

    if known_issues:

        response.append("")
        response.append("We identified the following known issue:")

        for issue in known_issues:

            issue_id = issue.get("issue_id")

            if issue_id:
                response.append(
                    f"- {issue_id}"
                )

    # Recommendations
    recommendations = decision.get(
        "recommendations",
        []
    )

    if recommendations:

        response.append("")
        response.append("Recommended action:")

        for recommendation in recommendations:

            action = recommendation.get(
                "action"
            )

            if action:
                response.append(
                    action
                )

    # Service credit
    service_credit = decision.get(
        "service_credit"
    )

    if service_credit is not None:

        response.append("")

        if service_credit.get("eligible"):

            credit = service_credit.get(
                "credit_inr"
            )

            response.append(
                f"Based on the available information, "
                f"you are eligible for a service credit "
                f"of INR {credit}."
            )

        else:

            reason = service_credit.get(
                "reason"
            )

            if reason:
                response.append(
                    f"Service-credit status: {reason}"
                )

    response.append("")
    response.append(
        "Please let us know if you need any further assistance."
    )

    response.append("")
    response.append(
        "Best regards,"
    )

    response.append(
        "ParcelPilot Customer Support"
    )

    return "\n".join(response)
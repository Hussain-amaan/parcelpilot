import re


def parse_response_target(text, severity):
    """
    Parse response targets from customer agreements.

    Expected format:

    P1: 15 minutes, 24x7
    P2: 1 hour
    P3: 8 business hours
    """

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        pattern = rf"^[\s\-•●*]*{severity}\s*:\s*(.+)$"

        match = re.match(
            pattern,
            line,
            re.IGNORECASE
        )

        if not match:
            continue

        target = match.group(1).strip()

        coverage = (
            "24x7"
            if "24x7" in target.lower()
            else "business_hours"
        )

        # Remove coverage from target
        target_without_coverage = re.sub(
            r",?\s*24x7",
            "",
            target,
            flags=re.IGNORECASE
        ).strip()

        # Minutes
        match = re.fullmatch(
            r"(\d+)\s*minutes?",
            target_without_coverage,
            re.IGNORECASE
        )

        if match:
            return {
                "severity": severity,
                "target_value": int(match.group(1)),
                "target_unit": "minutes",
                "coverage": coverage,
            }

        # Hours
        match = re.fullmatch(
            r"(\d+)\s*hours?",
            target_without_coverage,
            re.IGNORECASE
        )

        if match:
            return {
                "severity": severity,
                "target_value": int(match.group(1)),
                "target_unit": "hours",
                "coverage": coverage,
            }

        # Business hours
        match = re.fullmatch(
            r"(\d+)\s*business\s*hours?",
            target_without_coverage,
            re.IGNORECASE
        )

        if match:
            return {
                "severity": severity,
                "target_value": int(match.group(1)),
                "target_unit": "business_hours",
                "coverage": coverage,
            }

        # Business days
        match = re.fullmatch(
            r"(\d+)\s*business\s*days?",
            target_without_coverage,
            re.IGNORECASE
        )

        if match:
            return {
                "severity": severity,
                "target_value": int(match.group(1)),
                "target_unit": "business_days",
                "coverage": coverage,
            }

    return None


def parse_policy_table(text, plan, severity):
    """
    Parse response targets from the current Support Policy v3 table.

    Format:

    Plan P1 P2 P3

    Enterprise 30 minutes, 24x7 2 hours 1 business day
    Growth 2 business hours 4 business hours 2 business days
    Standard 4 business hours 1 business day 2 business days
    """

    normalized = " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    # Current Support Policy v3 values
    policy = {
        "Enterprise": {
            "P1": "30 minutes, 24x7",
            "P2": "2 hours",
            "P3": "1 business day",
        },
        "Growth": {
            "P1": "2 business hours",
            "P2": "4 business hours",
            "P3": "2 business days",
        },
        "Standard": {
            "P1": "4 business hours",
            "P2": "1 business day",
            "P3": "2 business days",
        },
    }

    if plan not in policy:
        return None

    if severity not in policy[plan]:
        return None

    target = policy[plan][severity]

    return parse_response_target(
        f"{severity}: {target}",
        severity
    )
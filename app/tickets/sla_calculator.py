from datetime import datetime, timedelta


DATE_FORMAT = "%d-%m-%Y %H:%M"


def calculate_deadline(
    created_at,
    target_value,
    target_unit,
    assessment_time,
):
    """
    Calculate SLA deadline and determine whether
    the response target has been breached.

    For this first version:
    - minutes and hours are handled as elapsed time
    - business-hours/business-days are temporarily
      treated as elapsed time

    A proper business-calendar implementation
    can be added afterward.
    """

    created = datetime.strptime(
        created_at,
        DATE_FORMAT
    )

    assessed = datetime.strptime(
        assessment_time,
        DATE_FORMAT
    )

    if target_unit == "minutes":

        deadline = created + timedelta(
            minutes=target_value
        )

    elif target_unit == "hours":

        deadline = created + timedelta(
            hours=target_value
        )

    elif target_unit == "business_hours":

        deadline = created + timedelta(
            hours=target_value
        )

    elif target_unit == "business_days":

        deadline = created + timedelta(
            days=target_value
        )

    else:
        raise ValueError(
            f"Unsupported target unit: {target_unit}"
        )

    return {
        "created_at": created_at,
        "assessment_time": assessment_time,
        "deadline": deadline.strftime(
            DATE_FORMAT
        ),
        "breached": assessed > deadline,
    }
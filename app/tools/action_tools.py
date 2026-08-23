from datetime import datetime
from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parents[2]

ESCALATION_FILE = (
    BASE_DIR
    / "data"
    / "escalations.json"
)


def _load_escalations():
    if not ESCALATION_FILE.exists():
        return []

    with open(
        ESCALATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def _save_escalations(escalations):
    ESCALATION_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        ESCALATION_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            escalations,
            file,
            indent=2,
        )


def create_escalation(
    ticket_id: str,
    account_id: str,
    reason: str,
    priority: str,
):
    """
    Create a mock support escalation.

    IMPORTANT:
    This function performs a state-changing action.
    It must only be called after explicit user confirmation.
    """

    escalations = _load_escalations()

    escalation_id = (
        f"ESC-{len(escalations) + 1:04d}"
    )

    escalation = {
        "escalation_id": escalation_id,
        "ticket_id": ticket_id,
        "account_id": account_id,
        "reason": reason,
        "priority": priority,
        "status": "CREATED",
        "created_at": datetime.now().isoformat(),
    }

    escalations.append(escalation)

    _save_escalations(escalations)

    return escalation
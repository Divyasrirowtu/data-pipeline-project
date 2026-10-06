import json

from app.cdc.validators.event_validator import validate_event


class CDCEventProcessor:
    """
    Validates and processes Debezium CDC events.
    """

    def process(self, raw_event):
        """
        Process one raw Kafka CDC event.

        Returns:
            dictionary containing:
            - valid
            - event
            - reason
        """

        try:
            if isinstance(raw_event, bytes):
                raw_event = raw_event.decode("utf-8")

            event = json.loads(raw_event)

        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            return {
                "valid": False,
                "event": None,
                "reason": f"Invalid JSON: {exc}",
            }

        valid, reason = validate_event(event)

        if not valid:
            return {
                "valid": False,
                "event": event,
                "reason": reason,
            }

        return {
            "valid": True,
            "event": event,
            "reason": None,
        }
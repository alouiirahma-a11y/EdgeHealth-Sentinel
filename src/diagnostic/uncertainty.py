def assess_uncertainty(confidence):
    """
    Convert model confidence into a safety-oriented status.

    This is a synthetic research prototype.
    The thresholds are illustrative and NOT clinically validated.
    """

    if confidence >= 0.85:
        return {
            "uncertainty": 1 - confidence,
            "status": "HIGH_CONFIDENCE",
            "decision": "PROCEED",
        }

    if confidence >= 0.60:
        return {
            "uncertainty": 1 - confidence,
            "status": "MODERATE_CONFIDENCE",
            "decision": "ADDITIONAL_EVIDENCE",
        }

    return {
        "uncertainty": 1 - confidence,
        "status": "LOW_CONFIDENCE",
        "decision": "HUMAN_REVIEW",
    }

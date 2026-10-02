def safety_decision(quality_status, confidence, ood_detected=False):
    if quality_status != "SUFFICIENT":
        return {
            "decision": "RETAKE_IMAGE",
            "reason": "IMAGE_QUALITY_INSUFFICIENT",
        }

    if ood_detected:
        return {
            "decision": "HUMAN_REVIEW",
            "reason": "OUT_OF_DISTRIBUTION",
        }

    if confidence < 0.60:
        return {
            "decision": "HUMAN_REVIEW",
            "reason": "LOW_CONFIDENCE",
        }

    if confidence < 0.85:
        return {
            "decision": "ADDITIONAL_EVIDENCE",
            "reason": "MODERATE_CONFIDENCE_REQUIRES_ADDITIONAL_EVIDENCE",
        }

    return {
        "decision": "PROCEED",
        "reason": "SAFETY_CHECK_PASSED",
    }

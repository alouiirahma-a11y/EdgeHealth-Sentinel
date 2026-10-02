# ============================================================
# EDGEHEALTH SENTINEL
# Equity Audit Engine
# ============================================================

def audit_equity(
    population,
    underserved_rate,
    resource_access_rate,
):
    """
    Synthetic equity audit.

    This prototype examines whether a scenario has
    a potential equity-access concern.

    It is NOT a validated fairness metric.
    """

    underserved_population = (
        population * underserved_rate
    )

    served_population = (
        population - underserved_population
    )

    # --------------------------------------------------------
    # EQUITY RISK
    # --------------------------------------------------------

    if underserved_rate >= 0.50:
        equity_risk = "HIGH"

    elif underserved_rate >= 0.30:
        equity_risk = "MODERATE"

    else:
        equity_risk = "LOW"

    # --------------------------------------------------------
    # ACCESS INTERPRETATION
    # --------------------------------------------------------

    if resource_access_rate < 50:
        access_status = "LOW ACCESS"

    elif resource_access_rate < 80:
        access_status = "MODERATE ACCESS"

    else:
        access_status = "HIGH ACCESS"

    # --------------------------------------------------------
    # EQUITY WARNING
    # --------------------------------------------------------

    if underserved_rate >= 0.40 and resource_access_rate < 50:

        equity_warning = (
            "High underserved population combined "
            "with low resource access."
        )

    elif underserved_rate >= 0.40:

        equity_warning = (
            "A substantial underserved population "
            "requires explicit equity monitoring."
        )

    elif resource_access_rate < 50:

        equity_warning = (
            "Low resource access requires equity review."
        )

    else:

        equity_warning = (
            "No high equity-access concern detected "
            "under this synthetic rule."
        )

    return {
        "underserved_population": underserved_population,
        "served_population": served_population,
        "underserved_rate": underserved_rate,
        "resource_access_rate": resource_access_rate,
        "equity_risk": equity_risk,
        "access_status": access_status,
        "equity_warning": equity_warning,
    }

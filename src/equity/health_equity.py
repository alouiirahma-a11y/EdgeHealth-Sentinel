# ============================================================
# EDGEHEALTH SENTINEL
# Health Equity Intelligence Engine
# ============================================================

def analyze_health_equity(
    population,
    underserved_rate,
    testing_coverage,
    evidence_debt,
    resource_availability,
    blind_spot_risk,
    geographic_access_risk,
    transport_access,
    connectivity,
):
    """
    Synthetic Health Equity Intelligence layer.

    This prototype examines the coexistence of:
    - underserved population
    - limited evidence coverage
    - evidence debt
    - resource constraints
    - health-system blind spots
    - geographic access barriers

    It is NOT a validated population-level fairness metric,
    causal model, or measure of health outcomes.
    """

    underserved_population = population * underserved_rate

    # --------------------------------------------------------
    # EVIDENCE EQUITY EXPOSURE
    # --------------------------------------------------------

    if testing_coverage < 25 and underserved_rate >= 0.40:
        evidence_equity_exposure = "HIGH"
    elif testing_coverage < 50 or underserved_rate >= 0.30:
        evidence_equity_exposure = "MODERATE"
    else:
        evidence_equity_exposure = "LOW"

    # --------------------------------------------------------
    # RESOURCE CONSTRAINT
    # --------------------------------------------------------

    if resource_availability < 50:
        resource_constraint = "HIGH"
    elif resource_availability < 80:
        resource_constraint = "MODERATE"
    else:
        resource_constraint = "LOW"

    # --------------------------------------------------------
    # GEOGRAPHIC ACCESS EXPOSURE
    # --------------------------------------------------------

    geographic_barrier = (
        geographic_access_risk == "HIGH"
        or transport_access == "LIMITED"
        or connectivity == "POOR"
    )

    if geographic_access_risk == "HIGH":
        geographic_exposure = "HIGH"
    elif geographic_barrier:
        geographic_exposure = "MODERATE"
    else:
        geographic_exposure = "LOW"

    # --------------------------------------------------------
    # EQUITY EXPOSURE
    # --------------------------------------------------------

    exposure_factors = 0

    if underserved_rate >= 0.40:
        exposure_factors += 1

    if testing_coverage < 25:
        exposure_factors += 1

    if evidence_debt > 0:
        exposure_factors += 1

    if resource_availability < 80:
        exposure_factors += 1

    if blind_spot_risk == "HIGH":
        exposure_factors += 1

    if geographic_exposure == "HIGH":
        exposure_factors += 1

    if exposure_factors >= 5:
        equity_exposure = "HIGH"
    elif exposure_factors >= 3:
        equity_exposure = "MODERATE"
    else:
        equity_exposure = "LOW"

    # --------------------------------------------------------
    # VISIBILITY GAP
    # --------------------------------------------------------

    if underserved_rate > 0 and testing_coverage < 50:
        visibility_gap = "POTENTIAL_HIGH_VISIBILITY_GAP"
    elif testing_coverage < 50:
        visibility_gap = "POTENTIAL_VISIBILITY_GAP"
    else:
        visibility_gap = "LOWER_VISIBILITY_GAP"

    # --------------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------------

    if equity_exposure == "HIGH":
        interpretation = (
            "Multiple structural constraints coexist with limited "
            "health-system evidence. The scenario therefore warrants "
            "explicit equity monitoring before interpreting low observed "
            "burden as low need."
        )

    elif equity_exposure == "MODERATE":
        interpretation = (
            "The scenario contains overlapping underserved, evidence, "
            "resource, or geographic constraints that may reduce visibility "
            "of unmet health needs."
        )

    else:
        interpretation = (
            "The synthetic scenario shows fewer simultaneous equity "
            "exposure factors, but this does not establish population-level "
            "equity or health outcomes."
        )

    return {
        "population": population,
        "underserved_population": underserved_population,
        "underserved_rate": underserved_rate,
        "testing_coverage": testing_coverage,
        "evidence_debt": evidence_debt,
        "resource_availability": resource_availability,
        "resource_constraint": resource_constraint,
        "blind_spot_risk": blind_spot_risk,
        "geographic_access_risk": geographic_access_risk,
        "geographic_exposure": geographic_exposure,
        "evidence_equity_exposure": evidence_equity_exposure,
        "visibility_gap": visibility_gap,
        "exposure_factors": exposure_factors,
        "equity_exposure": equity_exposure,
        "interpretation": interpretation,
    }

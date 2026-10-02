def analyze_evidence(
    actual_tests,
    expected_tests,
    rdt_per_month,
    underserved_rate,
    population,
    required_rdt_per_month,
):
    # --------------------------------------------------------
    # TESTING COVERAGE
    # --------------------------------------------------------

    if expected_tests > 0:
        testing_coverage = (actual_tests / expected_tests) * 100
    else:
        testing_coverage = 0

    # --------------------------------------------------------
    # CAPACITY UTILIZATION
    # --------------------------------------------------------

    if rdt_per_month > 0:
        capacity_utilization = (actual_tests / rdt_per_month) * 100
    else:
        capacity_utilization = 0

    # --------------------------------------------------------
    # EVIDENCE DEBT
    # --------------------------------------------------------

    evidence_debt = max(expected_tests - actual_tests, 0)

    # --------------------------------------------------------
    # EVIDENCE STATUS
    # --------------------------------------------------------

    if testing_coverage < 25:
        evidence_status = "HIGH"
    elif testing_coverage < 50:
        evidence_status = "MODERATE"
    else:
        evidence_status = "LOW"

    # --------------------------------------------------------
    # UNDERSERVED POPULATION
    # --------------------------------------------------------

    underserved_population = population * underserved_rate
    served_population = population - underserved_population

    # --------------------------------------------------------
    # BLIND-SPOT RISK
    # --------------------------------------------------------

    if testing_coverage < 50 and underserved_rate >= 0.40:
        blind_spot_risk = "HIGH"

    elif testing_coverage < 50 or underserved_rate >= 0.40:
        blind_spot_risk = "MODERATE"

    else:
        blind_spot_risk = "LOW"

    # --------------------------------------------------------
    # EVIDENCE SUFFICIENCY
    # --------------------------------------------------------

    evidence_sufficiency_score = min(testing_coverage, 100)

    # --------------------------------------------------------
    # RESOURCE AVAILABILITY PROXY
    #
    # IMPORTANT:
    # This is NOT a validated population access measure.
    # It represents the proportion of required RDT capacity
    # currently available in the synthetic scenario.
    # --------------------------------------------------------

    if required_rdt_per_month > 0:

        resource_availability_proxy = (
            rdt_per_month / required_rdt_per_month
        ) * 100

    else:
        resource_availability_proxy = 0

    resource_availability_proxy = min(
        resource_availability_proxy,
        100,
    )

    return {
        "testing_coverage": testing_coverage,
        "capacity_utilization": capacity_utilization,
        "evidence_debt": evidence_debt,
        "evidence_status": evidence_status,
        "evidence_sufficiency_score": evidence_sufficiency_score,
        "underserved_population": underserved_population,
        "served_population": served_population,
        "blind_spot_risk": blind_spot_risk,
        "resource_availability_proxy": resource_availability_proxy,
    }
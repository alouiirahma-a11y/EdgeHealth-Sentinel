from src.community.evidence import analyze_evidence
from src.equity.equity_audit import audit_equity
from src.equity.health_equity import analyze_health_equity


def simulate_region(
    region,
    health_workers=None,
    rdt_per_month=None,
    microscopes=None,
    actual_tests=None,
):
    """
    Run a synthetic what-if scenario.

    This is a prototype simulation model.
    It is NOT a clinical recommendation
    and NOT a validated health-planning model.
    """

    # --------------------------------------------------------
    # SIMULATED INPUTS
    # --------------------------------------------------------

    simulated_health_workers = (
        region["health_workers"]
        if health_workers is None
        else health_workers
    )

    simulated_rdt = (
        region["rdt_per_month"]
        if rdt_per_month is None
        else rdt_per_month
    )

    simulated_microscopes = (
        region["microscopes"]
        if microscopes is None
        else microscopes
    )

    simulated_tests = (
        region["actual_tests"]
        if actual_tests is None
        else actual_tests
    )

    # --------------------------------------------------------
    # EVIDENCE ENGINE
    # --------------------------------------------------------

    evidence = analyze_evidence(
        actual_tests=simulated_tests,
        expected_tests=region["expected_tests"],
        rdt_per_month=simulated_rdt,
        underserved_rate=region["underserved_rate"],
        population=region["population"],
        required_rdt_per_month=region["required_rdt_per_month"],
    )

    # --------------------------------------------------------
    # RESOURCE GAPS
    # --------------------------------------------------------

    health_worker_gap = max(
        region["required_health_workers"]
        - simulated_health_workers,
        0,
    )

    microscope_gap = max(
        region["required_microscopes"]
        - simulated_microscopes,
        0,
    )

    rdt_gap = max(
        region["required_rdt_per_month"]
        - simulated_rdt,
        0,
    )

    # --------------------------------------------------------
    # RESOURCE AVAILABILITY
    # --------------------------------------------------------

    if region["required_health_workers"] > 0:
        health_worker_availability = (
            simulated_health_workers
            / region["required_health_workers"]
        ) * 100
    else:
        health_worker_availability = 100

    if region["required_microscopes"] > 0:
        microscope_availability = (
            simulated_microscopes
            / region["required_microscopes"]
        ) * 100
    else:
        microscope_availability = 100

    if region["required_rdt_per_month"] > 0:
        rdt_availability = (
            simulated_rdt
            / region["required_rdt_per_month"]
        ) * 100
    else:
        rdt_availability = 100

    health_worker_availability = min(
        health_worker_availability,
        100,
    )

    microscope_availability = min(
        microscope_availability,
        100,
    )

    rdt_availability = min(
        rdt_availability,
        100,
    )

    # --------------------------------------------------------
    # CAPACITY SAFETY
    # --------------------------------------------------------

    if simulated_rdt > 0:
        capacity_exceeded = simulated_tests > simulated_rdt
    else:
        capacity_exceeded = simulated_tests > 0

    if capacity_exceeded:
        capacity_status = "CAPACITY EXCEEDED"

    elif (
        simulated_rdt > 0
        and simulated_tests == simulated_rdt
    ):
        capacity_status = "AT CAPACITY"

    else:
        capacity_status = "WITHIN CAPACITY"

    # --------------------------------------------------------
    # EQUITY AUDIT
    # --------------------------------------------------------

    equity = audit_equity(
        population=region["population"],
        underserved_rate=region["underserved_rate"],
        resource_access_rate=evidence[
            "resource_availability_proxy"
        ],
    )

    # --------------------------------------------------------
    # HEALTH EQUITY INTELLIGENCE
    # --------------------------------------------------------

    health_equity = analyze_health_equity(
        population=region["population"],
        underserved_rate=region["underserved_rate"],
        testing_coverage=evidence["testing_coverage"],
        evidence_debt=evidence["evidence_debt"],
        resource_availability=evidence[
            "resource_availability_proxy"
        ],
        blind_spot_risk=evidence["blind_spot_risk"],
        geographic_access_risk=region[
            "geographic_access_risk"
        ],
        transport_access=region["transport_access"],
        connectivity=region["connectivity"],
    )

    # --------------------------------------------------------
    # RETURN SCENARIO
    # --------------------------------------------------------

    return {
        "inputs": {
            "health_workers": simulated_health_workers,
            "rdt_per_month": simulated_rdt,
            "microscopes": simulated_microscopes,
            "actual_tests": simulated_tests,
        },

        "evidence": evidence,

        "resource_gaps": {
            "health_workers": health_worker_gap,
            "microscopes": microscope_gap,
            "rdt": rdt_gap,
        },

        "resource_availability": {
            "health_workers": health_worker_availability,
            "microscopes": microscope_availability,
            "rdt": rdt_availability,
        },

        "capacity": {
            "exceeded": capacity_exceeded,
            "status": capacity_status,
        },

        "equity": equity,

        "health_equity": health_equity,
    }


def compare_scenarios(baseline, scenario):
    """
    Compare baseline and what-if scenario.
    """

    baseline_evidence = baseline["evidence"]
    scenario_evidence = scenario["evidence"]

    baseline_equity = baseline.get("equity")
    scenario_equity = scenario.get("equity")

    baseline_health_equity = baseline.get("health_equity")
    scenario_health_equity = scenario.get("health_equity")

    comparison = {
        "testing_coverage_change": (
            scenario_evidence["testing_coverage"]
            - baseline_evidence["testing_coverage"]
        ),

        "evidence_debt_change": (
            scenario_evidence["evidence_debt"]
            - baseline_evidence["evidence_debt"]
        ),

        "blind_spot_changed": (
            baseline_evidence["blind_spot_risk"]
            != scenario_evidence["blind_spot_risk"]
        ),
    }

    if baseline_equity and scenario_equity:
        comparison["resource_availability_change"] = (
            scenario_equity["resource_access_rate"]
            - baseline_equity["resource_access_rate"]
        )

        comparison["equity_risk_changed"] = (
            baseline_equity["equity_risk"]
            != scenario_equity["equity_risk"]
        )

    if baseline_health_equity and scenario_health_equity:
        comparison["health_equity_exposure_changed"] = (
            baseline_health_equity["equity_exposure"]
            != scenario_health_equity["equity_exposure"]
        )

        comparison["evidence_equity_exposure_changed"] = (
            baseline_health_equity["evidence_equity_exposure"]
            != scenario_health_equity["evidence_equity_exposure"]
        )

        comparison["visibility_gap_changed"] = (
            baseline_health_equity["visibility_gap"]
            != scenario_health_equity["visibility_gap"]
        )

    return comparison

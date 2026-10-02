from src.simulation.what_if import simulate_region


def compose_interventions(region):
    """
    Compare predefined synthetic intervention scenarios.

    This is a prototype simulation tool.
    It does NOT provide clinical or operational recommendations.
    """

    scenarios = {
        "BASELINE": {},

        "ADD_HEALTH_WORKERS": {
            "health_workers": 4,
        },

        "ADD_MICROSCOPE": {
            "microscopes": 1,
        },

        "INCREASE_RDT_SUPPLY": {
            "rdt_per_month": 120,
        },

        "COMBINED_INTERVENTION": {
            "health_workers": 4,
            "microscopes": 1,
            "rdt_per_month": 120,
            "actual_tests": 100,
        },
    }

    results = {}

    for name, inputs in scenarios.items():
        results[name] = simulate_region(
            region,
            **inputs,
        )

    baseline = results["BASELINE"]
    baseline_evidence = baseline["evidence"]

    comparison = {}

    for name, result in results.items():

        evidence = result["evidence"]

        comparison[name] = {
            "testing_coverage": evidence["testing_coverage"],
            "evidence_debt": evidence["evidence_debt"],
            "capacity_utilization": evidence["capacity_utilization"],
            "blind_spot_risk": evidence["blind_spot_risk"],
            "resource_availability": result[
                "resource_availability"
            ],

            "testing_coverage_change": (
                evidence["testing_coverage"]
                - baseline_evidence["testing_coverage"]
            ),

            "evidence_debt_change": (
                evidence["evidence_debt"]
                - baseline_evidence["evidence_debt"]
            ),

            "capacity_utilization_change": (
                evidence["capacity_utilization"]
                - baseline_evidence["capacity_utilization"]
            ),
        }

    return {
        "scenarios": results,
        "comparison": comparison,
    }


def build_decision_trace(baseline, scenario, scenario_name):
    """
    Explain how a scenario changed relative to baseline.

    This is an explanatory trace, not an autonomous recommendation.
    """

    baseline_evidence = baseline["evidence"]
    scenario_evidence = scenario["evidence"]

    baseline_resources = baseline["resource_availability"]
    scenario_resources = scenario["resource_availability"]

    trace = {
        "scenario": scenario_name,
        "resource_effects": {},
        "evidence_effects": {},
        "capacity_effect": {},
        "blind_spot_effect": {},
        "interpretation": "",
    }

    # --------------------------------------------------------
    # RESOURCE EFFECTS
    # --------------------------------------------------------

    for resource in baseline_resources:

        before = baseline_resources[resource]
        after = scenario_resources[resource]

        trace["resource_effects"][resource] = {
            "before": before,
            "after": after,
            "change": after - before,
        }

    # --------------------------------------------------------
    # EVIDENCE EFFECTS
    # --------------------------------------------------------

    coverage_before = baseline_evidence[
        "testing_coverage"
    ]

    coverage_after = scenario_evidence[
        "testing_coverage"
    ]

    debt_before = baseline_evidence[
        "evidence_debt"
    ]

    debt_after = scenario_evidence[
        "evidence_debt"
    ]

    trace["evidence_effects"] = {
        "testing_coverage": {
            "before": coverage_before,
            "after": coverage_after,
            "change": coverage_after - coverage_before,
        },

        "evidence_debt": {
            "before": debt_before,
            "after": debt_after,
            "change": debt_after - debt_before,
        },
    }

    # --------------------------------------------------------
    # CAPACITY EFFECT
    # --------------------------------------------------------

    utilization_before = baseline_evidence[
        "capacity_utilization"
    ]

    utilization_after = scenario_evidence[
        "capacity_utilization"
    ]

    trace["capacity_effect"] = {
        "before": utilization_before,
        "after": utilization_after,
        "change": utilization_after - utilization_before,
    }

    # --------------------------------------------------------
    # BLIND-SPOT EFFECT
    # --------------------------------------------------------

    blind_spot_before = baseline_evidence[
        "blind_spot_risk"
    ]

    blind_spot_after = scenario_evidence[
        "blind_spot_risk"
    ]

    trace["blind_spot_effect"] = {
        "before": blind_spot_before,
        "after": blind_spot_after,
        "changed": blind_spot_before != blind_spot_after,
    }

    # --------------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------------

    coverage_changed = (
        coverage_after != coverage_before
    )

    debt_changed = (
        debt_after != debt_before
    )

    resource_changed = any(
        scenario_resources[key]
        != baseline_resources[key]
        for key in baseline_resources
    )

    if scenario_name == "BASELINE":

        interpretation = (
            "Baseline scenario. No intervention was applied."
        )

    elif not coverage_changed and resource_changed:

        interpretation = (
            "Resource availability changed, but observed "
            "testing activity did not increase. This scenario "
            "therefore did not change testing coverage."
        )

    elif coverage_changed and debt_changed:

        interpretation = (
            "The scenario changed observed testing activity, "
            "which increased testing coverage and reduced "
            "evidence debt relative to baseline."
        )

    else:

        interpretation = (
            "The scenario changed one or more system indicators "
            "without producing a corresponding change across "
            "all evidence indicators."
        )

    trace["interpretation"] = interpretation

    return trace


if __name__ == "__main__":

    from src.community.scenario import REGION_X

    result = compose_interventions(REGION_X)

    baseline = result["scenarios"]["BASELINE"]

    print("=" * 60)
    print("EDGEHEALTH SENTINEL")
    print("INTERVENTION COMPOSER + DECISION TRACE")
    print("=" * 60)

    print()

    for name, scenario in result["scenarios"].items():

        trace = build_decision_trace(
            baseline,
            scenario,
            name,
        )

        print(name)
        print("-" * 60)

        print("Resource Effects:")

        for resource, effect in trace[
            "resource_effects"
        ].items():

            print(
                f"  {resource}: "
                f"{effect['before']:.2f}% -> "
                f"{effect['after']:.2f}% "
                f"(change: {effect['change']:+.2f}%)"
            )

        print()
        print("Evidence Effects:")

        coverage = trace[
            "evidence_effects"
        ]["testing_coverage"]

        debt = trace[
            "evidence_effects"
        ]["evidence_debt"]

        print(
            f"  Testing Coverage: "
            f"{coverage['before']:.2f}% -> "
            f"{coverage['after']:.2f}% "
            f"(change: {coverage['change']:+.2f}%)"
        )

        print(
            f"  Evidence Debt: "
            f"{debt['before']} -> "
            f"{debt['after']} "
            f"(change: {debt['change']:+.0f})"
        )

        print()
        print("Capacity Effect:")

        capacity = trace["capacity_effect"]

        print(
            f"  Capacity Utilization: "
            f"{capacity['before']:.2f}% -> "
            f"{capacity['after']:.2f}% "
            f"(change: {capacity['change']:+.2f}%)"
        )

        print()
        print("Blind-Spot Effect:")

        blind_spot = trace[
            "blind_spot_effect"
        ]

        print(
            f"  Risk: "
            f"{blind_spot['before']} -> "
            f"{blind_spot['after']}"
        )

        print()
        print("Interpretation:")
        print(
            f"  {trace['interpretation']}"
        )

        print()
        print("=" * 60)

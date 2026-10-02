def generate_solution_options(
    baseline,
    baseline_evidence,
    community_context,
):
    resource_gaps = baseline.get("resource_gaps", {})

    microscope_gap = resource_gaps.get("microscopes", {})
    health_worker_gap = resource_gaps.get("health_workers", {})
    rdt_gap = resource_gaps.get("rdt", {})

    def gap_exists(value):
        if isinstance(value, dict):
            for key in ["gap", "gap_rate", "shortage", "required", "value"]:
                if key in value:
                    try:
                        return float(value[key]) > 0
                    except (TypeError, ValueError):
                        pass
            return False

        try:
            return float(value) > 0
        except (TypeError, ValueError):
            return False

    options = []

    if gap_exists(microscope_gap):
        options.append({
            "name": "Add Diagnostic Microscope",
            "gap": "MICROSCOPE_GAP",
            "expected_effect": "Increase potential microscopy capacity",
            "equity_relevance": "HIGH",
            "feasibility": 40,
            "uncertainty": "MODERATE",
        })

    if gap_exists(health_worker_gap):
        options.append({
            "name": "Add Health Worker Capacity",
            "gap": "HEALTH_WORKER_GAP",
            "expected_effect": "Increase available workforce capacity",
            "equity_relevance": "HIGH",
            "feasibility": 70,
            "uncertainty": "MODERATE",
        })

    if gap_exists(rdt_gap):
        options.append({
            "name": "Increase RDT Supply",
            "gap": "RDT_CAPACITY_GAP",
            "expected_effect": "Increase available rapid-test capacity",
            "equity_relevance": "MODERATE",
            "feasibility": 90,
            "uncertainty": "MODERATE",
        })

    if community_context["transport_access"] == "LIMITED":
        options.append({
            "name": "Improve Transport / Referral Access",
            "gap": "GEOGRAPHIC_ACCESS_GAP",
            "expected_effect": "Reduce simulated geographic access barrier",
            "equity_relevance": "HIGH",
            "feasibility": 60,
            "uncertainty": "HIGH",
        })

    if community_context["connectivity"] == "POOR":
        options.append({
            "name": "Improve Connectivity",
            "gap": "CONNECTIVITY_GAP",
            "expected_effect": "Improve potential information synchronization",
            "equity_relevance": "MODERATE",
            "feasibility": 65,
            "uncertainty": "HIGH",
        })

    if len(options) >= 2:
        options.append({
            "name": "Combined Multi-Resource Intervention",
            "gap": "MULTIPLE_SYSTEM_GAPS",
            "expected_effect": (
                "Simultaneously address multiple simulated "
                "health-system constraints"
            ),
            "equity_relevance": "HIGH",
            "feasibility": 50,
            "uncertainty": "HIGH",
        })

    return options


if __name__ == "__main__":
    print("Solution Recommendation Engine module created.")


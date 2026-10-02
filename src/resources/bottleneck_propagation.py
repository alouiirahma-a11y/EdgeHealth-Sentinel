def analyze_bottleneck_propagation(
    microscope_gap,
    health_worker_gap,
    rdt_gap,
    testing_coverage,
    evidence_debt,
    blind_spot_risk,
    underserved_rate,
):
    bottlenecks = []

    if microscope_gap > 0:
        bottlenecks.append({
            "resource": "MICROSCOPE",
            "capacity_effect": "Reduced microscopy capacity",
            "evidence_effect": "Fewer potential microscopy observations",
        })

    if health_worker_gap > 0:
        bottlenecks.append({
            "resource": "HEALTH_WORKERS",
            "capacity_effect": "Reduced workforce capacity",
            "evidence_effect": "Lower potential testing and follow-up capacity",
        })

    if rdt_gap > 0:
        bottlenecks.append({
            "resource": "RDT_SUPPLY",
            "capacity_effect": "Reduced rapid-testing capacity",
            "evidence_effect": "Lower potential testing coverage",
        })

    if testing_coverage < 25:
        evidence_state = "LOW_EVIDENCE_COVERAGE"
    elif testing_coverage < 50:
        evidence_state = "MODERATE_EVIDENCE_COVERAGE"
    else:
        evidence_state = "HIGHER_EVIDENCE_COVERAGE"

    if evidence_debt > 0:
        debt_state = "EVIDENCE_DEBT_PRESENT"
    else:
        debt_state = "NO_EVIDENCE_DEBT"

    if blind_spot_risk == "HIGH":
        blind_spot_state = "HIGH_BLIND_SPOT_RISK"
    else:
        blind_spot_state = blind_spot_risk

    if underserved_rate >= 0.40:
        equity_state = "HIGH_EQUITY_EXPOSURE"
    elif underserved_rate >= 0.30:
        equity_state = "MODERATE_EQUITY_EXPOSURE"
    else:
        equity_state = "LOWER_EQUITY_EXPOSURE"

    return {
        "bottlenecks": bottlenecks,
        "evidence_state": evidence_state,
        "debt_state": debt_state,
        "blind_spot_state": blind_spot_state,
        "equity_state": equity_state,
        "chain": [
            "RESOURCE_GAP",
            "CAPACITY_CONSTRAINT",
            "EVIDENCE_GAP",
            "EVIDENCE_DEBT",
            "BLIND_SPOT_RISK",
            "POTENTIAL_EQUITY_IMPACT",
        ],
        "interpretation": (
            "Conceptual simulation: a resource bottleneck may constrain "
            "service capacity, which can reduce observed evidence and "
            "increase uncertainty about unmet health needs."
        ),
    }


if __name__ == "__main__":
    result = analyze_bottleneck_propagation(
        microscope_gap=1,
        health_worker_gap=2,
        rdt_gap=40,
        testing_coverage=6.25,
        evidence_debt=375,
        blind_spot_risk="HIGH",
        underserved_rate=0.40,
    )

    print("Bottleneck propagation simulation")
    print(result["chain"])
    print(result["interpretation"])

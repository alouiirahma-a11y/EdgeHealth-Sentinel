from src.community.scenario import REGION_X
from src.community.evidence import analyze_evidence
from src.resources.resource_priority import calculate_resource_priority


def analyze_region(region):

    population = region["population"]
    health_workers = region["health_workers"]
    underserved_rate = region["underserved_rate"]

    # --------------------------------------------------------
    # COMMUNITY
    # --------------------------------------------------------

    underserved_population = (
        population * underserved_rate
    )

    served_population = (
        population - underserved_population
    )

    # --------------------------------------------------------
    # EVIDENCE ENGINE
    # --------------------------------------------------------

    evidence = analyze_evidence(
        actual_tests=region["actual_tests"],
        expected_tests=region["expected_tests"],
        rdt_per_month=region["rdt_per_month"],
        underserved_rate=underserved_rate,
        population=population,
        required_rdt_per_month=region["required_rdt_per_month"],
    )

    # --------------------------------------------------------
    # RESOURCE GAPS
    # --------------------------------------------------------

    required_health_workers = (
        region["required_health_workers"]
    )

    health_worker_gap = max(
        required_health_workers - health_workers,
        0,
    )

    health_worker_gap_rate = (
        health_worker_gap
        / required_health_workers
    ) * 100

    microscopes = region["microscopes"]

    required_microscopes = (
        region["required_microscopes"]
    )

    microscope_gap = max(
        required_microscopes - microscopes,
        0,
    )

    microscope_gap_rate = (
        microscope_gap
        / required_microscopes
    ) * 100

    rdt_per_month = region["rdt_per_month"]

    required_rdt_per_month = (
        region["required_rdt_per_month"]
    )

    rdt_gap = max(
        required_rdt_per_month - rdt_per_month,
        0,
    )

    rdt_gap_rate = (
        rdt_gap
        / required_rdt_per_month
    ) * 100

    # --------------------------------------------------------
    # RESOURCE PRIORITY ENGINE
    # --------------------------------------------------------

    resource_result = calculate_resource_priority(

        health_worker_gap_rate,
        microscope_gap_rate,
        rdt_gap_rate,

        region["health_worker_impact"],
        region["microscope_impact"],
        region["rdt_impact"],

        region["health_worker_feasibility"],
        region["microscope_feasibility"],
        region["rdt_feasibility"],

        region["health_worker_equity"],
        region["microscope_equity"],
        region["rdt_equity"],
    )

    # --------------------------------------------------------
    # STRUCTURED RESULT
    # --------------------------------------------------------

    return {

        "scenario": {
            "name": region["name"],
            "population": population,
        },

        "community": {
            "population": population,
            "health_workers": health_workers,
            "underserved_population": underserved_population,
            "served_population": served_population,
            "underserved_rate": underserved_rate,
        },

        "evidence": evidence,

        "resource_gaps": {

            "health_workers": {
                "gap": health_worker_gap,
                "gap_rate": health_worker_gap_rate,
            },

            "microscopes": {
                "gap": microscope_gap,
                "gap_rate": microscope_gap_rate,
            },

            "rdt": {
                "gap": rdt_gap,
                "gap_rate": rdt_gap_rate,
            },
        },

        "resource_priority": resource_result,

    }


# ============================================================
# TEST RUN
# ============================================================

if __name__ == "__main__":

    result = analyze_region(REGION_X)

    print("=" * 60)
    print("EDGEHEALTH SENTINEL")
    print("COMMUNITY INTELLIGENCE ENGINE")
    print("=" * 60)

    print()
    print("SCENARIO:")
    print(result["scenario"])

    print()
    print("COMMUNITY:")
    print(result["community"])

    print()
    print("EVIDENCE:")
    print(result["evidence"])

    print()
    print("RESOURCE GAPS:")
    print(result["resource_gaps"])

    print()
    print("RESOURCE PRIORITY:")
    print(result["resource_priority"])

    print()
    print("=" * 60)
    print("END OF COMMUNITY INTELLIGENCE ENGINE")
    print("=" * 60)
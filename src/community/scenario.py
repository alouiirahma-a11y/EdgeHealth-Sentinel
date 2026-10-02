# ============================================================
# EDGEHEALTH SENTINEL
# Synthetic Community Scenario
# ============================================================

# Synthetic scenario for prototype demonstration.
# NOT real-world health data.

REGION_X = {
    "name": "Region X",

    # Community
    "population": 8000,
    "health_workers": 2,
    "underserved_rate": 0.40,

    # Testing and evidence
    "rdt_per_month": 80,
    "actual_tests": 25,
    "expected_tests": 400,

    # Physical resources
    "microscopes": 0,

    # Required resources
    "required_health_workers": 4,
    "required_microscopes": 1,
    "required_rdt_per_month": 120,

    # Geographic and digital access
    "transport_access": "LIMITED",
    "connectivity": "POOR",
    "geographic_access_risk": "HIGH",

    # Resource impact assumptions
    "health_worker_impact": 80,
    "microscope_impact": 90,
    "rdt_impact": 60,

    # Feasibility assumptions
    "health_worker_feasibility": 70,
    "microscope_feasibility": 40,
    "rdt_feasibility": 90,

    # Equity assumptions
    "health_worker_equity": 80,
    "microscope_equity": 90,
    "rdt_equity": 50,
}

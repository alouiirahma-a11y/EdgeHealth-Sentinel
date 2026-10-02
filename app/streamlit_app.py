import sys
import tempfile
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.community.scenario import REGION_X
from src.community.region import analyze_region
from src.community.context import analyze_community_context
from src.simulation.what_if import simulate_region
from src.simulation.solution_recommendation import generate_solution_options
from src.simulation.intervention_composer import compose_interventions, build_decision_trace
from src.resources.bottleneck_propagation import analyze_bottleneck_propagation
from src.diagnostic.pipeline import run_diagnostic_pipeline


st.set_page_config(
    page_title="EdgeHealth Sentinel",
    page_icon="🛰️",
    layout="wide",
)


st.markdown(
    """
    <style>
    .stApp {
        background-color: #07111f;
        color: #f8fafc;
    }

    header {
        background-color: transparent;
    }

    [data-testid="stMetric"] {
        background-color: #0d1b2a;
        border: 1px solid #263b55;
        border-radius: 12px;
        padding: 14px;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    .stWidgetLabel {
        color: #e2e8f0;
    }

    .stMarkdown {
        color: #f8fafc;
    }

    .stCaption {
        color: #94a3b8;
    }

    [data-testid="stSidebar"] {
        background-color: #0d1b2a;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    button {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def pct(value):
    return f"{value:.2f}%"


def section(title, icon):
    st.header(f"{icon} {title}")


def show_metric_row(items):
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        with column:
            st.metric(label, value)


baseline = analyze_region(REGION_X)
baseline_evidence = baseline["evidence"]
baseline_resources = baseline["resource_priority"]
baseline_simulation = simulate_region(REGION_X)
baseline_equity = baseline_simulation["equity"]

community_context = analyze_community_context(
    population=REGION_X["population"],
    area_km2=250,
    settlements=12,
    health_facilities=1,
    health_workers=REGION_X["health_workers"],
    underserved_rate=REGION_X["underserved_rate"],
    transport_access="LIMITED",
    connectivity="POOR",
)


with st.sidebar:
    st.title("🛰️ EdgeHealth Sentinel")
    st.caption("Health-System Intelligence")
    st.caption("Edge AI • Evidence • Equity")

    st.markdown("### System Modules")
    st.write("🧭 Command View")
    st.write("🧠 Evidence Intelligence")
    st.write("⚙️ Resource Intelligence")
    st.write("⚖️ Equity Audit")
    st.write("🧪 What-If Simulator")
    st.write("🧩 Intervention Composer")
    st.write("🔍 Decision Trace")
    st.write("🛡️ Safety & Governance")

    st.warning("Synthetic research prototype.\n\nNot clinically validated.")


st.title("🛰️ EdgeHealth Sentinel")
st.subheader(
    "Adaptive, Uncertainty-Aware and Equity-Driven Edge AI for "
    "Health-System Intelligence in Resource-Constrained Communities."
)

st.success("◉ SYNTHETIC RESEARCH PROTOTYPE")

st.info(
    "**Core Intelligence Principle**\n\n"
    "EdgeHealth Sentinel does not simply ask whether AI can diagnose this patient.\n\n"
    "It asks whether the health system has enough evidence, resources and "
    "infrastructure to safely act — and where additional evidence or resources "
    "may be needed."
)


# ============================================================
# COMMUNITY HEALTH COMMAND VIEW
# ============================================================

section("Community Health Command View", "🛰️")
st.caption("Synthetic Region X — all values are simulated.")

show_metric_row(
    [
        ("Population", f'{baseline["community"]["population"]:,.0f}'),
        ("Testing Coverage", pct(baseline_evidence["testing_coverage"])),
        ("Evidence Debt", f'{baseline_evidence["evidence_debt"]:,.0f}'),
        ("Blind-Spot Risk", baseline_evidence["blind_spot_risk"]),
    ]
)

show_metric_row(
    [
        ("Health Workers", REGION_X["health_workers"]),
        ("RDT Availability", pct(baseline_evidence["resource_availability_proxy"])),
        ("Capacity Utilization", pct(baseline_evidence["capacity_utilization"])),
        ("Equity Risk", baseline_equity["equity_risk"]),
    ]
)


# ============================================================
# SYSTEM SITUATION
# ============================================================

section("System Situation", "🌐")

show_metric_row(
    [
        ("Population", f'{baseline["community"]["population"]:,.0f}'),
        (
            "Underserved Population",
            f'{baseline_evidence["underserved_population"]:,.0f} '
            f'({REGION_X["underserved_rate"] * 100:.0f}%)',
        ),
        ("Testing Coverage", pct(baseline_evidence["testing_coverage"])),
        ("Evidence Debt", f'{baseline_evidence["evidence_debt"]:,.0f}'),
        ("Blind-Spot Risk", baseline_evidence["blind_spot_risk"]),
    ]
)

st.write("**Priority resource identified by the synthetic model:**")
st.success(baseline_resources["priority_resource"])


# ============================================================
# COMMUNITY SITUATION
# ============================================================

section("Community Situation", "🏘️")

show_metric_row(
    [
        ("Population", f'{REGION_X["population"]:,.0f}'),
        ("Health Workers", REGION_X["health_workers"]),
        (
            "Underserved Population",
            f'{baseline_evidence["underserved_population"]:,.0f}',
        ),
        (
            "Underserved Rate",
            pct(REGION_X["underserved_rate"] * 100),
        ),
    ]
)


# ============================================================
# COMMUNITY & GEOGRAPHIC CONTEXT
# ============================================================

section("Community & Geographic Context", "🗺️")

st.caption(
    "Synthetic geographic and access context for prototype demonstration. "
    "These indicators are not validated measures of real-world healthcare access."
)

show_metric_row(
    [
        ("Area", f'{community_context["area_km2"]} km²'),
        (
            "Population Density",
            f'{community_context["population_density"]:.2f}/km²',
        ),
        ("Settlements", community_context["settlements"]),
        ("Health Facilities", community_context["health_facilities"]),
    ]
)

show_metric_row(
    [
        (
            "Population / Facility",
            f'{community_context["population_per_facility"]:,.0f}',
        ),
        (
            "Health Workers / 1,000",
            f'{community_context["health_worker_density_per_1000"]:.2f}',
        ),
        ("Transport", community_context["transport_access"]),
        ("Connectivity", community_context["connectivity"]),
    ]
)

st.info(
    f'Geographic Access Risk: **{community_context["geographic_access_risk"]}** — '
    "the prototype combines transport, connectivity, settlement dispersion, "
    "and facility coverage signals."
)


# ============================================================
# GEOGRAPHIC BLIND-SPOT INTELLIGENCE
# ============================================================

section("Geographic Blind-Spot Intelligence", "🕳️")

st.caption(
    "Prototype detection of areas that may be poorly observed because of "
    "limited testing, geographic access barriers, and underserved populations."
)

blind_spot_signals = []

if baseline_evidence["testing_coverage"] < 25:
    blind_spot_signals.append("LOW_TESTING_COVERAGE")

if community_context["geographic_access_risk"] == "HIGH":
    blind_spot_signals.append("HIGH_GEOGRAPHIC_ACCESS_RISK")

if community_context["connectivity"] == "POOR":
    blind_spot_signals.append("POOR_CONNECTIVITY")

if community_context["transport_access"] == "LIMITED":
    blind_spot_signals.append("LIMITED_TRANSPORT")

if baseline["community"]["underserved_rate"] >= 0.40:
    blind_spot_signals.append("HIGH_UNDERSERVICE")

if len(blind_spot_signals) >= 3:
    geographic_blind_spot = "HIGH"
elif len(blind_spot_signals) >= 1:
    geographic_blind_spot = "MODERATE"
else:
    geographic_blind_spot = "LOW"

show_metric_row(
    [
        ("Geographic Blind-Spot Risk", geographic_blind_spot),
        ("Signals Detected", len(blind_spot_signals)),
        ("Testing Coverage", pct(baseline_evidence["testing_coverage"])),
        ("Underserved Rate", pct(REGION_X["underserved_rate"] * 100)),
    ]
)

if geographic_blind_spot == "HIGH":
    st.warning(
        "Potential geographic blind spot detected. Low observed testing should "
        "not be interpreted as low health need when access barriers and evidence "
        "gaps are present."
    )
else:
    st.info(
        "No high geographic blind-spot signal detected under the current "
        "synthetic prototype rules."
    )

st.caption(
    "Synthetic prototype rule — not a validated epidemiological, geographic-access, "
    "or population-risk measure."
)


# ============================================================
# SOLUTION RECOMMENDATION ENGINE
# ============================================================

section("Solution Recommendation Engine", "🧩")

st.caption(
    "Prototype comparison of simulated interventions. The system does not "
    "make autonomous operational decisions."
)

solution_options = generate_solution_options(
    baseline=baseline,
    baseline_evidence=baseline_evidence,
    community_context=community_context,
)

st.info("AI proposes. Evidence constrains. Simulation tests. Humans decide.")

for option in solution_options:
    with st.container(border=True):
        st.markdown(f'### {option["name"]}')

        show_metric_row(
            [
                ("Gap Addressed", option["gap"]),
                ("Equity Relevance", option["equity_relevance"]),
                ("Feasibility", f'{option["feasibility"]}/100'),
                ("Uncertainty", option["uncertainty"]),
            ]
        )

        st.write(f'**Expected simulated effect:** {option["expected_effect"]}')

st.caption(
    "These are synthetic prototype scenarios. They are not validated recommendations "
    "for real-world resource allocation or clinical operations."
)


# ============================================================
# SITUATIONAL AWARENESS
# ============================================================

section("Situational Awareness", "👁️")

show_metric_row(
    [
        ("Testing Coverage", pct(baseline_evidence["testing_coverage"])),
        ("Evidence Debt", f'{baseline_evidence["evidence_debt"]:,.0f}'),
        ("Capacity Utilization", pct(baseline_evidence["capacity_utilization"])),
        ("Blind-Spot Risk", baseline_evidence["blind_spot_risk"]),
    ]
)


# ============================================================
# RESOURCE PRIORITY
# ============================================================

section("Resource Priority", "🎯")

show_metric_row(
    [
        ("Priority Resource", baseline_resources["priority_resource"]),
    ]
)

st.write(
    "The priority is generated from a synthetic score combining resource gap, "
    "estimated impact, feasibility and an equity factor."
)

st.warning(
    "This is an experimental decision-support model, not a validated "
    "resource-allocation algorithm."
)

with st.expander("Why This Priority?"):
    trace = baseline_resources["decision_trace"]

    for resource, data in trace.items():
        st.markdown(f"### {resource}")

        show_metric_row(
            [
                ("Gap Rate", f'{data["gap_rate"]:.2f}%'),
                ("Impact", f'{data["impact"]:.2f}'),
                ("Feasibility", f'{data["feasibility"]:.2f}'),
                ("Equity Factor", f'{data["equity"]:.2f}'),
            ]
        )

        show_metric_row(
            [
                ("Base Score", f'{data["base_score"]:.2f}'),
                (
                    "Equity-Adjusted Score",
                    f'{data["equity_adjusted_score"]:.2f}',
                ),
            ]
        )


# ============================================================
# EQUITY AUDIT
# ============================================================

section("Equity Audit", "⚖️")

show_metric_row(
    [
        ("Equity Risk", baseline_equity["equity_risk"]),
        (
            "Underserved Population",
            f'{baseline_equity["underserved_population"]:,.0f}',
        ),
        (
            "Resource Availability",
            pct(baseline_equity["resource_access_rate"]),
        ),
    ]
)

st.subheader("Equity Interpretation")
st.info(baseline_equity["equity_warning"])

st.caption(
    "This is a synthetic equity audit and is not a validated population-level "
    "fairness metric."
)


# ============================================================
# EVIDENCE INTELLIGENCE
# ============================================================

section("Evidence Intelligence", "🧠")

show_metric_row(
    [
        (
            "Evidence Sufficiency",
            pct(baseline_evidence["evidence_sufficiency_score"]),
        ),
        ("Evidence Status", baseline_evidence["evidence_status"]),
        ("Evidence Debt", f'{baseline_evidence["evidence_debt"]:,.0f}'),
        ("Testing Coverage", pct(baseline_evidence["testing_coverage"])),
    ]
)

st.subheader("Evidence Debt")

st.write(
    "Evidence Debt represents the difference between expected testing activity "
    "and observed testing activity in this synthetic scenario."
)

st.info(
    "A low number of observations should not automatically be interpreted "
    "as low disease prevalence."
)

st.subheader("Evidence Interpretation")

expected_tests = REGION_X["expected_tests"]
actual_tests = REGION_X["actual_tests"]
evidence_debt = baseline_evidence["evidence_debt"]
testing_coverage = baseline_evidence["testing_coverage"]

st.write(
    f"The scenario expects approximately **{expected_tests:,.0f}** tests "
    f"but currently records **{actual_tests:,.0f}** observed tests."
)

st.write(
    f"This creates an evidence debt of **{evidence_debt:,.0f}** observations, "
    f"with testing coverage at **{testing_coverage:.2f}%**."
)

if testing_coverage < 25:
    st.warning(
        "Evidence is currently limited. The system should treat low observed "
        "activity as an evidence gap rather than as evidence of low health need."
    )
elif testing_coverage < 50:
    st.warning(
        "Evidence is incomplete. Additional observations would improve "
        "situational awareness."
    )
else:
    st.success(
        "Observed testing activity provides stronger coverage of the expected "
        "testing demand under this synthetic scenario."
    )

with st.expander("Why Evidence Debt Matters"):
    st.write(
        "Evidence Debt measures how much expected observation is currently "
        "missing from the available evidence."
    )

    st.write(
        "A high Evidence Debt does not prove that disease burden is high or low. "
        "It indicates that the system has insufficient observations to characterize "
        "the situation confidently."
    )

    st.write(
        "This distinction helps prevent a common analytical error: interpreting "
        "absence of observations as absence of need."
    )

    st.caption("Synthetic prototype metric — not a validated epidemiological measure.")


# ============================================================
# RESOURCE INTELLIGENCE
# ============================================================

section("Resource Intelligence", "⚙️")

resource_gaps = baseline["resource_gaps"]
resource_scores = baseline_resources["scores"]
priority_resource = baseline_resources["priority_resource"]
decision_trace = baseline_resources["decision_trace"]

st.subheader("Resource Gaps")

show_metric_row(
    [
        ("Health Worker Gap", resource_gaps["health_workers"]["gap"]),
        ("Microscope Gap", resource_gaps["microscopes"]["gap"]),
        ("RDT Gap", resource_gaps["rdt"]["gap"]),
    ]
)

st.subheader("Resource Priority Scores")

show_metric_row(
    [
        ("Health Workers", f'{resource_scores["HEALTH WORKERS"]:.2f}'),
        ("Microscopes", f'{resource_scores["MICROSCOPES"]:.2f}'),
        ("RDT", f'{resource_scores["RDT"]:.2f}'),
    ]
)

st.info(
    f"The current synthetic scoring model identifies **{priority_resource}** "
    "as the highest-priority resource under this scenario."
)

st.subheader("Decision Trace")

st.write(
    "The decision trace shows the factors used by the prototype scoring model. "
    "It is provided for transparency and does not represent a validated "
    "resource-allocation method."
)

for resource, data in decision_trace.items():
    with st.expander(resource):
        show_metric_row(
            [
                ("Gap Rate", pct(data["gap_rate"])),
                ("Impact", f'{data["impact"]:.0f}'),
                ("Feasibility", f'{data["feasibility"]:.0f}'),
                ("Equity", f'{data["equity"]:.0f}'),
            ]
        )

        st.write(f'Base score: **{data["base_score"]:.2f}**')
        st.write(
            f'Equity-adjusted score: **{data["equity_adjusted_score"]:.2f}**'
        )

st.caption(
    "Synthetic prioritization model — scores are illustrative and have not "
    "been clinically or operationally validated."
)


# ============================================================
# RESOURCE BOTTLENECK PROPAGATION
# ============================================================

section("Resource Bottleneck Propagation", "🔗")

st.caption(
    "Conceptual simulation of how resource constraints may propagate into "
    "evidence gaps and uncertainty. This is not a validated causal model."
)

resource_gaps_for_bottleneck = baseline["resource_gaps"]

bottleneck_result = analyze_bottleneck_propagation(
    microscope_gap=resource_gaps_for_bottleneck["microscopes"]["gap"],
    health_worker_gap=resource_gaps_for_bottleneck["health_workers"]["gap"],
    rdt_gap=resource_gaps_for_bottleneck["rdt"]["gap"],
    testing_coverage=baseline_evidence["testing_coverage"],
    evidence_debt=baseline_evidence["evidence_debt"],
    blind_spot_risk=baseline_evidence["blind_spot_risk"],
    underserved_rate=REGION_X["underserved_rate"],
)

show_metric_row(
    [
        ("Evidence State", bottleneck_result["evidence_state"]),
        ("Debt State", bottleneck_result["debt_state"]),
        ("Blind-Spot State", bottleneck_result["blind_spot_state"]),
        ("Equity Exposure", bottleneck_result["equity_state"]),
    ]
)

st.subheader("Detected Bottlenecks")

for bottleneck in bottleneck_result["bottlenecks"]:
    with st.container(border=True):
        st.markdown(f'### {bottleneck["resource"]}')
        st.write(f'**Capacity effect:** {bottleneck["capacity_effect"]}')
        st.write(f'**Evidence effect:** {bottleneck["evidence_effect"]}')

st.subheader("Propagation Chain")
st.write(" → ".join(bottleneck_result["chain"]))
st.info(bottleneck_result["interpretation"])


# ============================================================
# WHAT-IF RESOURCE & INTERVENTION SIMULATOR
# ============================================================

section("What-If Resource & Intervention Simulator", "🧪")

st.info(
    "Interactive scenario laboratory.\n\n"
    "Change the values below to explore how the synthetic health-system "
    "indicators respond.\n\n"
    "The simulation does not provide clinical advice and does not predict "
    "real-world health outcomes."
)

col1, col2 = st.columns(2)

with col1:
    simulated_health_workers = st.slider(
        "Health Workers",
        min_value=0,
        max_value=10,
        value=REGION_X["health_workers"],
        step=1,
        key="sim_health_workers",
    )

    simulated_microscopes = st.slider(
        "Microscopes",
        min_value=0,
        max_value=5,
        value=REGION_X["microscopes"],
        step=1,
        key="sim_microscopes",
    )

with col2:
    simulated_rdt = st.slider(
        "RDTs per Month",
        min_value=0,
        max_value=300,
        value=REGION_X["rdt_per_month"],
        step=10,
        key="sim_rdt",
    )

    simulated_tests = st.slider(
        "Actual Tests",
        min_value=0,
        max_value=500,
        value=REGION_X["actual_tests"],
        step=5,
        key="sim_tests",
    )

simulation = simulate_region(
    REGION_X,
    health_workers=simulated_health_workers,
    rdt_per_month=simulated_rdt,
    microscopes=simulated_microscopes,
    actual_tests=simulated_tests,
)

simulation_evidence = simulation["evidence"]
simulation_equity = simulation["equity"]

st.subheader("Simulation Results")

show_metric_row(
    [
        ("Testing Coverage", pct(simulation_evidence["testing_coverage"])),
        ("Evidence Debt", f'{simulation_evidence["evidence_debt"]:,.0f}'),
        (
            "Capacity Utilization",
            pct(simulation_evidence["capacity_utilization"]),
        ),
        ("Blind-Spot Risk", simulation_evidence["blind_spot_risk"]),
    ]
)

st.subheader("Simulated Resource Availability")

show_metric_row(
    [
        (
            "Health Workers",
            pct(simulation["resource_availability"]["health_workers"]),
        ),
        (
            "Microscopes",
            pct(simulation["resource_availability"]["microscopes"]),
        ),
        ("RDT", pct(simulation["resource_availability"]["rdt"])),
    ]
)

st.subheader("Simulated Equity Impact")

show_metric_row(
    [
        ("Equity Risk", simulation_equity["equity_risk"]),
        (
            "Underserved Population",
            f'{simulation_equity["underserved_population"]:,.0f}',
        ),
        (
            "Resource Availability",
            pct(simulation_equity["resource_access_rate"]),
        ),
    ]
)

st.subheader("Simulated Resource Gaps")

show_metric_row(
    [
        (
            "Health Worker Gap",
            simulation["resource_gaps"]["health_workers"],
        ),
        (
            "Microscope Gap",
            simulation["resource_gaps"]["microscopes"],
        ),
        (
            "RDT Gap",
            simulation["resource_gaps"]["rdt"],
        ),
    ]
)

st.subheader("Capacity Status")

capacity = simulation["capacity"]

if capacity["exceeded"]:
    st.error(f'Capacity status: {capacity["status"]}')
elif capacity["status"] == "AT CAPACITY":
    st.warning(f'Capacity status: {capacity["status"]}')
else:
    st.success(f'Capacity status: {capacity["status"]}')

st.subheader("Simulation Interpretation")

baseline_simulation = simulate_region(REGION_X)

coverage_change = (
    simulation_evidence["testing_coverage"]
    - baseline_simulation["evidence"]["testing_coverage"]
)

debt_change = (
    simulation_evidence["evidence_debt"]
    - baseline_simulation["evidence"]["evidence_debt"]
)

if coverage_change != 0 or debt_change != 0:
    st.info(
        "Observed testing activity changed. This changed testing coverage "
        "and evidence debt relative to the baseline scenario."
    )
else:
    st.info(
        "Resource conditions changed, but observed testing activity remained unchanged.\n\n"
        "This means resource availability alone did not change the observed "
        "evidence level in this synthetic scenario."
    )


# ============================================================
# INTERVENTION COMPOSER
# ============================================================

section("Intervention Composer", "🧩")

st.info(
    "The Intervention Composer compares predefined synthetic scenarios.\n\n"
    "It does not automatically recommend an intervention."
)

composer = compose_interventions(REGION_X)
scenario_names = list(composer["scenarios"].keys())

selected_scenario = st.selectbox(
    "Select an intervention scenario",
    options=scenario_names,
    key="intervention_selector",
)

selected_result = composer["scenarios"][selected_scenario]
selected_comparison = composer["comparison"][selected_scenario]

st.subheader("Intervention Scenario")

show_metric_row(
    [
        ("Selected Scenario", selected_scenario),
    ]
)

show_metric_row(
    [
        (
            "Testing Coverage",
            pct(selected_comparison["testing_coverage"]),
        ),
        (
            "Evidence Debt",
            f'{selected_comparison["evidence_debt"]:,.0f}',
        ),
        (
            "Capacity Utilization",
            pct(selected_comparison["capacity_utilization"]),
        ),
        (
            "Blind-Spot Risk",
            selected_comparison["blind_spot_risk"],
        ),
    ]
)

st.subheader("Resource Effects")

resource_effects = selected_comparison["resource_availability"]
baseline_resource_effects = composer["comparison"]["BASELINE"][
    "resource_availability"
]

for resource in ("health_workers", "microscopes", "rdt"):
    before = baseline_resource_effects[resource]
    after = resource_effects[resource]
    change = after - before

    with st.expander(resource.replace("_", " ").title()):
        show_metric_row(
            [
                ("Before", pct(before)),
                ("After", pct(after)),
                ("Change", f"{change:+.2f}%"),
            ]
        )

st.subheader("Evidence Effects")

baseline_comparison = composer["comparison"]["BASELINE"]

coverage_before = baseline_comparison["testing_coverage"]
coverage_after = selected_comparison["testing_coverage"]

debt_before = baseline_comparison["evidence_debt"]
debt_after = selected_comparison["evidence_debt"]

show_metric_row(
    [
        ("Coverage Before", pct(coverage_before)),
        ("Coverage After", pct(coverage_after)),
        ("Coverage Change", f"{coverage_after - coverage_before:+.2f}%"),
    ]
)

show_metric_row(
    [
        ("Debt Before", f"{debt_before:,.0f}"),
        ("Debt After", f"{debt_after:,.0f}"),
        ("Debt Change", f"{debt_after - debt_before:+,.0f}"),
    ]
)

st.subheader("Capacity Effect")

capacity_before = baseline_comparison["capacity_utilization"]
capacity_after = selected_comparison["capacity_utilization"]

show_metric_row(
    [
        ("Before", pct(capacity_before)),
        ("After", pct(capacity_after)),
        ("Change", f"{capacity_after - capacity_before:+.2f}%"),
    ]
)

st.subheader("Blind-Spot Effect")

blind_before = baseline_comparison["blind_spot_risk"]
blind_after = selected_comparison["blind_spot_risk"]

show_metric_row(
    [
        ("Before", blind_before),
        ("After", blind_after),
        ("Changed", "YES" if blind_before != blind_after else "NO"),
    ]
)

section("Decision Trace", "🔍")

baseline_result = composer["scenarios"]["BASELINE"]

intervention_decision_trace = build_decision_trace(
    baseline_result,
    selected_result,
    selected_scenario,
)

st.write(f'**Selected scenario:** {intervention_decision_trace["scenario"]}')
st.write(f'**Interpretation:** {intervention_decision_trace["interpretation"]}')


# ============================================================
# DIAGNOSTIC SAFETY DEMO
# ============================================================

section("Diagnostic Safety Demo", "🩺")

st.info(
    "Upload a public or appropriately anonymized microscopy cell image to run "
    "the research prototype through the Quality Gate, trained ML model, "
    "uncertainty assessment, and Safety Governor."
)

uploaded_image = st.file_uploader(
    "Upload a microscopy cell image",
    type=["jpg", "jpeg", "png"],
    key="diagnostic_image_uploader",
)

if uploaded_image is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_image.getbuffer())
        temp_image_path = temp_file.name

    try:
        result = run_diagnostic_pipeline(temp_image_path)
        st.session_state["diagnostic_result"] = result

        quality_result = result["quality"]
        model_result = result.get("model")
        uncertainty_result = result.get("uncertainty")
        safety_result = result["safety"]

        st.subheader("🔬 Diagnostic Pipeline Result")

        if model_result is not None:
            show_metric_row(
                [
                    ("Prediction", model_result["prediction"]),
                    (
                        "Parasitized Probability",
                        f'{model_result["parasitized_probability"] * 100:.2f}%',
                    ),
                    (
                        "Model Confidence Proxy",
                        f'{model_result["confidence"] * 100:.2f}%',
                    ),
                    (
                        "Image Quality",
                        quality_result["quality_status"],
                    ),
                ]
            )

            st.subheader("🧠 Uncertainty Assessment")

            show_metric_row(
                [
                    (
                        "Status",
                        uncertainty_result["status"],
                    ),
                    (
                        "Uncertainty",
                        f'{uncertainty_result["uncertainty"] * 100:.2f}%',
                    ),
                    (
                        "Suggested Action",
                        uncertainty_result["decision"],
                    ),
                ]
            )

            st.subheader("🛡️ Safety Governor")

            if safety_result["decision"] == "PROCEED":
                st.success("Safety Governor: PROCEED")
            elif safety_result["decision"] == "HUMAN_REVIEW":
                st.warning("Safety Governor: HUMAN REVIEW")
            else:
                st.error(f'Safety Governor: {safety_result["decision"]}')

            show_metric_row(
                [
                    ("Final Decision", result["final_decision"]),
                    ("Reason", safety_result["reason"]),
                ]
            )

        else:
            st.error("The Quality Gate rejected the image.")

            show_metric_row(
                [
                    ("Quality Status", quality_result["quality_status"]),
                    ("Decision", result["final_decision"]),
                ]
            )

            st.write("Quality issues:")

            for issue in quality_result["issues"]:
                st.write(f"- {issue}")

    except Exception as error:
        st.error(f"Diagnostic pipeline error: {error}")


st.caption(
    "Research prototype only. The model is not clinically validated. "
    "Model probability is not a clinical diagnosis or calibrated clinical "
    "confidence. Human review remains necessary for uncertain or unsafe cases."
)


# ============================================================
# HUMAN REVIEW & DECISION TRACE
# ============================================================

section("Human Review & Decision Trace", "👩⚕️")

st.info(
    "When the Safety Governor cannot safely proceed, the prototype routes the "
    "case toward additional evidence or human review. This is a simulated "
    "research workflow."
)

diagnostic_result = st.session_state.get("diagnostic_result")

if diagnostic_result is not None:
    current_decision = diagnostic_result.get("final_decision", "UNKNOWN")
    safety_result = diagnostic_result.get("safety", {})
    uncertainty_result = diagnostic_result.get("uncertainty", {})

    if current_decision in ("ADDITIONAL_EVIDENCE", "HUMAN_REVIEW"):
        st.warning(
            f"AI decision: {current_decision}. "
            "Automated resolution is not considered sufficient."
        )

        st.subheader("🧭 Recommended Next Step")

        if current_decision == "ADDITIONAL_EVIDENCE":
            st.write(
                "Collect additional evidence before relying on the model output. "
                "Examples include another microscopy field, a repeat image, "
                "or an independent review."
            )
        else:
            st.write(
                "Escalate the case to a qualified human reviewer."
            )

        review_decision = st.selectbox(
            "Simulated reviewer decision",
            [
                "PENDING_REVIEW",
                "CONFIRMED_BY_HUMAN",
                "REJECTED_BY_HUMAN",
                "REQUEST_MORE_EVIDENCE",
            ],
            key="human_review_decision",
        )

        reviewer_note = st.text_area(
            "Reviewer note",
            placeholder="Document why the reviewer selected this action.",
            key="human_review_note",
        )

        if st.button(
            "Record Review Decision",
            key="record_review",
        ):
            st.session_state["review_record"] = {
                "ai_decision": current_decision,
                "uncertainty_status": uncertainty_result.get(
                    "status", "UNKNOWN"
                ),
                "safety_reason": safety_result.get(
                    "reason", "UNKNOWN"
                ),
                "human_decision": review_decision,
                "reviewer_note": reviewer_note,
            }

            st.success(
                "Human review decision recorded in the prototype."
            )

    if "review_record" in st.session_state:
        st.subheader("🧭 Decision Trace")

        trace = st.session_state["review_record"]

        show_metric_row(
            [
                ("AI Decision", trace["ai_decision"]),
                ("Uncertainty", trace["uncertainty_status"]),
                ("Safety Reason", trace["safety_reason"]),
                ("Human Decision", trace["human_decision"]),
            ]
        )

        if trace["reviewer_note"]:
            st.caption("Reviewer note")
            st.write(trace["reviewer_note"])

        st.caption(
            "Prototype audit trace only. No clinical decision is created "
            "by this interface."
        )


# ============================================================
# SAFETY & GOVERNANCE
# ============================================================

section("Safety & Governance", "🛡️")

st.warning("Prototype status")

st.write(
    "This dashboard uses synthetic data and experimental simulation logic."
)

st.write("It is not a clinical diagnostic system.")

st.write("It is not clinically validated.")

st.write(
    "It does not represent real-world disease prevalence, outbreak detection, "
    "population access, or resource-allocation recommendations."
)

st.write(
    "Resource and equity scores are prototype decision-support constructs "
    "and require external validation before any operational use."
)

with st.expander("Governance Principles"):
    st.subheader("Human Oversight")

    st.write(
        "High uncertainty or insufficient evidence should trigger human review "
        "rather than autonomous action."
    )

    st.divider()

    st.subheader("Evidence Awareness")

    st.write(
        "Missing observations are treated as evidence limitations rather than "
        "automatically interpreted as absence of disease."
    )

    st.divider()

    st.subheader("Auditability")

    st.write(
        "Important synthetic decisions and scenario changes are represented "
        "through explicit decision traces."
    )

    st.divider()

    st.subheader("Privacy")

    st.write(
        "The prototype is designed around synthetic, public or appropriately "
        "anonymized data rather than confidential institutional data."
    )

    st.divider()

    st.subheader("Controlled Learning")

    st.write(
        "Future learning workflows should use verified human-reviewed data "
        "rather than uncontrolled autonomous self-training."
    )


st.divider()
st.caption("EdgeHealth Sentinel")
st.caption("Health × Computer Science × AI × Equity × Responsible Innovation")
st.caption("Synthetic research prototype — 2026")


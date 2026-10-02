def calculate_resource_priority(
    health_worker_gap_rate,
    microscope_gap_rate,
    rdt_gap_rate,
    health_worker_impact,
    microscope_impact,
    rdt_impact,
    health_worker_feasibility,
    microscope_feasibility,
    rdt_feasibility,
    health_worker_equity,
    microscope_equity,
    rdt_equity,
):
    # --------------------------------------------------------
    # BASE SYNTHETIC PRIORITY SCORES
    # --------------------------------------------------------

    health_worker_score = (
        health_worker_gap_rate
        * health_worker_impact
        * health_worker_feasibility
        / 10000
    )

    microscope_score = (
        microscope_gap_rate
        * microscope_impact
        * microscope_feasibility
        / 10000
    )

    rdt_score = (
        rdt_gap_rate
        * rdt_impact
        * rdt_feasibility
        / 10000
    )

    # --------------------------------------------------------
    # EQUITY-ADJUSTED SCORES
    # --------------------------------------------------------

    health_worker_equity_score = (
        health_worker_score
        * health_worker_equity
        / 100
    )

    microscope_equity_score = (
        microscope_score
        * microscope_equity
        / 100
    )

    rdt_equity_score = (
        rdt_score
        * rdt_equity
        / 100
    )

    scores = {
        "HEALTH WORKERS": health_worker_equity_score,
        "MICROSCOPES": microscope_equity_score,
        "RDT": rdt_equity_score,
    }

    priority_resource = max(
        scores,
        key=scores.get
    )

    # --------------------------------------------------------
    # DECISION TRACE
    # --------------------------------------------------------

    decision_trace = {
        "HEALTH WORKERS": {
            "gap_rate": health_worker_gap_rate,
            "impact": health_worker_impact,
            "feasibility": health_worker_feasibility,
            "equity": health_worker_equity,
            "base_score": health_worker_score,
            "equity_adjusted_score": health_worker_equity_score,
        },

        "MICROSCOPES": {
            "gap_rate": microscope_gap_rate,
            "impact": microscope_impact,
            "feasibility": microscope_feasibility,
            "equity": microscope_equity,
            "base_score": microscope_score,
            "equity_adjusted_score": microscope_equity_score,
        },

        "RDT": {
            "gap_rate": rdt_gap_rate,
            "impact": rdt_impact,
            "feasibility": rdt_feasibility,
            "equity": rdt_equity,
            "base_score": rdt_score,
            "equity_adjusted_score": rdt_equity_score,
        },
    }

    return {
        "scores": scores,
        "priority_resource": priority_resource,
        "decision_trace": decision_trace,
    }

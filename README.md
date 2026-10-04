# EdgeHealth Sentinel

## Adaptive, Uncertainty-Aware and Equity-Driven Edge AI for Health-System Intelligence in Resource-Constrained Communities

> **AI proposes. Evidence constrains. Simulation tests. Humans decide.**

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://edgehealth-sentinel.streamlit.app/)
[![GitHub](https://img.shields.io/badge/Code-GitHub-black)](https://github.com/alouiirahma-a11y/EdgeHealth-Sentinel)

---

## 1. Overview

**EdgeHealth Sentinel** is an offline-first research prototype for health-system intelligence in resource-constrained environments.

The project explores how AI-assisted decision support can remain **uncertainty-aware, resource-aware, equity-aware, and human-governed** when testing capacity, health workers, equipment, transportation, connectivity, and available evidence are limited.

A central design principle is:

> **Low observed data should not automatically be interpreted as low health need.**

Instead, the prototype makes evidence gaps, evidence debt, health-system blind spots, resource constraints, geographic access limitations, and uncertainty visible to decision makers.

The system combines:

* AI-assisted malaria blood-smear image analysis
* Image-quality assessment
* Uncertainty-aware decision support
* Safety governance and human escalation
* Evidence intelligence and evidence-debt modeling
* Health-system blind-spot detection
* Geographic access awareness
* Resource modeling and prioritization
* Equity-oriented system indicators
* What-if resource and intervention simulation
* Bottleneck and intervention analysis
* Audit-oriented decision traces
* Offline/local execution

---

# 2. The Problem

In resource-constrained communities, the absence of health data can be caused by the absence of capacity rather than the absence of disease or need.

A simplified chain is:

**Limited resources**

↓

**Reduced testing and observation**

↓

**Evidence gaps**

↓

**Evidence debt**

↓

**Health-system blind spots**

↓

**Some populations become less visible**

↓

**Potential equity exposure**

Traditional dashboards can make low observed activity look like low need.

EdgeHealth Sentinel instead asks:

> **What if the data gap itself is part of the risk?**

---

# 3. Core Design Principle

The project is built around four stages:

### AI proposes

AI-assisted analysis can identify patterns and generate candidate signals.

### Evidence constrains

The system incorporates evidence availability, data coverage, resource constraints, and uncertainty rather than treating every prediction as equally reliable.

### Simulation tests

Decision makers can explore what-if scenarios before acting, such as changing testing capacity, equipment, or other constrained resources.

### Humans decide

The system is a decision-support prototype, not an autonomous clinical or operational decision maker.

---

# 4. Community Health Command View

The prototype uses a **synthetic community called Region X** to demonstrate the health-system intelligence layer.

### Baseline scenario

| Indicator              | Synthetic Value |
| ---------------------- | --------------: |
| Population             |           8,000 |
| Underserved population |           3,200 |
| Expected tests         |             400 |
| Actual tests           |              25 |
| Testing coverage       |           6.25% |
| Evidence debt          |             375 |
| Health workers         |               2 |
| Microscopes            |               0 |
| RDT capacity           |        80/month |
| Connectivity           |            Poor |
| Transport access       |         Limited |
| Blind-spot risk        |            High |

These values are **synthetic** and are used only to demonstrate the system.

### Key system indicators

**Testing coverage**

```text
actual tests / expected tests × 100
```

For Region X:

```text
25 / 400 × 100 = 6.25%
```

**Evidence debt**

```text
expected tests − actual tests
```

For Region X:

```text
400 − 25 = 375
```

The purpose of these indicators is to expose where limited observation may create a health-system blind spot.

---

# 5. Diagnostic AI Pipeline

The diagnostic component is a research baseline for malaria blood-smear image analysis.

### Pipeline

```text
Input Image
     ↓
Image Quality Gate
     ↓
HOG Feature Extraction
     ↓
Logistic Regression
     ↓
Model Probability
     ↓
Uncertainty Assessment
     ↓
Safety Governor
     ↓
Human Decision
```

The prototype does **not** treat a model probability as a clinical diagnosis or calibrated clinical confidence.

---

# 6. Model and Dataset

The prototype uses the:

**NIH-NLM-ThinBloodSmearsPf — Point Set**

from the U.S. National Library of Medicine (NLM), National Institutes of Health (NIH).

Official source:

https://data.lhncbc.nlm.nih.gov/public/Malaria/NIH-NLM-ThinBloodSmearsPf/Point%20Set/

### Prototype data processing

The project manifest contains:

* 807 manifest records
* 160 patients
* 800 source images available for processing
* 162,249 image patches
* Patch size: 128 × 128 pixels
* Training patches: 112,661
* Validation patches: 24,002
* Test patches: 25,586

### Labels

| Label       | Patches |
| ----------- | ------: |
| Parasitized |   6,801 |
| Uninfected  | 155,448 |

The train/validation/test split was performed at the **patient level** to reduce the risk of patient leakage between splits.

The original dataset is **not redistributed in this repository**.

More information is available in:

`docs/DATASET.md`

---

# 7. Diagnostic Baseline

The baseline model uses:

* Image quality assessment
* HOG — Histogram of Oriented Gradients
* Logistic Regression
* Uncertainty estimation
* Safety-governed escalation

### Test-set results

| Metric                | Result |
| --------------------- | -----: |
| Accuracy              |   0.87 |
| ROC-AUC               | 0.8317 |
| PR-AUC                | 0.3101 |
| Parasitized precision |   0.15 |
| Parasitized recall    |   0.62 |

These results describe the prototype's experimental test-set performance. They do **not** establish clinical validity, clinical safety, or deployment readiness.

---

# 8. Uncertainty and Safety Governor

A central feature of EdgeHealth Sentinel is that the model is not allowed to act as if every prediction were equally trustworthy.

The decision pathway is:

```text
Quality Gate
     ↓
Model
     ↓
Uncertainty
     ↓
Safety Governor
     ↓
Human Decision
```

The Safety Governor can route uncertain or unsafe cases toward additional evidence or human review instead of presenting the model output as a definitive answer.

Example prototype behavior:

```text
Prediction: Parasitized
Model probability: 81.36%
Image quality: Sufficient
Uncertainty: Moderate
Suggested action: Additional Evidence
Safety Governor: Additional Evidence
Final decision: Additional Evidence
```

The displayed probability is a **model output**, not a clinical diagnosis or calibrated clinical confidence.

---

# 9. Evidence Intelligence

EdgeHealth Sentinel explicitly models the relationship between available resources and available evidence.

The system identifies:

* Testing gaps
* Evidence debt
* Evidence coverage
* Blind-spot risk
* Geographic access limitations
* Underserved populations
* Connectivity constraints
* Transport limitations
* Resource bottlenecks

The objective is not simply to ask:

> "What does the available data say?"

but also:

> **"What important information might be missing because the system could not observe it?"**

---

# 10. Geographic Blind Spots

Geographic access is considered as part of the health-system intelligence layer.

The prototype can represent:

* Number of settlements
* Geographic area
* Distance/access constraints
* Transport limitations
* Connectivity limitations
* Underserved population
* Facility availability

This helps distinguish a lack of observed cases from a lack of observation capacity.

---

# 11. Resource Intelligence

The prototype models constrained resources such as:

* Health workers
* Microscopes
* RDT capacity
* Testing capacity
* Connectivity
* Transport

Instead of simply showing a resource shortage, the system can connect resource constraints to potential evidence gaps and blind spots.

This creates a chain from:

**Resource constraint → observation capacity → evidence gap → decision risk**

---

# 12. What-If Simulation

The **What-If** module allows users to explore hypothetical resource scenarios.

Examples include changing:

* Testing capacity
* Health-worker availability
* Microscopy capacity
* RDT availability
* Other constrained system resources

The simulation recalculates selected system indicators so decision makers can compare scenarios before taking action.

These are **simulation outputs**, not predictions of actual future health outcomes.

The prototype does not claim that a simulated intervention will improve real-world health equity.

---

# 13. Equity Intelligence

The project treats equity as a system-level visibility and access concern.

The prototype considers indicators such as:

* Underserved population
* Testing coverage
* Resource availability
* Geographic access
* Evidence gaps
* Blind-spot risk

These indicators are intended to reveal where system constraints may disproportionately reduce visibility.

They are **prototype indicators**, not validated clinical fairness metrics.

---

# 14. Decision Trace and Governance

The system is designed to support auditable reasoning.

The decision pathway can expose:

```text
Input
  ↓
Evidence
  ↓
Model output
  ↓
Uncertainty
  ↓
Safety rule
  ↓
Resource context
  ↓
Simulation
  ↓
Recommended action
  ↓
Human decision
```

This supports a governance principle:

> **The AI output should be explainable as part of a decision process, not treated as the decision itself.**

---

# 15. Technology Stack

### Programming

* Python 3.13

### Interface

* Streamlit

### Machine Learning

* scikit-learn
* HOG feature extraction
* Logistic Regression

### Image Processing

* Pillow
* scikit-image

### Data / Computation

* NumPy
* pandas

### Model Persistence

* joblib

---

# 16. Project Structure

```text
EdgeHealth-Sentinel/
│
├── app/
│   └── streamlit application
│
├── src/
│   ├── simulation/
│   ├── decision logic/
│   ├── resource analysis/
│   └── supporting modules
│
├── models/
│   └── trained prototype model
│
├── docs/
│   ├── DATASET.md
│   ├── EdgeHealth_Sentinel_Report.pdf
│   └── offline_validation.md
│
├── EdgeHealth_Sentinel_Code.zip
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 17. Running the Project

Clone the repository:

```bash
git clone https://github.com/alouiirahma-a11y/EdgeHealth-Sentinel.git
cd EdgeHealth-Sentinel
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app/streamlit_app.py
```

The application can then be opened in the local browser.

---

# 18. Live Demonstration

A hosted demonstration is available at:

**https://edgehealth-sentinel.streamlit.app/**

The live application demonstrates the decision-support interface, including:

* Community Command View
* Evidence intelligence
* Resource analysis
* Equity indicators
* What-If simulation
* Intervention analysis
* Decision trace
* Safety and governance logic

---

# 19. Reproducibility

The repository provides:

* Source code
* Requirements
* Model artifacts
* Dataset documentation
* Validation documentation
* Project report
* Lightweight source-code ZIP

Large raw datasets and generated image collections are intentionally excluded from the repository.

The original dataset should be obtained directly from the official NLM source and used according to its applicable documentation and terms.

---

# 20. Limitations

EdgeHealth Sentinel is a **research prototype**.

It is not:

* A clinically validated diagnostic system
* A replacement for clinicians or laboratory professionals
* An autonomous health-system decision maker
* A validated outbreak-detection system
* A validated fairness or equity measurement framework
* Evidence of real-world intervention effectiveness

Additional limitations include:

* The community scenario is synthetic.
* Simulation outputs represent modeled system indicators rather than observed health outcomes.
* The malaria model is a baseline research model.
* Model probabilities should not be interpreted as calibrated clinical confidence.
* The prototype requires human oversight for uncertain or unsafe cases.
* Resource-access indicators are proxies and should not be interpreted as validated population-level access measures.

---

# 21. Why This Approach Matters

Many AI systems focus on improving prediction accuracy.

EdgeHealth Sentinel asks a different question:

> **What happens when the system does not have enough evidence to make a reliable decision?**

In resource-constrained environments, missing data may itself be a signal of constrained capacity.

Therefore, the prototype attempts to make three things visible at the same time:

**What the AI sees.**

**What the health system cannot currently observe.**

**What decision-makers could test before acting.**

This creates a human-governed loop:

```text
Observe
   ↓
Assess Evidence
   ↓
Estimate Uncertainty
   ↓
Identify Blind Spots
   ↓
Simulate Options
   ↓
Review
   ↓
Human Decision
```

---

# 22. Hackathon Principle

> **AI proposes. Evidence constrains. Simulation tests. Humans decide.**

EdgeHealth Sentinel is designed around the idea that responsible AI for resource-constrained health systems should not only answer:

**"What does the model predict?"**

It should also ask:

**"How strong is the evidence?"**

**"What might we be missing?"**

**"Which constraints produced the evidence gap?"**

**"What happens if we change the available resources?"**

**"Where must a human remain in control?"**

---

## Author

**Rahma Aloui — Tunisia**

Background spanning public health, health education, public-sector data work, and computer science studies.

EdgeHealth Sentinel was developed as a solo research prototype for the **Hack-Nation 7th Global AI Hackathon — World Bank: Small AI for Development, Track A: Health**.

---

## Repository

https://github.com/alouiirahma-a11y/EdgeHealth-Sentinel

## Live Demo

https://edgehealth-sentinel.streamlit.app/

## Dataset Documentation

See:

`docs/DATASET.md`

## Project Report

See:

`docs/EdgeHealth_Sentinel_Report.pdf`

## Validation Notes

See:

`docs/offline_validation.md`

---

**Research prototype • Human-governed AI • Synthetic community simulation • Not clinically validated**


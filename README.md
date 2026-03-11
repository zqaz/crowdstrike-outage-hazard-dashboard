# CrowdStrike July 2024 Outage — Hazard & Business Impact Dashboard

An interactive **Streamlit dashboard** analyzing the **CrowdStrike July 19, 2024 Windows outage** as a hazard, business-impact, and GRC (Governance, Risk & Compliance) event. Built as part of academic coursework in Cybersecurity Policy.

---

## Overview

On July 19, 2024, a defective Rapid Response Content update released by CrowdStrike triggered the largest IT outage in recorded history — crashing approximately **8.5 million Windows machines** worldwide within a 78-minute window. This dashboard provides a multi-angle analytical view of the incident across six sectors and 27+ countries.

The central argument: **this was not a cyberattack**. It was a governance, operational resilience, and supply-chain risk failure.

---

## Dashboard Sections

| Page | Contents |
|---|---|
| Executive Overview | KPI metrics, flight cancellations, sector severity, top financial losses |
| Incident Timeline | Gantt-style update window vs. recovery duration, sector recovery hours |
| Global Impact Map | Choropleth world map, bubble geo-map, top-country severity bar chart |
| Airline Impact | Cancellation comparisons, global aviation impact by region |
| Financial Impact Analysis | Scatter plot (loss vs. recovery), top-loss bar chart, sector treemap |
| Recovery Analysis | Recovery phase line chart, grouped bar, sector × phase heat map |
| Cross-Sector Hazard Analysis | Treemap, radar chart, sector × region heat map, stacked bar |
| GRC / Control Failure Mapping | CIS 15/16/17 and NIST SP 800-161 control gap analysis |
| Data & Sources | Raw data tables and source citations |

---

## Data Sources

- **CrowdStrike Preliminary Post Incident Review (PIR)** — release/revert times, remediation commitments
- **Microsoft Security Blog** — 8.5 M affected Windows devices, <1% of Windows ecosystem
- **Reuters / AP** — Delta 1.3 M customers, 7,000 flights, ~$500 M impact; day-one airline cancellations
- **NHS England** — cancelled appointment figures
- **CISA Alert AA24-200A** — government alert and remediation guidance
- **Parametrix Cloud Outage Report** — global insured loss estimate (~$2.7 B)
- **Interos Supply Chain Risk Intelligence** — healthcare aggregate loss estimate (~$1.94 B)

> **Data note:** Some airline records are fully quantified (Delta, United, American day-one counts). Others are listed as affected but not quantified where no verified figures were publicly disclosed. Industry-aggregate financial estimates are from third-party analysts and are clearly labeled by confidence level in the dashboard.

---

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
crowdstrike_dashboard_project/
├── app.py
├── requirements.txt
└── data/
    ├── incident_anchors.csv
    ├── airline_impacts.csv
    ├── sector_hazards.csv
    ├── sources.csv
    ├── global_impact.csv
    ├── recovery_timeline.csv
    ├── financial_impact.csv
    └── sector_region_heatmap.csv
```

---

## Academic Context

This dashboard was produced for **INFO/CSSS 523 — Cybersecurity Policy** (University of Washington, Winter 2025) as a final project deliverable examining the policy, governance, and operational resilience dimensions of the CrowdStrike outage.

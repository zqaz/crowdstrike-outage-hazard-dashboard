
# CrowdStrike 2024 Outage — Streamlit Dashboard Project

This repository contains a **GitHub-ready Streamlit app** and a companion notebook for analyzing the **CrowdStrike 2024 Windows outage** as a **hazard, business-impact, and GRC event**.

## What is included
- `app.py` — Streamlit dashboard with multiple sections
- `data/incident_anchors.csv` — core facts and anchor metrics
- `data/airline_impacts.csv` — airline-specific impact data used in charts and tables
- `data/sector_hazards.csv` — sector-level hazard framing
- `data/sources.csv` — source list / citation log
- `notebooks/crowdstrike_outage_dashboard.ipynb` — analysis notebook you can run in Colab or Jupyter
- `requirements.txt` — packages for Streamlit Cloud

## Dashboard sections
1. Executive Overview
2. Incident Timeline
3. Airline Impact
4. Cross-Sector Hazard Analysis
5. GRC / Control Failure Mapping
6. Data & Sources

## Quick start (local)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repository.
2. Go to Streamlit Community Cloud.
3. Connect your GitHub repo.
4. Set `app.py` as the entrypoint.
5. Deploy.

## Notes on the data
- Some airline data is **fully quantified** (especially Delta, plus day-one AP counts for Delta / United / American).
- Some airlines are included as **affected but not quantified** because the source set did not provide verified cancellation totals.
- The dashboard is designed to be **transparent** about which values are precise and which are directional.

## Source backbone
- CrowdStrike PIR: release/revert times, undetected error, remediation commitments
- Microsoft blog: 8.5M affected Windows devices, <1% of Windows ecosystem
- Reuters (Delta): 1.3M customers, 7,000 flights, ~$500M impact
- AP: day-one cancellation counts for Delta, United, and American
- Reuters / CISA: cross-sector and airline disruption context

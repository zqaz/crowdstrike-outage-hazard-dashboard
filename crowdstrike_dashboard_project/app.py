
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="CrowdStrike Outage Hazard Dashboard", layout="wide")

@st.cache_data
def load_data():
    anchors = pd.read_csv("data/incident_anchors.csv")
    airlines = pd.read_csv("data/airline_impacts.csv")
    sectors = pd.read_csv("data/sector_hazards.csv")
    sources = pd.read_csv("data/sources.csv")
    return anchors, airlines, sectors, sources

anchors, airlines, sectors, sources = load_data()

st.title("CrowdStrike 2024 Outage — Hazard & Business Impact Dashboard")
st.caption("Interactive dashboard for board-level, operational, and GRC-focused analysis.")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Incident Timeline",
        "Airline Impact",
        "Cross-Sector Hazard Analysis",
        "GRC / Control Failure Mapping",
        "Data & Sources",
    ],
)

if page == "Executive Overview":
    st.header("Executive Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Incident window", "78 min")
    c2.metric("Affected Windows devices", "8.5M")
    c3.metric("Delta disrupted customers", "1.3M")
    c4.metric("Delta claimed impact", "$500M")

    st.markdown(
        """
        **Board-level interpretation**
        - This was **not a cyberattack**; it was an **availability and operational-resilience failure**.
        - A short vendor-side update window created **long-tail business disruption**.
        - The hazard was amplified by **concentration risk**, **lack of staged deployment safeguards**, and **manual recovery burden**.
        """
    )

    left, right = st.columns([1.2, 1])
    with left:
        fig = px.bar(
            airlines.dropna(subset=["cancelled_flights"]).query("period in ['5-day total after outage', 'July 19 only']"),
            x="airline",
            y="cancelled_flights",
            color="period",
            barmode="group",
            title="Publicly Reported Airline Flight Cancellations",
            labels={"cancelled_flights": "Cancelled flights", "airline": "Airline"},
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        sev = px.bar(
            sectors.sort_values("severity_score", ascending=True),
            x="severity_score",
            y="sector",
            orientation="h",
            title="Relative Hazard Severity by Sector",
            labels={"severity_score": "Severity (1–5)", "sector": "Sector"},
        )
        st.plotly_chart(sev, use_container_width=True)

elif page == "Incident Timeline":
    st.header("Incident Timeline")
    st.write("Use this page to show how a short release window turned into a multi-day recovery problem.")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[78], y=["Update window"], orientation='h',
        base=[4*60 + 9],
        text=["04:09 UTC release → 05:27 UTC revert"],
        textposition='inside',
        hovertemplate="%{text}<extra></extra>"
    ))
    fig.update_layout(
        title="CrowdStrike defective update window on July 19, 2024",
        xaxis=dict(
            title="UTC time",
            tickmode='array',
            tickvals=[240, 270, 300, 330],
            ticktext=["04:00", "04:30", "05:00", "05:30"]
        ),
        yaxis_title="",
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True)

    timeline_items = pd.DataFrame([
        {"time":"04:09 UTC","event":"Defective Rapid Response Content update released"},
        {"time":"04:09–05:27 UTC","event":"Online Windows hosts in scope could receive the defective update"},
        {"time":"05:27 UTC","event":"CrowdStrike reverted the defective update"},
        {"time":"After revert","event":"Organizations faced manual recovery at scale; operational disruption lasted far longer than the release window"},
    ])
    st.dataframe(timeline_items, use_container_width=True, hide_index=True)

    st.info("Hazard lesson: the technical trigger was brief, but recovery complexity created the real business crisis.")

elif page == "Airline Impact":
    st.header("Airline Impact")
    numeric = airlines.dropna(subset=["cancelled_flights"]).copy()

    col1, col2 = st.columns([1.4, 1])
    with col1:
        fig = px.bar(
            numeric,
            x="airline",
            y="cancelled_flights",
            color="period",
            title="Verified airline cancellation counts available in the source set",
            labels={"cancelled_flights":"Cancelled flights"}
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cards = pd.DataFrame({
            "Metric": ["Delta customers disrupted", "Delta flights canceled", "Delta claimed impact"],
            "Value": ["1.3M", "7,000", "$500M"]
        })
        st.table(cards)

    st.subheader("Publicly reported airline records")
    st.dataframe(airlines, use_container_width=True, hide_index=True)

    st.markdown(
        """
        **Hazard interpretation for aviation**
        - The outage disrupted frontline operations such as flight dispatch, crew systems, check-in, and recovery planning.
        - Delta provides the clearest public example of how an IT control failure can become a financial and reputational crisis.
        - Not every airline disclosed the same level of detail, so the dashboard distinguishes **verified counts** from **affected-but-not-quantified carriers**.
        """
    )

elif page == "Cross-Sector Hazard Analysis":
    st.header("Cross-Sector Hazard Analysis")
    fig = px.treemap(
        sectors,
        path=[px.Constant("All sectors"), "sector"],
        values="severity_score",
        color="severity_score",
        hover_data=["hazard_type", "examples"],
        title="Where the outage created the highest operational hazard"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(sectors, use_container_width=True, hide_index=True)

    st.markdown(
        """
        **Hazard themes explained**
        1. **Availability risk** — core systems became unusable at the moment organizations needed them.
        2. **Concentration risk** — one widely trusted vendor became a single point of failure.
        3. **Recovery asymmetry** — a short release mistake produced a much longer recovery burden.
        4. **Critical-infrastructure exposure** — small technical percentages can still hit hospitals, airlines, and banks disproportionately.
        """
    )

elif page == "GRC / Control Failure Mapping":
    st.header("GRC / Control Failure Mapping")
    grc = pd.DataFrame([
        {
            "Framework / Control": "CIS Control 16",
            "What it expects": "Secure software lifecycle, validation, and release discipline",
            "What the incident exposed": "Defective content reached production; staged deployment safeguards were insufficient",
            "Board-level implication": "Change governance and blast-radius control were not proportionate to operational risk",
        },
        {
            "Framework / Control": "CIS Control 15",
            "What it expects": "Service provider governance and critical-vendor oversight",
            "What the incident exposed": "Vendor resilience requirements and customer deployment guardrails were limited",
            "Board-level implication": "Third-party dependency became a concentration-risk issue",
        },
        {
            "Framework / Control": "CIS Control 17",
            "What it expects": "Incident response and recovery readiness",
            "What the incident exposed": "Recovery required large-scale manual remediation",
            "Board-level implication": "Technical reversal did not equal business recovery",
        },
        {
            "Framework / Control": "NIST SP 800-161",
            "What it expects": "Supply chain risk governance integrated into enterprise risk management",
            "What the incident exposed": "Vendor outage resilience was not strong enough at the governance / contractual layer",
            "Board-level implication": "Supply chain risk must be treated as enterprise risk, not just IT risk",
        },
    ])
    st.dataframe(grc, use_container_width=True, hide_index=True)

    st.success("Dashboard takeaway: this was not just a software defect; it was a governance, resilience, and supply-chain risk event.")

elif page == "Data & Sources":
    st.header("Data & Sources")
    st.subheader("Anchor metrics")
    st.dataframe(anchors, use_container_width=True, hide_index=True)
    st.subheader("Source log")
    st.dataframe(sources, use_container_width=True, hide_index=True)
    st.markdown(
        """
        **How to extend this app**
        - Add more airline or sector rows to the CSVs.
        - Add your own charts under each page section.
        - Replace the static severity score with a custom scoring model.
        - Deploy to Streamlit Community Cloud by pointing it to `app.py` and `requirements.txt`.
        """
    )

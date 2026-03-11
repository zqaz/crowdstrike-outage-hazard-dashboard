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
    global_impact = pd.read_csv("data/global_impact.csv")
    recovery = pd.read_csv("data/recovery_timeline.csv")
    financial = pd.read_csv("data/financial_impact.csv")
    heatmap = pd.read_csv("data/sector_region_heatmap.csv")
    return anchors, airlines, sectors, sources, global_impact, recovery, financial, heatmap

anchors, airlines, sectors, sources, global_impact, recovery, financial, heatmap = load_data()

st.title("CrowdStrike July 2024 Outage — Hazard & Business Impact Dashboard")
st.caption("Interactive board-level, operational, and GRC analysis of the largest IT outage in history.")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Incident Timeline",
        "Global Impact Map",
        "Airline Impact",
        "Financial Impact Analysis",
        "Recovery Analysis",
        "Cross-Sector Hazard Analysis",
        "GRC / Control Failure Mapping",
        "Data & Sources",
    ],
)

# ── EXECUTIVE OVERVIEW ──────────────────────────────────────────────────────
if page == "Executive Overview":
    st.header("Executive Overview")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Incident window", "78 min", help="Time between defective update release and revert")
    c2.metric("Affected Windows devices", "8.5 M", help="Microsoft estimate — global scope")
    c3.metric("Countries impacted", "27+", help="Nations with confirmed disruptions across multiple sectors")
    c4.metric("Delta claimed impact", "$500 M", help="5-day revenue and operational loss (Delta public statement)")
    c5.metric("Global insured losses", "~$2.7 B", help="Parametrix industry insurance loss estimate")

    st.markdown(
        """
        **Board-level interpretation**
        - This was **not a cyberattack** — it was an **availability, resilience, and supply-chain governance failure**.
        - A 78-minute vendor-side content update window triggered a **multi-day, cross-sector business crisis** across 27+ countries.
        - The root cause: a single trusted security vendor became an **enterprise-wide single point of failure** for critical infrastructure worldwide.
        """
    )

    left, right = st.columns([1.2, 1])
    with left:
        fig = px.bar(
            airlines.dropna(subset=["cancelled_flights"]).query(
                "period in ['5-day total after outage', 'July 19 only']"
            ),
            x="airline",
            y="cancelled_flights",
            color="period",
            barmode="group",
            title="Publicly Reported Airline Flight Cancellations",
            labels={"cancelled_flights": "Cancelled flights", "airline": "Airline"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(legend_title_text="Period")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        sev = px.bar(
            sectors.sort_values("severity_score", ascending=True),
            x="severity_score",
            y="sector",
            orientation="h",
            title="Relative Hazard Severity by Sector",
            labels={"severity_score": "Severity (1–5)", "sector": "Sector"},
            color="severity_score",
            color_continuous_scale="RdYlGn_r",
        )
        sev.update_coloraxes(showscale=False)
        st.plotly_chart(sev, use_container_width=True)

    st.subheader("Global Financial Exposure — Top Reported Losses")
    top_fin = (
        financial[financial["organization"] != "CrowdStrike (market cap)"]
        .nlargest(8, "estimated_loss_usd_m")
    )
    fig_fin = px.bar(
        top_fin,
        x="estimated_loss_usd_m",
        y="organization",
        orientation="h",
        color="sector",
        title="Estimated Financial Impact by Organization / Sector (USD Millions)",
        labels={"estimated_loss_usd_m": "Estimated Loss (USD M)", "organization": ""},
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_fin.update_layout(legend_title_text="Sector", yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_fin, use_container_width=True)

# ── INCIDENT TIMELINE ───────────────────────────────────────────────────────
elif page == "Incident Timeline":
    st.header("Incident Timeline")
    st.write("A 78-minute defective update window produced a multi-day global recovery crisis.")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[78], y=["Defective update window"],
        orientation="h",
        base=[4 * 60 + 9],
        marker_color="#e74c3c",
        text=["04:09 UTC → 05:27 UTC (78 min)"],
        textposition="inside",
        hovertemplate="%{text}<extra></extra>",
        name="Active defective window",
    ))
    fig.add_trace(go.Bar(
        x=[60 * 24 * 5],
        y=["Delta recovery period"],
        orientation="h",
        base=[5 * 60 + 27],
        marker_color="#e67e22",
        text=["05:27 UTC → ~5 days later (Delta full recovery)"],
        textposition="inside",
        hovertemplate="%{text}<extra></extra>",
        name="Delta recovery window",
        opacity=0.6,
    ))
    fig.update_layout(
        title="CrowdStrike Defective Update Window vs. Real-World Recovery Duration",
        xaxis=dict(
            title="Minutes from midnight UTC (July 19)",
            tickmode="array",
            tickvals=[240, 270, 300, 330, 360, 720, 1440, 2880, 7200],
            ticktext=["04:00", "04:30", "05:00", "05:30", "06:00", "+12 h", "+24 h", "+48 h", "+5 days"],
        ),
        yaxis_title="",
        height=320,
        barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Key Events")
    timeline_items = pd.DataFrame([
        {"UTC Time": "04:09", "Event": "Defective Rapid Response Content (RRC) update released to production"},
        {"UTC Time": "04:09–05:27", "Event": "All online Windows hosts running Falcon sensor could receive the defective file"},
        {"UTC Time": "05:27", "Event": "CrowdStrike detected and reverted the defective update channel file"},
        {"UTC Time": "05:27+", "Event": "Organizations faced manual, boot-by-boot remediation at scale; recovery took days"},
        {"UTC Time": "July 22", "Event": "Delta Air Lines still cancelling hundreds of flights daily (3 days after revert)"},
        {"UTC Time": "July 24", "Event": "Delta operations fully restored (~5 days after the original outage)"},
    ])
    st.dataframe(timeline_items, use_container_width=True, hide_index=True)

    st.subheader("Recovery Hours by Sector — How Long Did It Take?")
    phase_order = ["Detection", "Immediate Response", "Partial Restoration", "Major Recovery", "Full Recovery"]
    recovery_full = recovery[recovery["phase"] == "Full Recovery"].copy()
    fig_rec = px.bar(
        recovery_full.sort_values("hours_to_milestone", ascending=True),
        x="hours_to_milestone",
        y="sector",
        orientation="h",
        title="Hours to Full Recovery by Sector",
        labels={"hours_to_milestone": "Hours to Full Recovery", "sector": "Sector"},
        color="hours_to_milestone",
        color_continuous_scale="OrRd",
        text="hours_to_milestone",
    )
    fig_rec.update_traces(texttemplate="%{text:.0f} h", textposition="outside")
    fig_rec.update_coloraxes(showscale=False)
    fig_rec.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_rec, use_container_width=True)

    st.info(
        "Hazard lesson: the technical trigger was 78 minutes. "
        "Recovery complexity created the real business crisis — measured in days, not minutes."
    )

# ── GLOBAL IMPACT MAP ───────────────────────────────────────────────────────
elif page == "Global Impact Map":
    st.header("Global Impact Map")
    st.markdown(
        "The outage reached **27+ countries** across 6 regions within minutes of the defective update going live. "
        "The choropleth and bubble maps below show the geographic concentration of confirmed disruptions."
    )

    col_filter, _ = st.columns([1, 3])
    with col_filter:
        region_options = ["All Regions"] + sorted(global_impact["region"].unique().tolist())
        selected_region = st.selectbox("Filter by region", region_options)

    filtered = global_impact if selected_region == "All Regions" else global_impact[global_impact["region"] == selected_region]

    # Choropleth world map
    fig_map = px.choropleth(
        filtered,
        locations="iso_alpha",
        color="severity_score",
        hover_name="country",
        hover_data={
            "iso_alpha": False,
            "severity_score": True,
            "primary_sectors": True,
            "estimated_devices_k": True,
            "key_impact_note": True,
        },
        color_continuous_scale="YlOrRd",
        range_color=(0, 10),
        title="Confirmed Disruption Severity by Country (0 = none, 10 = highest)",
        labels={
            "severity_score": "Severity (0–10)",
            "estimated_devices_k": "Est. devices (K)",
            "primary_sectors": "Sectors affected",
            "key_impact_note": "Impact summary",
        },
    )
    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        coloraxis_colorbar=dict(title="Severity", tickvals=[0, 2, 4, 6, 8, 10]),
        height=500,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Bubble scatter on a geographic base
    st.subheader("Disruption Bubble Map — Device Exposure vs. Severity")
    fig_bubble = px.scatter_geo(
        filtered,
        locations="iso_alpha",
        color="region",
        size="estimated_devices_k",
        hover_name="country",
        hover_data={
            "iso_alpha": False,
            "severity_score": True,
            "primary_sectors": True,
            "estimated_devices_k": True,
        },
        size_max=50,
        projection="natural earth",
        title="Estimated Affected Devices (bubble size) and Region (color)",
        labels={
            "estimated_devices_k": "Est. devices (K)",
            "severity_score": "Severity",
            "primary_sectors": "Sectors",
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig_bubble.update_layout(height=480, margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Bar chart — severity by country top 15
    st.subheader("Top Affected Countries by Disruption Severity")
    top15 = filtered.nlargest(15, "severity_score")
    fig_bar = px.bar(
        top15.sort_values("severity_score"),
        x="severity_score",
        y="country",
        orientation="h",
        color="region",
        title="Disruption Severity Score by Country (Top 15)",
        labels={"severity_score": "Severity (0–10)", "country": ""},
        color_discrete_sequence=px.colors.qualitative.Safe,
        text="severity_score",
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(yaxis={"categoryorder": "total ascending"}, legend_title_text="Region")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.caption(
        "Severity scores are researcher-assigned composite ratings (0–10) based on public reports of sector breadth, "
        "device counts, and critical infrastructure impact. Not all countries disclosed full data."
    )

# ── AIRLINE IMPACT ──────────────────────────────────────────────────────────
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
            title="Verified Airline Cancellation Counts",
            labels={"cancelled_flights": "Cancelled flights"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cards = pd.DataFrame({
            "Metric": ["Delta customers disrupted", "Delta flights canceled", "Delta claimed impact"],
            "Value": ["1.3 M", "7,000", "$500 M"],
        })
        st.table(cards)

    # Stacked bar — airline region comparison from global_impact filtered to aviation
    st.subheader("Global Aviation Disruption by Region")
    aviation_region = heatmap[heatmap["sector"] == "Aviation"].copy()
    fig_av_region = px.bar(
        aviation_region.sort_values("impact_score", ascending=False),
        x="region",
        y="impact_score",
        color="region",
        title="Aviation Sector Impact Score by Region",
        labels={"impact_score": "Impact Score (0–10)", "region": "Region"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text="impact_score",
    )
    fig_av_region.update_traces(textposition="outside")
    fig_av_region.update_layout(showlegend=False)
    st.plotly_chart(fig_av_region, use_container_width=True)

    st.subheader("Publicly Reported Airline Records")
    st.dataframe(airlines, use_container_width=True, hide_index=True)

    st.markdown(
        """
        **Hazard interpretation for aviation**
        - The outage disrupted frontline operations: flight dispatch, crew systems, check-in, and recovery planning.
        - Delta provides the clearest public example of how an IT control failure became a financial and reputational crisis.
        - Airlines not listed with cancellation counts (Ryanair, Air India, Indian carriers) reported disruptions but did not disclose quantified numbers.
        """
    )

# ── FINANCIAL IMPACT ANALYSIS ────────────────────────────────────────────────
elif page == "Financial Impact Analysis":
    st.header("Financial Impact Analysis")
    st.markdown(
        "Estimates range from **$500 M** (Delta direct, stated) to **$2.7 B** in global insured losses (Parametrix) "
        "and **$9 B+** in CrowdStrike market-cap erosion. The scatter plot below maps financial exposure "
        "against recovery duration, revealing the asymmetry between outage duration and business cost."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Delta direct loss", "$500 M", help="Delta public statement")
    c2.metric("Global insured losses", "~$2.7 B", help="Parametrix insurance industry estimate")
    c3.metric("CrowdStrike market cap loss", "~$9 B", help="Stock decline July 19–26, 2024")

    # Scatter plot: financial loss vs recovery days, sized by devices, colored by sector
    st.subheader("Financial Loss vs. Recovery Days (Scatter Plot)")
    scatter_df = financial[financial["organization"] != "CrowdStrike (market cap)"].copy()

    fig_scatter = px.scatter(
        scatter_df,
        x="recovery_days",
        y="estimated_loss_usd_m",
        size="devices_affected_k",
        color="sector",
        hover_name="organization",
        hover_data={
            "estimated_loss_usd_m": True,
            "recovery_days": True,
            "devices_affected_k": True,
            "source_confidence": True,
            "region": True,
        },
        size_max=60,
        title="Estimated Loss (USD M) vs. Recovery Days — Bubble Size = Devices Affected",
        labels={
            "recovery_days": "Days to Full Recovery",
            "estimated_loss_usd_m": "Estimated Loss (USD M)",
            "devices_affected_k": "Devices Affected (K)",
            "source_confidence": "Confidence",
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
        log_y=True,
    )
    fig_scatter.update_layout(
        legend_title_text="Sector",
        xaxis_title="Days to Full Recovery",
        yaxis_title="Estimated Loss (USD M, log scale)",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Bar chart — top 10 losses excluding CrowdStrike stock
    st.subheader("Top Reported Financial Losses by Organization / Sector")
    top_loss = financial.nlargest(10, "estimated_loss_usd_m")
    fig_loss = px.bar(
        top_loss.sort_values("estimated_loss_usd_m"),
        x="estimated_loss_usd_m",
        y="organization",
        orientation="h",
        color="sector",
        title="Top 10 Estimated Losses (USD Millions)",
        labels={"estimated_loss_usd_m": "Estimated Loss (USD M)", "organization": ""},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text="estimated_loss_usd_m",
    )
    fig_loss.update_traces(texttemplate="$%{text:,.0f} M", textposition="outside")
    fig_loss.update_layout(
        yaxis={"categoryorder": "total ascending"},
        legend_title_text="Sector",
        xaxis_tickprefix="$",
    )
    st.plotly_chart(fig_loss, use_container_width=True)

    # Treemap of financial losses by sector
    st.subheader("Financial Exposure by Sector — Treemap")
    sector_totals = (
        financial[financial["source_confidence"] != "High"]
        .groupby("sector", as_index=False)["estimated_loss_usd_m"]
        .sum()
    )
    high_conf = financial[financial["source_confidence"] == "High"].copy()
    high_conf_sector = high_conf.groupby("sector", as_index=False)["estimated_loss_usd_m"].sum()
    all_sector = pd.concat([sector_totals, high_conf_sector]).groupby("sector", as_index=False)["estimated_loss_usd_m"].sum()

    fig_tree = px.treemap(
        all_sector,
        path=[px.Constant("Total estimated losses"), "sector"],
        values="estimated_loss_usd_m",
        color="estimated_loss_usd_m",
        color_continuous_scale="RdYlGn_r",
        title="Estimated Financial Impact by Sector (USD Millions — mixed confidence)",
        labels={"estimated_loss_usd_m": "Est. Loss (USD M)"},
    )
    st.plotly_chart(fig_tree, use_container_width=True)

    st.caption(
        "**Confidence note:** High-confidence figures (Delta, CrowdStrike stock) are from public statements or market data. "
        "Industry-aggregate estimates (Healthcare, Banking, Retail) are from third-party analysts and should be treated as indicative."
    )

# ── RECOVERY ANALYSIS ────────────────────────────────────────────────────────
elif page == "Recovery Analysis":
    st.header("Recovery Analysis")
    st.markdown(
        "The CrowdStrike revert took **78 minutes**. Sector recovery took anywhere from **12 hours** (Media) to "
        "**5 days** (Aviation / Delta). This page dissects the recovery asymmetry across all six sectors."
    )

    # Line chart — recovery phases per sector
    st.subheader("Recovery Phase Timeline — Hours to Each Milestone")
    phase_order = ["Detection", "Immediate Response", "Partial Restoration", "Major Recovery", "Full Recovery"]
    recovery["phase"] = pd.Categorical(recovery["phase"], categories=phase_order, ordered=True)
    recovery_sorted = recovery.sort_values(["sector", "phase"])

    fig_line = px.line(
        recovery_sorted,
        x="phase",
        y="hours_to_milestone",
        color="sector",
        markers=True,
        title="Hours to Reach Each Recovery Phase by Sector",
        labels={"hours_to_milestone": "Hours from Incident Start", "phase": "Recovery Phase"},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig_line.update_layout(
        legend_title_text="Sector",
        xaxis_title="Recovery Phase",
        yaxis_title="Hours from Incident Start",
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Grouped bar chart — all phases side by side per sector
    st.subheader("Detailed Phase Breakdown — All Sectors (Grouped Bar)")
    fig_grouped = px.bar(
        recovery_sorted,
        x="sector",
        y="hours_to_milestone",
        color="phase",
        barmode="group",
        title="Recovery Hours by Phase and Sector",
        labels={"hours_to_milestone": "Hours", "sector": "Sector", "phase": "Recovery Phase"},
        color_discrete_sequence=px.colors.sequential.Oranges[1:],
        category_orders={"phase": phase_order},
    )
    fig_grouped.update_layout(legend_title_text="Phase", xaxis_tickangle=-20)
    st.plotly_chart(fig_grouped, use_container_width=True)

    # Heatmap — hours to milestone as a grid
    st.subheader("Recovery Heatmap — Hours to Each Phase (Sector × Phase)")
    rec_pivot = recovery_sorted.pivot(index="sector", columns="phase", values="hours_to_milestone")
    rec_pivot = rec_pivot[phase_order]

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=rec_pivot.values,
            x=rec_pivot.columns.tolist(),
            y=rec_pivot.index.tolist(),
            colorscale="YlOrRd",
            text=rec_pivot.values,
            texttemplate="%{text:.1f} h",
            hovertemplate="Sector: %{y}<br>Phase: %{x}<br>Hours: %{z:.1f}<extra></extra>",
            colorbar=dict(title="Hours"),
        )
    )
    fig_heat.update_layout(
        title="Recovery Phase Duration Heatmap (Hours from Incident Start)",
        xaxis_title="Recovery Phase",
        yaxis_title="Sector",
        height=380,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Detailed Recovery Records")
    st.dataframe(recovery_sorted.reset_index(drop=True), use_container_width=True, hide_index=True)

    st.warning(
        "Recovery asymmetry: the 78-minute defective update window forced manual, "
        "machine-by-machine remediation at scale — no automated rollback could undo the BSOD state. "
        "Aviation took up to 120 hours because crew, gate, and dispatch systems all needed manual restart."
    )

# ── CROSS-SECTOR HAZARD ANALYSIS ─────────────────────────────────────────────
elif page == "Cross-Sector Hazard Analysis":
    st.header("Cross-Sector Hazard Analysis")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.treemap(
            sectors,
            path=[px.Constant("All sectors"), "sector"],
            values="severity_score",
            color="severity_score",
            hover_data=["hazard_type", "examples"],
            title="Operational Hazard Severity by Sector",
            color_continuous_scale="RdYlGn_r",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=sectors["severity_score"].tolist() + [sectors["severity_score"].iloc[0]],
            theta=sectors["sector"].tolist() + [sectors["sector"].iloc[0]],
            fill="toself",
            name="Hazard severity",
            line_color="#e74c3c",
            fillcolor="rgba(231, 76, 60, 0.25)",
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            title="Hazard Severity Radar Chart",
            showlegend=False,
            height=400,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Sector × Region Heat Map
    st.subheader("Sector × Region Impact Heat Map")
    region_order = ["North America", "Europe", "Asia-Pacific", "Middle East", "South America", "Africa"]
    sector_order = ["Aviation", "Healthcare", "Banking & Payments", "Government & Emergency", "Retail & Hospitality", "Media & Broadcasting"]

    heatmap_pivot = heatmap.pivot(index="sector", columns="region", values="impact_score")
    heatmap_pivot = heatmap_pivot.reindex(index=sector_order, columns=region_order)

    heatmap_text = heatmap.pivot(index="sector", columns="region", values="impact_score").reindex(
        index=sector_order, columns=region_order
    )

    fig_hm = go.Figure(
        data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns.tolist(),
            y=heatmap_pivot.index.tolist(),
            colorscale="RdYlGn_r",
            zmin=0,
            zmax=10,
            text=heatmap_text.values,
            texttemplate="%{text}",
            hovertemplate="Sector: %{y}<br>Region: %{x}<br>Impact Score: %{z}<extra></extra>",
            colorbar=dict(title="Impact<br>Score"),
        )
    )
    fig_hm.update_layout(
        title="Sector × Region Impact Intensity (0 = none, 10 = maximum)",
        xaxis_title="Region",
        yaxis_title="Sector",
        height=420,
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    # Stacked bar — total exposure per region across sectors
    st.subheader("Total Sector Exposure by Region (Stacked Bar)")
    fig_stacked = px.bar(
        heatmap,
        x="region",
        y="impact_score",
        color="sector",
        title="Cumulative Impact Score by Region (All Sectors Stacked)",
        labels={"impact_score": "Cumulative Impact Score", "region": "Region"},
        barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Bold,
        category_orders={"region": region_order},
    )
    fig_stacked.update_layout(legend_title_text="Sector", xaxis_tickangle=-15)
    st.plotly_chart(fig_stacked, use_container_width=True)

    st.dataframe(sectors, use_container_width=True, hide_index=True)

    st.markdown(
        """
        **Hazard themes explained**
        1. **Availability risk** — core systems became unusable at the moment organizations needed them most.
        2. **Concentration risk** — one widely trusted vendor became a universal single point of failure across all sectors and regions.
        3. **Recovery asymmetry** — a 78-minute defective release produced recovery timelines measured in hours to days.
        4. **Critical-infrastructure exposure** — even a <1% share of the Windows ecosystem can simultaneously knock out hospitals, airlines, banks, and emergency services.
        """
    )

# ── GRC / CONTROL FAILURE MAPPING ────────────────────────────────────────────
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
            "Board-level implication": "Third-party dependency became a concentration-risk issue at a global scale",
        },
        {
            "Framework / Control": "CIS Control 17",
            "What it expects": "Incident response and recovery readiness",
            "What the incident exposed": "Recovery required large-scale manual remediation; no automated rollback was available",
            "Board-level implication": "Technical reversal did not equal business recovery — sectors took 12 to 120 hours",
        },
        {
            "Framework / Control": "NIST SP 800-161",
            "What it expects": "Supply chain risk governance integrated into enterprise risk management",
            "What the incident exposed": "Vendor outage resilience was not embedded at the governance / contractual layer",
            "Board-level implication": "Supply chain risk must be treated as enterprise risk, not just an IT risk",
        },
    ])
    st.dataframe(grc, use_container_width=True, hide_index=True)

    st.subheader("Control Gap Severity — Visual Scoring")
    grc_scores = pd.DataFrame({
        "Control": ["CIS 16 — Change Governance", "CIS 15 — Vendor Oversight", "CIS 17 — Incident Response", "NIST 800-161 — Supply Chain"],
        "Gap Score": [9, 8, 7, 8],
        "Domain": ["Software Lifecycle", "Third-Party Risk", "Resilience & Recovery", "Supply Chain Risk"],
    })
    fig_grc = px.bar(
        grc_scores,
        x="Gap Score",
        y="Control",
        orientation="h",
        color="Domain",
        title="Estimated Control Gap Severity Exposed by the Incident (1–10)",
        labels={"Gap Score": "Gap Severity (1–10)", "Control": ""},
        color_discrete_sequence=px.colors.qualitative.Safe,
        text="Gap Score",
    )
    fig_grc.update_traces(textposition="outside")
    fig_grc.update_layout(yaxis={"categoryorder": "total ascending"}, legend_title_text="Domain")
    st.plotly_chart(fig_grc, use_container_width=True)

    st.success(
        "Dashboard takeaway: this was not just a software defect — it was a governance, "
        "resilience, and supply-chain risk event that exposed critical gaps in how enterprises "
        "manage trusted third-party software at scale."
    )

# ── DATA & SOURCES ────────────────────────────────────────────────────────────
elif page == "Data & Sources":
    st.header("Data & Sources")

    st.subheader("Anchor metrics")
    st.dataframe(anchors, use_container_width=True, hide_index=True)

    st.subheader("Source log")
    st.dataframe(sources, use_container_width=True, hide_index=True)

    st.subheader("New datasets added in this version")
    tabs = st.tabs(["Global Impact", "Recovery Timeline", "Financial Impact", "Sector × Region Heatmap"])
    with tabs[0]:
        st.dataframe(global_impact, use_container_width=True, hide_index=True)
    with tabs[1]:
        st.dataframe(recovery, use_container_width=True, hide_index=True)
    with tabs[2]:
        st.dataframe(financial, use_container_width=True, hide_index=True)
    with tabs[3]:
        st.dataframe(heatmap, use_container_width=True, hide_index=True)

    st.markdown(
        """
        **Additional sources consulted for new datasets**
        - Parametrix: *Cloud Outage Report* — global insured loss estimate (~$2.7 B)
        - Interos: *Supply Chain Risk Intelligence* — healthcare aggregate loss estimate (~$1.94 B)
        - CrowdStrike Preliminary Post Incident Review (PIR) — release/revert times, remediation commitments
        - Microsoft Security Blog — 8.5 M device count, <1% of Windows ecosystem
        - Reuters / AP — Delta, United, American flight counts; Delta $500 M impact statement
        - NHS England — cancelled appointment figures for England
        - CISA Alert AA24-200A — government alert and remediation guidance

        """
    )

"""
E-Commerce Customer & Sales Intelligence Dashboard
Streamlit front-end for the completed analytics project.
Run: streamlit run app.py
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Customer & Sales Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Resolve paths relative to this file so the app works from any working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DATA = os.path.join(BASE_DIR, "03_Clean_Data")

SALES_PATH = os.path.join(CLEAN_DATA, "clean_sales_data.csv")
CUST_SALES_PATH = os.path.join(CLEAN_DATA, "clean_customer_sales_data.csv")
RFM_PATH = os.path.join(CLEAN_DATA, "customer_rfm_segments.csv")

# ─────────────────────────────────────────────────────────────────────────────
# Data Loading (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading sales data…")
def load_sales() -> pd.DataFrame:
    df = pd.read_csv(SALES_PATH, low_memory=False, parse_dates=["InvoiceDate"])
    return df


@st.cache_data(show_spinner="Loading customer data…")
def load_customer_sales() -> pd.DataFrame:
    df = pd.read_csv(CUST_SALES_PATH, low_memory=False, parse_dates=["InvoiceDate"])
    return df


@st.cache_data(show_spinner="Loading RFM segments…")
def load_rfm() -> pd.DataFrame:
    df = pd.read_csv(RFM_PATH)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# Helper: check files exist
# ─────────────────────────────────────────────────────────────────────────────
def files_exist() -> bool:
    return all(os.path.exists(p) for p in [SALES_PATH, CUST_SALES_PATH, RFM_PATH])


# ─────────────────────────────────────────────────────────────────────────────
# Shared metric card helper
# ─────────────────────────────────────────────────────────────────────────────
def kpi_card(col, label: str, value: str, delta: str = ""):
    col.metric(label=label, value=value, delta=delta if delta else None)


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar navigation
# ─────────────────────────────────────────────────────────────────────────────
PAGES = {
    "📊 Executive Overview": "overview",
    "🛍️ Sales & Product Analysis": "sales",
    "👥 Customer & Risk Analysis": "customer",
}

with st.sidebar:
    st.title("🛒 E-Commerce Intelligence")
    st.caption("UCI Online Retail Dataset · Analytics Dashboard")
    st.markdown("---")
    selection = st.radio("Navigate to", list(PAGES.keys()))
    st.markdown("---")
    st.caption("Data: UCI Online Retail  \nAnalysis: Python / Pandas  \nDashboard: Streamlit")

page = PAGES[selection]

# ─────────────────────────────────────────────────────────────────────────────
# Guard: missing data files
# ─────────────────────────────────────────────────────────────────────────────
if not files_exist():
    st.error(
        "One or more required data files were not found. "
        "Please ensure the following files exist:\n"
        f"- `{SALES_PATH}`\n"
        f"- `{CUST_SALES_PATH}`\n"
        f"- `{RFM_PATH}`"
    )
    st.stop()

# Load data
sales_df = load_sales()
cust_df = load_customer_sales()
rfm_df = load_rfm()

# ─────────────────────────────────────────────────────────────────────────────
# Pre-compute reusable aggregates
# ─────────────────────────────────────────────────────────────────────────────
total_revenue = sales_df["Revenue"].sum()
total_orders = sales_df["InvoiceNo"].nunique()
total_customers = cust_df["CustomerID"].nunique()
total_products = sales_df["Description"].nunique()
aov = total_revenue / total_orders if total_orders else 0

monthly_revenue = (
    sales_df.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)

country_revenue = (
    sales_df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

top_products = (
    sales_df.groupby("Description")["Revenue"]
    .sum()
    .nlargest(10)
    .sort_values(ascending=True)
    .reset_index()
)

segment_counts = rfm_df["Segment"].value_counts().reset_index()
segment_counts.columns = ["Segment", "Customers"]

segment_revenue = (
    rfm_df.groupby("Segment")["Monetary"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"Monetary": "Revenue"})
)

at_risk = rfm_df[(rfm_df["R_Score"] <= 2) & (rfm_df["M_Score"] >= 3)].copy()

top_customers = rfm_df.sort_values("Monetary", ascending=False).head(10).copy()

# ─────────────────────────────────────────────────────────────────────────────
# Colour palette (consistent across charts)
# ─────────────────────────────────────────────────────────────────────────────
SEGMENT_COLORS = {
    "Champions": "#2563eb",
    "Loyal Customers": "#16a34a",
    "Potential Loyalists": "#d97706",
    "At Risk": "#dc2626",
    "Inactive / Others": "#6b7280",
}

CHART_TEMPLATE = "plotly_white"


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — Executive Overview
# ─────────────────────────────────────────────────────────────────────────────
if page == "overview":
    st.title("📊 Executive Overview")
    st.caption("High-level summary of revenue performance, customer base, and key business findings.")
    st.markdown("---")

    # ── KPI row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 Total Revenue", f"£{total_revenue:,.0f}")
    c2.metric("🧾 Total Orders", f"{total_orders:,}")
    c3.metric("👥 Total Customers", f"{total_customers:,}")
    c4.metric("📦 Total Products", f"{total_products:,}")
    c5.metric("🛒 Avg Order Value", f"£{aov:,.2f}")

    st.markdown("---")

    # ── Monthly Revenue Trend ─────────────────────────────────────────────────
    st.subheader("Monthly Revenue Trend")

    if not monthly_revenue.empty:
        fig_monthly = px.line(
            monthly_revenue,
            x="YearMonth",
            y="Revenue",
            markers=True,
            template=CHART_TEMPLATE,
            labels={"YearMonth": "Month", "Revenue": "Revenue (£)"},
            color_discrete_sequence=["#2563eb"],
        )
        fig_monthly.update_layout(
            xaxis_tickangle=-45,
            margin=dict(l=0, r=0, t=10, b=0),
            height=360,
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.info("Monthly revenue data unavailable.")

    st.markdown("---")

    # ── Top Countries ─────────────────────────────────────────────────────────
    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.subheader("Top 10 Countries by Revenue")
        top10_countries = country_revenue.head(10)
        fig_countries = px.bar(
            top10_countries,
            x="Revenue",
            y="Country",
            orientation="h",
            template=CHART_TEMPLATE,
            labels={"Revenue": "Revenue (£)", "Country": ""},
            color_discrete_sequence=["#2563eb"],
        )
        fig_countries.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=380,
        )
        st.plotly_chart(fig_countries, use_container_width=True)

    with col_b:
        st.subheader("Customer Segments at a Glance")
        if not segment_counts.empty:
            seg_colors = [SEGMENT_COLORS.get(s, "#94a3b8") for s in segment_counts["Segment"]]
            fig_seg_pie = px.pie(
                segment_counts,
                names="Segment",
                values="Customers",
                template=CHART_TEMPLATE,
                color="Segment",
                color_discrete_map=SEGMENT_COLORS,
                hole=0.4,
            )
            fig_seg_pie.update_traces(textposition="outside", textinfo="percent+label")
            fig_seg_pie.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=380,
                showlegend=False,
            )
            st.plotly_chart(fig_seg_pie, use_container_width=True)

    st.markdown("---")

    # ── Business Summary ──────────────────────────────────────────────────────
    st.subheader("📋 Business Summary — Key Findings")

    best_seg = segment_revenue.iloc[0]["Segment"] if not segment_revenue.empty else "N/A"
    best_seg_rev = segment_revenue.iloc[0]["Revenue"] if not segment_revenue.empty else 0
    top_product_name = top_products.iloc[-1]["Description"] if not top_products.empty else "N/A"
    top_product_rev = top_products.iloc[-1]["Revenue"] if not top_products.empty else 0
    top_country = country_revenue.iloc[0]["Country"] if not country_revenue.empty else "N/A"
    top_country_rev = country_revenue.iloc[0]["Revenue"] if not country_revenue.empty else 0

    uk_share = (top_country_rev / total_revenue * 100) if total_revenue else 0

    summary_items = [
        ("💰 Total Revenue", f"The dataset covers £{total_revenue:,.0f} in total sales revenue across "
         f"{total_orders:,} orders and {total_customers:,} unique customers."),
        ("🌍 Geographic Concentration",
         f"{top_country} dominates revenue with £{top_country_rev:,.0f} "
         f"({uk_share:.1f}% of total), followed by Netherlands, EIRE, Germany, and France."),
        ("📦 Top Product",
         f"**{top_product_name}** is the highest-revenue product at £{top_product_rev:,.0f}."),
        ("🏆 Highest-Value Segment",
         f"**{best_seg}** customers generated £{best_seg_rev:,.0f} in historical monetary value — "
         "the most valuable segment for revenue."),
        ("⚠️ At-Risk Customers",
         f"{len(at_risk):,} customers are flagged as potentially at-risk "
         f"(low recency, high past spend), representing £{at_risk['Monetary'].sum():,.0f} "
         "in historical revenue that is at risk of being lost."),
        ("📈 Seasonal Trend",
         "Revenue peaks in Q4 (October–November), consistent with holiday and seasonal shopping patterns."),
    ]

    for icon_label, text in summary_items:
        st.markdown(f"**{icon_label}**")
        st.markdown(f"> {text}")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — Sales & Product Analysis
# ─────────────────────────────────────────────────────────────────────────────
elif page == "sales":
    st.title("🛍️ Sales & Product Analysis")
    st.caption("Revenue breakdown by product, country, and time.")
    st.markdown("---")

    # ── KPI summary strip ────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Revenue", f"£{total_revenue:,.0f}")
    c2.metric("🧾 Total Orders", f"{total_orders:,}")
    c3.metric("📦 Unique Products", f"{total_products:,}")
    c4.metric("🛒 Avg Order Value", f"£{aov:,.2f}")
    st.markdown("---")

    # ── Top 10 Products by Revenue ───────────────────────────────────────────
    st.subheader("Top 10 Products by Revenue")

    if not top_products.empty:
        fig_prod = px.bar(
            top_products,
            x="Revenue",
            y="Description",
            orientation="h",
            template=CHART_TEMPLATE,
            labels={"Revenue": "Revenue (£)", "Description": ""},
            color_discrete_sequence=["#2563eb"],
            text=top_products["Revenue"].apply(lambda v: f"£{v:,.0f}"),
        )
        fig_prod.update_traces(textposition="outside")
        fig_prod.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Revenue (£)",
            margin=dict(l=0, r=0, t=10, b=0),
            height=420,
        )
        st.plotly_chart(fig_prod, use_container_width=True)

        with st.expander("View Top 10 Products Table"):
            disp = top_products.sort_values("Revenue", ascending=False).copy()
            disp["Revenue"] = disp["Revenue"].apply(lambda v: f"£{v:,.2f}")
            disp.index = range(1, len(disp) + 1)
            disp.columns = ["Product", "Revenue"]
            st.dataframe(disp, use_container_width=True)

        top_p = top_products.sort_values("Revenue", ascending=False).iloc[0]
        st.info(
            f"**Top product:** {top_p['Description']} generated £{top_p['Revenue']:,.0f} in revenue. "
            "DOTCOM POSTAGE and similar logistics-related items reflect the UK-centric fulfilment model."
        )
    else:
        st.info("Product data unavailable.")

    st.markdown("---")

    # ── Monthly Revenue Trend ─────────────────────────────────────────────────
    st.subheader("Monthly Revenue Trend")

    if not monthly_revenue.empty:
        fig_monthly = px.area(
            monthly_revenue,
            x="YearMonth",
            y="Revenue",
            template=CHART_TEMPLATE,
            labels={"YearMonth": "Month", "Revenue": "Revenue (£)"},
            color_discrete_sequence=["#2563eb"],
        )
        fig_monthly.update_layout(
            xaxis_tickangle=-45,
            margin=dict(l=0, r=0, t=10, b=0),
            height=340,
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

        peak_month = monthly_revenue.loc[monthly_revenue["Revenue"].idxmax()]
        trough_month = monthly_revenue.loc[monthly_revenue["Revenue"].idxmin()]
        st.info(
            f"**Peak month:** {peak_month['YearMonth']} — £{peak_month['Revenue']:,.0f}  \n"
            f"**Lowest month:** {trough_month['YearMonth']} — £{trough_month['Revenue']:,.0f}  \n"
            "Revenue builds steadily through the year and peaks sharply in Q4, driven by holiday demand."
        )
    else:
        st.info("Monthly revenue data unavailable.")

    st.markdown("---")

    # ── Top Countries by Revenue ──────────────────────────────────────────────
    st.subheader("Top Countries by Revenue")

    col_l, col_r = st.columns([1.4, 1])

    with col_l:
        top10c = country_revenue.head(10)
        fig_c = px.bar(
            top10c,
            x="Country",
            y="Revenue",
            template=CHART_TEMPLATE,
            labels={"Revenue": "Revenue (£)", "Country": ""},
            color_discrete_sequence=["#2563eb"],
            text=top10c["Revenue"].apply(lambda v: f"£{v/1000:.0f}k"),
        )
        fig_c.update_traces(textposition="outside")
        fig_c.update_layout(
            xaxis_tickangle=-35,
            margin=dict(l=0, r=0, t=10, b=0),
            height=380,
        )
        st.plotly_chart(fig_c, use_container_width=True)

    with col_r:
        st.markdown("##### Revenue by Country (Top 10)")
        disp_c = top10c.copy()
        disp_c["Share %"] = (disp_c["Revenue"] / total_revenue * 100).round(1)
        disp_c["Revenue"] = disp_c["Revenue"].apply(lambda v: f"£{v:,.0f}")
        disp_c.index = range(1, len(disp_c) + 1)
        st.dataframe(disp_c[["Country", "Revenue", "Share %"]], use_container_width=True)

        uk_pct = (country_revenue.iloc[0]["Revenue"] / total_revenue * 100) if total_revenue else 0
        st.info(
            f"United Kingdom accounts for **{uk_pct:.1f}%** of total revenue, "
            "reflecting the retailer's primary market. "
            "The Netherlands, EIRE, Germany, and France are the next most significant markets."
        )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — Customer & Risk Analysis
# ─────────────────────────────────────────────────────────────────────────────
elif page == "customer":
    st.title("👥 Customer & Risk Analysis")
    st.caption("RFM-based customer segmentation, at-risk identification, and top customer profiles.")
    st.markdown("---")

    # ── RFM explanation ───────────────────────────────────────────────────────
    with st.expander("ℹ️ What is RFM Segmentation?"):
        st.markdown(
            """
**RFM** stands for **Recency**, **Frequency**, and **Monetary** — three dimensions used to score
and segment customers based on their purchase behaviour:

| Dimension | Definition |
|---|---|
| **Recency (R)** | Days since the customer's last purchase (lower = more recent) |
| **Frequency (F)** | Number of distinct orders placed |
| **Monetary (M)** | Total historical spend |

Each dimension is scored 1–5 (5 = best). Customers are then grouped into segments:

| Segment | Criteria |
|---|---|
| **Champions** | R ≥ 4, F ≥ 4, M ≥ 4 |
| **Loyal Customers** | R ≥ 3, F ≥ 3 |
| **Potential Loyalists** | R ≥ 3, F ≥ 2 |
| **At Risk** | R ≤ 2, M ≥ 3 |
| **Inactive / Others** | All remaining customers |

**Potentially at-risk** customers: R_Score ≤ 2 AND M_Score ≥ 3 (previously high-value, now lapsing).
"""
        )

    st.markdown("---")

    # ── Customer Segment KPIs ─────────────────────────────────────────────────
    champions = rfm_df[rfm_df["Segment"] == "Champions"]
    loyal = rfm_df[rfm_df["Segment"] == "Loyal Customers"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Customers", f"{len(rfm_df):,}")
    c2.metric("🏆 Champions", f"{len(champions):,}")
    c3.metric("❤️ Loyal Customers", f"{len(loyal):,}")
    c4.metric("⚠️ At-Risk Customers", f"{len(at_risk):,}")

    st.markdown("---")

    # ── Segment charts ────────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Customers by Segment")
        if not segment_counts.empty:
            fig_seg_bar = px.bar(
                segment_counts.sort_values("Customers", ascending=True),
                x="Customers",
                y="Segment",
                orientation="h",
                template=CHART_TEMPLATE,
                color="Segment",
                color_discrete_map=SEGMENT_COLORS,
                text="Customers",
                labels={"Customers": "Number of Customers", "Segment": ""},
            )
            fig_seg_bar.update_traces(textposition="outside")
            fig_seg_bar.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=0),
                height=340,
            )
            st.plotly_chart(fig_seg_bar, use_container_width=True)

    with col_right:
        st.subheader("Revenue by Segment")
        if not segment_revenue.empty:
            fig_seg_rev = px.bar(
                segment_revenue.sort_values("Revenue", ascending=True),
                x="Revenue",
                y="Segment",
                orientation="h",
                template=CHART_TEMPLATE,
                color="Segment",
                color_discrete_map=SEGMENT_COLORS,
                text=segment_revenue.sort_values("Revenue", ascending=True)["Revenue"].apply(
                    lambda v: f"£{v:,.0f}"
                ),
                labels={"Revenue": "Historical Revenue (£)", "Segment": ""},
            )
            fig_seg_rev.update_traces(textposition="outside")
            fig_seg_rev.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=0),
                height=340,
            )
            st.plotly_chart(fig_seg_rev, use_container_width=True)

    # Segment summary table
    with st.expander("View Segment Summary Table"):
        seg_merge = segment_counts.merge(segment_revenue, on="Segment")
        seg_merge["Avg Revenue / Customer"] = (seg_merge["Revenue"] / seg_merge["Customers"]).round(2)
        seg_merge["Revenue"] = seg_merge["Revenue"].apply(lambda v: f"£{v:,.0f}")
        seg_merge["Avg Revenue / Customer"] = seg_merge["Avg Revenue / Customer"].apply(
            lambda v: f"£{v:,.2f}"
        )
        seg_merge = seg_merge.sort_values("Customers", ascending=False).reset_index(drop=True)
        st.dataframe(seg_merge, use_container_width=True)

    st.markdown("---")

    # ── At-Risk Customers ─────────────────────────────────────────────────────
    st.subheader("⚠️ Potentially At-Risk Customers")
    st.markdown(
        "Customers with **R_Score ≤ 2** and **M_Score ≥ 3** — previously valuable customers "
        "who have not purchased recently."
    )

    ar_c1, ar_c2, ar_c3 = st.columns(3)
    ar_c1.metric("At-Risk Count", f"{len(at_risk):,}")
    ar_c2.metric("Historical Revenue at Risk", f"£{at_risk['Monetary'].sum():,.0f}")
    ar_c3.metric("Avg Spend per At-Risk Customer", f"£{at_risk['Monetary'].mean():,.0f}")

    if not at_risk.empty:
        col_ar_l, col_ar_r = st.columns([1.3, 1])

        with col_ar_l:
            fig_ar_hist = px.histogram(
                at_risk,
                x="Monetary",
                nbins=30,
                template=CHART_TEMPLATE,
                labels={"Monetary": "Historical Spend (£)", "count": "Customers"},
                color_discrete_sequence=["#dc2626"],
                title="Distribution of At-Risk Customer Spend",
            )
            fig_ar_hist.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                height=320,
            )
            st.plotly_chart(fig_ar_hist, use_container_width=True)

        with col_ar_r:
            fig_ar_scatter = px.scatter(
                at_risk,
                x="Recency",
                y="Monetary",
                color="M_Score",
                template=CHART_TEMPLATE,
                labels={
                    "Recency": "Days Since Last Purchase",
                    "Monetary": "Historical Spend (£)",
                    "M_Score": "M Score",
                },
                color_continuous_scale="Reds",
                title="Recency vs. Spend for At-Risk Customers",
                opacity=0.7,
            )
            fig_ar_scatter.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                height=320,
            )
            st.plotly_chart(fig_ar_scatter, use_container_width=True)

        with st.expander("View At-Risk Customer Table (Top 50 by Spend)"):
            ar_display = (
                at_risk[["CustomerID", "Recency", "Frequency", "Monetary", "R_Score", "F_Score", "M_Score", "Segment"]]
                .sort_values("Monetary", ascending=False)
                .head(50)
                .copy()
            )
            ar_display["CustomerID"] = ar_display["CustomerID"].astype(str).str.replace(".0", "", regex=False)
            ar_display["Monetary"] = ar_display["Monetary"].apply(lambda v: f"£{v:,.2f}")
            ar_display.index = range(1, len(ar_display) + 1)
            st.dataframe(ar_display, use_container_width=True)

        st.warning(
            f"**{len(at_risk):,} customers** are potentially at risk, representing "
            f"**£{at_risk['Monetary'].sum():,.0f}** in historical revenue. "
            "Re-engagement campaigns targeting these customers could recover a significant portion of this value."
        )

    st.markdown("---")

    # ── Top Customers by Revenue ──────────────────────────────────────────────
    st.subheader("🏆 Top 10 Customers by Revenue")

    if not top_customers.empty:
        tc_display = top_customers[
            ["CustomerID", "Recency", "Frequency", "Monetary", "R_Score", "F_Score", "M_Score", "Segment"]
        ].copy()
        tc_display["CustomerID"] = tc_display["CustomerID"].astype(str).str.replace(".0", "", regex=False)

        fig_tc = px.bar(
            tc_display.sort_values("Monetary", ascending=True),
            x="Monetary",
            y="CustomerID",
            orientation="h",
            template=CHART_TEMPLATE,
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            labels={"Monetary": "Historical Spend (£)", "CustomerID": "Customer ID"},
            text=tc_display.sort_values("Monetary", ascending=True)["Monetary"].apply(
                lambda v: f"£{v:,.0f}"
            ),
        )
        fig_tc.update_traces(textposition="outside")
        fig_tc.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=400,
        )
        st.plotly_chart(fig_tc, use_container_width=True)

        with st.expander("View Top 10 Customers Table"):
            tc_display2 = tc_display.copy()
            tc_display2["Monetary"] = tc_display2["Monetary"].apply(lambda v: f"£{v:,.2f}")
            tc_display2.index = range(1, len(tc_display2) + 1)
            st.dataframe(tc_display2, use_container_width=True)

    st.markdown("---")

    # ── RFM Score Distribution ────────────────────────────────────────────────
    st.subheader("RFM Score Distribution")
    col_r1, col_r2, col_r3 = st.columns(3)

    for col_widget, score_col, label, color in [
        (col_r1, "R_Score", "Recency Score", "#2563eb"),
        (col_r2, "F_Score", "Frequency Score", "#16a34a"),
        (col_r3, "M_Score", "Monetary Score", "#d97706"),
    ]:
        if score_col in rfm_df.columns:
            score_counts = rfm_df[score_col].value_counts().sort_index().reset_index()
            score_counts.columns = ["Score", "Count"]
            fig_score = px.bar(
                score_counts,
                x="Score",
                y="Count",
                template=CHART_TEMPLATE,
                color_discrete_sequence=[color],
                labels={"Score": label, "Count": "Customers"},
                title=label,
            )
            fig_score.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                height=280,
                showlegend=False,
            )
            col_widget.plotly_chart(fig_score, use_container_width=True)

    st.markdown("---")

    # ── Interpretation ────────────────────────────────────────────────────────
    st.subheader("📋 Customer Analysis — Key Findings")

    largest_seg = segment_counts.iloc[0]["Segment"]
    largest_seg_count = segment_counts.iloc[0]["Customers"]
    top_rev_seg = segment_revenue.iloc[0]["Segment"]
    top_rev_seg_val = segment_revenue.iloc[0]["Revenue"]

    findings = [
        ("🏆 Champions",
         f"{len(champions):,} customers qualify as Champions — "
         "high recency, frequency, and spend. These are the retailer's most valuable customers and should be rewarded and retained."),
        ("📊 Largest Segment",
         f"**{largest_seg}** is the largest segment with {largest_seg_count:,} customers. "
         "This represents customers who have not met the thresholds for active engagement and may need re-activation campaigns."),
        ("💰 Highest-Revenue Segment",
         f"**{top_rev_seg}** customers generated £{top_rev_seg_val:,.0f} in historical monetary value, "
         "making them the most commercially important group."),
        ("⚠️ At-Risk Revenue",
         f"{len(at_risk):,} customers are classified as potentially at-risk, "
         f"with £{at_risk['Monetary'].sum():,.0f} in historical revenue at risk. "
         "Targeted re-engagement (e.g., win-back email campaigns, personalised offers) is recommended."),
        ("🔑 Retention Strategy",
         "Prioritise Champions and Loyal Customers for loyalty programmes. "
         "Potential Loyalists represent an upsell opportunity. "
         "At-Risk and Inactive segments require different re-activation approaches."),
    ]

    for title, text in findings:
        st.markdown(f"**{title}**")
        st.markdown(f"> {text}")


import streamlit as st
import plotly.express as px
import pandas as pd

from analyzer import analyze_url
from database import (
    create_table,
    save_scan,
    get_scan_history,
    get_dashboard_stats
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PhishGuard | Security Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM UI DESIGN
# --------------------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: #080F1C;
    color: #E2E8F0;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Headings */
h1, h2, h3 {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
}

p, label, .stMarkdown {
    color: #CBD5E1;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0D1728;
    border-right: 1px solid #1E293B;
}

section[data-testid="stSidebar"] h1 {
    color: #38BDF8 !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #142238, #101B2D);
    border: 1px solid #263B55;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.18);
}

div[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

div[data-testid="stMetricValue"] {
    color: #38BDF8;
    font-weight: 700;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #0284C7, #2563EB);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 22px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #0EA5E9, #3B82F6);
    color: white;
    border: none;
}

/* Input boxes */
.stTextInput input {
    background: #111E30;
    color: white;
    border: 1px solid #334155;
    border-radius: 9px;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background: #111E30;
    border-color: #334155;
    border-radius: 9px;
}

/* Dividers */
hr {
    border-color: #26364D;
}

/* Custom cards */
.pg-card {
    background: linear-gradient(145deg, #142238, #101B2D);
    border: 1px solid #263B55;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
}

.pg-small {
    color: #94A3B8;
    font-size: 13px;
    margin-bottom: 8px;
}

.pg-heading {
    color: #F8FAFC;
    font-size: 22px;
    font-weight: 700;
}

.pg-description {
    color: #94A3B8;
    font-size: 14px;
}

.pg-risk {
    font-size: 25px;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

create_table()

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🛡️ PhishGuard")
    st.caption("URL SECURITY INTELLIGENCE")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "URL Scanner",
            "Scan History",
            "About"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### 🟢 System Status")
    st.caption("PhishGuard is ready")

    st.markdown("---")
    st.caption("Built with Python & Streamlit")
    st.caption("PhishGuard v1.0")


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":

    st.title("Security Overview")
    st.markdown(
        "Monitor URL scans and review potential phishing threats."
    )

    total_scans, stats = get_dashboard_stats()

    st.markdown("### Security Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
         st.metric("TOTAL SCANS", total_scans)
 
    with col2:
         st.metric("LOW RISK", stats["LOW"])

    with col3:
        st.metric("MEDIUM RISK", stats["MEDIUM"])

    with col4:
        st.metric("HIGH RISK", stats["HIGH"])

    st.divider()

    st.subheader("📊 Threat Analytics")

    chart_col, info_col = st.columns([1.5, 1])

    chart_data = pd.DataFrame({
        "Risk Level": ["LOW", "MEDIUM", "HIGH"],
        "Number of URLs": [
            stats["LOW"],
            stats["MEDIUM"],
            stats["HIGH"]
        ]
    })

    with chart_col:

        fig = px.bar(
            chart_data,
            x="Risk Level",
            y="Number of URLs",
            color="Risk Level",
            color_discrete_map={
                "LOW": "#22C55E",
                "MEDIUM": "#F59E0B",
                "HIGH": "#EF4444"
            },
            text="Number of URLs",
            template="plotly_dark"
        )

        fig.update_layout(
            plot_bgcolor="#101B2D",
            paper_bgcolor="#101B2D",
            font_color="#E2E8F0",
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="Risk Classification",
            yaxis_title="Number of Scans"
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0
        )

        st.plotly_chart(fig, width="stretch")

    with info_col:

        st.markdown("""
        <div class="pg-card">
            <div class="pg-small">SECURITY INSIGHT</div>
            <div class="pg-heading">Threat Summary</div>
            <br>
            <p class="pg-description">
                PhishGuard evaluates URLs using rule-based
                security indicators.
            </p>
            <hr>
            <p>🟢 LOW — Fewer suspicious indicators</p>
            <p>🟠 MEDIUM — Some suspicious indicators</p>
            <p>🔴 HIGH — Multiple suspicious indicators</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("🕒 Recent Scans")

    history = get_scan_history()

    if history:

        recent_df = pd.DataFrame(
            history[:5],
            columns=[
                "ID",
                "URL",
                "Risk Score",
                "Risk Level",
                "Scan Time"
            ]
        )

        st.dataframe(
            recent_df[["URL", "Risk Score", "Risk Level", "Scan Time"]],
            width="stretch",
            hide_index=True
        )

    else:
        st.info("No scans available. Visit URL Scanner to analyze a URL.")


# --------------------------------------------------
# URL SCANNER PAGE
# --------------------------------------------------

# --------------------------------------------------
# URL SCANNER PAGE
# --------------------------------------------------

elif page == "URL Scanner":

    st.title("🔍 URL Security Scanner")

    st.markdown(
        "Inspect suspicious website addresses and identify "
        "potential phishing indicators."
    )

    st.markdown("""
    <div class="pg-card">
        <div class="pg-small">PHISHING DETECTION ENGINE</div>
        <div class="pg-heading">Website Security Analysis</div>
        <p class="pg-description">
            Enter a website URL below to examine its structure
            and detect potentially suspicious patterns.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # URL input form
    with st.form("url_scan_form"):

        url = st.text_input(
            "Enter Website URL",
            placeholder="https://example.com",
            help="Enter the complete website address."
        )

        submitted = st.form_submit_button(
            "🛡️ Scan Website",
            use_container_width=True
        )

    if submitted:

        if not url.strip():

            st.warning("Please enter a website URL.")

        else:

            try:

                with st.spinner("Inspecting URL for suspicious patterns..."):

                    result = analyze_url(url)

                    save_scan(
                        result["url"],
                        result["score"],
                        result["risk"]
                    )

                    st.session_state.last_result = result

                st.success("Security analysis completed successfully.")

            except Exception as e:

                st.error(f"Analysis failed: {e}")

    # Display analysis report
    result = st.session_state.last_result

    if result:

        st.divider()

        st.markdown("## Security Analysis Report")

        st.caption("TARGET WEBSITE")
        st.code(result["url"], language=None)

        risk = result["risk"]
        score = result["score"]
        indicators = result["indicators"]

        # Risk-specific presentation
        risk_styles = {
            "LOW": {
                "color": "#22C55E",
                "background": "#102B20",
                "message": "Fewer suspicious URL indicators detected."
            },
            "MEDIUM": {
                "color": "#F59E0B",
                "background": "#352711",
                "message": "Some suspicious URL indicators detected."
            },
            "HIGH": {
                "color": "#EF4444",
                "background": "#351717",
                "message": "Multiple suspicious URL indicators detected."
            }
        }

        style = risk_styles.get(risk, risk_styles["MEDIUM"])

        st.markdown(
            f"""
            <div style="
                background:{style['background']};
                border:1px solid {style['color']};
                border-radius:14px;
                padding:22px;
                margin:15px 0;
            ">
                <div style="
                    color:#94A3B8;
                    font-size:13px;
                    letter-spacing:1px;
                ">
                    SECURITY CLASSIFICATION
                </div>
                <div style="
                    color:{style['color']};
                    font-size:32px;
                    font-weight:800;
                    margin:8px 0;
                ">
                    {risk} RISK
                </div>
                <div style="color:#CBD5E1;">
                    {style['message']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Risk Score", score)

        with col2:
            st.metric("Indicators Detected", len(indicators))

        with col3:
            st.metric("Classification", risk)

        st.divider()

        # Indicator details
        st.markdown("### 🔎 Security Indicators")

        if indicators:

            st.write(
                "The following URL characteristics contributed "
                "to the risk assessment:"
            )

            for index, indicator in enumerate(indicators, start=1):

                st.warning(f"**{index}.** {indicator}")

        else:

            st.success(
                "No suspicious URL indicators were detected "
                "by the current analysis rules."
            )

        # Recommendations
        st.markdown("### 💡 Security Recommendation")

        if risk == "HIGH":

            st.error(
                "Avoid opening this website or entering personal "
                "information unless its authenticity is independently verified."
            )

        elif risk == "MEDIUM":

            st.warning(
                "Verify the website address and its authenticity "
                "before entering sensitive information."
            )

        else:

            st.info(
                "No major suspicious URL patterns were detected. "
                "Still verify the website before sharing sensitive information."
            )

        st.caption(
            "Disclaimer: PhishGuard uses rule-based URL analysis. "
            "Its risk score is a heuristic indicator, not a probability "
            "or guarantee that a website is safe or malicious."
        )

    else:

        st.info(
            "No analysis report yet. Enter a URL above to get started."
        )



# --------------------------------------------------
# SCAN HISTORY PAGE
# --------------------------------------------------

# --------------------------------------------------
# SCAN HISTORY PAGE
# --------------------------------------------------

elif page == "Scan History":

    st.title("📋 Security Scan History")

    st.markdown(
        "Review previously analyzed URLs and monitor detected threats."
    )

    history = get_scan_history()

    if history:

        df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "URL",
                "Risk Score",
                "Risk Level",
                "Scan Time"
            ]
        )

        # Summary cards
        st.subheader("History Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("TOTAL SCANS", len(df))

        with col2:
            st.metric(
                "LOW RISK",
                (df["Risk Level"] == "LOW").sum()
            )

        with col3:
            st.metric(
                "MEDIUM RISK",
                (df["Risk Level"] == "MEDIUM").sum()
            )

        with col4:
            st.metric(
                "HIGH RISK",
                (df["Risk Level"] == "HIGH").sum()
            )

        st.divider()

        # Search and filters
        st.subheader("🔍 Search and Filter")

        col1, col2 = st.columns([2, 1])

        with col1:
            search_query = st.text_input(
                "Search website URL",
                placeholder="Search for a URL..."
            )

        with col2:
            risk_filter = st.selectbox(
                "Risk classification",
                ["ALL", "LOW", "MEDIUM", "HIGH"]
            )

        filtered_df = df.copy()

        if search_query:
            filtered_df = filtered_df[
                filtered_df["URL"].str.contains(
                    search_query,
                    case=False,
                    na=False,
                    regex=False
                )
            ]

        if risk_filter != "ALL":
            filtered_df = filtered_df[
                filtered_df["Risk Level"] == risk_filter
            ]

        st.divider()

        # Results
        st.subheader("📑 Scan Records")

        st.caption(
            f"Displaying {len(filtered_df)} of {len(df)} records"
        )

        if not filtered_df.empty:

            # Color-coded risk levels
            def highlight_risk(column):

                styles = []

                for value in column:

                    if value == "LOW":
                        styles.append(
                            "background-color: #14532D; color: #BBF7D0;"
                        )

                    elif value == "MEDIUM":
                        styles.append(
                            "background-color: #78350F; color: #FEF3C7;"
                        )

                    elif value == "HIGH":
                        styles.append(
                            "background-color: #7F1D1D; color: #FECACA;"
                        )

                    else:
                        styles.append("")

                return styles

            styled_df = (
    filtered_df[
        ["ID", "URL", "Risk Score", "Risk Level", "Scan Time"]
    ]
    .style
    .set_properties(
        **{
            "background-color": "#111E30",
            "color": "#E2E8F0",
            "border-color": "#263B55"
        }
    )
    .apply(highlight_risk, subset=["Risk Level"])
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#1E293B"),
                ("color", "#38BDF8"),
                ("font-weight", "bold")
            ]
        }
    ])
)

            st.dataframe(
                styled_df,
                width="stretch",
                hide_index=True
            )

            # CSV Export
            st.divider()

            st.subheader("📥 Export Scan Records")

            csv_data = filtered_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="Download Filtered History (CSV)",
                data=csv_data,
                file_name="phishguard_scan_history.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:

            st.info("No records match your search or selected filter.")

    else:

        st.info(
            "No scan records available. Visit URL Scanner to analyze your first website."
        )



# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif page == "About":

    st.title("About PhishGuard")

    st.markdown("""
    <div class="pg-card">
        <div class="pg-heading">🛡️ PhishGuard</div>
        <p class="pg-description">
            A phishing URL risk analyzer built to identify
            potentially suspicious website addresses.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Project Overview")

    st.write(
        "PhishGuard is a Python-based security application "
        "that examines URL structures and identifies potential "
        "phishing indicators using rule-based detection."
    )

    st.subheader("Technology Stack")

    tech_col1, tech_col2 = st.columns(2)

    with tech_col1:
        st.markdown("""
        - **Python** — Core programming
        - **Streamlit** — User interface
        - **SQLite** — Scan history storage
        """)

    with tech_col2:
        st.markdown("""
        - **Pandas** — Data handling
        - **Plotly** — Analytics and charts
        - **Rule-based analysis** — URL risk indicators
        """)

    st.subheader("Important Disclaimer")

    st.warning(
        "PhishGuard is an educational security analysis tool. "
        "It does not guarantee that a website is safe or malicious. "
        "Its risk scores are based on simple URL heuristics."
    )

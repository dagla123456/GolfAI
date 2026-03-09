"""
GolfAI Command Centre
Version: v2.4

Change Summary:
- Adds Learning Insights section
- Adds Practice Effectiveness section
- Improves text contrast across cards/tabs/comparison
- Keeps professional UI styling
- Keeps persistent uploaded session handling
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from io import BytesIO

from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis
from golfai.trends import build_trend_data
from golfai.comparison import compare_latest_sessions
from golfai.learning_engine import build_learning_insights
from golfai.practice_effectiveness import build_practice_effectiveness


def inject_styles():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        color: #1f2430 !important;
    }

    .main-title {
        background: linear-gradient(90deg, #173f2d, #214d39);
        color: white;
        padding: 1.1rem 1.4rem;
        border-radius: 0.8rem;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 1rem;
    }

    .section-label {
        background: #f1f2f5;
        border-radius: 0.5rem;
        padding: 0.35rem 0.8rem;
        text-align: center;
        font-weight: 700;
        color: #2f3440;
        margin-bottom: 0.7rem;
    }

    .summary-card, .card, .metric-bar {
        background: white;
        border: 1px solid #e7e9ef;
        border-radius: 0.7rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        color: #1f2430 !important;
    }

    .summary-card {
        padding: 1rem 1.1rem;
        min-height: 92px;
        margin-bottom: 0.6rem;
    }

    .summary-label, .metric-item-label {
        font-size: 0.95rem;
        color: #5b6270 !important;
        margin-bottom: 0.25rem;
    }

    .summary-value, .metric-item-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1f2430 !important;
    }

    .summary-value-green {
        font-size: 1.35rem;
        font-weight: 700;
        color: #167c35 !important;
    }

    .card {
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1f2430 !important;
        margin-bottom: 0.7rem;
    }

    .metric-bar {
        padding: 0.9rem 1rem;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }

    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .metric-item {
        flex: 1;
        min-width: 140px;
    }

    .delta-up {
        color: #167c35;
        font-weight: 700;
    }

    .delta-down {
        color: #b42318;
        font-weight: 700;
    }

    div[data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    button[data-baseweb="tab"] {
        background: #eceef3 !important;
        border-radius: 0.6rem 0.6rem 0 0 !important;
        padding: 0.65rem 1rem !important;
    }

    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #1f2430 !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: #1f4a35 !important;
        color: white !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: white !important;
    }

    .stMarkdown, .stMarkdown p, .stCaption, .stMetric, .stMetric label,
    .stMetric div, label, p, div, span {
        color: #1f2430;
    }
    </style>
    """, unsafe_allow_html=True)


def render_title():
    st.markdown('<div class="main-title">GOLF AI COMMAND CENTRE</div>', unsafe_allow_html=True)


def render_summary_panel(data):
    st.markdown('<div class="section-label">SESSION SUMMARY</div>', unsafe_allow_html=True)

    row1 = st.columns(3)
    row2 = st.columns(3)

    with row1[0]:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Performance</div>
            <div class="summary-value">{data.get("performance_score", 0)}</div>
        </div>
        """, unsafe_allow_html=True)

    with row1[1]:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Primary Issue</div>
            <div class="summary-value">{data.get("primary_issue", "-")}</div>
        </div>
        """, unsafe_allow_html=True)

    with row1[2]:
        momentum = data.get("momentum_label", "-")
        momentum_class = "summary-value-green" if "Improving" in str(momentum) or "↑" in str(momentum) else "summary-value"
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Momentum</div>
            <div class="{momentum_class}">{momentum}</div>
        </div>
        """, unsafe_allow_html=True)

    with row2[0]:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Miss Bias</div>
            <div class="summary-value">{data.get("miss_bias", "-")}</div>
        </div>
        """, unsafe_allow_html=True)

    with row2[1]:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Blueprint %</div>
            <div class="summary-value-green">{data.get("blueprint_match_pct", 0)}%</div>
        </div>
        """, unsafe_allow_html=True)

    with row2[2]:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Corridor %</div>
            <div class="summary-value-green">{data.get("corridor_pct", 0)}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def render_shot_pattern_chart(data):
    points = data.get("shot_pattern_points", [])

    if not points:
        st.warning("No shot pattern data available.")
        return

    df = pd.DataFrame(points, columns=["Side Carry", "Carry Distance"])

    mean_side = data.get("mean_side", 0)
    mean_carry = data.get("mean_carry", 0)
    ellipse_width = data.get("ellipse_width", 0)
    ellipse_height = data.get("ellipse_height", 0)
    corridor_m = data.get("corridor_m", 5)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.axvspan(-corridor_m, corridor_m, alpha=0.10)
    ax.axvline(0, linewidth=1)
    ax.scatter(df["Side Carry"], df["Carry Distance"])
    ax.scatter(mean_side, mean_carry, marker="D", s=80)

    if ellipse_width > 0 and ellipse_height > 0:
        ellipse = Ellipse(
            (mean_side, mean_carry),
            width=ellipse_width * 2,
            height=ellipse_height * 2,
            fill=False,
            linewidth=2
        )
        ax.add_patch(ellipse)

    ax.set_title("Shot Pattern Visualization")
    ax.set_xlabel("Side Carry (m)")
    ax.set_ylabel("Carry Distance (m)")
    ax.grid(True, linewidth=0.5)

    st.pyplot(fig)


def render_trend_chart(x, y, title, ylabel):
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(x, y, marker="o")
    ax.set_title(title)
    ax.set_xlabel("Session Date")
    ax.set_ylabel(ylabel)
    ax.grid(True, linewidth=0.5)

    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    st.pyplot(fig)


def format_delta_html(value, suffix=""):
    try:
        value_num = float(value)
    except Exception:
        value_num = 0

    if value_num > 0:
        return f'<span class="delta-up">▲ +{value_num}{suffix}</span>'
    elif value_num < 0:
        return f'<span class="delta-down">▼ {value_num}{suffix}</span>'
    return f'<span>0{suffix}</span>'


def render_comparison_section():
    comparison = compare_latest_sessions()

    if not comparison.get("has_comparison", False):
        st.markdown(
            '<div class="card"><div class="card-title">Session Comparison</div>'
            '<div style="color:#1f2430;">Comparison will appear after at least two sessions are stored.</div></div>',
            unsafe_allow_html=True
        )
        return

    performance_delta = format_delta_html(comparison.get("performance_delta", 0))
    blueprint_delta = format_delta_html(comparison.get("blueprint_delta", 0), "%")
    lowpoint_delta = format_delta_html(comparison.get("lowpoint_delta", 0))
    corridor_delta = format_delta_html(comparison.get("corridor_delta", 0), "%")

    st.markdown(f"""
    <div class="card">
        <div class="card-title">Session Comparison</div>
        <div style="margin-bottom:0.7rem; color:#5b6270;">
            Previous: {comparison.get("previous_session", "Previous")} |
            Current: {comparison.get("current_session", "Current")}
        </div>
        <div style="display:grid; row-gap:0.9rem; color:#1f2430;">
            <div><strong>Performance</strong> &nbsp; {comparison.get("performance_prev", 0)} → {comparison.get("performance_curr", 0)} &nbsp; {performance_delta}</div>
            <div><strong>Blueprint %</strong> &nbsp; {comparison.get("blueprint_prev", 0)} → {comparison.get("blueprint_curr", 0)} &nbsp; {blueprint_delta}</div>
            <div><strong>Low Point</strong> &nbsp; {comparison.get("lowpoint_prev", 0)} → {comparison.get("lowpoint_curr", 0)} &nbsp; {lowpoint_delta}</div>
            <div><strong>Corridor %</strong> &nbsp; {comparison.get("corridor_prev", 0)} → {comparison.get("corridor_curr", 0)} &nbsp; {corridor_delta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_learning_section():
    learning = build_learning_insights()

    if not learning.get("has_learning", False):
        st.markdown(
            f'<div class="card"><div class="card-title">Learning Insights</div>'
            f'<div style="color:#1f2430;">{learning.get("message","Learning insights unavailable.")}</div></div>',
            unsafe_allow_html=True
        )
        return

    trend_to_symbol = {
        "Improving": "▲",
        "Stable": "■",
        "Worsening": "▼"
    }

    def fmt(label):
        symbol = trend_to_symbol.get(label, "•")
        color = "#167c35" if label == "Improving" else "#b42318" if label == "Worsening" else "#5b6270"
        return f'<span style="color:{color}; font-weight:700;">{symbol} {label}</span>'

    st.markdown(f"""
    <div class="card">
        <div class="card-title">Learning Insights</div>
        <div style="display:grid; row-gap:0.8rem; color:#1f2430;">
            <div><strong>Performance</strong> &nbsp; {fmt(learning.get("performance_trend","-"))}</div>
            <div><strong>Blueprint</strong> &nbsp; {fmt(learning.get("blueprint_trend","-"))}</div>
            <div><strong>Low Point</strong> &nbsp; {fmt(learning.get("lowpoint_trend","-"))}</div>
            <div><strong>Dispersion</strong> &nbsp; {fmt(learning.get("dispersion_trend","-"))}</div>
            <div><strong>Strike</strong> &nbsp; {fmt(learning.get("strike_trend","-"))}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_practice_effectiveness():
    effectiveness = build_practice_effectiveness()

    if not effectiveness.get("has_effectiveness", False):
        st.markdown(
            f'<div class="card"><div class="card-title">Practice Effectiveness</div>'
            f'<div style="color:#1f2430;">{effectiveness.get("message","Practice effectiveness unavailable.")}</div></div>',
            unsafe_allow_html=True
        )
        return

    direction = effectiveness.get("overall_direction", "-")
    best = effectiveness.get("best_improvement", "-")
    best_delta = effectiveness.get("best_delta", 0)
    risk = effectiveness.get("biggest_risk", "-")
    risk_delta = effectiveness.get("risk_delta", 0)
    recommendation = effectiveness.get("recommendation", "-")

    st.markdown(f"""
    <div class="card">
        <div class="card-title">Practice Effectiveness</div>

        <div style="margin-bottom:0.7rem; color:#1f2430;">
            <strong>Overall Direction:</strong> {direction}
        </div>

        <div style="margin-bottom:0.7rem; color:#1f2430;">
            <strong>Best Improvement:</strong> {best} ({best_delta})
        </div>

        <div style="margin-bottom:0.7rem; color:#1f2430;">
            <strong>Biggest Risk:</strong> {risk} ({risk_delta})
        </div>

        <div style="color:#1f2430;">
            <strong>Recommendation:</strong> {recommendation}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_practice_plan(data):
    plan = data.get("practice_plan", {})

    left, right = st.columns(2)

    with left:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Practice Plan</div>
            <div style="margin-bottom:0.9rem; color:#1f2430;"><strong>Priority:</strong> {plan.get("practice_priority", "-")}</div>
            <div style="margin-bottom:0.9rem; color:#1f2430;"><strong>Drill:</strong> {plan.get("recommended_drill", "-")}</div>
            <div style="color:#1f2430;"><strong>Goal:</strong> {plan.get("session_goal", "-")}</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        render_comparison_section()

    render_learning_section()
    render_practice_effectiveness()

    st.markdown(f"""
    <div class="metric-bar">
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-item-label">Target Smash</div>
                <div class="metric-item-value">{plan.get("target_smash", "-")}</div>
            </div>
            <div class="metric-item">
                <div class="metric-item-label">Attack Window</div>
                <div class="metric-item-value">{plan.get("target_attack_window", "-")}</div>
            </div>
            <div class="metric-item">
                <div class="metric-item-label">Launch Window</div>
                <div class="metric-item-value">{plan.get("target_launch_direction", "-")}</div>
            </div>
            <div class="metric-item">
                <div class="metric-item-label">Path Window</div>
                <div class="metric-item-value">{plan.get("target_path_window", "-")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_trend_dashboard():
    st.subheader("Trend Dashboard")
    trend = build_trend_data()

    if trend.get("has_history", False):
        tr1, tr2 = st.columns(2)
        with tr1:
            render_trend_chart(trend["dates"], trend["performance"], "Performance Trend", "Score")
        with tr2:
            render_trend_chart(trend["dates"], trend["blueprint"], "Blueprint Trend", "%")

        tr3, tr4 = st.columns(2)
        with tr3:
            render_trend_chart(trend["dates"], trend["lowpoint"], "Low Point Stability Trend", "Score")
        with tr4:
            render_trend_chart(trend["dates"], trend["dispersion"], "Dispersion Corridor Trend", "%")
    else:
        st.info("Trend history will appear after multiple sessions.")


def render_swing_section(data):
    st.subheader("Swing Blueprint")

    b1, b2 = st.columns(2)
    b1.metric("Blueprint Matches", f"{data.get('blueprint_matches', 0)} / {data.get('blueprint_total', 0)}")
    b2.metric("Match %", f"{data.get('blueprint_match_pct', 0)}%")

    st.write(
        f"Target Pattern → Smash {data.get('bp_smash_target', 0)} | "
        f"Path {data.get('bp_path_target', 0)}° | "
        f"Start {data.get('bp_start_target', 0)}° | "
        f"Carry {data.get('bp_carry_target', 0)}m"
    )

    st.divider()
    st.subheader("Session Intelligence")

    s1, s2 = st.columns(2)
    s1.metric("Momentum", data.get("momentum_label", "-"), f"{data.get('momentum_delta', 0)}")

    if data.get("drift_detected", False):
        s2.error("⚠️ Swing Drift Detected")
    else:
        s2.success("Swing Stable")

    st.write(
        f"Start Drift: {data.get('drift_start_delta', 0)}° | "
        f"Path Drift: {data.get('drift_path_delta', 0)}°"
    )

    st.divider()
    st.subheader("Mechanics Snapshot")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Strike", data.get("strike_quality", 0))
    m2.metric("Start Line", data.get("start_line_control", 0))
    m3.metric("Sequencing", data.get("sequencing_score", 0))
    m4.metric("Low Point", data.get("lowpoint_score", 0))


def render_dispersion_section(data):
    st.subheader("Dispersion Intelligence")

    d1, d2, d3 = st.columns(3)
    d1.metric("Miss Bias", data.get("miss_bias", "-"))
    d2.metric("Corridor %", f"{data.get('corridor_pct', 0)}%")
    d3.metric("Dispersion Area", data.get("dispersion_area", 0))

    st.write(
        f"Side Avg: {data.get('side_avg', 0)} m | "
        f"Side Std: {data.get('side_std', 0)} m | "
        f"Carry Std: {data.get('carry_std_disp', 0)} m"
    )

    st.divider()
    st.subheader("Shot Pattern")
    render_shot_pattern_chart(data)

    st.divider()
    st.subheader("Key Metrics")

    k1, k2, k3 = st.columns(3)
    k1.metric("Smash Avg", data.get("smash_avg", 0))
    k2.metric("Carry Avg", data.get("carry_avg", 0))
    k3.metric("Launch Avg", data.get("launch_avg", 0))


def render_diagnostics_section(data):
    st.subheader("Diagnostics")

    with st.expander("Low Point Diagnostics", expanded=False):
        st.write(
            f"Carry CV: {data.get('carry_cv', 0)} | "
            f"Attack Std: {data.get('attack_std', 0)} | "
            f"Launch Angle Std: {data.get('launch_angle_std', 0)} | "
            f"Spin CV: {data.get('spin_cv', 0)}"
        )

    with st.expander("Sequencing Diagnostics", expanded=False):
        st.write(
            f"Good: {data.get('good_sequence_pct', 0)}% | "
            f"Borderline: {data.get('borderline_pct', 0)}% | "
            f"Early Chest: {data.get('early_chest_pct', 0)}%"
        )

    with st.expander("Drift Diagnostics", expanded=False):
        st.write(
            f"Session Start: {data.get('drift_start_session', 0)} | "
            f"Last 15 Start: {data.get('drift_start_last15', 0)}"
        )
        st.write(
            f"Session Path: {data.get('drift_path_session', 0)} | "
            f"Last 15 Path: {data.get('drift_path_last15', 0)}"
        )


def command_centre_page():
    inject_styles()
    render_title()

    if "latest_upload_bytes" not in st.session_state:
        st.session_state["latest_upload_bytes"] = None
    if "latest_upload_name" not in st.session_state:
        st.session_state["latest_upload_name"] = None

    uploaded_file = st.file_uploader(
        "Upload CSV / Select Session",
        type=["csv"],
        key="command_centre_upload"
    )

    if uploaded_file is not None:
        st.session_state["latest_upload_bytes"] = uploaded_file.getvalue()
        st.session_state["latest_upload_name"] = uploaded_file.name

    data = None

    if st.session_state["latest_upload_bytes"] is not None:
        file_like = BytesIO(st.session_state["latest_upload_bytes"])
        file_like.name = st.session_state["latest_upload_name"]
        data = run_golfai_analysis(uploaded_file=file_like)

        st.caption(f"Loaded session: {st.session_state['latest_upload_name']}")
        if st.button("Clear uploaded session"):
            st.session_state["latest_upload_bytes"] = None
            st.session_state["latest_upload_name"] = None
            st.rerun()
    else:
        sessions = list_sessions()

        if sessions:
            selected = st.selectbox(
                "Select Session",
                sessions,
                index=len(sessions) - 1
            )
            data = run_golfai_analysis(session_file=selected)
        else:
            st.info("Upload an MLM2PRO CSV to begin analysis.")
            return

    render_summary_panel(data)

    overview_tab, swing_tab, dispersion_tab, trends_tab, diagnostics_tab = st.tabs(
        ["Overview", "Swing", "Dispersion", "Trends", "Diagnostics"]
    )

    with overview_tab:
        render_practice_plan(data)

    with swing_tab:
        render_swing_section(data)

    with dispersion_tab:
        render_dispersion_section(data)

    with trends_tab:
        render_trend_dashboard()

    with diagnostics_tab:
        render_diagnostics_section(data)

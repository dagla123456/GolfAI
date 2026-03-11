"""
GolfAI Command Centre
Version: v3.1

Change Summary:
- Keeps v3 structure: Overview / Focus / Progress / Swing
- Adds Performance Gauge to Overview
- Keeps Practice Effectiveness on Overview
- Keeps Learning Insights + Trend charts on Progress
- Keeps technical details on Swing
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Wedge
from io import BytesIO

from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis
from golfai.trends import build_trend_data
from golfai.comparison import compare_latest_sessions
from golfai.learning_engine import build_learning_insights
from golfai.practice_effectiveness import build_practice_effectiveness
from golfai.trend_intelligence import build_trend_intelligence


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
        font-size: 2.1rem;
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
            <div class="summary-label">Session Score</div>
            <div class="summary-value">{data.get("performance_score", 0)}</div>
        </div>
        """, unsafe_allow_html=True)

    with row1[1]:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Biggest Risk</div>
            <div class="summary-value">{data.get("primary_issue", "-")}</div>
        </div>
        """, unsafe_allow_html=True)

    with row1[2]:
        momentum = data.get("momentum_label", "-")
        momentum_class = "summary-value-green" if "Improving" in str(momentum) or "↑" in str(momentum) else "summary-value"
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Swing Direction</div>
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
            <div class="summary-label">Best Area</div>
            <div class="summary-value-green">{data.get("practice_plan", {}).get("practice_priority", "-")}</div>
        </div>
        """, unsafe_allow_html=True)

    with row2[2]:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Blueprint %</div>
            <div class="summary-value-green">{data.get("blueprint_match_pct", 0)}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def render_performance_gauge(score):
    """
    Visual performance gauge using matplotlib.
    Score expected: 0-100
    """
    score = max(0, min(100, float(score)))

    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.set_aspect("equal")
    ax.axis("off")

    # Arc zones: Poor / Improving / Good / Excellent
    zones = [
        (180, 144, "#d9534f"),  # Poor
        (144, 108, "#f0ad4e"),  # Improving
        (108, 72, "#f7d154"),   # Good
        (72, 36, "#7bc96f"),    # Better
        (36, 0, "#2e8b57"),     # Excellent
    ]

    for start, end, color in zones:
        wedge = Wedge((0, 0), 1.0, end, start, width=0.24, facecolor=color, edgecolor="white")
        ax.add_patch(wedge)

    # Needle
    angle = 180 - (score / 100.0) * 180
    x = 0.78 * np.cos(np.deg2rad(angle))
    y = 0.78 * np.sin(np.deg2rad(angle))
    ax.plot([0, x], [0, y], linewidth=3, color="#1f2430")
    ax.scatter([0], [0], s=90, color="#1f2430", zorder=5)

    # Score text
    ax.text(0, -0.05, f"{int(round(score))}", ha="center", va="center",
            fontsize=34, fontweight="bold", color="#243b5a")

    # Labels
    ax.text(-0.98, -0.32, "Poor", fontsize=10, color="#5b6270", ha="left")
    ax.text(-0.25, 0.98, "Improving", fontsize=10, color="#5b6270", ha="center")
    ax.text(0.98, -0.32, "Excellent", fontsize=10, color="#5b6270", ha="right")

    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.45, 1.15)

    st.subheader("Performance Gauge")
    st.pyplot(fig, clear_figure=True)


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

    ax.set_title("Shot Pattern")
    ax.set_xlabel("Side Carry (m)")
    ax.set_ylabel("Carry Distance (m)")
    ax.grid(True, linewidth=0.5)

    st.pyplot(fig, clear_figure=True)


def render_trend_chart(x, y, title, ylabel):
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(x, y, marker="o")
    ax.set_title(title)
    ax.set_xlabel("Session Date")
    ax.set_ylabel(ylabel)
    ax.grid(True, linewidth=0.5)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)


def render_session_comparison():
    comparison = compare_latest_sessions()

    st.subheader("Session vs Previous")

    if not comparison.get("has_comparison", False):
        st.info("Comparison will appear after at least two sessions are stored.")
        return

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Strike",
            comparison.get("performance_curr", 0),
            comparison.get("performance_delta", 0)
        )

    with c2:
        st.metric(
            "Blueprint",
            comparison.get("blueprint_curr", 0),
            comparison.get("blueprint_delta", 0)
        )

    with c3:
        st.metric(
            "Dispersion",
            comparison.get("corridor_curr", 0),
            comparison.get("corridor_delta", 0)
        )


def render_focus_section(data):
    st.subheader("Today's Focus")

    plan = data.get("practice_plan", {})

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Primary Focus", plan.get("practice_priority", "-"))
        st.metric("Recommended Drill", plan.get("recommended_drill", "-"))

    with c2:
        secondary = data.get("secondary_issue", "-")
        st.metric("Secondary Focus", secondary)
        st.info(plan.get("session_goal", "-"))


def render_learning_section():
    st.subheader("Learning Insights")

    learning = build_learning_insights()

    if not learning.get("has_learning", False):
        st.info(learning.get("message", "Learning insights unavailable."))
        return

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Performance", learning.get("performance_trend", "-"))
        st.metric("Strike", learning.get("strike_trend", "-"))

    with c2:
        st.metric("Blueprint", learning.get("blueprint_trend", "-"))
        st.metric("Low Point", learning.get("lowpoint_trend", "-"))

    with c3:
        st.metric("Dispersion", learning.get("dispersion_trend", "-"))


def render_practice_effectiveness():
    effectiveness = build_practice_effectiveness()

    st.subheader("Practice Effectiveness")

    if not effectiveness.get("has_effectiveness", False):
        st.info(effectiveness.get(
            "message",
            "Practice effectiveness appears after at least two sessions."
        ))
        return

    direction = effectiveness.get("overall_direction", "-")
    best = effectiveness.get("best_improvement", "-")
    best_delta = effectiveness.get("best_delta", 0)
    risk = effectiveness.get("biggest_risk", "-")
    risk_delta = effectiveness.get("risk_delta", 0)
    recommendation = effectiveness.get("recommendation", "-")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Overall Direction", direction)
        st.metric("Best Improvement", best, best_delta)

    with c2:
        st.metric("Biggest Risk", risk, risk_delta)

    st.write("**Recommendation**")
    st.write(recommendation)
    st.divider()

def render_trend_intelligence():
    st.subheader("Trend Intelligence")

    trend_info = build_trend_intelligence()

    if not trend_info.get("has_trends", False):
        st.info(trend_info.get("message", "Trend intelligence unavailable."))
        return

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Strongest Gain",
            trend_info.get("strongest_gain", "-"),
            trend_info.get("strongest_gain_delta", 0)
        )

    with c2:
        st.metric(
            "Biggest Concern",
            trend_info.get("biggest_concern", "-"),
            trend_info.get("biggest_concern_delta", 0)
        )

    st.write("**Next Priority**")
    st.write(trend_info.get("next_priority", "-"))

    st.caption(f"Based on last {trend_info.get('lookback_sessions', 0)} sessions")
    st.divider()

def render_progress_section():
    render_learning_section()
    render_trend_intelligence()
    render_practice_effectiveness()

    st.subheader("Progress Over Time")
    
    trend = build_trend_data()

    if trend.get("has_history", False):
        c1, c2 = st.columns(2)

        with c1:
            render_trend_chart(
                trend["dates"],
                trend["performance"],
                "Performance Trend",
                "Score"
            )

        with c2:
            render_trend_chart(
                trend["dates"],
                trend["dispersion"],
                "Dispersion Trend",
                "%"
            )
    else:
        st.info("Trend history will appear after multiple sessions.")


def render_swing_section(data):
    st.subheader("Swing Blueprint")

    c1, c2 = st.columns(2)
    c1.metric(
        "Blueprint Matches",
        f"{data.get('blueprint_matches', 0)} / {data.get('blueprint_total', 0)}"
    )
    c2.metric("Match %", f"{data.get('blueprint_match_pct', 0)}%")

    st.write(
        f"Target Pattern → Smash {data.get('bp_smash_target', 0)} | "
        f"Path {data.get('bp_path_target', 0)}° | "
        f"Start {data.get('bp_start_target', 0)}° | "
        f"Carry {data.get('bp_carry_target', 0)}m"
    )

    st.divider()
    st.subheader("Mechanics")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Strike", data.get("strike_quality", 0))
    m2.metric("Start Line", data.get("start_line_control", 0))
    m3.metric("Sequencing", data.get("sequencing_score", 0))
    m4.metric("Low Point", data.get("lowpoint_score", 0))

    st.divider()
    st.subheader("Dispersion")

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

    overview_tab, focus_tab, progress_tab, swing_tab = st.tabs(
        ["Overview", "Focus", "Progress", "Swing"]
    )

    with overview_tab:
        render_performance_gauge(data.get("performance_score", 0))
        st.divider()
        render_shot_pattern_chart(data)
        st.divider()
        render_session_comparison()
        st.divider()
        render_practice_effectiveness()

    with focus_tab:
        render_focus_section(data)

    with progress_tab:
        render_progress_section()

    with swing_tab:
        render_swing_section(data)

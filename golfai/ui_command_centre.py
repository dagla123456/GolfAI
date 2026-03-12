"""
GolfAI Command Centre
Version: v3.3

UX Uplift Pack v1
- Keeps current analytics stable
- Restores v3 structure: Overview / Focus / Progress / Swing
- Upgrades Overview to 2x2 dashboard grid
- Keeps Performance Gauge, Distance Intelligence, Shot Pattern,
  Session Comparison, and Practice Effectiveness
- Improves hierarchy and readability
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
from golfai.distance_engine import build_distance_intelligence
from golfai.v4_charts import build_v4_dispersion_chart, build_v4_distance_chart, build_v4_progress_chart
from golfai.distance_chart import render_distance_range_chart
from golfai.dispersion_chart import render_professional_dispersion_chart


def inject_styles():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        color: #1f2430 !important;
    }

    .main-title {
        background: linear-gradient(90deg, #173f2d, #214d39);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 0.9rem;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .dashboard-card {
        background: white;
        border: 1px solid #e6e9ef;
        border-radius: 0.9rem;
        padding: 1rem 1rem 0.8rem 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 0.8rem;
    }

    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1f2430 !important;
        margin-bottom: 0.6rem;
    }

    .summary-strip {
        background: #f5f7fa;
        border: 1px solid #e6e9ef;
        border-radius: 0.8rem;
        padding: 0.75rem 0.9rem;
        margin-bottom: 1rem;
    }

    button[data-baseweb="tab"] {
        background: #eceef3 !important;
        border-radius: 0.7rem 0.7rem 0 0 !important;
        padding: 0.65rem 1rem !important;
    }

    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #1f2430 !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: #1f4a35 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_title():
    st.markdown('<div class="main-title">GOLF AI COMMAND CENTRE</div>', unsafe_allow_html=True)


def render_summary_panel(data):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Session Score", data.get("performance_score", 0))
    with c2:
        st.metric("Biggest Risk", data.get("primary_issue", "-"))
    with c3:
        st.metric("Swing Direction", data.get("momentum_label", "-"))


def render_performance_gauge(score):
    score = max(0, min(100, float(score)))

    fig, ax = plt.subplots(figsize=(5.0, 3.1))
    ax.set_aspect("equal")
    ax.axis("off")

    zones = [
        (180, 144, "#d9534f"),
        (144, 108, "#f0ad4e"),
        (108, 72, "#f7d154"),
        (72, 36, "#7bc96f"),
        (36, 0, "#2e8b57"),
    ]

    for start, end, color in zones:
        wedge = Wedge((0, 0), 1.0, end, start, width=0.24,
                      facecolor=color, edgecolor="white")
        ax.add_patch(wedge)

    angle = 180 - (score / 100.0) * 180
    x = 0.78 * np.cos(np.deg2rad(angle))
    y = 0.78 * np.sin(np.deg2rad(angle))
    ax.plot([0, x], [0, y], linewidth=3, color="#1f2430")
    ax.scatter([0], [0], s=90, color="#1f2430", zorder=5)

    ax.text(0, -0.05, f"{int(round(score))}", ha="center", va="center",
            fontsize=30, fontweight="bold", color="#243b5a")

    ax.text(-0.95, -0.28, "Poor", fontsize=10, color="#5b6270", ha="left")
    ax.text(-0.15, 0.95, "Improving", fontsize=10, color="#5b6270", ha="center")
    ax.text(0.95, -0.28, "Excellent", fontsize=10, color="#5b6270", ha="right")

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.42, 1.08)

    st.markdown('<div class="section-title">Performance Gauge</div>', unsafe_allow_html=True)
    st.pyplot(fig, clear_figure=True)


def render_shot_pattern_chart(data):
    st.markdown('<div class="section-title">Shot Pattern</div>', unsafe_allow_html=True)

    fig = render_professional_dispersion_chart(data)
    if fig is None:
        st.info("No shot pattern data available.")
        return

    st.pyplot(fig, clear_figure=True)


def render_session_comparison_card():
    comparison = compare_latest_sessions()

    st.markdown('<div class="section-title">Session Comparison</div>', unsafe_allow_html=True)

    if not comparison.get("has_comparison", False):
        st.info("Comparison will appear after at least two sessions are stored.")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Strike", comparison.get("performance_curr", 0),
                  comparison.get("performance_delta", 0))
    with c2:
        st.metric("Blueprint", comparison.get("blueprint_curr", 0),
                  comparison.get("blueprint_delta", 0))
    with c3:
        st.metric("Dispersion", comparison.get("corridor_curr", 0),
                  comparison.get("corridor_delta", 0))


def render_practice_effectiveness_card():
    effectiveness = build_practice_effectiveness()

    st.markdown('<div class="section-title">Practice Effectiveness</div>', unsafe_allow_html=True)

    if not effectiveness.get("has_effectiveness", False):
        st.info(effectiveness.get("message", "Practice effectiveness unavailable."))
        return

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Overall Direction", effectiveness.get("overall_direction", "-"))
        st.metric("Best Improvement",
                  effectiveness.get("best_improvement", "-"),
                  effectiveness.get("best_delta", 0))
    with c2:
        st.metric("Biggest Risk",
                  effectiveness.get("biggest_risk", "-"),
                  effectiveness.get("risk_delta", 0))

    st.write("**Recommendation**")
    st.write(effectiveness.get("recommendation", "-"))


def render_distance_intelligence_card(data):
    st.markdown('<div class="section-title">Distance Intelligence</div>', unsafe_allow_html=True)

    distance_info = build_distance_intelligence(
        data.get("df"),
        club_label=data.get("club_label", "7i")
    )

    if not distance_info.get("has_distance_intel", False):
        st.info("Distance intelligence unavailable.")
        return

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Club", distance_info.get("club", "-"))
        st.metric("Average Carry", f'{distance_info.get("avg_carry", 0)} m')
        st.metric("Confidence", distance_info.get("confidence", "-"))
    with c2:
        st.metric("Reliable Range",
                  f'{distance_info.get("reliable_min", 0)}–{distance_info.get("reliable_max", 0)} m')
        st.metric("Full Range",
                  f'{distance_info.get("full_min", 0)}–{distance_info.get("full_max", 0)} m')
        st.metric("Spread", f'{distance_info.get("distance_spread", 0)} m')

    st.write("**Recommendation**")
    st.write(distance_info.get("recommendation", "-"))

    fig = build_v4_distance_chart(distance_info)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

    fig = render_distance_range_chart(distance_info)
    if fig is not None:
        st.pyplot(fig, clear_figure=True)


def render_focus_section(data):
    st.subheader("Today's Focus")
    plan = data.get("practice_plan", {})

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Primary Focus", plan.get("practice_priority", "-"))
        st.metric("Recommended Drill", plan.get("recommended_drill", "-"))
    with c2:
        st.metric("Secondary Focus", data.get("secondary_issue", "-"))
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


def render_trend_chart(x, y, title, ylabel):
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x, y, marker="o")
    ax.set_title(title)
    ax.set_xlabel("Session Date")
    ax.set_ylabel(ylabel)
    ax.grid(True, linewidth=0.5)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)


def render_progress_section():
    render_learning_section()
    st.subheader("Progress Over Time")

    trend = build_trend_data()
    fig = build_v4_progress_chart(trend)
    if fig is None:
        st.info("Trend history will appear after multiple sessions.")
    else:
        st.plotly_chart(fig, use_container_width=True)


def render_swing_section(data):
    st.subheader("Swing Blueprint")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Blueprint Matches",
                  f"{data.get('blueprint_matches', 0)} / {data.get('blueprint_total', 0)}")
    with c2:
        st.metric("Match %", f"{data.get('blueprint_match_pct', 0)}%")

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
            selected = st.selectbox("Select Session", sessions, index=len(sessions) - 1)
            data = run_golfai_analysis(session_file=selected)
        else:
            st.info("Upload an MLM2PRO CSV to begin analysis.")
            return

    st.markdown('<div class="summary-strip"></div>', unsafe_allow_html=True)
    render_summary_panel(data)

    overview_tab, focus_tab, progress_tab, swing_tab = st.tabs(
        ["Overview", "Focus", "Progress", "Swing"]
    )

    with overview_tab:
        top_left, top_right = st.columns(2)
        with top_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_performance_gauge(data.get("performance_score", 0))
            st.markdown('</div>', unsafe_allow_html=True)
        with top_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_distance_intelligence_card(data)
            st.markdown('</div>', unsafe_allow_html=True)

        bottom_left, bottom_right = st.columns(2)
        with bottom_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_shot_pattern_chart(data)
            st.markdown('</div>', unsafe_allow_html=True)
        with bottom_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_session_comparison_card()
            st.divider()
            render_practice_effectiveness_card()
            st.markdown('</div>', unsafe_allow_html=True)

    with focus_tab:
        render_focus_section(data)

    with progress_tab:
        render_progress_section()

    with swing_tab:
        render_swing_section(data)

"""
GolfAI Command Centre
Version: v3.2

Change Summary:
- Restructures UI into Overview / Focus / Progress / Swing
- Adds Performance Gauge to Overview
- Adds Distance Intelligence to Overview
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
from golfai.distance_engine import build_distance_intelligence


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
        font-size: 2.0rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #1f2430 !important;
        font-weight: 600 !important;
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

    fig, ax = plt.subplots(figsize=(5.2, 3.4))
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
        wedge = Wedge((0, 0), 1.0, end, start, width=0.24, facecolor=color, edgecolor="white")
        ax.add_patch(wedge)

    angle = 180 - (score / 100.0) * 180
    x = 0.78 * np.cos(np.deg2rad(angle))
    y = 0.78 * np.sin(np.deg2rad(angle))
    ax.plot([0, x], [0, y], linewidth=3, color="#1f2430")
    ax.scatter([0], [0], s=90, color="#1f2430", zorder=5)

    ax.text(0, -0.05, f"{int(round(score))}", ha="center", va="center",
            fontsize=34, fontweight="bold", color="#243b5a")

    ax.text(-0.98, -0.32, "Poor", fontsize=10, color="#5b6270", ha="left")
    ax.text(-0.25, 0.98, "Improving", fontsize=10, color="#5b6270", ha="center")
    ax.text(0.98, -0.32, "Excellent", fontsize=10, color="#5b6270", ha="right")

    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.45, 1.15)

    st.subheader("Performance Gauge")
    st.pyplot(fig, clear_figure=True)


def render_shot_pattern_chart(data):
    points = data.get("shot_pattern_points", [])
    st.subheader("Shot Pattern")

    if not points:
        st.warning("No shot pattern data available.")
        return

    df = pd.DataFrame(points, columns=["Side Carry", "Carry Distance"])
    mean_side = data.get("mean_side", 0)
    mean_carry = data.get("mean_carry", 0)
    ellipse_width = data.get("ellipse_width", 0)
    ellipse_height = data.get("ellipse_height", 0)
    corridor_m = data.get("corridor_m", 5)

    fig, ax = plt.subplots(figsize=(7.6, 6.2))
    ax.axvspan(-corridor_m, corridor_m, alpha=0.14)
    ax.axvline(0, linewidth=1.6, linestyle="--")
    ax.scatter(df["Side Carry"], df["Carry Distance"], s=52, alpha=0.85)
    ax.scatter(mean_side, mean_carry, marker="D", s=110, zorder=5)

    if ellipse_width > 0 and ellipse_height > 0:
        ellipse = Ellipse((mean_side, mean_carry), width=ellipse_width * 2, height=ellipse_height * 2,
                          fill=False, linewidth=2.2)
        ax.add_patch(ellipse)

    ax.set_title("Shot Dispersion Pattern", pad=12)
    ax.set_xlabel("Side Carry (m)")
    ax.set_ylabel("Carry Distance (m)")
    ax.grid(True, linewidth=0.45, alpha=0.6)

    x_pad = max(corridor_m, abs(df["Side Carry"]).max() if len(df) else 5) + 4
    y_min = max(0, df["Carry Distance"].min() - 8)
    y_max = df["Carry Distance"].max() + 8
    ax.set_xlim(-x_pad, x_pad)
    ax.set_ylim(y_min, y_max)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

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
        st.metric("Strike", comparison.get("performance_curr", 0), comparison.get("performance_delta", 0))
    with c2:
        st.metric("Blueprint", comparison.get("blueprint_curr", 0), comparison.get("blueprint_delta", 0))
    with c3:
        st.metric("Dispersion", comparison.get("corridor_curr", 0), comparison.get("corridor_delta", 0))


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


def render_practice_effectiveness():
    effectiveness = build_practice_effectiveness()
    st.subheader("Practice Effectiveness")

    if not effectiveness.get("has_effectiveness", False):
        st.info(effectiveness.get("message", "Practice effectiveness appears after at least two sessions."))
        return

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Overall Direction", effectiveness.get("overall_direction", "-"))
        st.metric("Best Improvement", effectiveness.get("best_improvement", "-"), effectiveness.get("best_delta", 0))
    with c2:
        st.metric("Biggest Risk", effectiveness.get("biggest_risk", "-"), effectiveness.get("risk_delta", 0))

    st.write("**Recommendation**")
    st.write(effectiveness.get("recommendation", "-"))
    st.divider()


def render_distance_intelligence(data):
    st.subheader("Distance Intelligence")

    distance_info = build_distance_intelligence(
        data.get("df"),
        club_label=data.get("club_label", "7i")
    )

    if not distance_info.get("has_distance_intel", False):
        st.info("Distance intelligence unavailable.")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Club", distance_info.get("club", "-"))
        st.metric("Average Carry", f'{distance_info.get("avg_carry", 0)} m')
    with c2:
        st.metric("Reliable Range", f'{distance_info.get("reliable_min", 0)}–{distance_info.get("reliable_max", 0)} m')
        st.metric("Confidence", distance_info.get("confidence", "-"))
    with c3:
        st.metric("Full Range", f'{distance_info.get("full_min", 0)}–{distance_info.get("full_max", 0)} m')
        st.metric("Spread", f'{distance_info.get("distance_spread", 0)} m')

    st.write("**Recommendation**")
    st.write(distance_info.get("recommendation", "-"))
    render_distance_range_chart(distance_info)


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



def render_distance_range_chart(distance_info):
    if not distance_info.get("has_distance_intel", False):
        return

    full_min = float(distance_info.get("full_min", 0))
    full_max = float(distance_info.get("full_max", 0))
    reliable_min = float(distance_info.get("reliable_min", 0))
    reliable_max = float(distance_info.get("reliable_max", 0))
    avg_carry = float(distance_info.get("avg_carry", 0))

    if full_max <= full_min:
        return

    fig, ax = plt.subplots(figsize=(8, 1.8))
    ax.set_xlim(full_min - 3, full_max + 3)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Full range line
    ax.hlines(y=0.5, xmin=full_min, xmax=full_max, linewidth=6, alpha=0.35)

    # Reliable range band
    ax.hlines(y=0.5, xmin=reliable_min, xmax=reliable_max, linewidth=12, alpha=0.9)

    # Average carry marker
    ax.plot(avg_carry, 0.5, marker="o", markersize=10)

    # Labels
    ax.text(full_min, 0.18, f"{full_min:.0f}", ha="center", va="center", fontsize=10)
    ax.text(full_max, 0.18, f"{full_max:.0f}", ha="center", va="center", fontsize=10)
    ax.text(avg_carry, 0.82, f"Avg {avg_carry:.1f} m", ha="center", va="center", fontsize=10)
    ax.text((reliable_min + reliable_max) / 2, 0.18,
            f"Reliable {reliable_min:.1f}–{reliable_max:.1f} m",
            ha="center", va="center", fontsize=10)

    st.subheader("Distance Range")
    st.pyplot(fig, clear_figure=True)
    st.divider()

def render_progress_section():
    render_learning_section()
    render_practice_effectiveness()

    st.subheader("Progress Over Time")
    trend = build_trend_data()

    if trend.get("has_history", False):
        c1, c2 = st.columns(2)
        with c1:
            render_trend_chart(trend["dates"], trend["performance"], "Performance Trend", "Score")
        with c2:
            render_trend_chart(trend["dates"], trend["dispersion"], "Dispersion Trend", "%")
    else:
        st.info("Trend history will appear after multiple sessions.")


def render_swing_section(data):
    st.subheader("Swing Blueprint")

    c1, c2 = st.columns(2)
    c1.metric("Blueprint Matches", f"{data.get('blueprint_matches', 0)} / {data.get('blueprint_total', 0)}")
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
        render_distance_intelligence(data)

    with focus_tab:
        render_focus_section(data)

    with progress_tab:
        render_progress_section()

    with swing_tab:
        render_swing_section(data)

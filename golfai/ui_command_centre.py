"""
GolfAI Command Centre
Version: v1.3

Change Summary:
- Restores full Command Centre layout
- Keeps GolfAI Diagnosis summary panel
- Keeps date-based Trend Dashboard
- Adds Session Comparison section
- Keeps CSV upload workflow
- Restores Blueprint, Session Intelligence,
  Mechanics Snapshot, Dispersion Intelligence,
  Key Metrics, and Diagnostics sections
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis
from golfai.trends import build_trend_data
from golfai.comparison import compare_latest_sessions


def render_summary_panel(data):
    st.subheader("GolfAI Diagnosis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Primary Issue", data.get("primary_issue", "-"))
        st.metric("Secondary Issue", data.get("secondary_issue", "-"))

    with col2:
        st.metric("Momentum", data.get("momentum_label", "-"))
        if data.get("drift_detected", False):
            st.error("Swing Drift Detected")
        else:
            st.success("Swing Stable")

    with col3:
        st.metric("Miss Bias", data.get("miss_bias", "-"))
        st.metric("Performance Score", data.get("performance_score", 0))

    st.divider()


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


def render_comparison_section():
    st.subheader("Session Comparison")

    comparison = compare_latest_sessions()

    if not comparison.get("has_comparison", False):
        st.info(comparison.get("message", "Comparison unavailable."))
        st.divider()
        return

    st.caption(
        f"Previous: {comparison.get('previous_session', 'Previous')}  |  "
        f"Current: {comparison.get('current_session', 'Current')}"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Performance",
        comparison.get("performance_curr", 0),
        comparison.get("performance_delta", 0)
    )
    c2.metric(
        "Blueprint %",
        comparison.get("blueprint_curr", 0),
        comparison.get("blueprint_delta", 0)
    )
    c3.metric(
        "Low Point",
        comparison.get("lowpoint_curr", 0),
        comparison.get("lowpoint_delta", 0)
    )
    c4.metric(
        "Corridor %",
        comparison.get("corridor_curr", 0),
        comparison.get("corridor_delta", 0)
    )

    st.divider()


def command_centre_page():
    st.title("GolfAI Command Centre")

    uploaded_file = st.file_uploader(
        "Upload MLM2PRO CSV",
        type=["csv"]
    )

    data = None

    if uploaded_file is not None:
        data = run_golfai_analysis(uploaded_file=uploaded_file)
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

    st.subheader("Practice Plan")

    plan = data.get("practice_plan", {})

    p1, p2 = st.columns(2)

    with p1:
        st.metric("Plan", plan.get("practice_plan_title", "-"))
        st.metric("Priority", plan.get("practice_priority", "-"))
        st.metric("Drill", plan.get("recommended_drill", "-"))

    with p2:
        st.info(plan.get("session_goal", "-"))

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Target Smash", plan.get("target_smash", "-"))
    t2.metric("Attack Window", plan.get("target_attack_window", "-"))
    t3.metric("Launch Window", plan.get("target_launch_direction", "-"))
    t4.metric("Path Window", plan.get("target_path_window", "-"))

    st.divider()

    render_comparison_section()

    st.subheader("Trend Dashboard")

    trend = build_trend_data()

    if trend.get("has_history", False):
        tr1, tr2 = st.columns(2)

        with tr1:
            render_trend_chart(
                trend["dates"],
                trend["performance"],
                "Performance Trend",
                "Score"
            )

        with tr2:
            render_trend_chart(
                trend["dates"],
                trend["blueprint"],
                "Blueprint Trend",
                "%"
            )

        tr3, tr4 = st.columns(2)

        with tr3:
            render_trend_chart(
                trend["dates"],
                trend["lowpoint"],
                "Low Point Stability Trend",
                "Score"
            )

        with tr4:
            render_trend_chart(
                trend["dates"],
                trend["dispersion"],
                "Dispersion Corridor Trend",
                "%"
            )
    else:
        st.info("Trend history will appear after multiple sessions.")

    st.divider()

    st.subheader("Swing Blueprint")

    b1, b2 = st.columns(2)
    b1.metric(
        "Blueprint Matches",
        f"{data.get('blueprint_matches', 0)} / {data.get('blueprint_total', 0)}"
    )
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

    st.divider()

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

    st.divider()

    with st.expander("Low Point Diagnostics"):
        st.write(
            f"Carry CV: {data.get('carry_cv', 0)} | "
            f"Attack Std: {data.get('attack_std', 0)} | "
            f"Launch Angle Std: {data.get('launch_angle_std', 0)} | "
            f"Spin CV: {data.get('spin_cv', 0)}"
        )

    with st.expander("Sequencing Diagnostics"):
        st.write(
            f"Good: {data.get('good_sequence_pct', 0)}% | "
            f"Borderline: {data.get('borderline_pct', 0)}% | "
            f"Early Chest: {data.get('early_chest_pct', 0)}%"
        )

    with st.expander("Drift Diagnostics"):
        st.write(
            f"Session Start: {data.get('drift_start_session', 0)} | "
            f"Last 15 Start: {data.get('drift_start_last15', 0)}"
        )
        st.write(
            f"Session Path: {data.get('drift_path_session', 0)} | "
            f"Last 15 Path: {data.get('drift_path_last15', 0)}"
        )

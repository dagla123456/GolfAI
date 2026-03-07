"""
GolfAI Command Centre
Version: v0.8

Changes in v0.8:
- Added CSV upload for Streamlit Cloud use
- Uses uploaded file when present
- Falls back to local session list if available
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis


def render_shot_pattern_chart(data):
    points = data.get("shot_pattern_points", [])

    if not points:
        st.warning("No shot pattern data available.")
        return

    df = pd.DataFrame(points, columns=["Side Carry", "Carry Distance"])

    mean_side = data.get("mean_side", 0.0)
    mean_carry = data.get("mean_carry", 0.0)
    ellipse_width = data.get("ellipse_width", 0.0)
    ellipse_height = data.get("ellipse_height", 0.0)
    corridor_m = data.get("corridor_m", 5.0)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.axvspan(-corridor_m, corridor_m, alpha=0.12)
    ax.axvline(0, linewidth=1)
    ax.scatter(df["Side Carry"], df["Carry Distance"], marker="o")
    ax.scatter([mean_side], [mean_carry], marker="D", s=80)

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
    ax.set_xlabel("Side Carry (m)  [Left (-) / Right (+)]")
    ax.set_ylabel("Carry Distance (m)")
    ax.grid(True, linewidth=0.5)

    st.pyplot(fig)


def command_centre_page():
    st.title("GolfAI Command Centre")

    uploaded_file = st.file_uploader(
        "Upload MLM2PRO session CSV",
        type=["csv"]
    )

    data = None

    if uploaded_file is not None:
        data = run_golfai_analysis(uploaded_file=uploaded_file)
    else:
        sessions = list_sessions()
        if sessions:
            selected_session = st.selectbox(
                "Select Session",
                sessions,
                index=len(sessions) - 1
            )
            data = run_golfai_analysis(session_file=selected_session)
        else:
            st.info("Upload an MLM2PRO CSV to begin analysis.")
            return

    practice_plan = data.get("practice_plan", {})

    st.caption(
        f"Session: {data.get('session_file', '-')} | "
        f"Shots analysed: {data.get('shots_analysed', 0)}"
    )

    st.subheader("Session Diagnosis")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Performance", data.get("performance_score", 0))
    c2.metric("Primary Issue", data.get("primary_issue", "-"))
    c3.metric("Secondary Issue", data.get("secondary_issue", "-"))
    c4.metric("One Cue", data.get("one_cue", "-"))

    st.divider()

    st.subheader("Practice Plan")
    p1, p2 = st.columns([1, 1])

    with p1:
        st.metric("Plan", practice_plan.get("practice_plan_title", "-"))
        st.metric("Priority", practice_plan.get("practice_priority", "-"))
        st.metric("Drill", practice_plan.get("recommended_drill", "-"))

    with p2:
        st.info(practice_plan.get("session_goal", "-"))

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Target Smash", practice_plan.get("target_smash", "-"))
    t2.metric("Attack Window", practice_plan.get("target_attack_window", "-"))
    t3.metric("Launch Window", practice_plan.get("target_launch_direction", "-"))
    t4.metric("Path Window", practice_plan.get("target_path_window", "-"))

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

    st.subheader("Shot Pattern Visualization")
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

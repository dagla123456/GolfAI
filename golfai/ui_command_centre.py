"""
GolfAI Command Centre
Version: v1.1

Change Summary:
- Adds Command Centre Summary Panel
- Keeps date-based Trend Dashboard
- Keeps CSV upload workflow
- Keeps shot pattern visualization
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis
from golfai.trends import build_trend_data


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

    ax.axvspan(-corridor_m, corridor_m, alpha=0.1)
    ax.axvline(0)
    ax.scatter(df["Side Carry"], df["Carry Distance"])
    ax.scatter(mean_side, mean_carry, marker="D", s=80)

    ellipse = Ellipse(
        (mean_side, mean_carry),
        width=ellipse_width * 2,
        height=ellipse_height * 2,
        fill=False,
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

    # --------------------------------
    # SUMMARY PANEL
    # --------------------------------
    render_summary_panel(data)

    # --------------------------------
    # PRACTICE PLAN
    # --------------------------------
    st.subheader("Practice Plan")

    plan = data.get("practice_plan", {})

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Plan", plan.get("practice_plan_title", "-"))
        st.metric("Priority", plan.get("practice_priority", "-"))
        st.metric("Drill", plan.get("recommended_drill", "-"))

    with col2:
        st.info(plan.get("session_goal", "-"))

    st.divider()

    # --------------------------------
    # TREND DASHBOARD
    # --------------------------------
    st.subheader("Trend Dashboard")

    trend = build_trend_data()

    if trend.get("has_history", False):
        col1, col2 = st.columns(2)

        with col1:
            render_trend_chart(
                trend["dates"],
                trend["performance"],
                "Performance Trend",
                "Score"
            )

        with col2:
            render_trend_chart(
                trend["dates"],
                trend["blueprint"],
                "Blueprint Trend",
                "%"
            )

        col3, col4 = st.columns(2)

        with col3:
            render_trend_chart(
                trend["dates"],
                trend["lowpoint"],
                "Low Point Stability Trend",
                "Score"
            )

        with col4:
            render_trend_chart(
                trend["dates"],
                trend["dispersion"],
                "Dispersion Corridor Trend",
                "%"
            )
    else:
        st.info("Trend history will appear after multiple sessions.")

    st.divider()

    # --------------------------------
    # SHOT PATTERN
    # --------------------------------
    st.subheader("Shot Pattern")
    render_shot_pattern_chart(data)

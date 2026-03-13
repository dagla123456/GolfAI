import streamlit as st
import plotly.graph_objects as go
from io import BytesIO

from golfai.v4_styles import get_v4_css
from golfai.v4_cards import card_open, card_close
from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis
from golfai.distance_engine import build_distance_intelligence
from golfai.comparison import compare_latest_sessions
from golfai.trends import build_trend_data
from golfai.v4_dispersion import build_v4_dispersion_figure
from golfai.v4_distance_profile import render_v4_distance_profile


def build_v4_gauge(score: float):
    score = max(0, min(100, float(score)))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 42, "color": "#f5f7fa"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#cfd8dc"},
            "bar": {"color": "rgba(0,0,0,0)"},
            "bgcolor": "#142c34",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 35], "color": "#ff4d4d"},
                {"range": [35, 55], "color": "#ff8c42"},
                {"range": [55, 72], "color": "#ffd166"},
                {"range": [72, 100], "color": "#1ed760"},
            ],
            "threshold": {
                "line": {"color": "#f5f7fa", "width": 5},
                "thickness": 0.8,
                "value": score
            }
        }
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="#142c34",
        font={"color": "#e8f0f2"}
    )
    return fig


def build_distance_profile_figure(distance_info):
    avg = float(distance_info.get("avg_carry", 0))
    rmin = float(distance_info.get("reliable_min", 0))
    rmax = float(distance_info.get("reliable_max", 0))
    fmin = float(distance_info.get("full_min", 0))
    fmax = float(distance_info.get("full_max", 0))

    fig = go.Figure()

    fig.add_shape(
        type="rect",
        x0=fmin, x1=fmax, y0=0.36, y1=0.64,
        line=dict(width=0),
        fillcolor="rgba(160,170,180,0.18)"
    )

    fig.add_shape(
        type="rect",
        x0=rmin, x1=rmax, y0=0.28, y1=0.72,
        line=dict(width=0),
        fillcolor="rgba(30,215,96,0.85)"
    )

    fig.add_trace(go.Scatter(
        x=[avg],
        y=[0.5],
        mode="markers+text",
        marker=dict(size=16, color="rgba(255,90,90,1)"),
        text=[f"Avg {avg:.1f}m"],
        textposition="top center",
        textfont=dict(color="white", size=13),
        showlegend=False
    ))

    fig.add_annotation(x=fmin, y=0.12, text=f"{fmin:.0f}m", showarrow=False, font=dict(color="white", size=12))
    fig.add_annotation(x=fmax, y=0.12, text=f"{fmax:.0f}m", showarrow=False, font=dict(color="white", size=12))
    fig.add_annotation(
        x=(rmin + rmax) / 2,
        y=0.88,
        text=f"Reliable {rmin:.1f}–{rmax:.1f}m",
        showarrow=False,
        font=dict(color="#dff7ea", size=13)
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#142c34",
        plot_bgcolor="#142c34",
        xaxis=dict(range=[fmin - 5, fmax + 5], visible=False),
        yaxis=dict(range=[0, 1], visible=False)
    )

    return fig


def render_distance_profile(data):
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
    with c2:
        st.metric("Avg Carry", f'{distance_info.get("avg_carry", 0)} m')
    with c3:
        st.metric("Confidence", distance_info.get("confidence", "-"))

    render_v4_distance_profile(distance_info)

    st.write("**Recommendation**")
    st.write(distance_info.get("recommendation", "-"))


def render_session_summary(data):
    comparison = compare_latest_sessions()

    strike_value = data.get("strike_quality", 0)
    blueprint_value = data.get("blueprint_match_pct", 0)
    dispersion_value = data.get("start_line_control", 0)

    strike_delta = comparison.get("performance_delta", 0) if comparison.get("has_comparison", False) else 0
    blueprint_delta = comparison.get("blueprint_delta", 0) if comparison.get("has_comparison", False) else 0
    dispersion_delta = comparison.get("corridor_delta", 0) if comparison.get("has_comparison", False) else 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Strike Quality", strike_value, strike_delta)

    with c2:
        st.metric("Blueprint Match", f"{blueprint_value}%", blueprint_delta)

    with c3:
        st.metric("Dispersion Control", dispersion_value, dispersion_delta)




def render_progress_chart():
    trend = build_trend_data()

    if not trend.get("has_history", False):
        st.info("Trend history will appear after multiple sessions.")
        return

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["dates"],
        y=trend["performance"],
        mode="lines+markers",
        name="Performance",
        line=dict(color="#1ed760", width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=trend["dates"],
        y=trend["dispersion"],
        mode="lines+markers",
        name="Dispersion",
        line=dict(color="#ff8c42", width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2"),
        legend=dict(orientation="h", y=1.05, x=0)
    )

    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")

    st.plotly_chart(fig, use_container_width=True)

def render_v4_dashboard_shell():
    st.markdown(get_v4_css(), unsafe_allow_html=True)
    st.markdown('<div class="v4-shell">', unsafe_allow_html=True)
    st.markdown('<div class="v4-title">GOLF AI COMMAND CENTRE</div>', unsafe_allow_html=True)

    if "latest_upload_bytes" not in st.session_state:
        st.session_state["latest_upload_bytes"] = None
    if "latest_upload_name" not in st.session_state:
        st.session_state["latest_upload_name"] = None

    uploaded_file = st.file_uploader(
        "Upload CSV / Select Session",
        type=["csv"],
        key="v4_dashboard_upload"
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
    else:
        sessions = list_sessions()
        if sessions:
            selected = st.selectbox("Select Session", sessions, index=len(sessions) - 1)
            data = run_golfai_analysis(session_file=selected)
        else:
            st.info("Upload an MLM2PRO CSV to begin analysis.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        card_open("Performance Score")
        gauge = build_v4_gauge(data.get("performance_score", 0))
        st.plotly_chart(gauge, use_container_width=True)
        card_close()

    with row1_col2:
        card_open("Carry Distance Profile")
        render_distance_profile(data)
        card_close()

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        card_open("Shot Dispersion")
        fig = build_v4_dispersion_figure(data)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No shot pattern data available.")
        card_close()

    with row2_col2:
        card_open("Session Summary")
        render_session_summary(data)
        card_close()

    row3_col1, row3_col2 = st.columns([1.1, 1.0])
    with row3_col1:
        card_open("Progress Over Time")
        render_progress_chart()
        card_close()

    with row3_col2:
        card_open("Practice Focus")
        st.write("V4 placeholder")
        card_close()

    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import plotly.graph_objects as go
from io import BytesIO

from golfai.v4_styles import get_v4_css
from golfai.v4_cards import card_open, card_close
from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis
from golfai.distance_engine import build_distance_intelligence
from golfai.v4_charts import build_v4_distance_chart


def build_v4_gauge(score: float):
    score = max(0, min(100, float(score)))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 42, "color": "#f5f7fa"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#cfd8dc"},
            "bar": {"color": "rgba(0,0,0,0)"},
            "bgcolor": "#0f1f26",
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

    st.caption(
        f'Reliable {distance_info.get("reliable_min", 0)}–{distance_info.get("reliable_max", 0)} m'
        f'   |   Full {distance_info.get("full_min", 0)}–{distance_info.get("full_max", 0)} m'
    )

    fig = build_v4_distance_chart(distance_info)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

    st.write("**Recommendation**")
    st.write(distance_info.get("recommendation", "-"))


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
        st.write("V4 placeholder")
        card_close()

    with row2_col2:
        card_open("Session Summary")
        st.write("V4 placeholder")
        card_close()

    row3_col1, row3_col2 = st.columns([1.1, 1.0])
    with row3_col1:
        card_open("Progress Over Time")
        st.write("V4 placeholder")
        card_close()

    with row3_col2:
        card_open("Practice Focus")
        st.write("V4 placeholder")
        card_close()

    st.markdown('</div>', unsafe_allow_html=True)

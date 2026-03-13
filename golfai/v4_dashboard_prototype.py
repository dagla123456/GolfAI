import streamlit as st
import plotly.graph_objects as go
from golfai.v4_styles import get_v4_css
from golfai.v4_cards import card_open, card_close


def build_mock_gauge():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=78,
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
                "value": 78
            }
        }
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#142c34",
        font={"color": "#e8f0f2"}
    )
    return fig


def build_mock_distance():
    fig = go.Figure()
    fig.add_shape(type="rect", x0=72, x1=132, y0=0.38, y1=0.62, line=dict(width=0), fillcolor="rgba(160,170,180,0.18)")
    fig.add_shape(type="rect", x0=95, x1=113, y0=0.28, y1=0.72, line=dict(width=0), fillcolor="rgba(30,215,96,0.88)")
    fig.add_trace(go.Scatter(
        x=[102.5], y=[0.5],
        mode="markers+text",
        marker=dict(size=16, color="rgba(255,90,90,1)"),
        text=["Avg 102.5m"],
        textposition="top center",
        textfont=dict(color="white", size=13),
        showlegend=False
    ))
    fig.add_annotation(x=72, y=0.1, text="72m", showarrow=False, font=dict(color="white", size=12))
    fig.add_annotation(x=132, y=0.1, text="132m", showarrow=False, font=dict(color="white", size=12))
    fig.add_annotation(x=104, y=0.88, text="Reliable 95–113m", showarrow=False, font=dict(color="#dff7ea", size=13))
    fig.update_layout(
        height=190,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#142c34",
        plot_bgcolor="#142c34",
        xaxis=dict(range=[65, 138], visible=False),
        yaxis=dict(range=[0, 1], visible=False)
    )
    return fig


def build_mock_dispersion():
    fig = go.Figure()

    fig.add_vrect(x0=-5, x1=5, fillcolor="rgba(30,215,96,0.16)", line_width=0, layer="below")
    fig.add_vline(x=0, line_width=2.2, line_dash="dash", line_color="rgba(255,255,255,0.45)")

    ex = [-8,-4,0,4,8,7,3,-1,-5,-7,-5,-1,3,6,4,0,-3,-6,-8]
    ey = [116,121,124,121,116,110,105,103,105,110,116,121,124,121,116,112,110,112,116]
    fig.add_trace(go.Scatter(
        x=ex, y=ey, mode="lines",
        line=dict(color="rgba(255,255,255,0.82)", width=2.6),
        fill="toself", fillcolor="rgba(30,215,96,0.12)",
        hoverinfo="skip", showlegend=False
    ))

    shots_x = [-2.8,-1.5,-0.3,0.8,2.1,-1.2,0.5,1.6,-0.8,2.8,-2.2,0.2]
    shots_y = [104,108,111,109,105,114,116,113,118,107,110,112]
    fig.add_trace(go.Scatter(
        x=shots_x, y=shots_y, mode="markers",
        marker=dict(size=10, color="rgba(230,255,200,0.9)", line=dict(width=1, color="rgba(0,0,0,0.25)")),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(x=[0.4], y=[110.5], mode="markers",
        marker=dict(size=28, color="rgba(255,70,70,0.18)"), showlegend=False))
    fig.add_trace(go.Scatter(x=[0.4], y=[110.5], mode="markers",
        marker=dict(size=16, color="rgba(255,70,70,1)", symbol="diamond",
                    line=dict(width=1.2, color="rgba(255,255,255,0.55)")),
        showlegend=False))

    fig.update_layout(
        height=320,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2")
    )
    fig.update_xaxes(title="Side Carry (m)", range=[-12, 12], gridcolor="rgba(255,255,255,0.07)", zeroline=False)
    fig.update_yaxes(title="Carry Distance (m)", range=[98, 122], gridcolor="rgba(255,255,255,0.07)", zeroline=False)
    return fig


def build_mock_progress():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=["S1","S2","S3","S4","S5"], y=[52,58,61,69,78],
        mode="lines+markers", name="Performance",
        line=dict(color="#1ed760", width=3), marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=["S1","S2","S3","S4","S5"], y=[36,40,44,47,53],
        mode="lines+markers", name="Consistency",
        line=dict(color="#ff8c42", width=3), marker=dict(size=8)
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2"),
        legend=dict(orientation="h", y=1.05, x=0)
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


def render_summary_tiles():
    cols = st.columns(3)
    cards = [
        ("Strike Quality", "65", "▲ +6", "#1ed760"),
        ("Blueprint Match", "52%", "▲ +7", "#1ed760"),
        ("Dispersion Control", "29", "▼ -4", "#ff6b6b"),
    ]
    for col, (label, value, delta, color) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 16px;
                padding: 14px 12px;
                min-height: 118px;
            ">
                <div style="color:#c7d4da; font-size:13px; margin-bottom:10px;">{label}</div>
                <div style="color:#f4f7fa; font-size:32px; font-weight:800; line-height:1;">{value}</div>
                <div style="margin-top:10px; color:{color}; font-weight:700; font-size:14px;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)


def render_practice_focus():
    st.markdown("**Primary Issue**")
    st.write("Club Path")
    st.markdown("**Secondary Issue**")
    st.write("Start Line")
    st.markdown("**Recommended Focus**")
    st.write("• Neutral forearm setup")
    st.write("• Pause at the top")
    st.write("• Arms fall before chest rotates")
    st.markdown("**Practice Plan**")
    st.write("Session Goal: Stabilise strike and low point")
    st.write("Recommended Drill: Pause Transition Drill")


def render_v4_dashboard_prototype():
    st.markdown(get_v4_css(), unsafe_allow_html=True)
    st.markdown('<div class="v4-shell">', unsafe_allow_html=True)

    components_html = """
    <div style="
        background: linear-gradient(135deg,#183a2d,#1f4a35);
        padding:14px 18px;
        border-radius:18px;
        margin-bottom:10px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        box-shadow:0 10px 24px rgba(0,0,0,0.28);
        color:white;
        font-family:Arial, sans-serif;
    ">
        <div>
            <div style="font-size:22px;font-weight:800;color:white;margin-bottom:6px;letter-spacing:0.02em;">
                GolfAI Command Centre
            </div>
            <div style="color:#d8eee4;font-size:14px;margin-bottom:2px;">
                Session: mlm2pro_shotexport_011826.csv
            </div>
            <div style="color:#d8eee4;font-size:14px;">
                Shots Analysed: 53
            </div>
        </div>
        <div style="
            font-size:14px;
            color:#e7fff2;
            background:rgba(255,255,255,0.10);
            padding:10px 16px;
            border-radius:10px;
            font-weight:600;
        ">
            AI Practice Intelligence
        </div>
    </div>
    """
    import streamlit.components.v1 as components
    components.html(components_html, height=110)

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        card_open("Performance Score")
        st.plotly_chart(build_mock_gauge(), use_container_width=True)
        card_close()
    with row1_col2:
        card_open("Carry Distance Profile")
        st.plotly_chart(build_mock_distance(), use_container_width=True)
        st.write("**Recommendation**")
        st.write("Use this club confidently for 95–113 m.")
        card_close()

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        card_open("Shot Dispersion")
        st.plotly_chart(build_mock_dispersion(), use_container_width=True)
        card_close()
    with row2_col2:
        card_open("Session Summary")
        render_summary_tiles()
        card_close()

    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        card_open("Progress Over Time")
        st.plotly_chart(build_mock_progress(), use_container_width=True)
        card_close()
    with row3_col2:
        card_open("Practice Focus")
        render_practice_focus()
        card_close()

    st.markdown("</div>", unsafe_allow_html=True)

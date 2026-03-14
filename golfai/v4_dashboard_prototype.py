import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components
from golfai.v4_styles import get_v4_css
from golfai.v4_cards import card_open, card_close


def build_mock_gauge():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=78,
        number={"font": {"size": 28, "color": "#f5f7fa"}},
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
                "line": {"color": "#f5f7fa", "width": 3},
                "thickness": 0.8,
                "value": 78
            }
        }
    ))
    fig.update_layout(
        height=145,
        margin=dict(l=4, r=4, t=4, b=4),
        paper_bgcolor="#142c34",
        font={"color": "#e8f0f2"}
    )
    return fig


def build_mock_distance():
    fig = go.Figure()
    fig.add_shape(type="rect", x0=72, x1=132, y0=0.40, y1=0.60, line=dict(width=0), fillcolor="rgba(160,170,180,0.18)")
    fig.add_shape(type="rect", x0=95, x1=113, y0=0.32, y1=0.68, line=dict(width=0), fillcolor="rgba(30,215,96,0.88)")
    fig.add_trace(go.Scatter(
        x=[102.5], y=[0.5],
        mode="markers+text",
        marker=dict(size=10, color="rgba(255,90,90,1)"),
        text=["Avg 102.5m"],
        textposition="top center",
        textfont=dict(color="white", size=10),
        showlegend=False
    ))
    fig.add_annotation(x=72, y=0.10, text="72m", showarrow=False, font=dict(color="white", size=9))
    fig.add_annotation(x=132, y=0.10, text="132m", showarrow=False, font=dict(color="white", size=9))
    fig.add_annotation(x=104, y=0.84, text="Reliable 95–113m", showarrow=False, font=dict(color="#dff7ea", size=10))
    fig.update_layout(
        height=120,
        margin=dict(l=4, r=4, t=4, b=4),
        paper_bgcolor="#142c34",
        plot_bgcolor="#142c34",
        xaxis=dict(range=[65, 138], visible=False),
        yaxis=dict(range=[0, 1], visible=False)
    )
    return fig


def build_mock_dispersion():
    fig = go.Figure()

    fig.add_hrect(y0=98, y1=122, fillcolor="rgba(255,255,255,0.015)", line_width=0, layer="below")
    fig.add_vrect(x0=-5, x1=5, fillcolor="rgba(110,200,120,0.18)", line_width=0, layer="below")
    fig.add_vline(x=0, line_width=2.0, line_dash="dash", line_color="rgba(255,255,255,0.55)")
    fig.add_hline(y=110.5, line_width=1.4, line_color="rgba(255,255,255,0.35)")

    ex1 = [-8,-4,0,4,8,7,3,-1,-5,-7,-5,-1,3,6,4,0,-3,-6,-8]
    ey1 = [116,121,124,121,116,110,105,103,105,110,116,121,124,121,116,112,110,112,116]
    fig.add_trace(go.Scatter(
        x=ex1, y=ey1, mode="lines",
        line=dict(color="rgba(255,255,255,0.82)", width=2.2),
        fill="toself", fillcolor="rgba(130,210,100,0.14)",
        hoverinfo="skip", showlegend=False
    ))

    ex2 = [-5,-2,0,2,5,4,2,-1,-3,-4,-3,-1,2,4,3,0,-2,-4,-5]
    ey2 = [113,116,118,116,113,110,108,107,108,110,113,116,118,116,113,111,110,111,113]
    fig.add_trace(go.Scatter(
        x=ex2, y=ey2, mode="lines",
        line=dict(color="rgba(120,255,150,0.28)", width=1.1),
        fill="toself", fillcolor="rgba(120,255,150,0.10)",
        hoverinfo="skip", showlegend=False
    ))

    shots_x = [-2.8,-1.5,-0.3,0.8,2.1,-1.2,0.5,1.6,-0.8,2.8,-2.2,0.2,1.2,-1.9,2.4]
    shots_y = [104,108,111,109,105,114,116,113,118,107,110,112,109,111,114]
    fig.add_trace(go.Scatter(
        x=shots_x, y=shots_y, mode="markers",
        marker=dict(
            size=7,
            color="rgba(240,245,210,0.96)",
            line=dict(width=0.8, color="rgba(30,30,30,0.35)")
        ),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[0.4], y=[110.5], mode="markers",
        marker=dict(size=20, color="rgba(255,70,70,0.18)"),
        hoverinfo="skip", showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[0.4], y=[110.5], mode="markers",
        marker=dict(
            size=11,
            color="rgba(255,70,70,1)",
            symbol="diamond",
            line=dict(width=1.0, color="rgba(255,255,255,0.55)")
        ),
        showlegend=False
    ))

    fig.update_layout(
        height=155,
        margin=dict(l=4, r=4, t=4, b=4),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2")
    )
    fig.update_xaxes(
        title="Side Carry (m)",
        range=[-12, 12],
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10)
    )
    fig.update_yaxes(
        title="Carry Distance (m)",
        range=[98, 122],
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10)
    )
    return fig


def build_mock_progress():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=["S1","S2","S3","S4","S5"], y=[52,58,61,69,78],
        mode="lines+markers", name="Performance",
        line=dict(color="#1ed760", width=2.5), marker=dict(size=5)
    ))
    fig.add_trace(go.Scatter(
        x=["S1","S2","S3","S4","S5"], y=[36,40,44,47,53],
        mode="lines+markers", name="Consistency",
        line=dict(color="#ff8c42", width=2.5), marker=dict(size=5)
    ))
    fig.update_layout(
        height=120,
        margin=dict(l=4, r=4, t=4, b=4),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2"),
        legend=dict(orientation="h", y=1.02, x=0, font=dict(size=8))
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9))
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9))
    return fig


def render_summary_tiles():
    cols = st.columns(3)
    cards = [
        ("Strike", "65", "▲ +6", "#1ed760"),
        ("Blueprint", "52%", "▲ +7", "#1ed760"),
        ("Dispersion", "29", "▼ -4", "#ff6b6b"),
    ]
    for col, (label, value, delta, color) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 6px 6px;
                min-height: 62px;
            ">
                <div style="color:#c7d4da; font-size:10px; margin-bottom:4px;">{label}</div>
                <div style="color:#f4f7fa; font-size:18px; font-weight:800; line-height:1;">{value}</div>
                <div style="margin-top:4px; color:{color}; font-weight:700; font-size:11px;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        margin-top:6px;
        color:#d5e0e6;
        font-size:11px;
        line-height:1.25;
    ">
        Contact improving. Dispersion still slightly left-biased.
    </div>
    """, unsafe_allow_html=True)


def render_practice_focus():
    st.markdown("""
    <div style="font-size:11px; line-height:1.25; color:#eaf2f5;">
        <div style="font-weight:800; margin-bottom:4px;">Recommended Focus</div>
        <div>• Neutral forearm setup</div>
        <div>• Pause at the top</div>
        <div>• Arms fall before chest rotates</div>
        <div style="font-weight:800; margin-top:8px; margin-bottom:4px;">Practice Plan</div>
        <div><b>Goal:</b> Stabilise strike and low point</div>
        <div><b>Drill:</b> Pause Transition Drill</div>
    </div>
    """, unsafe_allow_html=True)


def render_v4_dashboard_prototype():
    st.markdown(get_v4_css(), unsafe_allow_html=True)
    st.markdown('<div class="v4-shell">', unsafe_allow_html=True)

    header_html = """
    <div style="
        background: linear-gradient(135deg,#183a2d,#1f4a35);
        padding:8px 12px;
        border-radius:14px;
        margin-bottom:6px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        box-shadow:0 8px 18px rgba(0,0,0,0.24);
        color:white;
        font-family:Arial, sans-serif;
    ">
        <div>
            <div style="font-size:16px;font-weight:800;color:white;margin-bottom:3px;letter-spacing:0.02em;">
                GolfAI Command Centre
            </div>
            <div style="color:#d8eee4;font-size:11px;margin-bottom:1px;">
                Session: mlm2pro_shotexport_011826.csv
            </div>
            <div style="color:#d8eee4;font-size:11px;">
                Shots Analysed: 53
            </div>
        </div>
        <div style="
            font-size:11px;
            color:#e7fff2;
            background:rgba(255,255,255,0.10);
            padding:6px 9px;
            border-radius:9px;
            font-weight:600;
        ">
            AI Practice Intelligence
        </div>
    </div>
    """
    components.html(header_html, height=68)

    top_left, top_right = st.columns(2)
    with top_left:
        card_open("Performance Score")
        st.plotly_chart(build_mock_gauge(), use_container_width=True, config={"displayModeBar": False})
        card_close()
    with top_right:
        card_open("Carry Distance Profile")
        st.plotly_chart(build_mock_distance(), use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div style="font-size:11px; color:#d7e5ea; margin-top:2px;">Reliable carry window: 95–113 m</div>', unsafe_allow_html=True)
        card_close()

    middle_left, middle_right = st.columns([1.05, 0.95])
    with middle_left:
        card_open("Shot Dispersion")
        st.plotly_chart(build_mock_dispersion(), use_container_width=True, config={"displayModeBar": False})
        card_close()
    with middle_right:
        card_open("Session Summary")
        render_summary_tiles()
        card_close()

    bottom_left, bottom_right = st.columns([1.05, 0.95])
    with bottom_left:
        card_open("Progress Over Time")
        st.plotly_chart(build_mock_progress(), use_container_width=True, config={"displayModeBar": False})
        card_close()
    with bottom_right:
        card_open("Practice Focus")
        render_practice_focus()
        card_close()

    st.markdown("</div>", unsafe_allow_html=True)

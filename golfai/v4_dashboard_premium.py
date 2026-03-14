import streamlit as st
import plotly.graph_objects as go
from golfai.scoring import build_session_score


def get_premium_css():
    return """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background:
            radial-gradient(circle at top left, rgba(35, 95, 70, 0.18), transparent 28%),
            linear-gradient(180deg, #050d12 0%, #0a171d 100%) !important;
        color: #eef3f7 !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(35, 95, 70, 0.18), transparent 28%),
            linear-gradient(180deg, #050d12 0%, #0a171d 100%) !important;
    }

    .block-container {
        padding-top: 0.35rem !important;
        padding-bottom: 0.15rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        max-width: 1450px !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.35rem !important;
    }

    .premium-shell {
        padding: 0.02rem 0.02rem 0.15rem 0.02rem;
    }

    .premium-header {
        background: linear-gradient(135deg, rgba(20,48,39,0.96), rgba(17,38,31,0.96));
        border: 1px solid rgba(120, 190, 155, 0.18);
        border-radius: 20px;
        padding: 12px 16px;
        margin-bottom: 8px;
        box-shadow:
            0 12px 24px rgba(0,0,0,0.24),
            inset 0 0 0 1px rgba(255,255,255,0.02);
    }

    .premium-card {
        background:
            linear-gradient(180deg, rgba(20,34,42,0.98), rgba(10,20,26,0.99));
        border: 1px solid rgba(130, 188, 164, 0.13);
        border-radius: 20px;
        padding: 0.55rem 0.65rem 0.45rem 0.65rem;
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.015) inset,
            0 12px 24px rgba(0,0,0,0.26),
            0 0 22px rgba(60,160,120,0.03);
        margin-bottom: 0.32rem;
    }

    .premium-card-title {
        font-size: 0.75rem;
        font-weight: 800;
        color: #f2f7fa;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        padding-bottom: 0.18rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    .js-plotly-plot, .plot-container {
        height: 100% !important;
    }
    </style>
    """


def premium_card_open(title):
    st.markdown(
        f"""
        <div class="premium-card">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:4px;
            ">
                <div class="premium-card-title">{title}</div>
                <div style="
                    width:6px;
                    height:6px;
                    border-radius:50%;
                    background:#1ed760;
                    box-shadow:0 0 8px rgba(30,215,96,0.55);
                "></div>
            </div>
        """,
        unsafe_allow_html=True,
    )


def premium_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def get_performance_context(detector_results=None):
    if detector_results:
        score_data = build_session_score(detector_results)
        performance_score = score_data.get("performance_score", 78)
        primary_issue = score_data.get("primary_issue", "Strike Quality")
        secondary_issue = score_data.get("secondary_issue", "Start Line Control")
    else:
        performance_score = 78
        primary_issue = "Strike Quality"
        secondary_issue = "Sequencing"

    if performance_score >= 80:
        performance_label = "Excellent"
        trend_text = "▲ Strong Session"
        trend_color = "#1ed760"
    elif performance_score >= 65:
        performance_label = "Good"
        trend_text = "▲ Improving"
        trend_color = "#1ed760"
    elif performance_score >= 50:
        performance_label = "Developing"
        trend_text = "● Mixed Session"
        trend_color = "#ffd166"
    else:
        performance_label = "Needs Work"
        trend_text = "▼ Below Standard"
        trend_color = "#ff6b6b"

    return {
        "performance_score": performance_score,
        "performance_label": performance_label,
        "trend_text": trend_text,
        "trend_color": trend_color,
        "primary_issue": primary_issue,
        "secondary_issue": secondary_issue,
    }


def build_premium_gauge(score_value):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score_value,
            number={"font": {"size": 30, "color": "#f5f7fa"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#cfd8dc"},
                "bar": {"color": "rgba(0,0,0,0)"},
                "bgcolor": "#13252d",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 35], "color": "#ff4d4d"},
                    {"range": [35, 55], "color": "#ff8c42"},
                    {"range": [55, 72], "color": "#ffd166"},
                    {"range": [72, 100], "color": "#1ed760"},
                ],
                "threshold": {
                    "line": {"color": "#f5f7fa", "width": 4},
                    "thickness": 0.85,
                    "value": score_value,
                },
            },
        )
    )
    fig.update_layout(
        height=155,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="#13252d",
        font={"color": "#e8f0f2"},
    )
    return fig


def render_premium_distance_card():
    avg = 102.5
    reliable_min = 95
    reliable_max = 113
    full_min = 72
    full_max = 132
    spread = full_max - full_min

    avg_pos = (avg - full_min) / spread * 100
    reliable_left = (reliable_min - full_min) / spread * 100
    reliable_width = (reliable_max - reliable_min) / spread * 100

    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            margin-bottom:10px;
        ">
            <div>
                <div style="
                    font-size:32px;
                    font-weight:800;
                    color:#f5f7fa;
                    line-height:0.95;
                    margin-bottom:2px;
                ">
                    {avg:.1f}m
                </div>
                <div style="
                    font-size:11px;
                    color:#d7e5ea;
                    font-weight:700;
                    letter-spacing:0.06em;
                    text-transform:uppercase;
                ">
                    Average Carry
                </div>
            </div>

            <div style="text-align:right;">
                <div style="
                    font-size:11px;
                    color:#9fd9b4;
                    font-weight:700;
                    letter-spacing:0.05em;
                    text-transform:uppercase;
                    margin-bottom:2px;
                ">
                    Trust Window
                </div>
                <div style="
                    font-size:18px;
                    color:#f3fbf6;
                    font-weight:800;
                    line-height:1;
                ">
                    {reliable_min:.0f}–{reliable_max:.0f}m
                </div>
            </div>
        </div>

        <div style="
            position:relative;
            height:20px;
            border-radius:999px;
            background:linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
            border:1px solid rgba(255,255,255,0.06);
            overflow:visible;
            margin-top:6px;
            margin-bottom:12px;
        ">
            <div style="
                position:absolute;
                left:{reliable_left:.2f}%;
                width:{reliable_width:.2f}%;
                height:20px;
                top:0;
                border-radius:999px;
                background:linear-gradient(90deg, #169c4f, #1ed760);
                box-shadow:0 0 12px rgba(30,215,96,0.22);
            "></div>

            <div style="
                position:absolute;
                left:{avg_pos:.2f}%;
                top:50%;
                width:16px;
                height:16px;
                border-radius:50%;
                background:#ff5a5a;
                border:2px solid rgba(255,255,255,0.80);
                transform:translate(-50%, -50%);
                box-shadow:0 0 10px rgba(255,90,90,0.40);
            "></div>
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-top:4px;
        ">
            <div style="
                font-size:11px;
                color:#c7d4da;
                font-weight:700;
            ">
                {full_min:.0f}m
            </div>
            <div style="
                font-size:10px;
                color:#9fb8c2;
                font-weight:700;
                letter-spacing:0.08em;
                text-transform:uppercase;
            ">
                Full Range
            </div>
            <div style="
                font-size:11px;
                color:#c7d4da;
                font-weight:700;
            ">
                {full_max:.0f}m
            </div>
        </div>

        <div style="
            text-align:center;
            margin-top:8px;
            font-size:10px;
            color:#c7d4da;
            line-height:1.2;
        ">
            Reliable carry is clustering inside the green corridor
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_premium_dispersion():
    shots_x = [-2.8, -1.5, -0.3, 0.8, 2.1, -1.2, 0.5, 1.6, -0.8, 2.8, -2.2, 0.2, 1.2, -1.9, 2.4]
    shots_y = [104, 108, 111, 109, 105, 114, 116, 113, 118, 107, 110, 112, 109, 111, 114]

    latest_x = 0.4
    latest_y = 110.5

    trend_x = -0.6
    trend_y = 109.4

    ellipse_x = [-6.8, -3.8, -1.2, 1.8, 4.8, 5.8, 4.2, 1.5, -1.8, -4.8, -6.0, -5.4, -3.0, 0.0, 2.8, 4.8, 3.2, 0.4, -2.8, -5.8, -6.8]
    ellipse_y = [115.8, 119.2, 120.8, 120.3, 117.2, 112.0, 107.6, 105.2, 104.8, 106.0, 109.2, 113.4, 117.2, 118.8, 118.0, 115.2, 111.0, 108.2, 107.2, 110.0, 115.8]

    fig = go.Figure()

    fig.add_hrect(
        y0=98,
        y1=122,
        fillcolor="rgba(255,255,255,0.012)",
        line_width=0,
        layer="below",
    )

    fig.add_vrect(
        x0=-3.2,
        x1=3.2,
        fillcolor="rgba(42,199,121,0.12)",
        line_width=0,
        layer="below",
    )

    fig.add_vrect(
        x0=-5.5,
        x1=5.5,
        fillcolor="rgba(42,199,121,0.05)",
        line_width=0,
        layer="below",
    )

    fig.add_vline(
        x=0,
        line_width=2.2,
        line_dash="dash",
        line_color="rgba(255,255,255,0.54)",
    )

    fig.add_trace(
        go.Scatter(
            x=ellipse_x,
            y=ellipse_y,
            mode="lines",
            line=dict(color="rgba(0,0,0,0)", width=0),
            fill="toself",
            fillcolor="rgba(120,255,170,0.10)",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=shots_x,
            y=shots_y,
            mode="markers",
            marker=dict(
                size=18,
                color="rgba(130,255,190,0.11)",
                line=dict(width=0),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=shots_x,
            y=shots_y,
            mode="markers",
            marker=dict(
                size=8.5,
                color="rgba(242,255,246,0.99)",
                line=dict(width=0.9, color="rgba(80,120,100,0.35)"),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[trend_x],
            y=[trend_y],
            mode="markers",
            marker=dict(
                size=24,
                color="rgba(86,174,255,0.16)",
                line=dict(width=0),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[trend_x],
            y=[trend_y],
            mode="markers",
            marker=dict(
                size=11,
                color="rgba(82,166,255,1)",
                symbol="circle",
                line=dict(width=1.2, color="rgba(255,255,255,0.78)"),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[latest_x],
            y=[latest_y],
            mode="markers",
            marker=dict(
                size=28,
                color="rgba(255,79,79,0.15)",
                line=dict(width=0),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[latest_x],
            y=[latest_y],
            mode="markers",
            marker=dict(
                size=12,
                color="rgba(255,88,88,1)",
                symbol="diamond",
                line=dict(width=1.2, color="rgba(255,255,255,0.72)"),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_annotation(
        x=0,
        y=120.7,
        text="Target Line",
        showarrow=False,
        font=dict(color="#cfe0e6", size=10),
    )

    fig.add_annotation(
        x=trend_x,
        y=121.2,
        text="Last 5 Avg",
        showarrow=False,
        font=dict(color="#9fd1ff", size=10),
    )

    fig.add_annotation(
        x=latest_x + 1.4,
        y=119.9,
        text="Latest Avg",
        showarrow=False,
        font=dict(color="#ffb1b1", size=10),
    )

    fig.update_layout(
        height=162,
        margin=dict(l=4, r=4, t=8, b=4),
        paper_bgcolor="#13252d",
        plot_bgcolor="#0c1b22",
        font=dict(color="#e8f0f2"),
    )

    fig.update_xaxes(
        title="Side Carry (m)",
        range=[-12, 12],
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10),
        fixedrange=True,
    )

    fig.update_yaxes(
        title="Carry Distance (m)",
        range=[98, 122],
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10),
        fixedrange=True,
    )

    return fig


def render_v4_dashboard_premium(detector_results=None):
    performance = get_performance_context(detector_results)

    st.markdown(get_premium_css(), unsafe_allow_html=True)
    st.markdown('<div class="premium-shell">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="premium-header">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="
                        font-size:18px;
                        font-weight:800;
                        color:white;
                        line-height:1;
                        margin-bottom:4px;
                        letter-spacing:0.03em;
                    ">
                        GolfAI
                    </div>
                    <div style="
                        font-size:11px;
                        font-weight:700;
                        color:#d8eee4;
                        letter-spacing:0.10em;
                        text-transform:uppercase;
                        margin-bottom:4px;
                    ">
                        Command Centre
                    </div>
                    <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                        <div style="
                            background:rgba(255,255,255,0.08);
                            color:#e7fff2;
                            font-size:10px;
                            font-weight:700;
                            padding:4px 8px;
                            border-radius:999px;
                            border:1px solid rgba(255,255,255,0.06);
                        ">
                            7 Iron
                        </div>
                        <div style="color:#d8eee4; font-size:11px;">
                            53 shots
                        </div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="
                        font-size:10px;
                        color:#bfe7d3;
                        letter-spacing:0.10em;
                        text-transform:uppercase;
                        font-weight:700;
                        margin-bottom:3px;
                    ">
                        Active Session
                    </div>
                    <div style="
                        font-size:11px;
                        color:#f3fbf6;
                        font-weight:700;
                        line-height:1.15;
                    ">
                        mlm2pro_shotexport_011826.csv
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns(2)

    with top_left:
        premium_card_open("Performance Score")
        st.plotly_chart(
            build_premium_gauge(performance["performance_score"]),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown(
            f"""
            <div style="
                text-align:center;
                margin-top:4px;
                font-size:12px;
                font-weight:700;
                color:{performance["trend_color"]};
                letter-spacing:0.02em;
                line-height:1.1;
            ">
                {performance["trend_text"]} · {performance["performance_label"]}
            </div>
            <div style="
                text-align:center;
                margin-top:4px;
                font-size:10px;
                color:#c7d4da;
                line-height:1.2;
            ">
                Priority: {performance["primary_issue"]} | Next: {performance["secondary_issue"]}
            </div>
            """,
            unsafe_allow_html=True,
        )
        premium_card_close()

    with top_right:
        premium_card_open("Carry Distance Profile")
        render_premium_distance_card()
        premium_card_close()

    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)

    full_width = st.columns([1])[0]
    with full_width:
        premium_card_open("Shot Dispersion")

        st.markdown(
            """
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                margin-bottom:4px;
            ">
                <div>
                    <div style="
                        font-size:12px;
                        color:#9fd9b4;
                        font-weight:700;
                        letter-spacing:0.04em;
                        text-transform:uppercase;
                        margin-bottom:2px;
                    ">
                        Bias
                    </div>
                    <div style="
                        font-size:18px;
                        color:#f5f7fa;
                        font-weight:800;
                        line-height:1;
                    ">
                        Slight Left
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="
                        font-size:12px;
                        color:#c7d4da;
                        font-weight:700;
                        letter-spacing:0.04em;
                        text-transform:uppercase;
                        margin-bottom:2px;
                    ">
                        Width
                    </div>
                    <div style="
                        font-size:18px;
                        color:#f5f7fa;
                        font-weight:800;
                        line-height:1;
                    ">
                        8.4m
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            build_premium_dispersion(),
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown(
            """
            <div style="
                text-align:center;
                margin-top:3px;
                font-size:10px;
                color:#c7d4da;
                line-height:1.2;
            ">
                Red = latest session average · Blue = last 5 sessions average
            </div>
            <div style="
                text-align:center;
                margin-top:2px;
                font-size:10px;
                color:#c7d4da;
                line-height:1.2;
            ">
                Today is moving 1.0m closer to centre than recent trend
            </div>
            """,
            unsafe_allow_html=True,
        )

        premium_card_close()

    st.markdown("</div>", unsafe_allow_html=True)

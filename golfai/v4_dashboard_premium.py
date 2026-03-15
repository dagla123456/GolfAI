import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from golfai.scoring import build_session_score
from golfai.session_history import load_history


def get_premium_css():
    return """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background:
            radial-gradient(circle at top left, rgba(35, 95, 70, 0.16), transparent 28%),
            linear-gradient(180deg, #050d12 0%, #0a171d 100%) !important;
        color: #eef3f7 !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(35, 95, 70, 0.16), transparent 28%),
            linear-gradient(180deg, #050d12 0%, #0a171d 100%) !important;
    }

    .block-container {
        padding-top: 0.20rem !important;
        padding-bottom: 0.03rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        max-width: 1450px !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.16rem !important;
    }

    .premium-card {
        background:
            linear-gradient(180deg, rgba(20,34,42,0.98), rgba(10,20,26,0.99));
        border: 1px solid rgba(130, 188, 164, 0.12);
        border-radius: 18px;
        padding: 0.42rem 0.52rem 0.32rem 0.52rem;
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.015) inset,
            0 10px 22px rgba(0,0,0,0.24),
            0 0 18px rgba(60,160,120,0.025);
        margin-bottom: 0.14rem;
    }

    .premium-card-title {
        font-size: 0.70rem;
        font-weight: 800;
        color: #f2f7fa;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.14rem;
        padding-bottom: 0.10rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    .premium-header {
        background: linear-gradient(135deg, rgba(20,48,39,0.96), rgba(17,38,31,0.96));
        border: 1px solid rgba(120, 190, 155, 0.16);
        border-radius: 18px;
        padding: 10px 14px;
        margin-bottom: 5px;
        box-shadow:
            0 10px 22px rgba(0,0,0,0.22),
            inset 0 0 0 1px rgba(255,255,255,0.02);
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
                margin-bottom:3px;
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
    else:
        performance_score = 78
    return performance_score


def build_mini_gauge(score):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"font": {"size": 18, "color": "white"}},
            gauge={
                "axis": {"range": [0, 100], "visible": False},
                "bar": {"color": "rgba(0,0,0,0)"},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "#ff4d4d"},
                    {"range": [40, 65], "color": "#ffd166"},
                    {"range": [65, 100], "color": "#1ed760"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 3},
                    "thickness": 0.85,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        height=70,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
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

    html = f"""
    <div style="color:#eef3f7;font-family:Arial,sans-serif;padding-top:1px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
            <div>
                <div style="font-size:28px;font-weight:800;color:#f5f7fa;line-height:0.95;margin-bottom:2px;">
                    {avg:.1f}m
                </div>
                <div style="font-size:10px;color:#d7e5ea;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">
                    Average Carry
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:10px;color:#9fd9b4;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:2px;">
                    Trust Window
                </div>
                <div style="font-size:16px;color:#f3fbf6;font-weight:800;line-height:1;">
                    {reliable_min:.0f}–{reliable_max:.0f}m
                </div>
            </div>
        </div>

        <div style="position:relative;height:18px;border-radius:999px;background:linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));border:1px solid rgba(255,255,255,0.06);overflow:visible;margin-top:4px;margin-bottom:10px;">
            <div style="position:absolute;left:{reliable_left:.2f}%;width:{reliable_width:.2f}%;height:18px;top:0;border-radius:999px;background:linear-gradient(90deg, #169c4f, #1ed760);box-shadow:0 0 12px rgba(30,215,96,0.22);"></div>
            <div style="position:absolute;left:{avg_pos:.2f}%;top:50%;width:14px;height:14px;border-radius:50%;background:#ff5a5a;border:2px solid rgba(255,255,255,0.80);transform:translate(-50%, -50%);box-shadow:0 0 10px rgba(255,90,90,0.40);"></div>
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:2px;">
            <div style="font-size:10px;color:#c7d4da;font-weight:700;">{full_min:.0f}m</div>
            <div style="font-size:9px;color:#9fb8c2;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;">Full Range</div>
            <div style="font-size:10px;color:#c7d4da;font-weight:700;">{full_max:.0f}m</div>
        </div>

        <div style="text-align:center;margin-top:7px;font-size:9px;color:#c7d4da;line-height:1.2;">
            Reliable carry is clustering inside the green corridor
        </div>
    </div>
    """
    components.html(html, height=132)


def render_premium_summary_card(session_summary):
    strike_quality = session_summary.get("strike_quality", 0)
    blueprint_match = session_summary.get("blueprint_match_pct", 0)
    corridor_pct = session_summary.get("corridor_pct", 0)
    performance_score = session_summary.get("performance_score", 0)
    primary_issue = session_summary.get("primary_issue", "Unknown")

    html = f"""
    <div style="color:#eef3f7;font-family:Arial,sans-serif;padding-top:1px;">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
            <div style="background:linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:8px 8px 7px 8px;">
                <div style="font-size:9px;color:#c7d4da;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Strike Quality</div>
                <div style="font-size:22px;color:#f5f7fa;font-weight:800;line-height:1;margin-bottom:4px;">{strike_quality}</div>
                <div style="font-size:10px;color:#ffd166;font-weight:700;">Live</div>
            </div>

            <div style="background:linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:8px 8px 7px 8px;">
                <div style="font-size:9px;color:#c7d4da;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Blueprint</div>
                <div style="font-size:22px;color:#f5f7fa;font-weight:800;line-height:1;margin-bottom:4px;">{blueprint_match:.1f}%</div>
                <div style="font-size:10px;color:#ffd166;font-weight:700;">Live</div>
            </div>

            <div style="background:linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:8px 8px 7px 8px;">
                <div style="font-size:9px;color:#c7d4da;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Dispersion</div>
                <div style="font-size:22px;color:#f5f7fa;font-weight:800;line-height:1;margin-bottom:4px;">{corridor_pct:.1f}%</div>
                <div style="font-size:10px;color:#ffd166;font-weight:700;">Corridor</div>
            </div>

            <div style="background:linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:8px 8px 7px 8px;">
                <div style="font-size:9px;color:#c7d4da;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Performance</div>
                <div style="font-size:22px;color:#f5f7fa;font-weight:800;line-height:1;margin-bottom:4px;">{performance_score}</div>
                <div style="font-size:10px;color:#ffd166;font-weight:700;">Score</div>
            </div>
        </div>

        <div style="background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:8px 9px;">
            <div style="font-size:9px;color:#9fd9b4;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:3px;">Session Read</div>
            <div style="font-size:11px;color:#f3fbf6;font-weight:700;line-height:1.2;">
                Primary issue: {primary_issue}
            </div>
        </div>
    </div>
    """
    components.html(html, height=235)

def render_premium_focus_card():
    html = """
    <div style="color:#eef3f7;font-family:Arial,sans-serif;padding-top:1px;">
        <div style="background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:8px 10px;margin-bottom:8px;">
            <div style="font-size:9px;color:#9fd9b4;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Recommended Focus</div>
            <div style="font-size:11px;color:#f3fbf6;font-weight:700;line-height:1.32;">
                • Neutral forearm setup<br>
                • Pause at the top<br>
                • Arms fall before chest rotates
            </div>
        </div>

        <div style="background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:8px 10px;margin-bottom:8px;">
            <div style="font-size:9px;color:#9fd9b4;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Practice Goal</div>
            <div style="font-size:11px;color:#f3fbf6;font-weight:700;line-height:1.28;">
                Stabilise strike and low point control
            </div>
        </div>

        <div style="background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:8px 10px;">
            <div style="font-size:9px;color:#9fd9b4;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Primary Drill</div>
            <div style="font-size:11px;color:#f3fbf6;font-weight:700;line-height:1.28;">
                Pause Transition Drill
            </div>
        </div>
    </div>
    """
    components.html(html, height=220)


def build_progress_chart():

    history = load_history()

    if len(history) < 2:
        return go.Figure()

    sessions = list(range(1, len(history) + 1))

    strike_quality = [h.get("strike_quality", 0) for h in history]
    blueprint_match = [h.get("blueprint_match_pct", 0) for h in history]
    dispersion_control = [h.get("corridor_pct", 0) for h in history]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=sessions,
        y=strike_quality,
        mode="lines+markers",
        name="Strike Quality",
        line=dict(color="#1ed760", width=3),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=sessions,
        y=blueprint_match,
        mode="lines+markers",
        name="Blueprint Match",
        line=dict(color="#56a6ff", width=3),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=sessions,
        y=dispersion_control,
        mode="lines+markers",
        name="Dispersion Corridor",
        line=dict(color="#ff8c42", width=3),
        marker=dict(size=7)
    ))

    fig.update_layout(
        height=230,
        margin=dict(l=4, r=4, t=40, b=4),
        paper_bgcolor="#13252d",
        plot_bgcolor="#0b1920",
        font=dict(color="#e8f0f2"),
        legend=dict(
            orientation="h",
            y=1.14,
            yanchor="bottom",
            x=0.0,
            xanchor="left",
            font=dict(size=9),
            bgcolor="rgba(0,0,0,0)"
        ),
    )

    fig.update_xaxes(
        title="Session",
        gridcolor="rgba(255,255,255,0.04)",
        tickfont=dict(size=9),
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.05)",
        tickfont=dict(size=9),
    )

    return fig


def build_premium_dispersion(detector_results=None):
    if detector_results and "shot_pattern_data" in detector_results:
        shot_data = detector_results["shot_pattern_data"]
        points = shot_data.get("shot_pattern_points", [])

        shots_x = [p[0] for p in points]
        shots_y = [p[1] for p in points]
    else:
        shots_x = []
        shots_y = []

    # Latest session centroid
    if shots_x and shots_y:
        latest_x = sum(shots_x) / len(shots_x)
        latest_y = sum(shots_y) / len(shots_y)
    else:
        latest_x = 0
        latest_y = 110

    # Last 5 sessions centroid (trend)
    from golfai.session_history import load_history

    history = load_history()

    trend_x = latest_x
    trend_y = latest_y

    if len(history) >= 5:
        last5 = history[-5:]

        xs = []
        ys = []

        for s in last5:
            info = s.get("shot_pattern_data", {})
            points = info.get("shot_pattern_points", [])

            for p in points:
                xs.append(p[0])
                ys.append(p[1])

        if xs and ys:
            trend_x = sum(xs) / len(xs)
            trend_y = sum(ys) / len(ys)

    ellipse_x = [-6.8, -3.8, -1.2, 1.8, 4.8, 5.8, 4.2, 1.5, -1.8, -4.8, -6.0, -5.4, -3.0, 0.0, 2.8, 4.8, 3.2, 0.4, -2.8, -5.8, -6.8]
    ellipse_y = [115.8, 119.2, 120.8, 120.3, 117.2, 112.0, 107.6, 105.2, 104.8, 106.0, 109.2, 113.4, 117.2, 118.8, 118.0, 115.2, 111.0, 108.2, 107.2, 110.0, 115.8]
    
    fig = go.Figure()

    fig.add_hrect(y0=98, y1=122, fillcolor="rgba(255,255,255,0.010)", line_width=0, layer="below")
    fig.add_hrect(y0=105, y1=115.5, fillcolor="rgba(255,255,255,0.018)", line_width=0, layer="below")
    fig.add_vrect(x0=-2.8, x1=2.8, fillcolor="rgba(42,199,121,0.14)", line_width=0, layer="below")
    fig.add_vrect(x0=-5.2, x1=5.2, fillcolor="rgba(42,199,121,0.05)", line_width=0, layer="below")

    for x in [-8, -4, 4, 8]:
        fig.add_vline(x=x, line_width=0.8, line_color="rgba(255,255,255,0.04)")
    for y in [102, 106, 110, 114, 118]:
        fig.add_hline(y=y, line_width=0.8, line_color="rgba(255,255,255,0.035)")

    fig.add_vline(x=0, line_width=2.4, line_dash="dash", line_color="rgba(255,255,255,0.58)")

    fig.add_trace(go.Scatter(
        x=ellipse_x, y=ellipse_y, mode="lines",
        line=dict(color="rgba(0,0,0,0)", width=0),
        fill="toself", fillcolor="rgba(120,255,170,0.11)",
        hoverinfo="skip", showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[-4.2, -2.0, 0.0, 2.4, 4.0, 3.0, 1.0, -1.4, -3.2, -4.2],
        y=[112.8, 116.0, 116.8, 115.6, 112.6, 108.8, 106.8, 107.0, 109.0, 112.8],
        mode="lines",
        line=dict(color="rgba(0,0,0,0)", width=0),
        fill="toself", fillcolor="rgba(130,255,190,0.08)",
        hoverinfo="skip", showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=shots_x, y=shots_y, mode="markers",
        marker=dict(size=20, color="rgba(130,255,190,0.11)", line=dict(width=0)),
        hoverinfo="skip", showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=shots_x, y=shots_y, mode="markers",
        marker=dict(size=8.8, color="rgba(244,255,247,0.99)", line=dict(width=0.8, color="rgba(70,110,90,0.28)")),
        hoverinfo="skip", showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[trend_x], y=[trend_y], mode="markers",
        marker=dict(size=26, color="rgba(86,174,255,0.18)", line=dict(width=0)),
        hoverinfo="skip", showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[trend_x], y=[trend_y], mode="markers",
        marker=dict(size=11.5, color="rgba(82,166,255,1)", symbol="circle", line=dict(width=1.2, color="rgba(255,255,255,0.82)")),
        hoverinfo="skip", showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[latest_x], y=[latest_y], mode="markers",
        marker=dict(size=30, color="rgba(255,79,79,0.16)", line=dict(width=0)),
        hoverinfo="skip", showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[latest_x], y=[latest_y], mode="markers",
        marker=dict(size=12.5, color="rgba(255,88,88,1)", symbol="diamond", line=dict(width=1.2, color="rgba(255,255,255,0.78)")),
        hoverinfo="skip", showlegend=False
    ))

    fig.add_annotation(x=0, y=120.4, text="Target Line", showarrow=False, font=dict(color="#cfe0e6", size=10))
    fig.add_annotation(x=trend_x - 0.4, y=119.0, text="Last 5 Avg", showarrow=False, font=dict(color="#9fd1ff", size=10))
    fig.add_annotation(x=latest_x + 1.9, y=118.0, text="Latest Avg", showarrow=False, font=dict(color="#ffb1b1", size=10))

    fig.update_layout(
        height=240,
        margin=dict(l=4, r=4, t=8, b=4),
        paper_bgcolor="#13252d",
        plot_bgcolor="#0b1920",
        font=dict(color="#e8f0f2"),
    )

    fig.update_xaxes(
        title="Side Carry (m)",
        range=[-12, 12],
        gridcolor="rgba(255,255,255,0.00)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10),
        fixedrange=True,
    )

    fig.update_yaxes(
        title="Carry Distance (m)",
        range=[98, 122],
        gridcolor="rgba(255,255,255,0.00)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10),
        fixedrange=True,
    )

    return fig


def render_v4_dashboard_premium(detector_results=None, pipeline_output=None):
    if pipeline_output:
        session_summary = pipeline_output["session_summary"]
        performance_score = session_summary.get("performance_score", 0)
    else:
        session_summary = {
            "strike_quality": 65,
            "blueprint_match_pct": 52.0,
            "corridor_pct": 38.0,
            "performance_score": 78,
            "primary_issue": "No session loaded"
        }
        performance_score = get_performance_context(detector_results)

    st.markdown(get_premium_css(), unsafe_allow_html=True)

    header_left, header_right = st.columns([5, 1])

    with header_left:
        st.markdown(
            """
            <div class="premium-header">
                <div style="font-size:17px;font-weight:800;color:white;line-height:1;margin-bottom:4px;letter-spacing:0.03em;">
                    GolfAI
                </div>
                <div style="font-size:10px;font-weight:700;color:#d8eee4;letter-spacing:0.10em;text-transform:uppercase;margin-bottom:4px;">
                    Command Centre
                </div>
                <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
                    <div style="background:rgba(255,255,255,0.08);color:#e7fff2;font-size:9px;font-weight:700;padding:4px 8px;border-radius:999px;border:1px solid rgba(255,255,255,0.06);">
                        7 Iron
                    </div>
                    <div style="color:#d8eee4;font-size:10px;">
                        53 shots
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_right:
        gauge_col, menu_col = st.columns([3, 1])

        with gauge_col:
            st.plotly_chart(
                build_mini_gauge(performance_score),
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with menu_col:
            st.markdown(
                """
                <div style="display:flex;justify-content:center;align-items:center;height:64px;font-size:22px;color:#e6f2ef;">
                    ☰
                </div>
                """,
                unsafe_allow_html=True,
            )

    main_left, main_right = st.columns([1.00, 1.22])

    with main_left:
        premium_card_open("Carry Distance Profile")
        render_premium_distance_card()
        premium_card_close()

        premium_card_open("Session Summary")
        render_premium_summary_card(session_summary)
        premium_card_close()

        premium_card_open("Practice Focus")
        render_premium_focus_card()
        premium_card_close()

    with main_right:
        premium_card_open("Shot Dispersion")

        bias_value = "Unknown"
        width_value = "0.0m"

        if detector_results and "dispersion_info" in detector_results:
            disp = detector_results["dispersion_info"]
            bias_value = disp.get("miss_bias", "Unknown")
            width_value = f"{disp.get('side_std', 0) * 2:.1f}m"

        st.markdown(
            f"""
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:3px;">
                <div>
                    <div style="font-size:11px;color:#9fd9b4;font-weight:700;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:2px;">
                        Bias
                    </div>
                    <div style="font-size:17px;color:#f5f7fa;font-weight:800;line-height:1;">
                        {bias_value}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:11px;color:#c7d4da;font-weight:700;letter-spacing:0.04em;text-transform:uppercase;margin-bottom:2px;">
                        Width
                    </div>
                    <div style="font-size:17px;color:#f5f7fa;font-weight:800;line-height:1;">
                        {width_value}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            build_premium_dispersion(detector_results),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown(
            """
            <div style="text-align:center;margin-top:2px;font-size:9px;color:#c7d4da;line-height:1.2;">
                Red = latest session average · Blue = last 5 sessions average
            </div>
            <div style="text-align:center;margin-top:1px;font-size:9px;color:#c7d4da;line-height:1.2;">
                Today is moving 1.0m closer to centre than recent trend
            </div>
            """,
            unsafe_allow_html=True,
        )
        premium_card_close()

        premium_card_open("Progress Over Time")
        st.plotly_chart(
            build_progress_chart(),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown(
            """
            <div style="text-align:center;margin-top:3px;font-size:9px;color:#c7d4da;line-height:1.2;">
                Strike and blueprint are improving. Dispersion control still lags.
            </div>
            """,
            unsafe_allow_html=True,
        )
        premium_card_close()

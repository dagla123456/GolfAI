import streamlit as st
import plotly.graph_objects as go
from golfai.v4_styles import get_v4_css
from golfai.v4_cards import card_open, card_close
from golfai.v4_header import render_v4_header
from golfai.scoring import build_session_score


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
        trend_text = "▲ Strong session"
        trend_color = "#1ed760"
    elif performance_score >= 65:
        performance_label = "Good"
        trend_text = "▲ Improving"
        trend_color = "#1ed760"
    elif performance_score >= 50:
        performance_label = "Developing"
        trend_text = "● Mixed session"
        trend_color = "#ffd166"
    else:
        performance_label = "Needs Work"
        trend_text = "▼ Below standard"
        trend_color = "#ff6b6b"

    return {
        "performance_score": performance_score,
        "performance_label": performance_label,
        "trend_text": trend_text,
        "trend_color": trend_color,
        "primary_issue": primary_issue,
        "secondary_issue": secondary_issue,
    }


def build_mock_gauge(score_value):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score_value,
            number={"font": {"size": 26, "color": "#f5f7fa"}},
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
                    "value": score_value,
                },
            },
        )
    )
    fig.update_layout(
        height=140,
        margin=dict(l=8, r=8, t=10, b=8),
        paper_bgcolor="#142c34",
        font={"color": "#e8f0f2"},
    )
    return fig


def build_mock_distance():
    avg = 102.5
    reliable_min = 95
    reliable_max = 113
    full_min = 72
    full_max = 132

    fig = go.Figure()

    fig.add_shape(
        type="rect",
        x0=full_min,
        x1=full_max,
        y0=0.40,
        y1=0.60,
        line=dict(width=1, color="rgba(255,255,255,0.08)"),
        fillcolor="rgba(255,255,255,0.05)",
    )

    fig.add_shape(
        type="rect",
        x0=reliable_min,
        x1=reliable_max,
        y0=0.34,
        y1=0.66,
        line=dict(width=0),
        fillcolor="rgba(30,215,96,0.88)",
    )

    fig.add_trace(
        go.Scatter(
            x=[avg],
            y=[0.50],
            mode="markers",
            marker=dict(
                size=14,
                color="rgba(255,90,90,1)",
                line=dict(width=2, color="rgba(255,255,255,0.80)"),
            ),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    fig.add_annotation(
        x=(reliable_min + reliable_max) / 2,
        y=0.18,
        text=f"Reliable Window  {reliable_min}–{reliable_max}m",
        showarrow=False,
        font=dict(color="#dff7ea", size=11),
    )

    fig.update_layout(
        height=118,
        margin=dict(l=6, r=6, t=6, b=6),
        paper_bgcolor="#142c34",
        plot_bgcolor="#142c34",
        font=dict(color="#e8f0f2"),
        xaxis=dict(
            range=[68, 136],
            showgrid=False,
            zeroline=False,
            tickmode="array",
            tickvals=[full_min, reliable_min, avg, reliable_max, full_max],
            ticktext=[f"{full_min}m", f"{reliable_min}", f"{avg:.0f}", f"{reliable_max}", f"{full_max}m"],
            tickfont=dict(size=10, color="#cfd8dc"),
            fixedrange=True,
        ),
        yaxis=dict(range=[0, 1], visible=False, fixedrange=True),
    )
    return fig


def build_mock_dispersion():
    fig = go.Figure()

    fig.add_hrect(y0=98, y1=122, fillcolor="rgba(255,255,255,0.015)", line_width=0, layer="below")
    fig.add_vrect(x0=-5, x1=5, fillcolor="rgba(110,200,120,0.18)", line_width=0, layer="below")
    fig.add_vline(x=0, line_width=2.0, line_dash="dash", line_color="rgba(255,255,255,0.55)")
    fig.add_hline(y=110.5, line_width=1.4, line_color="rgba(255,255,255,0.35)")

    ex1 = [-8, -4, 0, 4, 8, 7, 3, -1, -5, -7, -5, -1, 3, 6, 4, 0, -3, -6, -8]
    ey1 = [116, 121, 124, 121, 116, 110, 105, 103, 105, 110, 116, 121, 124, 121, 116, 112, 110, 112, 116]
    fig.add_trace(
        go.Scatter(
            x=ex1,
            y=ey1,
            mode="lines",
            line=dict(color="rgba(255,255,255,0.82)", width=2.2),
            fill="toself",
            fillcolor="rgba(130,210,100,0.14)",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    ex2 = [-5, -2, 0, 2, 5, 4, 2, -1, -3, -4, -3, -1, 2, 4, 3, 0, -2, -4, -5]
    ey2 = [113, 116, 118, 116, 113, 110, 108, 107, 108, 110, 113, 116, 118, 116, 113, 111, 110, 111, 113]
    fig.add_trace(
        go.Scatter(
            x=ex2,
            y=ey2,
            mode="lines",
            line=dict(color="rgba(120,255,150,0.28)", width=1.1),
            fill="toself",
            fillcolor="rgba(120,255,150,0.10)",
            hoverinfo="skip",
            showlegend=False,
        )
    )

    shots_x = [-2.8, -1.5, -0.3, 0.8, 2.1, -1.2, 0.5, 1.6, -0.8, 2.8, -2.2, 0.2, 1.2, -1.9, 2.4]
    shots_y = [104, 108, 111, 109, 105, 114, 116, 113, 118, 107, 110, 112, 109, 111, 114]
    fig.add_trace(
        go.Scatter(
            x=shots_x,
            y=shots_y,
            mode="markers",
            marker=dict(
                size=7,
                color="rgba(240,245,210,0.96)",
                line=dict(width=0.8, color="rgba(30,30,30,0.35)"),
            ),
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[0.4],
            y=[110.5],
            mode="markers",
            marker=dict(size=20, color="rgba(255,70,70,0.18)"),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0.4],
            y=[110.5],
            mode="markers",
            marker=dict(
                size=11,
                color="rgba(255,70,70,1)",
                symbol="diamond",
                line=dict(width=1.0, color="rgba(255,255,255,0.55)"),
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        height=155,
        margin=dict(l=4, r=4, t=4, b=4),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2"),
    )
    fig.update_xaxes(
        title="Side Carry (m)",
        range=[-12, 12],
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10),
    )
    fig.update_yaxes(
        title="Carry Distance (m)",
        range=[98, 122],
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10),
    )
    return fig


def build_mock_progress():
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=["S1", "S2", "S3", "S4", "S5"],
            y=[52, 58, 61, 69, 78],
            mode="lines+markers",
            name="Performance",
            line=dict(color="#1ed760", width=2.5),
            marker=dict(size=5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=["S1", "S2", "S3", "S4", "S5"],
            y=[36, 40, 44, 47, 53],
            mode="lines+markers",
            name="Consistency",
            line=dict(color="#ff8c42", width=2.5),
            marker=dict(size=5),
        )
    )
    fig.update_layout(
        height=120,
        margin=dict(l=4, r=4, t=4, b=4),
        paper_bgcolor="#142c34",
        plot_bgcolor="#0f1f26",
        font=dict(color="#e8f0f2"),
        legend=dict(orientation="h", y=1.02, x=0, font=dict(size=8)),
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
            st.markdown(
                f"""
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
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div style="
            margin-top:6px;
            color:#d5e0e6;
            font-size:11px;
            line-height:1.25;
        ">
            Contact improving. Dispersion still slightly left-biased.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_practice_focus():
    st.markdown(
        """
        <div style="font-size:11px; line-height:1.25; color:#eaf2f5;">
            <div style="font-weight:800; margin-bottom:4px;">Recommended Focus</div>
            <div>• Neutral forearm setup</div>
            <div>• Pause at the top</div>
            <div>• Arms fall before chest rotates</div>
            <div style="font-weight:800; margin-top:8px; margin-bottom:4px;">Practice Plan</div>
            <div><b>Goal:</b> Stabilise strike and low point</div>
            <div><b>Drill:</b> Pause Transition Drill</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_v4_dashboard_prototype(detector_results=None):
    performance = get_performance_context(detector_results)

    st.markdown(get_v4_css(), unsafe_allow_html=True)
    st.markdown('<div class="v4-shell">', unsafe_allow_html=True)

    render_v4_header(
        {
            "session_file": "mlm2pro_shotexport_011826.csv",
            "shots_analysed": 53,
            "club_label": "7 Iron",
            "mode_label": "Command Centre",
        }
    )

    top_left, top_right = st.columns(2)
    with top_left:
        card_open("Performance Score")
        st.plotly_chart(
            build_mock_gauge(performance["performance_score"]),
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
        card_close()

    with top_right:
        card_open("Carry Distance Profile")

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
                        font-size:30px;
                        font-weight:800;
                        color:#f5f7fa;
                        line-height:0.95;
                        margin-bottom:2px;
                    ">
                        102.5m
                    </div>
                    <div style="
                        font-size:11px;
                        color:#d7e5ea;
                        font-weight:700;
                        letter-spacing:0.05em;
                        text-transform:uppercase;
                    ">
                        Average Carry
                    </div>
                </div>
                <div style="
                    text-align:right;
                    font-size:11px;
                    line-height:1.2;
                ">
                    <div style="color:#9fd9b4; font-weight:700;">Reliable Window</div>
                    <div style="color:#f3fbf6; font-weight:800;">95–113m</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(
            build_mock_distance(),
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown(
            """
            <div style="
                text-align:center;
                margin-top:2px;
                font-size:10px;
                color:#c7d4da;
                line-height:1.2;
            ">
                Full range: 72m to 132m
            </div>
            """,
            unsafe_allow_html=True,
        )

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

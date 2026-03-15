import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from golfai.scoring import build_session_score


# ---------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------

def get_premium_css():

    return """
    <style>

    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background:
            radial-gradient(circle at top left, rgba(35,95,70,0.16), transparent 28%),
            linear-gradient(180deg,#050d12 0%,#0a171d 100%) !important;
        color:#eef3f7 !important;
    }

    .block-container {
        padding-top:0.22rem !important;
        padding-bottom:0.05rem !important;
        padding-left:0.8rem !important;
        padding-right:0.8rem !important;
        max-width:1450px !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap:0.18rem !important;
    }

    .premium-card {
        background:
        linear-gradient(180deg, rgba(20,34,42,0.98), rgba(10,20,26,0.99));
        border:1px solid rgba(130,188,164,0.12);
        border-radius:18px;
        padding:0.45rem 0.55rem 0.35rem 0.55rem;
        margin-bottom:0.15rem;
    }

    .premium-card-title {
        font-size:0.70rem;
        font-weight:800;
        color:#f2f7fa;
        letter-spacing:0.08em;
        text-transform:uppercase;
        margin-bottom:0.15rem;
        padding-bottom:0.1rem;
        border-bottom:1px solid rgba(255,255,255,0.07);
    }

    </style>
    """


# ---------------------------------------------------
# CARD HELPERS
# ---------------------------------------------------

def premium_card_open(title):

    st.markdown(
        f"""
        <div class="premium-card">
        <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:2px;
        ">
        <div class="premium-card-title">{title}</div>
        <div style="width:6px;height:6px;border-radius:50%;background:#1ed760"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def premium_card_close():

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------
# PERFORMANCE SCORE
# ---------------------------------------------------

def get_performance_context(detector_results=None):

    if detector_results:
        score_data = build_session_score(detector_results)
        score = score_data.get("performance_score", 78)
    else:
        score = 78

    return score


# ---------------------------------------------------
# MINI HEADER GAUGE
# ---------------------------------------------------

def build_mini_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"font":{"size":18,"color":"white"}},
            gauge={
                "axis":{"range":[0,100],"visible":False},
                "bar":{"color":"rgba(0,0,0,0)"},
                "bgcolor":"rgba(0,0,0,0)",
                "borderwidth":0,
                "steps":[
                    {"range":[0,40],"color":"#ff4d4d"},
                    {"range":[40,65],"color":"#ffd166"},
                    {"range":[65,100],"color":"#1ed760"}
                ],
                "threshold":{
                    "line":{"color":"white","width":3},
                    "thickness":0.85,
                    "value":score
                }
            }
        )
    )

    fig.update_layout(
        height=70,
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


# ---------------------------------------------------
# DISTANCE CARD
# ---------------------------------------------------

def render_distance_card():

    html="""
    <div style="color:#eef3f7;font-family:Arial">

    <div style="display:flex;justify-content:space-between;margin-bottom:6px">

    <div>
    <div style="font-size:26px;font-weight:800">102.5m</div>
    <div style="font-size:10px;color:#cfd8dc">Average Carry</div>
    </div>

    <div style="text-align:right">
    <div style="font-size:10px;color:#9fd9b4">Trust Window</div>
    <div style="font-size:16px;font-weight:700">95–113m</div>
    </div>

    </div>

    <div style="height:18px;border-radius:10px;background:#24343b"></div>

    </div>
    """

    components.html(html,height=120)


# ---------------------------------------------------
# SESSION SUMMARY
# ---------------------------------------------------

def render_session_summary():

    html="""
    <div style="color:#eef3f7;font-family:Arial">

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">

    <div>
    <div style="font-size:10px;color:#cfd8dc">Strike Quality</div>
    <div style="font-size:22px;font-weight:800">65</div>
    </div>

    <div>
    <div style="font-size:10px;color:#cfd8dc">Blueprint</div>
    <div style="font-size:22px;font-weight:800">52%</div>
    </div>

    <div>
    <div style="font-size:10px;color:#cfd8dc">Dispersion</div>
    <div style="font-size:22px;font-weight:800">29</div>
    </div>

    <div>
    <div style="font-size:10px;color:#cfd8dc">Efficiency</div>
    <div style="font-size:22px;font-weight:800">1.31</div>
    </div>

    </div>

    </div>
    """

    components.html(html,height=140)


# ---------------------------------------------------
# PRACTICE FOCUS
# ---------------------------------------------------

def render_practice_focus():

    html="""
    <div style="color:#eef3f7;font-family:Arial">

    <div style="font-size:11px;font-weight:700;margin-bottom:6px">
    Recommended Focus
    </div>

    <div style="font-size:11px">
    • Neutral forearm setup<br>
    • Pause transition<br>
    • Arms drop before chest
    </div>

    </div>
    """

    components.html(html,height=140)


# ---------------------------------------------------
# PROGRESS CHART
# ---------------------------------------------------

def build_progress_chart():

    sessions=["S1","S2","S3","S4","S5"]

    strike=[48,54,57,61,65]
    blueprint=[36,40,44,48,52]
    dispersion=[32,35,37,33,29]

    fig=go.Figure()

    fig.add_trace(go.Scatter(
        x=sessions,
        y=strike,
        mode="lines+markers",
        name="Strike",
        line=dict(color="#1ed760",width=3)
    ))

    fig.add_trace(go.Scatter(
        x=sessions,
        y=blueprint,
        mode="lines+markers",
        name="Blueprint",
        line=dict(color="#56a6ff",width=3)
    ))

    fig.add_trace(go.Scatter(
        x=sessions,
        y=dispersion,
        mode="lines+markers",
        name="Dispersion",
        line=dict(color="#ff8c42",width=3)
    ))

    fig.update_layout(
        height=150,
        margin=dict(l=4,r=4,t=10,b=4),
        paper_bgcolor="#13252d",
        plot_bgcolor="#0b1920",
        legend=dict(orientation="h")
    )

    return fig


# ---------------------------------------------------
# DISPERSION CHART
# ---------------------------------------------------

def build_dispersion_chart():

    shots_x=[-2,-1,0,1,2]
    shots_y=[108,110,112,109,111]

    fig=go.Figure()

    fig.add_trace(go.Scatter(
        x=shots_x,
        y=shots_y,
        mode="markers",
        marker=dict(size=10,color="white")
    ))

    fig.update_layout(
        height=150,
        margin=dict(l=4,r=4,t=10,b=4),
        paper_bgcolor="#13252d",
        plot_bgcolor="#0b1920"
    )

    return fig


# ---------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------

def render_v4_dashboard_premium(detector_results=None):

    score=get_performance_context(detector_results)

    st.markdown(get_premium_css(),unsafe_allow_html=True)

    header_left,header_right=st.columns([5,1])

    with header_left:

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#143027,#11261f);
        border-radius:16px;
        padding:10px 14px;
        ">
        <div style="font-size:18px;font-weight:800;color:white">GolfAI</div>
        <div style="font-size:10px;color:#d8eee4">Command Centre</div>
        <div style="font-size:10px;color:#d8eee4;margin-top:2px">7 Iron · 53 shots</div>
        </div>
        """,unsafe_allow_html=True)

    with header_right:

        g,m=st.columns([3,1])

        with g:

            st.plotly_chart(
                build_mini_gauge(score),
                use_container_width=True,
                config={"displayModeBar":False}
            )

        with m:

            st.markdown(
                "<div style='font-size:22px;text-align:center'>☰</div>",
                unsafe_allow_html=True
            )

    col1,col2=st.columns(2)

    with col1:
        premium_card_open("Carry Distance Profile")
        render_distance_card()
        premium_card_close()

    with col2:
        premium_card_open("Shot Dispersion")
        st.plotly_chart(build_dispersion_chart(),use_container_width=True)
        premium_card_close()

    col3,col4=st.columns(2)

    with col3:
        premium_card_open("Session Summary")
        render_session_summary()
        premium_card_close()

    with col4:
        premium_card_open("Progress Over Time")
        st.plotly_chart(build_progress_chart(),use_container_width=True)
        premium_card_close()

    col5,_=st.columns(2)

    with col5:
        premium_card_open("Practice Focus")
        render_practice_focus()
        premium_card_close()

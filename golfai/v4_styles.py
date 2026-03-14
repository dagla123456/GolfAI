def get_v4_css():
    return """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background: linear-gradient(180deg, #07141a 0%, #0b1d24 100%) !important;
        color: #eef3f7 !important;
    }

    .stApp {
        background: linear-gradient(180deg, #07141a 0%, #0b1d24 100%) !important;
    }

    .block-container {
        padding-top: 0.45rem !important;
        padding-bottom: 0.2rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        max-width: 1450px !important;
    }

    .v4-shell {
        padding: 0.05rem 0.05rem 0.2rem 0.05rem;
    }

    .v4-title {
        text-align: left;
        font-size: 1.55rem;
        font-weight: 800;
        color: #f5f7fa;
        letter-spacing: 0.03em;
        margin: 0.02rem 0 0.3rem 0;
        line-height: 1.0;
    }

    .v4-card {
        background: radial-gradient(circle at top left, rgba(27,53,61,0.96), rgba(10,22,28,0.96));
        border: 1px solid rgba(110, 170, 150, 0.18);
        border-radius: 16px;
        padding: 0.55rem 0.65rem 0.4rem 0.65rem;
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.02) inset,
            0 8px 20px rgba(0,0,0,0.26),
            0 0 16px rgba(60,160,120,0.05);
        margin-bottom: 0.4rem;
    }

    .v4-card-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #f0f4f8;
        margin-bottom: 0.3rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 0.2rem;
        line-height: 1.05;
    }

    .v4-subtle {
        color: #b8c6cf;
        font-size: 0.78rem;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.35rem !important;
    }

    div[data-testid="stMetric"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.15rem !important;
        line-height: 1.0 !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.72rem !important;
        line-height: 1.0 !important;
    }

    div[data-testid="stFileUploader"] {
        margin-bottom: 0.3rem;
    }

    div[data-baseweb="tab-list"] {
        gap: 0.25rem;
    }

    button[data-baseweb="tab"] {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 0.32rem 0.6rem !important;
        min-height: 30px !important;
    }

    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #dce6eb !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(180deg, #2e8b57, #1f5d3d) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: white !important;
    }

    .js-plotly-plot, .plot-container {
        height: 180px !important;
    }
    </style>
    """

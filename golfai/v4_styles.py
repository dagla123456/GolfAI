def get_v4_css():
    return """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background:
            radial-gradient(circle at top left, rgba(24, 64, 54, 0.14), transparent 28%),
            linear-gradient(180deg, #061218 0%, #0a1b22 100%) !important;
        color: #eef3f7 !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(24, 64, 54, 0.14), transparent 28%),
            linear-gradient(180deg, #061218 0%, #0a1b22 100%) !important;
    }

    .block-container {
        padding-top: 0.38rem !important;
        padding-bottom: 0.16rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        max-width: 1450px !important;
    }

    .v4-shell {
        padding: 0.03rem 0.03rem 0.18rem 0.03rem;
    }

    .v4-title {
        text-align: left;
        font-size: 1.5rem;
        font-weight: 800;
        color: #f5f7fa;
        letter-spacing: 0.025em;
        margin: 0.01rem 0 0.24rem 0;
        line-height: 1.0;
    }

    .v4-card {
        background:
            linear-gradient(180deg, rgba(22, 45, 53, 0.96), rgba(10, 20, 26, 0.98));
        border: 1px solid rgba(130, 188, 164, 0.13);
        border-radius: 18px;
        padding: 0.52rem 0.62rem 0.38rem 0.62rem;
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.018) inset,
            0 10px 22px rgba(0,0,0,0.24),
            0 0 18px rgba(60,160,120,0.035);
        margin-bottom: 0.34rem;
        backdrop-filter: blur(2px);
    }

    .v4-card-title {
        font-size: 0.78rem;
        font-weight: 800;
        color: #f2f7fa;
        margin-bottom: 0.24rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        padding-bottom: 0.18rem;
        line-height: 1.0;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }

    .v4-subtle {
        color: #aebec7;
        font-size: 0.74rem;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.3rem !important;
    }

    div[data-testid="stMetric"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.08rem !important;
        line-height: 1.0 !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.68rem !important;
        line-height: 1.0 !important;
    }

    div[data-testid="stFileUploader"] {
        margin-bottom: 0.24rem;
    }

    div[data-baseweb="tab-list"] {
        gap: 0.22rem;
    }

    button[data-baseweb="tab"] {
        background: rgba(255,255,255,0.055) !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 0.28rem 0.54rem !important;
        min-height: 28px !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
    }

    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #dce6eb !important;
        font-weight: 700 !important;
        font-size: 0.76rem !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(180deg, #2e8b57, #1f5d3d) !important;
        border: 1px solid rgba(120, 210, 155, 0.25) !important;
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

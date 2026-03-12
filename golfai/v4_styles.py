def get_v4_css():
    return """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background: linear-gradient(180deg, #07141a 0%, #0b1d24 100%) !important;
        color: #eef3f7 !important;
    }

    .v4-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        color: #f5f7fa;
        letter-spacing: 0.04em;
        margin: 0.2rem 0 1rem 0;
    }

    .v4-shell {
        padding: 0.4rem 0.2rem 1rem 0.2rem;
    }

    .v4-card {
        background: radial-gradient(circle at top left, rgba(27,53,61,0.96), rgba(10,22,28,0.96));
        border: 1px solid rgba(110, 170, 150, 0.18);
        border-radius: 18px;
        padding: 1rem 1rem 0.8rem 1rem;
        box-shadow:
            0 0 0 1px rgba(255,255,255,0.02) inset,
            0 10px 30px rgba(0,0,0,0.30),
            0 0 20px rgba(60,160,120,0.06);
        margin-bottom: 1rem;
    }

    .v4-card-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f0f4f8;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 0.45rem;
    }

    .v4-subtle {
        color: #b8c6cf;
        font-size: 0.92rem;
    }

    .stMetric {
        background: transparent !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 0.45rem;
    }

    button[data-baseweb="tab"] {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0.7rem 1rem !important;
    }

    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #dce6eb !important;
        font-weight: 700 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(180deg, #2e8b57, #1f5d3d) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: white !important;
    }
    </style>
    """

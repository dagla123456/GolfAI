import streamlit.components.v1 as components


def render_v4_header(data):
    session = data.get("session_file", "Practice Session")
    shots = data.get("shots_analysed", 0)

    html = f"""
    <div style="
        background: linear-gradient(135deg,#183a2d,#1f4a35);
        padding:22px 24px;
        border-radius:18px;
        margin-bottom:18px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        box-shadow:0 10px 24px rgba(0,0,0,0.28);
        color:white;
        font-family:Arial, sans-serif;
    ">
        <div>
            <div style="
                font-size:28px;
                font-weight:800;
                color:white;
                margin-bottom:6px;
                letter-spacing:0.02em;
            ">
                GolfAI Command Centre
            </div>

            <div style="color:#d8eee4;font-size:14px;margin-bottom:2px;">
                Session: {session}
            </div>

            <div style="color:#d8eee4;font-size:14px;">
                Shots Analysed: {shots}
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

    components.html(html, height=120)

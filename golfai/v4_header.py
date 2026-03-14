import streamlit.components.v1 as components


def render_v4_header(data):
    session = data.get("session_file", "Practice Session")
    shots = data.get("shots_analysed", 0)
    club = data.get("club_label", "7 Iron")
    mode = data.get("mode_label", "Command Centre")

    html = f"""
    <div style="
        background:
            linear-gradient(135deg, rgba(20,48,39,0.96), rgba(17,38,31,0.96));
        border: 1px solid rgba(120, 190, 155, 0.18);
        border-radius: 18px;
        margin-bottom: 8px;
        padding: 10px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow:
            0 10px 22px rgba(0,0,0,0.22),
            inset 0 0 0 1px rgba(255,255,255,0.02);
        color: white;
        font-family: Arial, sans-serif;
    ">
        <div style="display:flex; flex-direction:column; justify-content:center;">
            <div style="
                font-size: 18px;
                font-weight: 800;
                color: white;
                margin-bottom: 4px;
                letter-spacing: 0.03em;
                line-height: 1;
            ">
                GolfAI
            </div>

            <div style="
                font-size: 11px;
                font-weight: 700;
                color: #d8eee4;
                letter-spacing: 0.10em;
                text-transform: uppercase;
                margin-bottom: 4px;
            ">
                {mode}
            </div>

            <div style="
                display:flex;
                gap:8px;
                flex-wrap:wrap;
                align-items:center;
            ">
                <div style="
                    background: rgba(255,255,255,0.08);
                    color: #e7fff2;
                    font-size: 10px;
                    font-weight: 700;
                    padding: 4px 8px;
                    border-radius: 999px;
                    border: 1px solid rgba(255,255,255,0.06);
                ">
                    {club}
                </div>

                <div style="
                    color:#d8eee4;
                    font-size:11px;
                ">
                    {shots} shots
                </div>
            </div>
        </div>

        <div style="
            display:flex;
            flex-direction:column;
            align-items:flex-end;
            justify-content:center;
            text-align:right;
        ">
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
                max-width:260px;
                line-height:1.15;
            ">
                {session}
            </div>
        </div>
    </div>
    """

    components.html(html, height=78)

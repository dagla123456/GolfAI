import streamlit.components.v1 as components


def render_v4_distance_profile(distance_info):
    avg = float(distance_info.get("avg_carry", 0))
    rmin = float(distance_info.get("reliable_min", 0))
    rmax = float(distance_info.get("reliable_max", 0))
    fmin = float(distance_info.get("full_min", 0))
    fmax = float(distance_info.get("full_max", 0))

    span = max(fmax - fmin, 1)

    avg_pos = max(0, min(100, (avg - fmin) / span * 100))
    rmin_pos = max(0, min(100, (rmin - fmin) / span * 100))
    rmax_pos = max(0, min(100, (rmax - fmin) / span * 100))

    html = f"""
    <div style="
        color:#e8f0f2;
        font-family:Arial, sans-serif;
        padding-top:2px;
    ">
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            margin-bottom:10px;
        ">
            <div>
                <div style="
                    font-size:28px;
                    font-weight:800;
                    color:#f5f7fa;
                    line-height:1;
                    margin-bottom:2px;
                ">
                    {avg:.1f}m
                </div>
                <div style="
                    font-size:11px;
                    font-weight:700;
                    color:#cfe0e6;
                    letter-spacing:0.08em;
                    text-transform:uppercase;
                ">
                    Average Carry
                </div>
            </div>

            <div style="
                text-align:right;
                font-size:11px;
                line-height:1.25;
            ">
                <div style="color:#9fd9b4; font-weight:700;">Reliable Window</div>
                <div style="color:#f3fbf6; font-weight:800;">{rmin:.0f}–{rmax:.0f}m</div>
            </div>
        </div>

        <div style="
            position:relative;
            height:16px;
            background:linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
            border:1px solid rgba(255,255,255,0.06);
            border-radius:999px;
            overflow:visible;
            margin-top:6px;
            margin-bottom:14px;
        ">
            <div style="
                position:absolute;
                left:{rmin_pos}%;
                width:{max(rmax_pos-rmin_pos, 2)}%;
                top:0;
                height:16px;
                background:linear-gradient(90deg, #169c4f, #1ed760);
                border-radius:999px;
                box-shadow:0 0 10px rgba(30,215,96,0.22);
            "></div>

            <div style="
                position:absolute;
                left:{avg_pos}%;
                top:50%;
                width:14px;
                height:14px;
                background:#ff5a5a;
                border:2px solid rgba(255,255,255,0.75);
                border-radius:50%;
                transform:translate(-50%, -50%);
                box-shadow:0 0 10px rgba(255,90,90,0.40);
            "></div>
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-top:2px;
            font-size:11px;
            color:#c7d4da;
            font-weight:600;
        ">
            <div>{fmin:.0f}m</div>
            <div style="
                color:#9fb8c2;
                font-size:10px;
                letter-spacing:0.08em;
                text-transform:uppercase;
                font-weight:700;
            ">
                Full Range
            </div>
            <div>{fmax:.0f}m</div>
        </div>
    </div>
    """

    components.html(html, height=118)

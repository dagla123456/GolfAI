import streamlit.components.v1 as components


def render_v4_distance_profile(distance_info):
    avg = distance_info.get("avg_carry", 0)
    rmin = distance_info.get("reliable_min", 0)
    rmax = distance_info.get("reliable_max", 0)
    fmin = distance_info.get("full_min", 0)
    fmax = distance_info.get("full_max", 0)

    span = max(fmax - fmin, 1)

    avg_pos = (avg - fmin) / span * 100
    rmin_pos = (rmin - fmin) / span * 100
    rmax_pos = (rmax - fmin) / span * 100

    html = f"""
    <div style="padding-top:8px; color:#e8f0f2; font-family:Arial, sans-serif;">
        <div style="
            position:relative;
            height:28px;
            background:#2c3a40;
            border-radius:14px;
            margin-top:20px;
            overflow:visible;
        ">
            <div style="
                position:absolute;
                left:{rmin_pos}%;
                width:{rmax_pos-rmin_pos}%;
                height:28px;
                background:#1ed760;
                border-radius:14px;
            "></div>

            <div style="
                position:absolute;
                left:{avg_pos}%;
                top:-6px;
                width:16px;
                height:16px;
                background:#ff5a5a;
                border-radius:50%;
                transform:translateX(-50%);
                box-shadow:0 0 8px rgba(255,90,90,0.45);
            "></div>
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            margin-top:8px;
            color:#cfd8dc;
            font-size:12px;
        ">
            <span>{fmin:.0f}m</span>
            <span>{fmax:.0f}m</span>
        </div>

        <div style="
            text-align:center;
            margin-top:8px;
            font-size:13px;
            color:#e8f5e9;
            font-weight:600;
        ">
            Reliable Distance: {rmin:.1f}m – {rmax:.1f}m
        </div>
    </div>
    """

    components.html(html, height=120)

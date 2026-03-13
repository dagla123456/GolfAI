import streamlit as st


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

    st.markdown(f"""
    <div style="padding-top:8px">

    <div style="
        position:relative;
        height:28px;
        background:#2c3a40;
        border-radius:14px;
        margin-top:20px;
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
        "></div>

    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        margin-top:6px;
        color:#cfd8dc;
        font-size:12px;
    ">
        <span>{fmin:.0f}m</span>
        <span>{fmax:.0f}m</span>
    </div>

    <div style="
        text-align:center;
        margin-top:6px;
        font-size:13px;
        color:#e8f5e9;
    ">
        Reliable Distance: {rmin:.1f}m – {rmax:.1f}m
    </div>

    </div>
    """, unsafe_allow_html=True)

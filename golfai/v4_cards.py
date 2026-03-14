import streamlit as st


def card_open(title):
    st.markdown(
        f"""
        <div class="v4-card">
            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                margin-bottom:6px;
            ">
                <div class="v4-card-title">{title}</div>
                <div style="
                    width:6px;
                    height:6px;
                    border-radius:50%;
                    background:#1ed760;
                    box-shadow:0 0 6px rgba(30,215,96,0.6);
                "></div>
            </div>
        """,
        unsafe_allow_html=True,
    )


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

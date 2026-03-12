import streamlit as st
from golfai.v4_styles import get_v4_css
from golfai.v4_cards import card_open, card_close


def render_v4_dashboard_shell():
    st.markdown(get_v4_css(), unsafe_allow_html=True)

    st.markdown('<div class="v4-shell">', unsafe_allow_html=True)
    st.markdown('<div class="v4-title">GOLF AI COMMAND CENTRE</div>', unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        card_open("Performance Score")
        st.write("V4 placeholder")
        card_close()

    with row1_col2:
        card_open("Carry Distance Profile")
        st.write("V4 placeholder")
        card_close()

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        card_open("Shot Dispersion")
        st.write("V4 placeholder")
        card_close()

    with row2_col2:
        card_open("Session Summary")
        st.write("V4 placeholder")
        card_close()

    row3_col1, row3_col2 = st.columns([1.1, 1.0])
    with row3_col1:
        card_open("Progress Over Time")
        st.write("V4 placeholder")
        card_close()

    with row3_col2:
        card_open("Practice Focus")
        st.write("V4 placeholder")
        card_close()

    st.markdown('</div>', unsafe_allow_html=True)

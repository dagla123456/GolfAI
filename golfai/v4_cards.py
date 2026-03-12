
import streamlit as st

def card_open(title):
    st.markdown(f'''
    <div class="v4-card">
        <div class="v4-card-title">{title}</div>
    ''', unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

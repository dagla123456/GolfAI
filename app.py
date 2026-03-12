"""
GolfAI Streamlit App
Version: v1.2

Change Summary:
- Replaces sidebar navigation with top mode switch
- Improves mobile usability
- Keeps Command Centre and On Course modes
"""

import streamlit as st

from golfai.v4_dashboard import render_v4_dashboard_shell
from golfai.oncourse_ui import oncourse_page

st.set_page_config(
    page_title="GolfAI",
    layout="wide"
)

st.markdown("""
<style>
div[data-testid="stRadio"] > div {
    flex-direction: row;
    gap: 0.75rem;
}

div[data-testid="stRadio"] label {
    background: #e9edf2;
    padding: 0.55rem 1rem;
    border-radius: 0.7rem;
    border: 1px solid #d8dee8;
}

div[data-testid="stRadio"] label p {
    color: #1f2430 !important;
    font-weight: 600 !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: #1f4a35 !important;
    border: 1px solid #1f4a35 !important;
}

div[data-testid="stRadio"] label:has(input:checked) p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

mode = st.radio(
    "GolfAI Mode",
    ["Command Centre", "On Course"],
    horizontal=True,
    label_visibility="collapsed"
)

if mode == "Command Centre":
    render_v4_dashboard_shell()
else:
    oncourse_page()

"""
GolfAI Streamlit App
Version: v2.0

Change Summary:
- Switches Command Centre to the new premium dashboard build
- Keeps On Course mode
- Preserves top mode switch for tablet-friendly use
"""

import streamlit as st

from golfai.v4_dashboard_premium import render_v4_dashboard_premium
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
    render_v4_dashboard_premium(detector_results=detector_results, pipeline_output=pipeline_output)
else:
    oncourse_page()

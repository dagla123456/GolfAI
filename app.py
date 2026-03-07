"""
GolfAI Streamlit App
Version: v0.4

Purpose:
Stable entry point for GolfAI Streamlit use.
"""

import streamlit as st
from golfai.ui_command_centre import command_centre_page

st.set_page_config(
    page_title="GolfAI",
    layout="wide"
)

command_centre_page()

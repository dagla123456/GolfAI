"""
GolfAI Streamlit App
Version: v1.1

Change Summary:
- Adds sidebar navigation
- Supports Command Centre
- Supports On-Course Mode
"""

import streamlit as st

from golfai.ui_command_centre import command_centre_page
from golfai.oncourse_ui import oncourse_page

st.set_page_config(
    page_title="GolfAI",
    layout="wide"
)

page = st.sidebar.selectbox(
    "GolfAI",
    ["Command Centre", "On Course"]
)

if page == "Command Centre":
    command_centre_page()

elif page == "On Course":
    oncourse_page()

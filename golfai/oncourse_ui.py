from pathlib import Path
import streamlit as st
from golfai.cue_engine import build_oncourse_cues

BASE_DIR = Path(__file__).resolve().parent
CUE_IMAGE_DIR = BASE_DIR / "cue_images"


def inject_oncourse_styles():
    st.markdown("""
    <style>
    .oc-title {
        color: #173f2d;
        font-size: 1.9rem;
        font-weight: 800;
        margin-bottom: 0.15rem;
    }

    .oc-subtitle {
        color: #214d39;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .oc-focus {
        color: #1f2430;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .oc-card {
        background: white;
        border: 1px solid #e7e9ef;
        border-radius: 0.9rem;
        padding: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    .oc-cue-title {
        color: #173f2d;
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 0.45rem;
        margin-bottom: 0.25rem;
        text-align: center;
    }

    .oc-cue-desc {
        color: #3d4654;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 0.1rem;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div,
    .stMarkdown p,
    .stCaption {
        color: #1f2430 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_cue_block(image_name, cue_title, cue_desc):
    st.markdown('<div class="oc-card">', unsafe_allow_html=True)

    if image_name:
        img_path = CUE_IMAGE_DIR / image_name
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

    st.markdown(
        f'<div class="oc-cue-title">{cue_title}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="oc-cue-desc">{cue_desc}</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


def oncourse_page():
    inject_oncourse_styles()

    st.markdown('<div class="oc-title">GOLF AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="oc-subtitle">ON COURSE MODE</div>', unsafe_allow_html=True)
    st.markdown("### TODAY'S SWING FOCUS")

    cues = build_oncourse_cues()

    if not cues["has_cues"]:
        st.info(cues["message"])
        return

    primary_cue = cues.get("primary_cue")
    secondary_cue = cues.get("secondary_cue")

    if primary_cue and secondary_cue:
        render_cue_block(
            cues.get("primary_image"),
            cues.get("primary_cue", ""),
            cues.get("primary_desc", "")
        )
        render_cue_block(
            cues.get("secondary_image"),
            cues.get("secondary_cue", ""),
            cues.get("secondary_desc", "")
        )
    elif primary_cue:
        render_cue_block(
            cues.get("primary_image"),
            cues.get("primary_cue", ""),
            cues.get("primary_desc", "")
        )
    else:
        st.info("No on-course cues available yet.")
        return

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Miss Pattern", cues.get("miss_bias", "-"))
    with c2:
        st.metric("Session Momentum", cues.get("momentum", "-"))

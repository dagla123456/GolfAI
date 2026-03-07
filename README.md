# GolfAI

GolfAI is a Streamlit-based golf practice intelligence app built to analyse launch monitor session data and turn it into practical coaching guidance.

## Current capabilities

- Session diagnosis
- Strike quality analysis
- Start line control
- Low point stability
- Sequencing analysis
- Blueprint swing detection
- Session momentum
- Swing drift detection
- Dispersion intelligence
- Shot pattern visualization
- Practice plan generation

## Project structure

- `app.py` → Streamlit entry point
- `golfai/` → package containing engine, detectors, scoring, coaching, and UI logic

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py

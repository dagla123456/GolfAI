"""
GolfAI Session History
Version: v0.1

Stores lightweight session summaries so GolfAI
can build trend intelligence later.
"""

import json
import os

HISTORY_FILE = "session_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_session_summary(summary):

    history = load_history()

    history.append(summary)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return history


def last_sessions(n=5):
    history = load_history()
    return history[-n:]

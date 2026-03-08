"""
GolfAI Session History
Version: v0.2

Stores session summaries and prevents duplicate entries.
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

    session_id = summary.get("session_id")

    if session_id is None:
        return history

    for session in history:
        if session.get("session_id") == session_id:
            return history

    history.append(summary)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return history


def last_sessions(n=5):
    history = load_history()
    return history[-n:]

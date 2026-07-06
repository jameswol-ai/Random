import json
from config import MEMORY_FILE, DEFAULT_STATE


def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r"))
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()


def save_memory(state):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass
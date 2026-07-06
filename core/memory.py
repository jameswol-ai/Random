# core/memory.py
import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("arc_memory.json")

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2), encoding="utf-8")

def log_event(memory, msg: str):
    memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory(memory)
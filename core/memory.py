import json
from pathlib import Path

MEMORY_FILE = Path("arc_v32_memory.json")

DEFAULT_STATE = {
    "designs": [],
    "evolution": [],
    "logs": [],
    "dna_bias": {
        "avg_columns": 22,
        "avg_beams": 45
    }
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w"), indent=2)
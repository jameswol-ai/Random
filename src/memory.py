import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DEFAULT_MEMORY = {
    "version": "V4 Evolution Studio",
    "projects": [],
    "saved_designs": [],
    "logs": []
}

def get_memory_path(username: str) -> Path:
    return DATA_DIR / f"{username}_random_memory.json"

def load_memory(username: str) -> dict:
    path = get_memory_path(username)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in DEFAULT_MEMORY:
                if key not in data:
                    data[key] = DEFAULT_MEMORY[key]
            return data
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(username: str, memory: dict):
    with open(get_memory_path(username), "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

def log_event(username: str, memory: dict, text: str):
    memory["logs"].append({"time": datetime.now().isoformat(), "event": text})
    save_memory(username, memory)

# =========================================================
# 🧠 META RANDOM V5 — SELF-AUTHORING REALITY ENGINE
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="META RANDOM V5", layout="wide")

# =========================================================
# 🧠 META MEMORY CORE (SELF-MODIFYING SUBSTRATE)
# =========================================================

MEMORY_FILE = Path("meta_random.json")

DEFAULT_MEMORY = {
    "cities": [],
    "designs": [],
    "engines": [],
    "knowledge": [],
    "rules": {}
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text())
            for k in DEFAULT_MEMORY:
                if k not in data:
                    data[k] = DEFAULT_MEMORY[k]
            return data
        except:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))

memory = load_memory()

# =========================================================
# 🧬 RULE EVOLUTION ENGINE (META LAYER)
# =========================================================

def evolve_rule_schema(rules):
    """Rules can mutate structurally, not just numerically."""

    if not rules:
        rules = {
            "design_pressure": 1.0,
            "city_growth": 1.0
        }

    # numeric drift
    for k in list(rules.keys()):
        rules[k] += random.uniform(-0.05, 0.08)

    # spontaneous rule creation (META EVENT)
    if random.random() > 0.7:
        new_rule = f"rule_{uuid.uuid4().hex[:4]}"
        rules[new_rule] = random.uniform(0.5, 1.5)

    return rules

# =========================================================
# 🧬 EVOLVING GENERATORS (SELF-MODIFYING BEHAVIOR)
# =========================================================

def generate_rooms(rules):
    base = ["Living", "Kitchen", "Core"]

    variance = int(rules.get("design_pressure", 1.0) * random.randint(0, 3))

    extra = [f"Room-{i}" for i in range(variance)]

    return base + extra + ["Bath"]

def score_design(rules):
    base = random.randint(60, 100)
    pressure = rules.get("design_pressure", 1.0)

    return {
        "circulation": min(100, base + pressure * 3),
        "efficiency": random.randint(60, 100),
        "adaptation": random.randint(60, 100),
        "structure": random.randint(60, 100),
        "meta_score": round(random.uniform(0, 1) * pressure, 3)
    }

def evolve_city(city, rules):
    city["population"] = int(city["population"] * random.uniform(0.95, 1.1))
    city["adaptation"] = city.get("adaptation", 50) + random.randint(-3, 5)
    return city

# =========================================================
# 🧠 META EVOLUTION STEP (THE KEY LOOP)
# =========================================================

memory["rules"] = evolve_rule_schema(memory.get("rules", {}))
rules = memory["rules"]

# auto-bootstrap
if len(memory["engines"]) < 2:
    memory["engines"].append({
        "id": str(uuid.uuid4())[:8],
        "dna": {"meta": 1.0},
        "power": 0.5
    })

for c in memory["cities"]:
    evolve_city(c, rules)

# =========================================================
# 🌱 SPAWNING EVENTS
# =========================================================

if random.random() > 0.6:
    memory["cities"].append({
        "id": str(uuid.uuid4())[:8],
        "population": random.randint(5000, 200000),
        "adaptation": random.randint(40, 100),
        "created": datetime.now().isoformat()
    })

# =========================================================
# 💾 SAVE STATE
# =========================================================

save_memory(memory)

# =========================================================
# 🧠 UI — META CORE VIEW
# =========================================================

st.title("🧠 META RANDOM V5 — SELF-AUTHORING ENGINE")

st.subheader("🧬 Active Rules (Now Mutable Structure)")
st.json(rules)

col1, col2, col3 = st.columns(3)
col1.metric("Cities", len(memory["cities"]))
col2.metric("Designs", len(memory["designs"]))
col3.metric("Engines", len(memory["engines"]))

st.divider()

# =========================================================
# 🏙 CITIES
# =========================================================

st.subheader("🏙 Evolving Cities")
st.json(memory["cities"])

# =========================================================
# 🧬 DESIGN GENERATION
# =========================================================

if st.button("Generate Meta Design"):
    design = {
        "rooms": generate_rooms(rules),
        "score": score_design(rules),
        "created": datetime.now().isoformat()
    }
    memory["designs"].append(design)
    save_memory(memory)

st.subheader("🧬 Designs")
st.json(memory["designs"])

# =========================================================
# ⚙ ENGINE VIEW
# =========================================================

st.subheader("⚙ Engines")
st.json(memory["engines"])

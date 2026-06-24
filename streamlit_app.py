# =========================================================
# 🧠 RANDOM V4.2 — SELF-REWRITING CIVILIZATION ENGINE
# =========================================================

import streamlit as st
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="RANDOM V4.2", layout="wide")

# =========================================================
# MEMORY CORE
# =========================================================

MEMORY_FILE = Path("random_memory.json")

DEFAULT_MEMORY = {
    "projects": [],
    "designs": [],
    "cities": [],
    "knowledge": [],
    "engines": [],
    "rules": {
        "design_weight": 1.0,
        "city_growth_factor": 1.0
    }
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
# 🧬 EVOLUTION ENGINE (GENETIC SYSTEM)
# =========================================================

def engine_dna():
    return {
        "creativity": random.uniform(0, 1),
        "stability": random.uniform(0, 1),
        "complexity": random.uniform(0, 1)
    }

def mutate_dna(dna):
    return {
        k: min(1.0, max(0.0, v + random.uniform(-0.1, 0.1)))
        for k, v in dna.items()
    }

def breed_engine(parent=None):
    dna = engine_dna() if not parent else mutate_dna(parent["dna"])
    return {
        "id": str(uuid.uuid4())[:8],
        "dna": dna,
        "power": round(sum(dna.values()) / 3, 3),
        "created": datetime.now().isoformat()
    }

# =========================================================
# 🧠 SELF-REWRITING RULE SYSTEM
# =========================================================

def evolve_rules(memory):
    rules = memory["rules"]

    # system adapts based on history size
    pressure = len(memory["designs"]) + len(memory["cities"])

    rules["design_weight"] = 1.0 + (pressure * 0.001)
    rules["city_growth_factor"] = 1.0 + (pressure * 0.002)

    return rules

# =========================================================
# ARCHITECTURE GENERATION (EVOLVED)
# =========================================================

def generate_rooms(bedrooms, rules):
    base = ["Living", "Kitchen", "Dining"]

    # mutation: creativity increases room variance
    extra_rooms = int(rules["design_weight"] * random.randint(0, 2))

    return base + [f"Bedroom {i+1}" for i in range(bedrooms + extra_rooms)] + ["Bath"]

def score_design(rules):
    base = random.randint(70, 100)
    bias = rules["design_weight"] * 5

    scores = {
        "circulation": min(100, base + bias),
        "light": random.randint(70, 100),
        "efficiency": random.randint(70, 100),
        "structure": random.randint(70, 100),
    }
    scores["overall"] = round(sum(scores.values()) / 4, 1)
    return scores

def plot_rooms(rooms):
    fig, ax = plt.subplots()

    for i, r in enumerate(rooms[:8]):
        ax.add_patch(plt.Rectangle((i % 4, i // 4), 1, 1, fill=False))
        ax.text(i % 4 + 0.5, i // 4 + 0.5, r[:6], ha="center")

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2)
    ax.axis("off")

    return fig

# =========================================================
# SYSTEM EVOLUTION STEP
# =========================================================

memory["rules"] = evolve_rules(memory)
rules = memory["rules"]

# auto-birth engine if ecosystem is small
if len(memory["engines"]) < 3:
    memory["engines"].append({
        "name": "AutoCore",
        "dna": engine_dna(),
        "power": 0.5
    })

save_memory(memory)

# =========================================================
# SIDEBAR
# =========================================================

page = st.sidebar.selectbox(
    "RANDOM CIVILIZATION",
    [
        "Dashboard",
        "Design Studio",
        "City Simulator",
        "Knowledge Base",
        "Engine Lab"
    ] + [e["name"] for e in memory["engines"]]
)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("🧠 RANDOM V4.2 CIVILIZATION CORE")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Designs", len(memory["designs"]))
    c2.metric("Cities", len(memory["cities"]))
    c3.metric("Engines", len(memory["engines"]))
    c4.metric("Rule Pressure", round(rules["design_weight"], 2))

# =========================================================
# DESIGN STUDIO
# =========================================================

elif page == "Design Studio":
    st.title("🏗 Evolutionary Design Studio")

    bedrooms = st.slider("Bedrooms", 1, 10, 3)

    if st.button("Generate Evolved Design"):
        rooms = generate_rooms(bedrooms, rules)
        design = {
            "rooms": rooms,
            "scores": score_design(rules),
            "created": datetime.now().isoformat()
        }

        memory["designs"].append(design)
        save_memory(memory)

        st.write("Rooms:", rooms)
        st.json(design["scores"])
        st.pyplot(plot_rooms(rooms))

# =========================================================
# CITY SIMULATOR
# =========================================================

elif page == "City Simulator":
    st.title("🌆 Adaptive City Engine")

    if st.button("Spawn City"):
        city = {
            "population": int(random.randint(5000, 200000) * rules["city_growth_factor"]),
            "districts": random.randint(2, 30),
            "infrastructure": random.randint(10, 100),
            "created": datetime.now().isoformat()
        }

        memory["cities"].append(city)
        save_memory(memory)

    st.json(memory["cities"])

# =========================================================
# KNOWLEDGE BASE
# =========================================================

elif page == "Knowledge Base":
    st.title("📚 Civilization Memory")

    text = st.text_input("Add Knowledge")

    if st.button("Store") and text.strip():
        memory["knowledge"].append({
            "text": text,
            "created": datetime.now().isoformat()
        })
        save_memory(memory)

    st.json(memory["knowledge"])

# =========================================================
# ENGINE LAB (GENETIC EVOLUTION)
# =========================================================

elif page == "Engine Lab":
    st.title("🧬 Engine Evolution Lab")

    if st.button("Breed Engine"):
        parent = random.choice(memory["engines"]) if memory["engines"] else None
        new_engine = breed_engine(parent)
        memory["engines"].append(new_engine)
        save_memory(memory)

    st.subheader("Engine Genome Pool")
    st.json(memory["engines"])

# =========================================================
# ENGINE PAGES (DYNAMIC)
# =========================================================

elif page in [e["name"] for e in memory["engines"]]:
    engine = next(e for e in memory["engines"] if e["name"] == page)

    st.title(f"🧬 Engine Node: {engine['name']}")
    st.json(engine["dna"])
    st.metric("Power Index", engine["power"])

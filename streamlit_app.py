# =========================================================
# RANDOM V8
# Evolutionary Architecture Intelligence System
# Multi-Agent + Genetic Design Evolution Engine
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V8",
    page_icon="🧬",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# THEME
# =========================================================

st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0b1220, #050814);
}
.main {
    background: transparent;
}
h1 {
    color: #38bdf8;
}
h2,h3 {
    color: #7dd3fc;
}
.stMetric {
    background: rgba(17,24,39,0.6);
    border-radius: 12px;
    border: 1px solid #1f2937;
    padding: 12px;
}
.stButton>button {
    background: linear-gradient(135deg,#2563eb,#38bdf8);
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY
# =========================================================

DEFAULT = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": []
}

def load():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE))
        except:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save():
    try:
        json.dump(st.session_state.memory, open(MEMORY_FILE, "w"), indent=2)
    except:
        pass

def log(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save()

if "memory" not in st.session_state:
    st.session_state.memory = load()

mem = st.session_state.memory

# =========================================================
# ARCHITECTURE DOMAINS
# =========================================================

ARCH = {
    "Residential": ["House","Apartment","Villa"],
    "Commercial": ["Office","School","Hospital","Hotel"],
    "Industrial": ["Warehouse","Factory","Plant"]
}

def domain_of(t):
    for k,v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

# =========================================================
# BASE DESIGN ENGINE
# =========================================================

def base_design(btype, bedrooms):

    domain = domain_of(btype)

    return {
        "type": btype,
        "domain": domain,
        "rooms": ["Space"] * random.randint(3,8),
        "structure": {
            "columns": random.randint(10,30),
            "beams": random.randint(20,60)
        },
        "cost": random.randint(200000, 3000000),
        "bedrooms": bedrooms
    }

# =========================================================
# MUTATION ENGINE 🧬
# =========================================================

def mutate(design):

    mutated = json.loads(json.dumps(design))  # deep copy

    # structural mutation
    mutated["structure"]["columns"] += random.randint(-2, 3)
    mutated["structure"]["beams"] += random.randint(-5, 5)

    # room mutation
    if random.random() > 0.5:
        mutated["rooms"].append("Extra Module")

    # cost drift
    mutated["cost"] += random.randint(-100000, 200000)

    return mutated

# =========================================================
# FITNESS FUNCTION 🏆
# =========================================================

def fitness(d):

    structure_score = max(0, 100 - abs(d["structure"]["columns"] - 20))
    cost_score = max(0, 100 - (d["cost"] // 50000))
    complexity_score = min(100, len(d["rooms"]) * 10)

    return {
        "structure": structure_score,
        "cost": cost_score,
        "complexity": complexity_score
    }

def total_score(f):
    return int(sum(f.values()) / len(f))

# =========================================================
# EVOLUTION ENGINE 🌍
# =========================================================

def evolve_population(btype, bedrooms, generations=3, pop_size=5):

    population = [base_design(btype, bedrooms) for _ in range(pop_size)]
    history = []

    for g in range(generations):

        scored = []

        for d in population:
            f = fitness(d)
            d["fitness"] = f
            d["score"] = total_score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)

        best = scored[0]
        history.append({
            "generation": g,
            "best_score": best["score"]
        })

        # selection (top 50%)
        survivors = scored[:max(2, pop_size//2)]

        # reproduction (mutation)
        new_population = []

        for s in survivors:
            new_population.append(s)
            new_population.append(mutate(s))

        population = new_population[:pop_size]

    return scored[0], history, scored

# =========================================================
# PROJECT SYSTEM
# =========================================================

def new_project(name, t):
    mem["projects"].append({
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "type": t,
        "domain": domain_of(t),
        "created": datetime.now().isoformat()
    })
    save()
    log("Project created")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧬 RANDOM V8")
st.sidebar.caption("Evolutionary Architecture Intelligence System")

page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Projects",
    "Evolution Lab",
    "Memory"
])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🧬 RANDOM V8 Control Core")

    c1,c2,c3 = st.columns(3)
    c1.metric("Projects", len(mem["projects"]))
    c2.metric("Designs", len(mem["designs"]))
    c3.metric("Evolution Runs", len(mem["evolution"]))

    st.divider()
    st.subheader("System Log")

    for l in mem["logs"][-10:]:
        st.write(f"{l.get('time')} → {l.get('msg')}")

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":

    st.title("📁 Projects")

    name = st.text_input("Name")
    t = st.selectbox("Type", sum(ARCH.values(), []))

    if st.button("Create"):
        new_project(name, t)
        st.success("Created")

    for p in mem["projects"]:
        with st.expander(p["name"]):
            st.json(p)

# =========================================================
# EVOLUTION LAB 🧬
# =========================================================

elif page == "Evolution Lab":

    st.title("🧬 Evolutionary Design Lab")

    left,right = st.columns([1,2])

    with left:
        btype = st.selectbox("Building Type", sum(ARCH.values(), []))
        bedrooms = st.slider("Bedrooms", 1, 10, 3)
        gens = st.slider("Generations", 1, 8, 3)
        pop = st.slider("Population", 3, 10, 5)

        run = st.button("Evolve Architecture")

    if run:

        best, history, final_pop = evolve_population(
            btype, bedrooms, gens, pop
        )

        mem["evolution"].append({
            "id": str(uuid.uuid4())[:8],
            "best": best,
            "history": history,
            "created": datetime.now().isoformat()
        })

        save()
        log("Evolution run completed")

        st.success("Evolution Complete")

        st.subheader("🏆 Best Evolved Design")
        st.json(best)

        st.subheader("📈 Evolution Curve")

        st.line_chart([h["best_score"] for h in history])

        st.subheader("👥 Final Population")

        for d in final_pop:
            st.markdown(f"### Score: {d['score']}")
            st.json(d)

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 Memory System")

    tab1,tab2,tab3 = st.tabs(["Projects","Designs","Evolution"])

    with tab1:
        st.json(mem["projects"])

    with tab2:
        st.json(mem["designs"])

    with tab3:
        st.json(mem["evolution"])

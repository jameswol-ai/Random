# =========================================================
# RANDOM ARCHITECTURE INTELLIGENCE ENGINE
# EVOLUTION + COUNCIL + STRUCTURAL SIMULATION OS
# SINGLE FILE STREAMLIT MASTER BUILD
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
    page_title="Random Studio Engine OS",
    page_icon="📐",
    layout="wide"
)

MEMORY_FILE = Path("arc_memory.json")

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.03em;
}

.arc-blueprint-canvas {
    display:flex;
    flex-wrap:wrap;
    gap:16px;
    background:#0b0f1a;
    padding:20px;
    border-radius:12px;
}

.arc-room-module {
    flex:1 1 220px;
    padding:16px;
    border-radius:10px;
    color:white;
    border:1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT_STATE = {
    "projects": [],
    "designs": [],
    "logs": [],
    "evolution": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.load(open(MEMORY_FILE, "r"))
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        json.dump(st.session_state.memory, open(MEMORY_FILE, "w"), indent=2)
    except:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# init
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "active_design" not in st.session_state:
    st.session_state.active_design = None

if "history" not in st.session_state:
    st.session_state.history = []

mem = st.session_state.memory

# =========================================================
# ARCH SYSTEM
# =========================================================

ARCH = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Office", "Hotel", "Clinic"],
    "Industrial": ["Warehouse", "Factory"]
}

def domain(t):
    for k,v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

def base(btype, beds):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "type": btype,
        "domain": domain(btype),
        "bedrooms": beds,
        "area": 120 + beds * 18,
        "structure": {
            "columns": random.randint(14, 36),
            "beams": random.randint(28, 72)
        }
    }

def mutate(d):
    d = json.loads(json.dumps(d))
    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-4, 5)
    d["area"] += random.randint(-5, 20)
    return d

def fitness(d):
    r = d["structure"]["beams"] / max(1, d["structure"]["columns"])
    return max(0, 100 - abs(r - 2.1) * 20)

def run_evo(btype, beds, gens, pop):
    popu = [base(btype, beds) for _ in range(pop)]
    hist = []

    for _ in range(gens):
        scored = []
        for d in popu:
            d["score"] = fitness(d)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)
        hist.append(scored[0]["score"])

        survivors = scored[:max(2, pop//2)]
        popu = survivors + [mutate(random.choice(survivors)) for _ in survivors]
        popu = popu[:pop]

    return scored[0], hist

def floor(d):
    return [
        {"name":"Living","w":6,"h":5,"color":"#1e3a8a"},
        {"name":"Kitchen","w":4,"h":4,"color":"#065f46"}
    ] + [
        {"name":f"Bedroom {i+1}","w":4,"h":4,"color":"#4c1d95"}
        for i in range(d["bedrooms"])
    ]

# =========================================================
# COUNCIL SYSTEM (NEW UPGRADE)
# =========================================================

class Council:
    def evaluate(self, d):
        structural = min(100, d["structure"]["columns"] * 3)
        cost = 100 - random.randint(0, 30)
        spatial = min(100, len(floor(d)) * 8)

        agents = [
            {"agent":"Structural", "score":structural, "note":"Load balance assessed"},
            {"agent":"Cost", "score":cost, "note":"Budget pressure analyzed"},
            {"agent":"Spatial", "score":spatial, "note":"Room distribution evaluated"}
        ]

        final = int(sum(a["score"] for a in agents)/len(agents))

        verdict = "APPROVED" if final > 60 else "REVIEW REQUIRED"

        return {
            "agents": agents,
            "final": final,
            "verdict": verdict
        }

council = Council()

# =========================================================
# RENDER
# =========================================================

def render(plan):
    html = '<div class="arc-blueprint-canvas">'
    for r in plan:
        html += f"""
        <div class="arc-room-module" style="background:{r['color']}">
            <b>{r['name']}</b><br>
            {r['w']}m × {r['h']}m
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📐 ARC OS")

page = st.sidebar.radio("Mode", ["Dashboard", "Lab", "Memory"])

ARCH_FLAT = sum(ARCH.values(), [])

btype = st.sidebar.selectbox("Type", ARCH_FLAT)
beds = st.sidebar.slider("Beds", 1, 8, 3)
gens = st.sidebar.slider("Generations", 2, 15, 5)
pop = st.sidebar.slider("Population", 4, 20, 8)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":
    st.title("📐 ARC CONTROL CORE")

    c1,c2,c3 = st.columns(3)
    c1.metric("Designs", len(mem["designs"]))
    c2.metric("Evolution Runs", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

# =========================================================
# LAB
# =========================================================

elif page == "Lab":
    st.title("🌍 GENERATIVE LAB + COUNCIL")

    if st.button("Run Engine"):
        best, hist = run_evo(btype, beds, gens, pop)

        best["plan"] = floor(best)
        best["council"] = council.evaluate(best)

        mem["designs"].append(best)
        mem["evolution"].append({
            "id": str(uuid.uuid4())[:6],
            "best": best["id"],
            "score": best["score"]
        })

        st.session_state.active_design = best
        st.session_state.history = hist

        log_event(f"Generated {best['id']}")

    if st.session_state.active_design:
        d = st.session_state.active_design

        st.subheader(f"Design {d['id']}")

        a,b,c = st.columns(3)
        a.metric("Score", d["score"])
        b.metric("Area", d["area"])
        c.metric("Council", d["council"]["final"])

        tab1, tab2 = st.tabs(["Blueprint", "Council"])

        with tab1:
            render(d["plan"])

        with tab2:
            st.subheader("Council Report")
            for a in d["council"]["agents"]:
                st.write(a)

            st.success(d["council"]["verdict"])

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":
    st.title("🧠 SYSTEM MEMORY")
    st.json(mem)

    if st.button("Reset"):
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.active_design = None
        st.session_state.history = []
        save_memory()
        st.rerun()
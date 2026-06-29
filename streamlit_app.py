# =========================================================
# RANDOM V7 (BEAUTIFIED)
# Autonomous Architecture Intelligence System
# Multi-Agent + Scoring + Optimization Engine
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
    page_title="RANDOM V7",
    page_icon="🏗️",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# 🎨 PREMIUM UI THEME
# =========================================================

st.markdown("""
<style>

/* Background */
body {
    background: radial-gradient(circle at top, #0b1220, #050814);
}

/* Main container */
.main {
    background: transparent;
}

/* Headings */
h1 {
    color: #38bdf8;
    font-weight: 800;
    letter-spacing: 1px;
}

h2, h3 {
    color: #7dd3fc;
}

/* Cards (metrics) */
div[data-testid="metric-container"] {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.2);
    padding: 14px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #38bdf8);
    color: white;
    border-radius: 12px;
    padding: 0.6em 1em;
    border: none;
    font-weight: 600;
}

/* Expander */
details {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 10px;
    padding: 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0a1020;
    border-right: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY SYSTEM
# =========================================================

DEFAULT = {
    "projects": [],
    "designs": [],
    "logs": []
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

ARCHITECTURE = {
    "Residential": ["House", "Apartment", "Villa"],
    "Commercial": ["Office", "School", "Hospital", "Hotel"],
    "Industrial": ["Warehouse", "Factory", "Plant"]
}

def get_domain(btype):
    for k, v in ARCHITECTURE.items():
        if btype in v:
            return k
    return "Unknown"

# =========================================================
# ENGINE SYSTEM
# =========================================================

class Engine:
    def __init__(self, name):
        self.name = name

    def run(self, data):
        return {}

class RoomEngine(Engine):
    def run(self, data):

        d = data["domain"]
        b = data.get("bedrooms", 1)

        if d == "Residential":
            rooms = ["Living", "Kitchen", "Dining"] + [f"Bedroom {i+1}" for i in range(b)] + ["Bathroom"]
        elif d == "Commercial":
            rooms = ["Reception", "Office", "Meeting Room", "Storage"]
        elif d == "Industrial":
            rooms = ["Production Floor", "Storage", "Loading Bay", "Control Room"]
        else:
            rooms = ["Generic Space"]

        return {"rooms": rooms}

class GridEngine(Engine):
    def run(self, data):
        return {
            "grid": {
                "x": list("ABCDE"),
                "y": [1,2,3,4,5],
                "spacing": "6m x 6m"
            }
        }

class StructureEngine(Engine):
    def run(self, data):
        return {
            "structure": {
                "columns": random.randint(10, 40),
                "beams": random.randint(20, 80),
                "slabs": random.randint(5, 20)
            }
        }

class CostEngine(Engine):
    def run(self, data):
        return {
            "cost": {
                "estimate": random.randint(150000, 5000000),
                "currency": "USD"
            }
        }

ENGINES = [
    RoomEngine("Room"),
    GridEngine("Grid"),
    StructureEngine("Structure"),
    CostEngine("Cost")
]

# =========================================================
# AGENTS
# =========================================================

AGENTS = [
    "Architect AI",
    "Structural AI",
    "Cost AI",
    "Efficiency AI",
    "Safety AI"
]

def agent_score():
    return {
        "architecture": random.randint(60, 100),
        "structure": random.randint(60, 100),
        "cost": random.randint(50, 100),
        "efficiency": random.randint(60, 100),
        "safety": random.randint(70, 100)
    }

def total_score(s):
    return int(sum(s.values()) / len(s))

# =========================================================
# DESIGN ENGINE
# =========================================================

def generate_design(btype, bedrooms):

    domain = get_domain(btype)

    data = {
        "type": btype,
        "domain": domain,
        "bedrooms": bedrooms
    }

    result = {}

    for e in ENGINES:
        result.update(e.run(data))

    scores = agent_score()
    result["scores"] = scores
    result["score"] = total_score(scores)
    result["domain"] = domain

    return result

# =========================================================
# MULTI VARIANT ENGINE
# =========================================================

def generate_variants(btype, bedrooms, n=3):

    variants = [generate_design(btype, bedrooms) for _ in range(n)]
    best = max(variants, key=lambda x: x["score"])
    return variants, best

# =========================================================
# PROJECTS
# =========================================================

def new_project(name, ptype):
    if not name:
        return

    mem["projects"].append({
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "type": ptype,
        "domain": get_domain(ptype),
        "created": datetime.now().isoformat()
    })

    save()
    log(f"Project created: {name}")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏗 RANDOM V7")
st.sidebar.caption("Autonomous Architecture Intelligence System")

page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Projects",
    "Design Lab",
    "Agents",
    "Memory"
])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🏗 Control Center")

    c1,c2,c3 = st.columns(3)

    c1.metric("📁 Projects", len(mem["projects"]))
    c2.metric("🏗 Designs", len(mem["designs"]))
    c3.metric("📜 Logs", len(mem["logs"]))

    st.divider()
    st.subheader("📡 System Activity Stream")

    for l in mem["logs"][-10:][::-1]:
        st.markdown(
            f"""
            <div style="padding:10px;margin:6px 0;
            background:#0f172a;border-radius:10px;
            border:1px solid #1f2937">
            🕒 {l.get('time','')} <br>
            ⚡ {l.get('msg','')}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# PROJECTS
# =========================================================

elif page == "Projects":

    st.title("📁 Project Hub")

    name = st.text_input("Project Name")
    ptype = st.selectbox("Type", sum(ARCHITECTURE.values(), []))

    if st.button("Create Project"):
        new_project(name, ptype)
        st.success("Project Created")

    st.divider()

    for p in mem["projects"]:
        with st.expander(f"📁 {p['name']} ({p['domain']})"):
            st.json(p)

# =========================================================
# DESIGN LAB
# =========================================================

elif page == "Design Lab":

    st.title("🧠 AI Design Lab")

    left,right = st.columns([1,2])

    with left:
        btype = st.selectbox("Building Type", sum(ARCHITECTURE.values(), []))
        bedrooms = st.slider("Bedrooms", 1, 10, 3)
        run = st.button("Generate Variants")

    if run:

        variants, best = generate_variants(btype, bedrooms)

        design_pack = {
            "id": str(uuid.uuid4())[:8],
            "type": btype,
            "domain": get_domain(btype),
            "variants": variants,
            "best": best,
            "created": datetime.now().isoformat()
        }

        mem["designs"].append(design_pack)
        save()
        log("Design competition executed")

        st.success("Competition Complete")

        st.subheader("🏆 Winning Design")

        st.json(best)

        st.subheader("📊 Scoreboard")

        cols = st.columns(len(AGENTS))
        for i,(k,v) in enumerate(best["scores"].items()):
            cols[i].metric(k.capitalize(), v)

        with st.expander("All Variants"):
            for i,v in enumerate(variants):
                st.markdown(f"### Variant {i+1} — Score: {v['score']}")
                st.json(v)

# =========================================================
# AGENTS
# =========================================================

elif page == "Agents":

    st.title("🤖 AI Agents")

    for a in AGENTS:
        st.success(f"🟢 {a}")

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 Memory System")

    tab1,tab2,tab3 = st.tabs(["Projects","Designs","Logs"])

    with tab1:
        st.json(mem["projects"])

    with tab2:
        st.json(mem["designs"])

    with tab3:
        st.json(mem["logs"])

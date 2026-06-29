# =========================================================
# RANDOM V10
# Autonomous Civilization Operating System
# Multi-City + Economy + Competition + Evolution
# Single-File Streamlit Edition
# =========================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import copy

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="RANDOM V10",
    page_icon="🌐",
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
h1 { color: #38bdf8; }
h2,h3 { color: #7dd3fc; }

div[data-testid="metric-container"] {
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
# MEMORY (SAFE + STABLE)
# =========================================================

DEFAULT = {
    "cities": [],
    "logs": []
}

def safe_load():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                for k in DEFAULT:
                    data.setdefault(k, DEFAULT[k])
                return data
        except:
            return copy.deepcopy(DEFAULT)
    return copy.deepcopy(DEFAULT)

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
    st.session_state.memory = safe_load()

mem = st.session_state.memory

# =========================================================
# WORLD ECONOMY 🌍
# =========================================================

def generate_resources():
    return {
        "energy": random.randint(50, 100),
        "materials": random.randint(50, 100),
        "population": random.randint(50, 100),
        "tech": random.randint(40, 100)
    }

# =========================================================
# CITY CREATION 🏙
# =========================================================

def create_city(name):

    city = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "resources": generate_resources(),
        "health": random.randint(60, 100),
        "influence": random.randint(50, 100),
        "age": 0,
        "created": datetime.now().isoformat()
    }

    mem["cities"].append(city)
    save()
    log(f"City created: {name}")

    return city

# =========================================================
# CITY GOVERNANCE AI 🧠
# =========================================================

def govern(city):

    r = city["resources"]

    policy = {
        "build_rate": random.uniform(0.5, 1.5),
        "trade_focus": random.choice(["energy", "materials", "tech"]),
        "stability": random.randint(60, 100)
    }

    # resource drift
    r["energy"] += random.randint(-5, 5)
    r["materials"] += random.randint(-5, 5)
    r["population"] += random.randint(-3, 4)
    r["tech"] += random.randint(-2, 5)

    # clamp
    for k in r:
        r[k] = max(0, min(100, r[k]))

    return policy

# =========================================================
# CITY INTERACTION 🌐
# =========================================================

def interact(cities):

    for c in cities:
        for other in cities:
            if c["id"] == other["id"]:
                continue

            diff = c["resources"]["tech"] - other["resources"]["tech"]

            if diff > 20:
                c["influence"] += 2
                other["influence"] -= 2

            elif diff < -20:
                c["influence"] -= 2
                other["influence"] += 2

# =========================================================
# CITY EVOLUTION 🌱
# =========================================================

def evolve_city(city):

    city["age"] += 1

    gov = govern(city)

    city["health"] += random.randint(-3, 4)

    # resource influence
    city["health"] += (city["resources"]["tech"] // 20)

    city["health"] = max(0, min(100, city["health"]))

    return gov

# =========================================================
# WORLD SIMULATION LOOP 🌍
# =========================================================

def simulate_world():

    cities = mem["cities"]

    for c in cities:
        evolve_city(c)

    interact(cities)

    save()
    log("World simulation tick executed")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌐 RANDOM V10")
st.sidebar.caption("Autonomous Civilization OS")

page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "World",
    "Cities",
    "Simulation",
    "Memory"
])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🌐 Civilization Core Dashboard")

    c1,c2,c3 = st.columns(3)

    c1.metric("Cities", len(mem["cities"]))
    c2.metric("Avg Health", int(sum([c["health"] for c in mem["cities"]]) / len(mem["cities"])) if mem["cities"] else 0)
    c3.metric("Logs", len(mem["logs"]))

    st.divider()
    st.subheader("System Activity")

    for l in mem["logs"][-10:]:
        st.write(f"{l.get('time')} → {l.get('msg')}")

# =========================================================
# WORLD VIEW 🌍
# =========================================================

elif page == "World":

    st.title("🌍 World Overview")

    if not mem["cities"]:
        st.warning("No cities exist yet.")
    else:
        for c in mem["cities"]:
            st.subheader(c["name"])
            st.write("Health:", c["health"])
            st.write("Influence:", c["influence"])
            st.json(c["resources"])
            st.divider()

# =========================================================
# CITIES 🏙
# =========================================================

elif page == "Cities":

    st.title("🏙 City Registry")

    name = st.text_input("City Name")

    if st.button("Create City"):
        create_city(name)
        st.success("City Created")

    for c in mem["cities"]:
        with st.expander(c["name"]):
            st.json(c)

# =========================================================
# SIMULATION LOOP ⚙️
# =========================================================

elif page == "Simulation":

    st.title("⚙ World Simulation Engine")

    st.info("Run one tick of civilization evolution")

    if st.button("Run Simulation Tick"):
        simulate_world()
        st.success("Simulation Complete")

    if mem["cities"]:
        st.subheader("Live City Status")

        for c in mem["cities"]:
            st.write(f"{c['name']} → Health {c['health']} | Influence {c['influence']}")

# =========================================================
# MEMORY 🧠
# =========================================================

elif page == "Memory":

    st.title("🧠 System Memory")

    tab1,tab2 = st.tabs(["Cities","Logs"])

    with tab1:
        st.json(mem["cities"])

    with tab2:
        st.json(mem["logs"])

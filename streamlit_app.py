# =========================================================
# RANDOM V9
# City Evolution Architecture Intelligence System
# Stable Multi-Agent Evolution + City Simulation Layer
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
    page_title="RANDOM V9",
    page_icon="🌍",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# SAFE THEME
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
    border: 1px solid #1f2937;
    border-radius: 12px;
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
# MEMORY (CRASH-PROOF)
# =========================================================

DEFAULT = {
    "cities": [],
    "projects": [],
    "evolution": [],
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
        with open(MEMORY_FILE, "w") as f:
            json.dump(st.session_state.memory, f, indent=2)
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
# CITY SYSTEM 🌍
# =========================================================

ZONES = ["Central", "Residential", "Industrial", "Commercial"]

def create_city(name):
    city = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "zones": {
            z: {
                "buildings": random.randint(2, 5),
                "health": random.randint(60, 100)
            } for z in ZONES
        },
        "created": datetime.now().isoformat()
    }

    mem["cities"].append(city)
    save()
    log(f"City created: {name}")

    return city

# =========================================================
# ARCHITECTURE DOMAIN SYSTEM
# =========================================================

ARCH = {
    "Residential": ["House", "Apartment", "Villa"],
    "Commercial": ["Office", "School", "Hotel"],
    "Industrial": ["Warehouse", "Factory", "Plant"]
}

def domain_of(t):
    for k,v in ARCH.items():
        if t in v:
            return k
    return "Unknown"

# =========================================================
# DESIGN CORE
# =========================================================

def base_design(btype, zone):

    return {
        "type": btype,
        "domain": domain_of(btype),
        "zone": zone,
        "structure": {
            "columns": random.randint(10,30),
            "beams": random.randint(20,60)
        },
        "cost": random.randint(200000, 4000000),
        "population_fit": random.randint(60,100)
    }

# =========================================================
# MUTATION ENGINE 🧬
# =========================================================

def mutate(design):
    d = copy.deepcopy(design)

    d["structure"]["columns"] += random.randint(-2, 3)
    d["structure"]["beams"] += random.randint(-5, 5)

    d["cost"] += random.randint(-150000, 250000)
    d["population_fit"] += random.randint(-5, 5)

    d["population_fit"] = max(0, min(100, d["population_fit"]))

    return d

# =========================================================
# FITNESS FUNCTION 🏆
# =========================================================

def fitness(d):
    structure = max(0, 100 - abs(d["structure"]["columns"] - 20))
    cost = max(0, 100 - (d["cost"] // 60000))
    population = d["population_fit"]

    return {
        "structure": structure,
        "cost": cost,
        "population": population
    }

def score(f):
    return int(sum(f.values()) / len(f))

# =========================================================
# EVOLUTION ENGINE 🌱
# =========================================================

def evolve(zone, btype, generations=3, pop_size=5):

    population = [base_design(btype, zone) for _ in range(pop_size)]
    history = []

    for g in range(generations):

        scored = []

        for d in population:
            f = fitness(d)
            d["fitness"] = f
            d["score"] = score(f)
            scored.append(d)

        scored.sort(key=lambda x: x["score"], reverse=True)

        best = scored[0]
        history.append({
            "generation": g,
            "score": best["score"]
        })

        survivors = scored[:max(2, pop_size//2)]

        new_pop = []

        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate(s))

        population = new_pop[:pop_size]

    return scored[0], history, scored

# =========================================================
# CITY EVOLUTION 🌍
# =========================================================

def evolve_city(city_id):

    city = next(c for c in mem["cities"] if c["id"] == city_id)

    evolution_result = {
        "city_id": city_id,
        "zones": {},
        "time": datetime.now().isoformat()
    }

    for zone in city["zones"]:

        zone_data = city["zones"][zone]

        best, history, population = evolve(
            zone=zone,
            btype=random.choice(sum(ARCH.values(), [])),
            generations=3,
            pop_size=5
        )

        evolution_result["zones"][zone] = {
            "best": best,
            "history": history,
            "population": population
        }

        city["zones"][zone]["health"] = min(100, best["score"])

    mem["evolution"].append(evolution_result)
    save()
    log(f"City evolved: {city_id}")

    return evolution_result

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌍 RANDOM V9")
st.sidebar.caption("City Evolution Intelligence System")

page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Cities",
    "City Lab",
    "Memory"
])

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("🌍 City Intelligence Core")

    c1,c2,c3 = st.columns(3)

    c1.metric("Cities", len(mem["cities"]))
    c2.metric("Evolution Runs", len(mem["evolution"]))
    c3.metric("Logs", len(mem["logs"]))

    st.divider()
    st.subheader("System Activity")

    for l in mem["logs"][-10:]:
        st.write(f"{l.get('time')} → {l.get('msg')}")

# =========================================================
# CITIES
# =========================================================

elif page == "Cities":

    st.title("🏙 City Registry")

    name = st.text_input("City Name")

    if st.button("Create City"):
        create_city(name)
        st.success("City Created")

    st.divider()

    for c in mem["cities"]:
        with st.expander(c["name"]):
            st.json(c)

# =========================================================
# CITY LAB 🌍
# =========================================================

elif page == "City Lab":

    st.title("🌍 City Evolution Lab")

    if len(mem["cities"]) == 0:
        st.warning("Create a city first.")
    else:

        city_names = {c["name"]: c["id"] for c in mem["cities"]}
        selected = st.selectbox("Select City", list(city_names.keys()))

        if st.button("Evolve City"):

            result = evolve_city(city_names[selected])

            st.success("Evolution Complete")

            st.subheader("Zone Health Overview")

            for zone, data in result["zones"].items():
                st.write(f"{zone}: {data['best']['score']}")

# =========================================================
# MEMORY
# =========================================================

elif page == "Memory":

    st.title("🧠 System Memory")

    tab1,tab2,tab3 = st.tabs(["Cities","Evolution","Logs"])

    with tab1:
        st.json(mem["cities"])

    with tab2:
        st.json(mem["evolution"])

    with tab3:
        st.json(mem["logs"])

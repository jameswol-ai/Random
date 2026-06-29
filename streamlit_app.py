# =========================================================
# RANDOM V11
# Civilization Intelligence Universe OS
# Multi-City + Migration + Trade + Alliances + Evolution
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
    page_title="RANDOM V11",
    page_icon="🌐",
    layout="wide"
)

MEMORY_FILE = Path("random_memory.json")

# =========================================================
# SAFE MEMORY CORE
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
# WORLD CONSTANTS 🌍
# =========================================================

RESOURCES = ["energy", "materials", "tech", "population"]

def gen_resources():
    return {r: random.randint(40, 100) for r in RESOURCES}

# =========================================================
# CITY CREATION 🏙
# =========================================================

def create_city(name):

    city = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "resources": gen_resources(),
        "health": random.randint(60, 100),
        "stability": random.randint(50, 100),
        "alliances": [],
        "enemies": [],
        "created": datetime.now().isoformat()
    }

    mem["cities"].append(city)
    save()
    log(f"City founded: {name}")

    return city

# =========================================================
# GOVERNANCE AI 🧠
# =========================================================

def govern(city):

    r = city["resources"]

    policy = {
        "growth_focus": random.choice(["tech", "population", "energy"]),
        "trade_openness": random.randint(40, 100),
        "stability_focus": random.randint(40, 100)
    }

    # resource drift
    for k in r:
        r[k] += random.randint(-5, 5)
        r[k] = max(0, min(100, r[k]))

    return policy

# =========================================================
# MIGRATION SYSTEM 🚶‍♂️🌍
# =========================================================

def migration(cities):

    if len(cities) < 2:
        return

    for c in cities:
        if c["resources"]["population"] < 50:
            target = random.choice([x for x in cities if x["id"] != c["id"]])
            transfer = random.randint(1, 5)

            c["resources"]["population"] += transfer
            target["resources"]["population"] -= transfer

# =========================================================
# TRADE SYSTEM 💰
# =========================================================

def trade(cities):

    for c in cities:
        partner = random.choice(cities)

        if c["id"] == partner["id"]:
            continue

        resource = random.choice(RESOURCES)

        if c["resources"][resource] > partner["resources"][resource]:
            c["resources"][resource] -= 2
            partner["resources"][resource] += 2

# =========================================================
# ALLIANCE SYSTEM 🤝
# =========================================================

def diplomacy(cities):

    for c in cities:
        other = random.choice(cities)

        if c["id"] == other["id"]:
            continue

        if random.random() > 0.7:
            if other["id"] not in c["alliances"]:
                c["alliances"].append(other["id"])

# =========================================================
# COLLAPSE SYSTEM 📉
# =========================================================

def collapse_check(city):

    if city["health"] < 20 or city["stability"] < 20:
        city["resources"]["population"] -= random.randint(5, 15)

        if city["resources"]["population"] < 10:
            city["health"] = 0

# =========================================================
# EVOLUTION STEP 🌱
# =========================================================

def evolve_city(city):

    gov = govern(city)

    city["health"] += random.randint(-3, 4)
    city["stability"] += random.randint(-2, 3)

    city["health"] = max(0, min(100, city["health"]))
    city["stability"] = max(0, min(100, city["stability"]))

    collapse_check(city)

    return gov

# =========================================================
# WORLD SIMULATION 🌐
# =========================================================

def world_tick():

    cities = mem["cities"]

    for c in cities:
        evolve_city(c)

    migration(cities)
    trade(cities)
    diplomacy(cities)

    save()
    log("World tick executed")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌐 RANDOM V11")
st.sidebar.caption("Civilization Intelligence Universe")

page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "World",
    "Cities",
    "Simulation",
    "Memory"
])

# =========================================================
# DASHBOARD 📊
# =========================================================

if page == "Dashboard":

    st.title("🌐 Civilization Control Core")

    c1,c2,c3 = st.columns(3)

    c1.metric("Cities", len(mem["cities"]))

    avg_health = (
        sum(c["health"] for c in mem["cities"]) / len(mem["cities"])
        if mem["cities"] else 0
    )

    c2.metric("Avg Health", round(avg_health, 1))
    c3.metric("Logs", len(mem["logs"]))

    st.divider()

    st.subheader("System Activity")

    for l in mem["logs"][-10:]:
        st.write(f"{l.get('time')} → {l.get('msg')}")

# =========================================================
# WORLD VIEW 🌍
# =========================================================

elif page == "World":

    st.title("🌍 World State")

    if not mem["cities"]:
        st.warning("No cities exist yet.")
    else:
        for c in mem["cities"]:
            st.subheader(c["name"])
            st.write(f"Health: {c['health']} | Stability: {c['stability']}")
            st.json(c["resources"])
            st.write(f"🤝 Alliances: {len(c['alliances'])}")
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
# SIMULATION ⚙️
# =========================================================

elif page == "Simulation":

    st.title("⚙ World Simulation Engine")

    st.info("Each tick evolves civilization dynamics")

    if st.button("Run World Tick"):
        world_tick()
        st.success("Simulation complete")

    if mem["cities"]:
        st.subheader("Live City Status")

        for c in mem["cities"]:
            st.write(
                f"{c['name']} → H:{c['health']} "
                f"S:{c['stability']} "
                f"P:{c['resources']['population']}"
            )

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

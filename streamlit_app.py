# =========================================================
# RANDOM V23
# AI Council Architecture OS (Playable Debate Engine)
# =========================================================

import streamlit as st
import uuid
import random
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Random V23 Council OS",
    page_icon="🏛️",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "memory" not in st.session_state:
    st.session_state.memory = {
        "designs": [],
        "logs": []
    }

if "debate_log" not in st.session_state:
    st.session_state.debate_log = []

if "final_design" not in st.session_state:
    st.session_state.final_design = None

mem = st.session_state.memory

# =========================================================
# 🎭 AI COUNCIL MEMBERS
# =========================================================

COUNCIL = [
    "🏗 Chief Architect",
    "🧠 Structural Analyst",
    "💰 Cost Engineer",
    "🌱 Sustainability Agent",
    "📋 Compliance Officer",
    "⚡ Chaos Agent"
]

def agent_opinion(goal):
    """Each agent produces a biased evaluation"""
    return {
        "🏗 Chief Architect": f"Design coherence score is strong. Prioritize spatial harmony for '{goal}'.",
        "🧠 Structural Analyst": "Beam-column ratios must remain stable under load simulations.",
        "💰 Cost Engineer": "Budget risk detected. Material optimization required.",
        "🌱 Sustainability Agent": "Recommend low-carbon materials and passive cooling systems.",
        "📋 Compliance Officer": "Ensure adherence to zoning + structural code constraints.",
        "⚡ Chaos Agent": "Break symmetry. Add unconventional spatial distortion for innovation."
    }

def vote_score():
    return random.randint(60, 98)

# =========================================================
# 🧪 DESIGN GENERATOR (CORE ENGINE)
# =========================================================

def generate_design(goal):
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "goal": goal,
        "area": random.randint(120, 600),
        "cost": random.randint(100000, 900000),
        "score": random.randint(65, 95),
        "rooms": ["Living", "Kitchen", "Bath"] + ["Room"] * random.randint(2, 6),
        "structure": {
            "columns": random.randint(12, 40),
            "beams": random.randint(25, 80)
        }
    }

# =========================================================
# 🏛️ COUNCIL DEBATE ENGINE (V23 CORE FEATURE)
# =========================================================

def run_council_debate(goal):
    debate = []
    votes = []

    opinions = agent_opinion(goal)

    for agent in COUNCIL:
        stance = opinions[agent]
        score = vote_score()

        votes.append(score)

        debate.append({
            "agent": agent,
            "statement": stance,
            "vote": score
        })

    final_score = sum(votes) / len(votes)

    return debate, final_score

# =========================================================
# 🎮 UI NAVIGATION
# =========================================================

st.sidebar.title("🏛️ V23 Council OS")

page = st.sidebar.radio(
    "Control Panel",
    [
        "🏠 Dashboard",
        "🧪 Playable Council",
        "📊 Evolution History",
        "🧠 Memory"
    ]
)

# =========================================================
# 🏠 DASHBOARD
# =========================================================

if page == "🏠 Dashboard":
    st.title("🏛️ Random V23 Architecture Council")

    col1, col2 = st.columns(2)

    col1.metric("Stored Designs", len(mem["designs"]))
    col2.metric("Debates Run", len(mem["logs"]))

    st.markdown("### ⚡ Latest Activity")

    for log in reversed(mem["logs"][-5:]):
        st.write(f"🕒 {log['time'][11:19]} → {log['msg']}")

# =========================================================
# 🧪 PLAYABLE COUNCIL MODE
# =========================================================

elif page == "🧪 Playable Council":
    st.title("🏛️ AI Council Debate System (Playable)")

    goal = st.text_input("Define your architectural mission:", "Futuristic eco villa on hillside")

    if st.button("⚔️ Run Council Debate", use_container_width=True):

        st.markdown("## 🧠 Council Debate Begins...\n")

        debate, score = run_council_debate(goal)

        st.session_state.debate_log = debate

        # show debate
        for d in debate:
            st.markdown(f"""
### {d['agent']}
- 💬 {d['statement']}
- 🗳 Vote: **{d['vote']}**
""")

        st.markdown("---")
        st.success(f"🏛️ Council Consensus Score: {score:.2f}")

        # final design generation
        design = generate_design(goal)
        design["council_score"] = score

        st.session_state.final_design = design

        mem["designs"].append(design)
        mem["logs"].append({
            "time": datetime.now().isoformat(),
            "msg": f"Council generated design {design['id']} (score {score:.1f})"
        })

    # FINAL OUTPUT PANEL
    if st.session_state.final_design:
        d = st.session_state.final_design

        st.markdown("## 🏗 Final Council-Approved Design")

        c1, c2, c3 = st.columns(3)
        c1.metric("Council Score", f"{d['council_score']:.2f}")
        c2.metric("Area", f"{d['area']} m²")
        c3.metric("Budget", f"${d['cost']:,}")

        st.markdown("### 🧱 Structure")
        st.json(d["structure"])

        st.markdown("### 🧩 Rooms")
        st.write(d["rooms"])

# =========================================================
# 📊 EVOLUTION HISTORY
# =========================================================

elif page == "📊 Evolution History":
    st.title("📊 Design Evolution Timeline")

    scores = [d.get("score", 0) for d in mem["designs"]]

    if scores:
        st.line_chart(scores)
    else:
        st.info("No evolution data yet.")

# =========================================================
# 🧠 MEMORY
# =========================================================

elif page == "🧠 Memory":
    st.title("🧠 System Memory")

    st.json(mem)

    if st.button("🧹 Reset Memory"):
        st.session_state.memory = {"designs": [], "logs": []}
        st.rerun()
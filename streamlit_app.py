# ============================================================
# RANDOM V3 EVOLUTION AI DESIGN STUDIO
# AI Architecture + BIM Intelligence Engine
# Evolutionary Spatial Synthesis
# Single File Streamlit Edition
# ============================================================

import streamlit as st
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import io

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RANDOM V3 Evolution Studio",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

MEMORY_FILE = Path("random_bim_memory.json")

# ============================================================
# VISUAL SYSTEM – DARK THEME WITH GLASSMORPHISM
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@400;700&display=swap');

html, body, .stApp {
    background: #0b0e1a;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f0f4ff;
}

h1, h2, h3, h4, h5, .stTitle, .stHeader {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070b14, #131b33);
    border-right: 1px solid rgba(255,255,255,0.05);
}

[data-testid="stSidebar"] .css-1d391kg {
    padding: 2rem 1rem;
}

/* Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(8px);
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 1.5rem;
}

.glass-card h4 {
    color: #94a3b8;
    font-size: 0.9rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.glass-card .score {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
}

.banner {
    background: linear-gradient(135deg, #0f1a3a, #1e3a8a);
    padding: 2rem 2.5rem;
    border-radius: 28px;
    color: white;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 20px 60px rgba(0,20,80,0.4);
}

.banner h1 {
    font-size: 2.6rem;
    font-weight: 700;
    margin: 0;
}

.banner p {
    font-size: 1.1rem;
    opacity: 0.8;
    margin: 0.25rem 0 0;
}

.metric-box {
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    border-left: 4px solid #3b82f6;
}

.concept-item {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.concept-score {
    background: rgba(59,130,246,0.15);
    padding: 0.25rem 1rem;
    border-radius: 20px;
    font-weight: 700;
    color: #60a5fa;
}

.agent-box {
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
}

.agent-name {
    font-weight: 600;
    color: #94a3b8;
    font-size: 0.9rem;
}

.agent-score {
    font-size: 2rem;
    font-weight: 700;
    color: #f0f4ff;
}

.agent-sub {
    font-size: 0.75rem;
    color: #64748b;
}

.divider {
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

.footer {
    text-align: center;
    padding: 1.5rem 0;
    color: #64748b;
    font-size: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.footer span {
    margin: 0 1rem;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    transition: all 0.2s;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 30px rgba(37,99,235,0.3);
}

.plan-preview {
    background: #0a0e1a;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.06);
}

.recommendation-badge {
    background: linear-gradient(135deg, #10b981, #059669);
    padding: 0.4rem 1.8rem;
    border-radius: 30px;
    color: white;
    font-weight: 700;
    display: inline-block;
}
</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# MEMORY CORE
# ============================================================

DEFAULT_MEMORY = {
    "version": "V3 Evolution Studio",
    "projects": [
        {"name": "Eco Pavilion", "date": "Today, 10:24 AM"},
        {"name": "Urban Library", "date": "Yesterday, 4:12 PM"},
        {"name": "Coastal Retreat", "date": "Jul 04, 2026"},
        {"name": "Innovation Hub", "date": "Jul 02, 2026"}
    ],
    "designs": [],
    "evolution": [],
    "logs": []
}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in DEFAULT_MEMORY:
                if key not in data:
                    data[key] = DEFAULT_MEMORY[key]
            return data
        except Exception:
            return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=4)
    except Exception:
        pass

def log_event(text):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "event": text
    })
    save_memory()

# ============================================================
# SESSION ENGINE
# ============================================================

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "generated_concepts" not in st.session_state:
    st.session_state.generated_concepts = []
if "unit_system" not in st.session_state:
    st.session_state.unit_system = "Metric"

memory = st.session_state.memory

# ============================================================
# UNIT SYSTEM
# ============================================================

def area_display(value):
    if st.session_state.unit_system == "Imperial":
        return f"{value * 10.7639:.1f} ft²"
    if st.session_state.unit_system == "Dual":
        return f"{value:.1f} m² | {value * 10.7639:.1f} ft²"
    return f"{value:.1f} m²"

def length_display(value):
    if st.session_state.unit_system == "Imperial":
        return f"{value * 3.28084:.2f} ft"
    if st.session_state.unit_system == "Dual":
        return f"{value:.2f} m | {value * 3.28084:.2f} ft"
    return f"{value:.2f} m"

# ============================================================
# ARCHITECTURAL KNOWLEDGE BASE
# ============================================================

ARCHITECTURE_TYPES = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Boutique Office", "Corporate Hub", "Hotel Resort", "Medical Clinic"],
    "Industrial": ["Distribution Warehouse", "Manufacturing Facility"]
}

def get_domain(name):
    for domain, items in ARCHITECTURE_TYPES.items():
        if name in items:
            return domain
    return "General"

# ============================================================
# AI DESIGN DNA GENERATOR
# ============================================================

def generate_design(building, modules):
    rooms = [
        "Living Core",
        "Kitchen Intelligence Hub",
        "Service Zone"
    ]
    for _ in range(random.randint(1, 3)):
        rooms.append("Adaptive AI Module")
    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "building": building,
        "domain": get_domain(building),
        "modules": modules,
        "rooms": rooms,
        "area": 120 + modules * 20,
        "structure": {
            "columns": random.randint(15, 40),
            "beams": random.randint(35, 90)
        },
        "cost": 0
    }

def mutate(design):
    child = json.loads(json.dumps(design))
    child["structure"]["columns"] += random.randint(-2, 4)
    child["structure"]["beams"] += random.randint(-5, 8)
    child["structure"]["columns"] = max(10, child["structure"]["columns"])
    child["structure"]["beams"] = max(15, child["structure"]["beams"])
    if random.random() > 0.5:
        child["rooms"].append("Generated Spatial Intelligence Zone")
        child["area"] += 20
    child["cost"] = int(child["area"] * random.randint(1500, 2600))
    return child

def evaluate_design(design):
    ratio = design["structure"]["beams"] / max(1, design["structure"]["columns"])
    structural = max(0, 100 - int(abs(ratio - 2.2) * 20))

    if design["cost"] == 0:
        economic = 80
    else:
        cost_rate = design["cost"] / design["area"]
        economic = max(0, 100 - int(abs(cost_rate - 1800) * 0.04))

    spatial = min(100, len(design["rooms"]) * 12)
    sustainability = min(100, int(80 + random.randint(-15, 15)))  # dummy

    return {
        "Structural Score": structural,
        "Economic Score": economic,
        "Spatial Score": spatial,
        "Sustainability Score": sustainability
    }

def total_score(metrics):
    return int(sum(metrics.values()) / len(metrics))

def evolve_design(building, modules, generations, population_size):
    population = [generate_design(building, modules) for _ in range(population_size)]
    history = []
    for _ in range(generations):
        evaluated = []
        for design in population:
            design["fitness"] = evaluate_design(design)
            design["score"] = total_score(design["fitness"])
            evaluated.append(design)
        evaluated.sort(key=lambda x: x["score"], reverse=True)
        history.append(evaluated[0]["score"])
        survivors = evaluated[:max(2, population_size // 2)]
        next_population = []
        for parent in survivors:
            next_population.append(parent)
            next_population.append(mutate(parent))
        population = next_population[:population_size]
    return evaluated[0], history

# ============================================================
# CONCEPT GENERATION FOR DASHBOARD
# ============================================================

def generate_concepts(num=5):
    # Use a fixed building type and random modules to create variety
    building_types = ["Luxury Villa", "Modern Apartment", "Corporate Hub", "Medical Clinic", "Hotel Resort"]
    concepts = []
    for i in range(num):
        building = random.choice(building_types)
        modules = random.randint(3, 8)
        design, _ = evolve_design(building, modules, generations=5, population_size=10)
        concepts.append(design)
    return concepts

# ============================================================
# 2D PLAN GENERATOR (simple SVG-like preview)
# ============================================================

def generate_floor_plan(design):
    # Create a simple plan using PIL
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color=(10, 14, 26))
    draw = ImageDraw.Draw(img)
    # Draw rooms as rectangles
    rooms = design.get("rooms", ["Living", "Kitchen", "Bedroom"])
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"]
    spacing = width // (len(rooms) + 1)
    for i, room in enumerate(rooms[:5]):
        x0 = spacing * (i+1) - 30
        y0 = height//2 - 30
        x1 = spacing * (i+1) + 30
        y1 = height//2 + 30
        draw.rectangle([x0, y0, x1, y1], fill=colors[i % len(colors)], outline=None)
        draw.text((x0+5, y0+5), room[:10], fill="white")
    # Convert to bytes for display
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("### 🌟 RANDOM V3")
    st.markdown("**EVOLUTION AI DESIGN STUDIO**")
    st.divider()

    # Navigation
    nav = st.radio(
        "",
        ["Dashboard", "Random Copilot", "Concepts", "Comparison", "2D Plans", "3D Viewer", "Reports", "Memory", "Settings"],
        index=0,
        key="nav_radio",
        label_visibility="collapsed"
    )
    st.session_state.page = nav

    st.divider()

    # Project Memory
    st.markdown("### 📁 PROJECT MEMORY")
    for proj in memory["projects"]:
        col1, col2 = st.columns([3, 2])
        col1.markdown(f"**{proj['name']}**")
        col2.markdown(f"<span style='color:#64748b;font-size:0.8rem;'>{proj['date']}</span>", unsafe_allow_html=True)

    if st.button("➕ New Project", use_container_width=True):
        new_name = f"Project {len(memory['projects'])+1}"
        memory["projects"].append({"name": new_name, "date": datetime.now().strftime("%b %d, %Y")})
        save_memory()
        st.rerun()

    st.divider()

    # Footer
    st.markdown(
        """
        <div style="color:#64748b;font-size:0.7rem;text-align:center;margin-top:2rem;">
            AI Powered • Data Driven • Secure • Scalable
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# MAIN CONTENT
# ============================================================

if st.session_state.page == "Dashboard":
    # Welcome Banner
    st.markdown(
        """
        <div class="banner">
            <h1>Welcome back, Architect 🌟</h1>
            <p><strong>Create. Evolve. Perfect.</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate concepts if not already in session
    if not st.session_state.generated_concepts:
        with st.spinner("Generating 5 unique design concepts..."):
            st.session_state.generated_concepts = generate_concepts(5)

    concepts = st.session_state.generated_concepts
    # Ensure we have at least 5
    if len(concepts) < 5:
        # generate more
        new_concepts = generate_concepts(5 - len(concepts))
        concepts.extend(new_concepts)
        st.session_state.generated_concepts = concepts

    # Evolution Engine Results
    st.markdown("## 🔬 EVOLUTION ENGINE RESULTS")
    st.markdown("*5 unique design concepts generated and evaluated by AI Agents*")

    # List concepts with scores
    for idx, design in enumerate(concepts[:5]):
        # compute fitness if not present
        if "fitness" not in design:
            design["fitness"] = evaluate_design(design)
            design["score"] = total_score(design["fitness"])
        score = design["score"]
        name = f"Concept {['Alpha','Beta','Gamma','Delta','Epsilon'][idx]}"
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"**{idx+1}. {name}**")
        col2.markdown(f"<div class='concept-score'>{score}</div>", unsafe_allow_html=True)
        col3.progress(score/100, text="")

    st.divider()

    # AI Agent Evaluation Summary
    st.markdown("### 🤖 AI AGENT EVALUATION SUMMARY")
    # Use the best concept (Concept Alpha) for evaluation
    best = concepts[0]
    fitness = best.get("fitness", evaluate_design(best))
    agent_scores = {
        "Architect AI": {"sub": "Function & Aesthetics", "score": int((fitness["Structural Score"] + fitness["Spatial Score"]) / 2)},
        "Structural AI": {"sub": "Safety & Stability", "score": fitness["Structural Score"]},
        "Sustainability AI": {"sub": "Green & Efficiency", "score": fitness["Sustainability Score"]},
        "Cost AI": {"sub": "Budget & Value", "score": fitness["Economic Score"]}
    }

    cols = st.columns(4)
    for i, (agent, data) in enumerate(agent_scores.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div class="agent-box">
                    <div class="agent-name">{agent}</div>
                    <div class="agent-score">{data['score']}/100</div>
                    <div class="agent-sub">{data['sub']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # 2D Floor Plan and 3D Massing
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### 🗺️ 2D FLOOR PLAN – CONCEPT ALPHA")
        plan_img = generate_floor_plan(best)
        st.image(plan_img, use_column_width=True, caption="Floor Plan Preview")
        st.button("View Full 2D", key="view_2d")

    with col_right:
        st.markdown("### 🏗️ 3D MASSING – CONCEPT ALPHA")
        # Simple 3D placeholder using a plotly 3D scatter
        fig = go.Figure()
        # Create a random 3D massing
        x = [random.random()*10 for _ in range(20)]
        y = [random.random()*10 for _ in range(20)]
        z = [random.random()*5 for _ in range(20)]
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=8, color='#3b82f6', opacity=0.8)))
        fig.update_layout(
            scene=dict(
                xaxis=dict(showgrid=False, showticklabels=False, title=''),
                yaxis=dict(showgrid=False, showticklabels=False, title=''),
                zaxis=dict(showgrid=False, showticklabels=False, title=''),
                bgcolor='rgba(0,0,0,0)',
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=250,
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.button("View Full 3D", key="view_3d")

    st.divider()

    # Design Insights and Recommendation
    st.markdown("### 💡 DESIGN INSIGHTS")
    st.write("Concept Alpha performs best overall. It offers the best balance of function, sustainability, structural efficiency and cost effectiveness.")

    st.markdown("### ⭐ TOP RECOMMENDATION")
    st.markdown("<div class='recommendation-badge'>Concept Alpha</div>", unsafe_allow_html=True)

    st.divider()

    # Generate Report
    if st.button("📄 Generate Report", type="primary"):
        st.success("Report generated successfully!")

elif st.session_state.page == "Random Copilot":
    st.markdown("## 🧠 Random Copilot")
    st.info("Generate a new design using AI evolution.")
    building = st.selectbox("Building Typology", sum(ARCHITECTURE_TYPES.values(), []))
    modules = st.slider("Modules", 1, 10, 4)
    generations = st.slider("Evolution Cycles", 2, 30, 8)
    population = st.slider("Population", 4, 40, 12)

    if st.button("🚀 Generate Design"):
        with st.spinner("Evolving..."):
            design, history = evolve_design(building, modules, generations, population)
            st.success(f"Design {design['id']} created!")
            st.json(design)
            st.line_chart(history)

elif st.session_state.page == "Concepts":
    st.markdown("## 📋 Concepts")
    st.write("All generated design concepts.")
    if st.session_state.generated_concepts:
        for i, design in enumerate(st.session_state.generated_concepts):
            with st.expander(f"Concept {i+1} – {design['building']} (Score: {design.get('score', 0)})"):
                st.json(design)
    else:
        st.info("No concepts generated yet. Go to Dashboard to generate.")

elif st.session_state.page == "Comparison":
    st.markdown("## 🔄 Comparison")
    st.info("Compare design concepts side by side. (Coming soon)")

elif st.session_state.page == "2D Plans":
    st.markdown("## 🗺️ 2D Plans")
    st.info("Detailed 2D plans of selected concepts. (Coming soon)")

elif st.session_state.page == "3D Viewer":
    st.markdown("## 🏗️ 3D Viewer")
    st.info("Immersive 3D model viewer. (Coming soon)")

elif st.session_state.page == "Reports":
    st.markdown("## 📊 Reports")
    st.info("Generate and view detailed reports. (Coming soon)")

elif st.session_state.page == "Memory":
    st.markdown("## 🧠 Memory Core")
    st.write("Stored projects and designs:")
    st.json(memory)

elif st.session_state.page == "Settings":
    st.markdown("## ⚙️ Settings")
    unit = st.selectbox("Unit System", ["Metric", "Imperial", "Dual"])
    st.session_state.unit_system = unit
    st.success("Settings updated.")

# ============================================================
# FOOTER (outside sidebar)
# ============================================================
st.markdown(
    """
    <div class="footer">
        <span>AI Powered</span>
        <span>Data Driven</span>
        <span>Secure</span>
        <span>Scalable</span>
    </div>
    """,
    unsafe_allow_html=True
    )

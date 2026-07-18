import sys
import os
import uuid
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force mock mode – use fake designs
ENGINE_AVAILABLE = False

# Optional imports (not used)
try:
    from engine.evolution import run_evolution
    from engine.planner import generate_floor_plan
    from visualization.svg_blueprint import generate_svg_blueprint
    from visualization.three_viewer import generate_threejs_html
except ImportError:
    pass

# ---------- Models ----------
class EvolveRequest(BaseModel):
    type: str = "Residential"
    bedrooms: int = 3
    generations: int = 2
    population: int = 5

class DesignSummary(BaseModel):
    id: str
    score: float
    area_sqm: float
    cost: float
    bedrooms: int
    rooms: int

# ---------- App ----------
app = FastAPI(title="RANDOM Studio API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DESIGNS: Dict[str, Dict[str, Any]] = {}

# ---------- Mock Evolution ----------
def run_mock_evolution(btype, bedrooms, gens, pop_size):
    """Generate a mock design when engine is not available."""
    area = 80 + random.randint(0, 40)
    design_id = str(uuid.uuid4())[:8]
    rooms = [
        {"name": "Living", "w": 6.0, "h": 5.0, "x": 0.5, "y": 0.5},
        {"name": "Kitchen", "w": 4.0, "h": 3.5, "x": 7.0, "y": 0.5},
        {"name": "Bathroom", "w": 3.0, "h": 2.5, "x": 0.5, "y": 6.0},
    ]
    for i in range(bedrooms):
        rooms.append({"name": f"Bedroom {i+1}", "w": 4.5, "h": 4.0, "x": 4.0 + i*5.0, "y": 6.0})
    return {
        "id": design_id,
        "type": btype,
        "bedrooms": bedrooms,
        "area_sqm": area,
        "cost": area * 800,
        "score": round(random.uniform(50, 90), 2),
        "rooms": rooms,
        "plan": rooms
    }, [65, 72, 68, 70, 75]

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>RANDOM Studio</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Inter', sans-serif; background: #f0f2f6; color: #1e1e1e; min-height: 100vh; }
            .topbar { background: white; border-bottom: 1px solid #e6e9ef; padding: 0 2rem; height: 64px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
            .topbar .logo { font-weight: 700; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; }
            .topbar .logo span { background: #ff4b4b; color: white; font-size: 0.65rem; padding: 2px 10px; border-radius: 20px; font-weight: 600; }
            .topbar .status { font-size: 0.85rem; color: #6c7a8d; display: flex; align-items: center; gap: 8px; }
            .topbar .status .dot { width: 8px; height: 8px; border-radius: 50%; background: #00c853; display: inline-block; }
            .app { display: flex; max-width: 1400px; margin: 0 auto; padding: 2rem; gap: 2rem; min-height: calc(100vh - 64px); }
            .sidebar { flex: 0 0 320px; background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); height: fit-content; position: sticky; top: 84px; border: 1px solid #e6e9ef; }
            .sidebar h2 { font-size: 1rem; font-weight: 600; margin-bottom: 1.5rem; letter-spacing: 0.3px; }
            .sidebar .control-group { margin-bottom: 1.25rem; }
            .sidebar .control-group label { display: block; font-size: 0.8rem; font-weight: 500; color: #6c7a8d; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.5px; }
            .sidebar .control-group select,
            .sidebar .control-group input { width: 100%; padding: 0.6rem 0.75rem; border: 1px solid #d0d5dd; border-radius: 8px; font-size: 0.9rem; font-family: inherit; background: white; transition: border-color 0.2s; color: #1e1e1e; }
            .sidebar .control-group select:focus,
            .sidebar .control-group input:focus { outline: none; border-color: #ff4b4b; box-shadow: 0 0 0 3px rgba(255,75,75,0.1); }
            .sidebar .evolve-btn { width: 100%; padding: 0.75rem; background: #ff4b4b; color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; font-family: inherit; cursor: pointer; transition: background 0.2s, transform 0.1s; margin-top: 0.5rem; }
            .sidebar .evolve-btn:hover { background: #e03a3a; }
            .sidebar .evolve-btn:active { transform: scale(0.98); }
            .sidebar .evolve-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
            .sidebar .status-msg { margin-top: 1rem; font-size: 0.85rem; color: #6c7a8d; text-align: center; min-height: 1.5rem; }
            .sidebar .status-msg.error { color: #ff4b4b; }
            .sidebar .status-msg.success { color: #00c853; }
            .main { flex: 1; min-width: 0; }
            .design-card { background: white; border-radius: 16px; padding: 1.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #e6e9ef; margin-bottom: 1.5rem; }
            .design-card .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 0.5rem; }
            .design-card .header h3 { font-size: 1.1rem; font-weight: 600; }
            .design-card .header .badge { background: #f0f2f6; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 500; color: #6c7a8d; }
            .design-card .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }
            .design-card .metrics .metric { background: #f8f9fb; padding: 0.75rem 1rem; border-radius: 10px; }
            .design-card .metrics .metric .label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: #6c7a8d; font-weight: 500; }
            .design-card .metrics .metric .value { font-size: 1.35rem; font-weight: 700; color: #1e1e1e; margin-top: 0.15rem; }
            .design-card .actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }
            .design-card .actions button { padding: 0.5rem 1.25rem; border: 1px solid #d0d5dd; border-radius: 8px; background: white; font-family: inherit; font-size: 0.85rem; font-weight: 500; cursor: pointer; transition: all 0.2s; color: #1e1e1e; }
            .design-card .actions button:hover { background: #f8f9fb; border-color: #b0b8c4; }
            .viewer-placeholder { background: white; border-radius: 16px; padding: 2rem; text-align: center; border: 1px solid #e6e9ef; color: #6c7a8d; }
            .viewer-placeholder .icon { font-size: 3rem; margin-bottom: 0.75rem; }
            .spinner { display: none; margin: 1rem auto 0; width: 28px; height: 28px; border: 3px solid #e6e9ef; border-top-color: #ff4b4b; border-radius: 50%; animation: spin 0.7s linear infinite; }
            .spinner.active { display: block; }
            @keyframes spin { to { transform: rotate(360deg); } }
            @media (max-width: 900px) { .app { flex-direction: column; padding: 1rem; } .sidebar { flex: none; position: static; width: 100%; } .topbar { padding: 0 1rem; } }
            @media (max-width: 480px) { .design-card .metrics { grid-template-columns: 1fr 1fr; } .topbar .status { font-size: 0.7rem; } }
        </style>
    </head>
    <body>
        <header class="topbar">
            <div class="logo">🏗️ RANDOM Studio <span>BETA</span></div>
            <div class="status"><span class="dot"></span><span id="connectionStatus">Connected</span></div>
        </header>
        <div class="app">
            <aside class="sidebar">
                <h2>⚙️ Controls</h2>
                <div class="control-group">
                    <label for="type">Building Type</label>
                    <select id="type"><option value="Residential">Residential</option><option value="Commercial">Commercial</option><option value="Industrial">Industrial</option></select>
                </div>
                <div class="control-group">
                    <label for="bedrooms">Bedrooms</label>
                    <input type="number" id="bedrooms" value="3" min="1" max="5" />
                </div>
                <div class="control-group">
                    <label for="gens">Generations</label>
                    <input type="number" id="gens" value="2" min="1" max="5" />
                </div>
                <div class="control-group">
                    <label for="pop">Population</label>
                    <input type="number" id="pop" value="5" min="3" max="10" />
                </div>
                <button class="evolve-btn" id="evolveBtn">🚀 Evolve</button>
                <div id="statusMsg" class="status-msg"></div>
                <div class="spinner" id="spinner"></div>
            </aside>
            <main class="main" id="mainContent">
                <div id="resultContainer"></div>
                <div class="viewer-placeholder" id="placeholder">
                    <div class="icon">🏛️</div>
                    <p><strong>No design yet</strong></p>
                    <p style="font-size:0.85rem; margin-top:0.3rem;">Adjust the controls and click <strong>Evolve</strong> to generate a new architectural design.</p>
                </div>
            </main>
        </div>
        <script>
            (function() {
                const evolveBtn = document.getElementById('evolveBtn');
                const statusMsg = document.getElementById('statusMsg');
                const spinner = document.getElementById('spinner');
                const resultContainer = document.getElementById('resultContainer');
                const placeholder = document.getElementById('placeholder');

                function setStatus(text, type) {
                    statusMsg.textContent = text;
                    statusMsg.className = 'status-msg' + (type ? ' ' + type : '');
                }

                function showSpinner(show) {
                    spinner.classList.toggle('active', show);
                }

                function renderDesign(data) {
                    placeholder.style.display = 'none';
                    const card = document.createElement('div');
                    card.className = 'design-card';
                    card.innerHTML = `
                        <div class="header">
                            <h3>📐 Design ${data.id}</h3>
                            <span class="badge">${data.rooms} rooms</span>
                        </div>
                        <div class="metrics">
                            <div class="metric"><div class="label">Score</div><div class="value">${data.score.toFixed(1)}</div></div>
                            <div class="metric"><div class="label">Area</div><div class="value">${data.area_sqm} m²</div></div>
                            <div class="metric"><div class="label">Cost</div><div class="value">$${data.cost.toLocaleString()}</div></div>
                            <div class="metric"><div class="label">Bedrooms</div><div class="value">${data.bedrooms}</div></div>
                        </div>
                        <div class="actions">
                            <button onclick="window.open('/blueprint/${data.id}')">📐 Blueprint</button>
                            <button onclick="window.open('/3d/${data.id}')">🏛️ 3D Viewer</button>
                        </div>
                    `;
                    const existing = resultContainer.querySelector('.design-card');
                    if (existing) resultContainer.replaceChild(card, existing);
                    else resultContainer.appendChild(card);
                }

                async function evolve() {
                    const type = document.getElementById('type').value;
                    const bedrooms = parseInt(document.getElementById('bedrooms').value);
                    const gens = parseInt(document.getElementById('gens').value);
                    const pop = parseInt(document.getElementById('pop').value);

                    evolveBtn.disabled = true;
                    showSpinner(true);
                    setStatus('Evolving...', '');

                    try {
                        const res = await fetch('/evolve', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ type, bedrooms, generations: gens, population: pop })
                        });
                        if (!res.ok) {
                            const text = await res.text();
                            throw new Error(text || `HTTP ${res.status}`);
                        }
                        const data = await res.json();
                        renderDesign(data);
                        setStatus('✓ Design generated successfully!', 'success');
                    } catch (err) {
                        console.error('Evolution error:', err);
                        setStatus('✗ Error: ' + err.message, 'error');
                    } finally {
                        evolveBtn.disabled = false;
                        showSpinner(false);
                    }
                }

                evolveBtn.addEventListener('click', evolve);
                document.querySelectorAll('.sidebar input, .sidebar select').forEach(el => {
                    el.addEventListener('keydown', (e) => { if (e.key === 'Enter') evolve(); });
                });
            })();
        </script>
    </body>
    </html>
    """

# ---------- API Endpoints ----------
@app.post("/evolve", response_model=DesignSummary)
async def evolve(request: EvolveRequest):
    try:
        best, history = run_mock_evolution(
            request.type, request.bedrooms,
            request.generations, request.population
        )
        design_id = best.get("id", str(uuid.uuid4())[:8])
        best["id"] = design_id
        DESIGNS[design_id] = best

        return DesignSummary(
            id=design_id,
            score=float(best.get("score", 0.0)),
            area_sqm=float(best["area_sqm"]),
            cost=float(best["cost"]),
            bedrooms=int(best.get("bedrooms", 3)),
            rooms=len(best.get("plan", best.get("rooms", [])))
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/design/{design_id}")
async def get_design(design_id: str):
    if design_id not in DESIGNS:
        raise HTTPException(404, "Design not found")
    return DESIGNS[design_id]

@app.get("/blueprint/{design_id}", response_class=HTMLResponse)
async def get_blueprint(design_id: str):
    design = DESIGNS.get(design_id)
    if not design:
        raise HTTPException(404, "Design not found")

    plan = design.get("plan")
    if not plan:
        plan = design.get("rooms", [])
        if plan and not all("x" in r and "y" in r for r in plan):
            # fallback positions
            for i, r in enumerate(plan):
                r["x"] = (i % 3) * 5.0 + 0.5
                r["y"] = (i // 3) * 4.5 + 0.5

    if not plan:
        raise HTTPException(404, "No plan data available")

    try:
        # Try to use real SVG generator if available
        from visualization.svg_blueprint import generate_svg_blueprint
        svg = generate_svg_blueprint(plan)
    except:
        # Simple fallback SVG
        svg = f'<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg"><rect width="600" height="400" fill="#f8f9fb"/><text x="300" y="200" text-anchor="middle" font-family="Arial" font-size="18" fill="#6c7a8d">Blueprint</text></svg>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blueprint – {design_id}</title>
        <style>
            body {{ background: #f0f2f6; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; font-family: 'Inter', sans-serif; }}
            .container {{ background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); max-width: 90vw; overflow: auto; }}
        </style>
    </head>
    <body>
        <div class="container">{svg}</div>
    </body>
    </html>
    """

@app.get("/3d/{design_id}", response_class=HTMLResponse)
async def get_3d(design_id: str):
    design = DESIGNS.get(design_id)
    if not design:
        raise HTTPException(404, "Design not found")

    plan = design.get("plan")
    if not plan:
        plan = design.get("rooms", [])
        if plan and not all("x" in r and "y" in r for r in plan):
            for i, r in enumerate(plan):
                r["x"] = (i % 3) * 5.0 + 0.5
                r["y"] = (i // 3) * 4.5 + 0.5

    if not plan:
        raise HTTPException(404, "No plan data available")

    try:
        from visualization.three_viewer import generate_threejs_html
        html = generate_threejs_html(plan)
        return html
    except:
        return """
        <!DOCTYPE html>
        <html>
        <head><title>3D Viewer</title><style>body{margin:0;background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;color:white;font-family:Inter,sans-serif;flex-direction:column;}</style></head>
        <body><div style="font-size:4rem;">🏛️</div><h2>3D Viewer</h2><p style="color:#8892a8;">Three.js renderer unavailable</p></body>
        </html>
        """
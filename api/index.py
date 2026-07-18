import sys
import os
import uuid
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Engine imports – make sure these exist
from engine.evolution import run_evolution
from engine.planner import generate_floor_plan
from visualization.svg_blueprint import generate_svg_blueprint
from visualization.three_viewer import generate_threejs_html
# If you have exports, uncomment later
# from engine.export_ifc import export_ifc
# from engine.export_gltf import generate_gltf

# ---------- Models ----------
class EvolveRequest(BaseModel):
    type: str = "Residential"
    bedrooms: int = 3
    generations: int = 2      # was 5 – Vercel-friendly
    population: int = 5       # was 20

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

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def root():
    # (Keep your existing HTML – we'll improve the JS in a moment)
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RANDOM Studio</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #f5f0eb; }
            .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .row { display: flex; gap: 10px; flex-wrap: wrap; align-items: end; }
            label { font-weight: bold; margin-right: 4px; }
            input, select, button { padding: 8px 12px; border-radius: 6px; border: 1px solid #ccc; font-size: 14px; }
            button { background: #1a73e8; color: white; border: none; cursor: pointer; font-weight: bold; }
            button:hover { background: #1557b0; }
            .btn-group { margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; }
            .btn-group button { background: #4a4a4a; }
            .btn-group button:hover { background: #2d2d2d; }
            .metric { display: inline-block; margin-right: 20px; }
            #result { margin-top: 20px; }
            #loading { display: none; margin: 10px 0; font-weight: bold; }
            #error { display: none; color: red; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🏗️ RANDOM Studio</h1>
        <div class="card">
            <h3>⚙️ Evolve a design</h3>
            <div class="row">
                <div><label>Type</label><select id="type"><option>Residential</option><option>Commercial</option></select></div>
                <div><label>Bedrooms</label><input id="bedrooms" type="number" value="3" min="1" max="5"></div>
                <div><label>Generations</label><input id="gens" type="number" value="2" min="1" max="5"></div>
                <div><label>Population</label><input id="pop" type="number" value="5" min="3" max="10"></div>
                <button onclick="evolve()" id="evolveBtn">🚀 Evolve</button>
            </div>
            <div id="loading">⏳ Evolving... (may take a few seconds)</div>
            <div id="error"></div>
        </div>
        <div id="result"></div>

        <script>
        async function evolve() {
            const btn = document.getElementById('evolveBtn');
            const loader = document.getElementById('loading');
            const errorDiv = document.getElementById('error');
            const resultDiv = document.getElementById('result');
            
            btn.disabled = true;
            loader.style.display = 'block';
            errorDiv.style.display = 'none';
            errorDiv.textContent = '';
            resultDiv.innerHTML = '';

            const type = document.getElementById('type').value;
            const bedrooms = parseInt(document.getElementById('bedrooms').value);
            const gens = parseInt(document.getElementById('gens').value);
            const pop = parseInt(document.getElementById('pop').value);

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
                resultDiv.innerHTML = `
                    <div class="card">
                        <h3>Design ${data.id}</h3>
                        <div class="metric">Score: <strong>${data.score.toFixed(2)}</strong></div>
                        <div class="metric">Area: <strong>${data.area_sqm} m²</strong></div>
                        <div class="metric">Cost: <strong>$${data.cost.toLocaleString()}</strong></div>
                        <div class="metric">Rooms: <strong>${data.rooms}</strong></div>
                        <div class="btn-group">
                            <button onclick="window.open('/blueprint/${data.id}')">📐 Blueprint</button>
                            <button onclick="window.open('/3d/${data.id}')">🏛️ 3D Viewer</button>
                            <!-- <button onclick="window.open('/export/ifc/${data.id}')">📄 IFC</button> -->
                            <!-- <button onclick="window.open('/export/gltf/${data.id}')">🔷 glTF</button> -->
                        </div>
                    </div>
                `;
            } catch (err) {
                errorDiv.textContent = 'Error: ' + err.message;
                errorDiv.style.display = 'block';
            } finally {
                btn.disabled = false;
                loader.style.display = 'none';
            }
        }
        </script>
    </body>
    </html>
    """

@app.post("/evolve", response_model=DesignSummary)
async def evolve(request: EvolveRequest):
    try:
        best, history = run_evolution(
            btype=request.type,
            bedrooms=request.bedrooms,
            gens=request.generations,
            pop_size=request.population
        )
        best["plan"] = generate_floor_plan(best)
        design_id = best.get("id", str(uuid.uuid4())[:8])
        best["id"] = design_id
        DESIGNS[design_id] = best
        if "cost" not in best:
            best["cost"] = best.get("area_sqm", 0) * 800
        return DesignSummary(
            id=design_id,
            score=best.get("score", 0.0),
            area_sqm=best["area_sqm"],
            cost=best["cost"],
            bedrooms=best.get("bedrooms", 3),
            rooms=len(best.get("plan", []))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/design/{design_id}")
async def get_design(design_id: str):
    if design_id not in DESIGNS:
        raise HTTPException(404, "Design not found")
    return DESIGNS[design_id]

@app.get("/blueprint/{design_id}", response_class=HTMLResponse)
async def get_blueprint(design_id: str):
    design = DESIGNS.get(design_id)
    if not design or "plan" not in design:
        raise HTTPException(404, "Design or plan not found")
    svg = generate_svg_blueprint(design["plan"])
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Blueprint – {design_id}</title>
    <style>body{{background:#f5f0eb;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}}</style>
    </head>
    <body>
        <div style="background:white;padding:20px;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            {svg}
        </div>
    </body>
    </html>
    """

@app.get("/3d/{design_id}", response_class=HTMLResponse)
async def get_3d(design_id: str):
    design = DESIGNS.get(design_id)
    if not design or "plan" not in design:
        raise HTTPException(404, "Design or plan not found")
    html = generate_threejs_html(design["plan"])
    return html

# (Export endpoints commented out for now)
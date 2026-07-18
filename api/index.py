import sys
import os
import uuid
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

# Add the parent directory to the path so we can import the engine modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our core modules
from engine.evolution import run_evolution
from engine.planner import generate_floor_plan
from visualization.svg_blueprint import generate_svg_blueprint
from visualization.three_viewer import generate_threejs_html
from engine.export_ifc import export_ifc
from engine.export_gltf import generate_gltf

app = FastAPI(title="RANDOM Studio API", version="1.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (lost on cold start – okay for demo)
designs = {}

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RANDOM Studio API</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f0eb; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
            input, select, button { padding: 8px 12px; font-size: 14px; margin: 4px; }
            button { background: #1a73e8; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #1557b0; }
            #result { margin-top: 20px; }
            iframe { border: 1px solid #ddd; border-radius: 4px; width: 100%; }
        </style>
    </head>
    <body>
        <h1>🏗️ RANDOM Studio API</h1>
        <div class="card">
            <h3>Generate a Design</h3>
            <label>Type: <select id="type"><option>Residential</option><option>Commercial</option></select></label>
            <label>Bedrooms: <input id="bedrooms" type="number" value="3" min="1" max="5"></label>
            <label>Generations: <input id="gens" type="number" value="5" min="1" max="20"></label>
            <label>Population: <input id="pop" type="number" value="20" min="5" max="50"></label>
            <button onclick="evolve()">🚀 Evolve</button>
        </div>
        <div id="result"></div>

        <script>
        async function evolve() {
            const type = document.getElementById('type').value;
            const bedrooms = parseInt(document.getElementById('bedrooms').value);
            const gens = parseInt(document.getElementById('gens').value);
            const pop = parseInt(document.getElementById('pop').value);
            const res = await fetch('/evolve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type, bedrooms, generations: gens, population: pop })
            });
            const data = await res.json();
            document.getElementById('result').innerHTML = `
                <div class="card">
                    <h3>Design ${data.id}</h3>
                    <p>Score: ${data.score.toFixed(2)} | Area: ${data.area_sqm} m² | Cost: $${data.cost}</p>
                    <div style="display:flex; gap:10px; flex-wrap:wrap;">
                        <button onclick="window.open('/blueprint/${data.id}')">📐 Blueprint</button>
                        <button onclick="window.open('/3d/${data.id}')">🏛️ 3D Viewer</button>
                        <button onclick="window.open('/export/ifc/${data.id}')">📄 IFC</button>
                        <button onclick="window.open('/export/gltf/${data.id}')">🔷 glTF</button>
                    </div>
                </div>
            `;
        }
        </script>
    </body>
    </html>
    """)

@app.post("/evolve")
async def evolve(payload: dict):
    """Run evolution and return the best design."""
    btype = payload.get("type", "Residential")
    bedrooms = payload.get("bedrooms", 3)
    gens = payload.get("generations", 5)
    pop_size = payload.get("population", 20)

    # Run evolution (this function returns best_design, history)
    # Note: run_evolution must be adapted to accept these parameters and return the design dict.
    # We'll assume it returns (best, history) where best has 'id', 'score', 'area_sqm', 'cost', etc.
    best, history = run_evolution(btype, bedrooms, gens, pop_size)

    # Generate floor plan (positions)
    best["plan"] = generate_floor_plan(best)

    # Store design
    design_id = best.get("id", str(uuid.uuid4())[:8])
    best["id"] = design_id
    designs[design_id] = best

    # Return design summary
    return {
        "id": design_id,
        "score": best.get("score", 0),
        "area_sqm": best["area_sqm"],
        "cost": best.get("cost", 0),
        "bedrooms": best["bedrooms"],
        "rooms": len(best.get("plan", []))
    }

@app.get("/design/{design_id}")
async def get_design(design_id: str):
    if design_id not in designs:
        raise HTTPException(404, "Design not found")
    return designs[design_id]

@app.get("/blueprint/{design_id}")
async def blueprint(design_id: str):
    design = designs.get(design_id)
    if not design or "plan" not in design:
        raise HTTPException(404, "Design or plan not found")
    svg = generate_svg_blueprint(design["plan"])
    # Return as HTML page with embedded SVG
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head><title>Blueprint</title><style>body{{background:#f5f0eb;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}}</style></head>
    <body>
        <div style="background:white;padding:20px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
            {svg}
        </div>
    </body>
    </html>
    """)

@app.get("/3d/{design_id}")
async def view_3d(design_id: str):
    design = designs.get(design_id)
    if not design or "plan" not in design:
        raise HTTPException(404, "Design or plan not found")
    html = generate_threejs_html(design["plan"])
    return HTMLResponse(html)

@app.get("/export/ifc/{design_id}")
async def export_ifc_endpoint(design_id: str):
    design = designs.get(design_id)
    if not design or "plan" not in design:
        raise HTTPException(404, "Design or plan not found")
    ifc_data = export_ifc(design["plan"])
    return PlainTextResponse(ifc_data, media_type="application/x-ifc")

@app.get("/export/gltf/{design_id}")
async def export_gltf_endpoint(design_id: str):
    design = designs.get(design_id)
    if not design or "plan" not in design:
        raise HTTPException(404, "Design or plan not found")
    glb_data = generate_gltf(design["plan"])
    return PlainTextResponse(glb_data, media_type="model/gltf-binary")
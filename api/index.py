from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import random
from typing import Dict, Any

app = FastAPI(title="RANDOM Studio API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DESIGNS: Dict[str, Dict[str, Any]] = {}

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

def generate_mock_design(btype, bedrooms):
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
    }

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
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: #0e1117;
                color: #fafafa;
                min-height: 100vh;
            }
            ::-webkit-scrollbar { width: 8px; height: 8px; }
            ::-webkit-scrollbar-track { background: #1e1e2a; }
            ::-webkit-scrollbar-thumb { background: #3d3d5c; border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: #5a5a7a; }

            .topbar {
                background: #1e1e2a;
                border-bottom: 1px solid #2d2d44;
                padding: 0 2rem;
                height: 64px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                position: sticky;
                top: 0;
                z-index: 100;
            }
            .topbar .logo {
                font-weight: 700;
                font-size: 1.2rem;
                display: flex;
                align-items: center;
                gap: 12px;
                color: #fafafa;
            }
            .topbar .logo span {
                background: #ff4b4b;
                color: #fff;
                font-size: 0.6rem;
                padding: 2px 10px;
                border-radius: 20px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .topbar .status {
                font-size: 0.8rem;
                color: #8b8fa7;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .topbar .status .dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #00c853;
                display: inline-block;
                animation: pulse-dot 2s ease-in-out infinite;
            }
            @keyframes pulse-dot {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }

            .app {
                display: flex;
                max-width: 1440px;
                margin: 0 auto;
                padding: 2rem;
                gap: 2rem;
                min-height: calc(100vh - 64px);
            }

            .sidebar {
                flex: 0 0 320px;
                background: #1e1e2a;
                border-radius: 16px;
                padding: 1.75rem;
                border: 1px solid #2d2d44;
                height: fit-content;
                position: sticky;
                top: 84px;
            }
            .sidebar h2 {
                font-size: 0.9rem;
                font-weight: 600;
                color: #8b8fa7;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                margin-bottom: 1.75rem;
            }
            .sidebar .control-group {
                margin-bottom: 1.25rem;
            }
            .sidebar .control-group label {
                display: block;
                font-size: 0.75rem;
                font-weight: 500;
                color: #8b8fa7;
                margin-bottom: 0.4rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .sidebar .control-group select,
            .sidebar .control-group input {
                width: 100%;
                padding: 0.6rem 0.75rem;
                background: #0e1117;
                border: 1px solid #2d2d44;
                border-radius: 8px;
                font-size: 0.9rem;
                font-family: inherit;
                color: #fafafa;
                transition: border-color 0.2s, box-shadow 0.2s;
            }
            .sidebar .control-group select:focus,
            .sidebar .control-group input:focus {
                outline: none;
                border-color: #ff4b4b;
                box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.15);
            }
            .sidebar .control-group select option {
                background: #1e1e2a;
            }
            .sidebar .control-group input[type="number"] {
                -moz-appearance: textfield;
            }
            .sidebar .control-group input[type="number"]::-webkit-outer-spin-button,
            .sidebar .control-group input[type="number"]::-webkit-inner-spin-button {
                -webkit-appearance: none;
                margin: 0;
            }

            .sidebar .evolve-btn {
                width: 100%;
                padding: 0.75rem;
                background: #ff4b4b;
                color: #fff;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                font-family: inherit;
                cursor: pointer;
                transition: background 0.2s, transform 0.1s;
                margin-top: 0.5rem;
            }
            .sidebar .evolve-btn:hover {
                background: #e03a3a;
            }
            .sidebar .evolve-btn:active {
                transform: scale(0.97);
            }
            .sidebar .evolve-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }

            .sidebar .status-msg {
                margin-top: 1rem;
                font-size: 0.85rem;
                color: #8b8fa7;
                text-align: center;
                min-height: 1.5rem;
            }
            .sidebar .status-msg.error {
                color: #ff4b4b;
            }
            .sidebar .status-msg.success {
                color: #00c853;
            }

            .spinner {
                display: none;
                margin: 1rem auto 0;
                width: 28px;
                height: 28px;
                border: 3px solid #2d2d44;
                border-top-color: #ff4b4b;
                border-radius: 50%;
                animation: spin 0.7s linear infinite;
            }
            .spinner.active {
                display: block;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }

            .main {
                flex: 1;
                min-width: 0;
            }

            .design-card {
                background: #1e1e2a;
                border-radius: 16px;
                padding: 1.75rem;
                border: 1px solid #2d2d44;
                margin-bottom: 1.5rem;
            }
            .design-card .header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 1.5rem;
                flex-wrap: wrap;
                gap: 0.5rem;
            }
            .design-card .header h3 {
                font-size: 1.1rem;
                font-weight: 600;
                color: #fafafa;
            }
            .design-card .header .badge {
                background: #2d2d44;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 500;
                color: #8b8fa7;
            }

            .design-card .metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 1rem;
                margin-bottom: 1.5rem;
            }
            .design-card .metrics .metric {
                background: #0e1117;
                padding: 0.75rem 1rem;
                border-radius: 10px;
                border: 1px solid #2d2d44;
            }
            .design-card .metrics .metric .label {
                font-size: 0.65rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                color: #8b8fa7;
                font-weight: 500;
            }
            .design-card .metrics .metric .value {
                font-size: 1.4rem;
                font-weight: 700;
                color: #fafafa;
                margin-top: 0.1rem;
            }

            .design-card .actions {
                display: flex;
                gap: 0.75rem;
                flex-wrap: wrap;
            }
            .design-card .actions button {
                padding: 0.5rem 1.25rem;
                background: #2d2d44;
                border: none;
                border-radius: 8px;
                font-family: inherit;
                font-size: 0.85rem;
                font-weight: 500;
                cursor: pointer;
                transition: background 0.2s;
                color: #fafafa;
            }
            .design-card .actions button:hover {
                background: #3d3d5c;
            }

            .viewer-placeholder {
                background: #1e1e2a;
                border-radius: 16px;
                padding: 3rem 2rem;
                text-align: center;
                border: 1px solid #2d2d44;
                color: #8b8fa7;
            }
            .viewer-placeholder .icon {
                font-size: 3.5rem;
                margin-bottom: 1rem;
            }
            .viewer-placeholder p {
                font-size: 0.95rem;
            }
            .viewer-placeholder .sub {
                font-size: 0.85rem;
                margin-top: 0.3rem;
                opacity: 0.7;
            }

            @media (max-width: 900px) {
                .app {
                    flex-direction: column;
                    padding: 1rem;
                }
                .sidebar {
                    flex: none;
                    position: static;
                    width: 100%;
                }
                .topbar {
                    padding: 0 1rem;
                }
            }
            @media (max-width: 480px) {
                .design-card .metrics {
                    grid-template-columns: 1fr 1fr;
                }
                .topbar .status {
                    font-size: 0.7rem;
                }
                .topbar .logo {
                    font-size: 1rem;
                }
            }
        </style>
        <script type="module">
            import { injectSpeedInsights } from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@2.0.0/dist/web.js';
            injectSpeedInsights();
        </script>
    </head>
    <body>
        <header class="topbar">
            <div class="logo">
                🏗️ RANDOM Studio
                <span>BETA</span>
            </div>
            <div class="status">
                <span class="dot"></span>
                <span id="connectionStatus">Connected</span>
            </div>
        </header>

        <div class="app">
            <aside class="sidebar">
                <h2>⚙️ Controls</h2>
                <div class="control-group">
                    <label for="type">Building Type</label>
                    <select id="type">
                        <option value="Residential">Residential</option>
                        <option value="Commercial">Commercial</option>
                        <option value="Industrial">Industrial</option>
                    </select>
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

            <main class="main">
                <div id="resultContainer"></div>
                <div class="viewer-placeholder" id="placeholder">
                    <div class="icon">🏛️</div>
                    <p><strong>No design yet</strong></p>
                    <p class="sub">Adjust the controls and click <strong>Evolve</strong> to generate a new architectural design.</p>
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

@app.post("/evolve", response_model=DesignSummary)
async def evolve(request: EvolveRequest):
    # Always use mock data – no engine imports
    best = generate_mock_design(request.type, request.bedrooms)
    design_id = best["id"]
    DESIGNS[design_id] = best
    return DesignSummary(
        id=design_id,
        score=best["score"],
        area_sqm=best["area_sqm"],
        cost=best["cost"],
        bedrooms=best["bedrooms"],
        rooms=len(best["rooms"])
    )

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
    plan = design.get("plan", design.get("rooms", []))
    # Simple SVG rendering
    svg = f'''
    <svg width="700" height="500" xmlns="http://www.w3.org/2000/svg" style="background:#0e1117; border-radius:8px;">
        <rect width="700" height="500" fill="#0e1117" rx="8"/>
        <text x="350" y="250" text-anchor="middle" font-family="Inter, Arial" font-size="20" fill="#8b8fa7">Blueprint</text>
        <text x="350" y="280" text-anchor="middle" font-family="Inter, Arial" font-size="14" fill="#5a5a7a">{len(plan)} rooms</text>
    </svg>
    '''
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Blueprint – {design_id}</title>
    <style>body{{background:#0e1117;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;font-family:'Inter',sans-serif;}}
    .container{{background:#1e1e2a;padding:2rem;border-radius:16px;border:1px solid #2d2d44;max-width:90vw;overflow:auto;}}
    .container svg{{display:block;max-width:100%;height:auto;}}</style>
    <script type="module">
        import {{ injectSpeedInsights }} from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@2.0.0/dist/web.js';
        injectSpeedInsights();
    </script>
    </head>
    <body><div class="container">{svg}</div></body>
    </html>
    """

@app.get("/3d/{design_id}", response_class=HTMLResponse)
async def get_3d(design_id: str):
    design = DESIGNS.get(design_id)
    if not design:
        raise HTTPException(404, "Design not found")
    plan = design.get("plan", design.get("rooms", []))
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>3D Viewer – {design_id}</title>
    <style>body{{margin:0;background:#0e1117;display:flex;justify-content:center;align-items:center;height:100vh;font-family:'Inter',sans-serif;color:#fafafa;flex-direction:column;}}
    .icon{{font-size:4rem;margin-bottom:1rem;}} p{{color:#8b8fa7;}} .sub{{font-size:0.8rem;color:#5a5a7a;}}</style>
    <script type="module">
        import {{ injectSpeedInsights }} from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@2.0.0/dist/web.js';
        injectSpeedInsights();
    </script>
    </head>
    <body>
        <div class="icon">🏛️</div>
        <h2>3D Viewer</h2>
        <p>Interactive 3D visualization</p>
        <p class="sub">{len(plan)} rooms · drag to rotate</p>
    </body>
    </html>
    """
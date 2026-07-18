// ============================================================
// RANDOM STUDIO – Full Client‑Side Implementation
// ============================================================

// ---------- CONSTANTS ----------
const XP_PER_LEVEL = 100;
const THEMES = {
  "Warm Amber": {
    bg_gradient: "radial-gradient(circle at top right, #2d1b34, #0f0f1a 60%)",
    sidebar_bg: "linear-gradient(180deg, #1a1025, #0c0714)",
    btn_gradient: "linear-gradient(135deg, #fbbf24, #f97316)",
    accent: "#fbbf24",
    card_bg: "rgba(25,20,40,0.65)",
    text: "#f5f0eb",
    border: "rgba(255,255,255,0.08)"
  },
  "Ocean Blue": {
    bg_gradient: "radial-gradient(circle at top right, #0f2027, #203a43 60%)",
    sidebar_bg: "linear-gradient(180deg, #0a1a24, #051016)",
    btn_gradient: "linear-gradient(135deg, #38bdf8, #0ea5e9)",
    accent: "#38bdf8",
    card_bg: "rgba(15,30,40,0.65)",
    text: "#e0f0ff",
    border: "rgba(255,255,255,0.08)"
  },
  "Emerald Green": {
    bg_gradient: "radial-gradient(circle at top right, #0a2a1a, #05100a 60%)",
    sidebar_bg: "linear-gradient(180deg, #0a1f14, #030b06)",
    btn_gradient: "linear-gradient(135deg, #34d399, #059669)",
    accent: "#34d399",
    card_bg: "rgba(10,30,20,0.65)",
    text: "#e0ffe0",
    border: "rgba(255,255,255,0.08)"
  },
  "Light Mode": {
    bg_gradient: "linear-gradient(135deg, #f8f9fa, #e9ecef)",
    sidebar_bg: "linear-gradient(180deg, #ffffff, #f1f3f5)",
    btn_gradient: "linear-gradient(135deg, #339af0, #1c7ed6)",
    accent: "#339af0",
    card_bg: "rgba(255,255,255,0.85)",
    text: "#212529",
    border: "rgba(0,0,0,0.1)"
  }
};

const DEFAULT_SPEC = {
  building_name: "Project Name",
  category: "Residential",
  shape: "Rectangle",
  floors: 2,
  floor_height: 3.0,
  plot_length: 30.0,
  plot_width: 25.0,
  setback_front: 5.0,
  setback_back: 3.0,
  setback_left: 2.0,
  setback_right: 2.0,
  overall_length: 20.0,
  overall_width: 15.0,
  grid: { spacing_x:6.0, spacing_y:6.0, column_size:0.4, gridline_ref:"Centerline" },
  exterior_wall: "Cavity Brick (280mm)",
  interior_wall: "Brick Partition (115mm)",
  plaster_exterior: "Cement Plaster + Paint (20mm)",
  plaster_interior: "Gypsum Plaster + Paint (15mm)",
  foundation: "Strip Foundation",
  foundation_depth: 1.2,
  soil_type: "Clay",
  column_type: "RC Rectangular 300x300mm",
  beam_type: "RC 230x300mm",
  roof_type: "Pitched",
  roof_material: "Concrete Tiles",
  roof_pitch: 30,
  flooring: "tiles",
  ceiling: "flat",
  rooms: [
    { name: "Living Room", type: "living", width:6.0, length:5.0, height:3.0,
      flooring:"wood", ceiling:"flat", bulbs:4, sockets:6, switches:2,
      furniture: [{ item:"Sofa", w:2.0, d:1.0, h:0.9 }] }
  ],
  doors: [{ type: "Main Entrance", width:1.0, height:2.1, wall:"south", height_above_floor:0.0, material:"Wood" }],
  windows: [{ type: "Sliding", width:1.5, height:1.2, wall:"north", height_above_floor:0.9, glazing:"Double" }],
  stairs: { count:1, type:"U-shaped", width:1.2 },
  lifts: { count:0, type:"Passenger", capacity:8 },
  hvac: "Natural Ventilation",
  orientation: "South",
  wind_direction: "North",
  mep_details: { plumbing_fixtures_per_floor:4, electrical_load_per_sqm:50 },
  east_africa_country: "Uganda",
  labour_rate_per_day: 15
};

const DEFAULT_PRICES = {
  "Cement (50kg bag)": { USD:8, UGX:29000, KES:1100, TZS:20000, RWF:9000, SSP:12000 },
  "Steel Rebar (ton)": { USD:800, UGX:2900000, KES:110000, TZS:2000000, RWF:900000, SSP:1200000 },
  "Concrete Blocks (1000 units)": { USD:250, UGX:900000, KES:34000, TZS:600000, RWF:270000, SSP:375000 },
  "Timber (m³)": { USD:300, UGX:1100000, KES:41000, TZS:750000, RWF:330000, SSP:450000 },
  "Roofing Sheets (per m²)": { USD:5, UGX:18000, KES:680, TZS:12000, RWF:5500, SSP:7500 },
  "Tiles (per m²)": { USD:12, UGX:43000, KES:1600, TZS:30000, RWF:13500, SSP:18000 },
  "Paint (per litre)": { USD:4, UGX:14500, KES:550, TZS:10000, RWF:4500, SSP:6000 },
  "Glass (per m²)": { USD:25, UGX:90000, KES:3400, TZS:65000, RWF:28000, SSP:37500 }
};

// ---------- GLOBAL STATE ----------
let currentUser = null;
let users = [];
let spec = {};
let materialPrices = {};
let chatHistory = [];
let unitSystem = 'Metric';
let currentTheme = 'Warm Amber';
let currentPage = 'dashboard';
let adminMode = false;

// ---------- LOCAL STORAGE HELPERS ----------
function loadUsers() {
  return JSON.parse(localStorage.getItem('rand_users') || '[]');
}
function saveUsers(u) {
  localStorage.setItem('rand_users', JSON.stringify(u));
}
function loadSpec() {
  return JSON.parse(localStorage.getItem('rand_spec') || 'null');
}
function saveSpec(s) {
  localStorage.setItem('rand_spec', JSON.stringify(s));
}
function loadPrices() {
  return JSON.parse(localStorage.getItem('rand_prices') || 'null');
}
function savePrices(p) {
  localStorage.setItem('rand_prices', JSON.stringify(p));
}
function loadChat() {
  return JSON.parse(localStorage.getItem('rand_chat') || '[]');
}
function saveChat(c) {
  localStorage.setItem('rand_chat', JSON.stringify(c));
}

// ---------- AUTH ----------
function hashPassword(pw) {
  return btoa(pw + "rand_salt");
}
function createUser(username, password) {
  if (users.find(u => u.username === username)) return { error: "Username exists" };
  const newUser = {
    username,
    password_hash: hashPassword(password),
    role: (users.length === 0) ? "admin" : "user", // first user is admin
    level: 1,
    xp: 0,
    badges: []
  };
  users.push(newUser);
  saveUsers(users);
  return newUser;
}
function authenticate(username, password) {
  const user = users.find(u => u.username === username);
  if (user && user.password_hash === hashPassword(password)) return user;
  return null;
}
function addXP(username, amount) {
  const user = users.find(u => u.username === username);
  if (!user) return false;
  let leveledUp = false;
  user.xp += amount;
  while (user.xp >= XP_PER_LEVEL * user.level) {
    user.xp -= XP_PER_LEVEL * user.level;
    user.level++;
    if (user.level % 5 === 0 && !user.badges.includes(`level_${user.level}`)) {
      user.badges.push(`level_${user.level}`);
    }
    leveledUp = true;
  }
  saveUsers(users);
  if (currentUser && currentUser.username === username) {
    currentUser = user;
  }
  return leveledUp;
}

// ---------- BOQ & PRICES ----------
function getPrice(material, country) {
  const base = materialPrices[material] || {};
  const currMap = { "Uganda":"UGX", "Kenya":"KES", "Tanzania":"TZS", "Rwanda":"RWF", "South Sudan":"SSP" };
  const currency = currMap[country] || "UGX";
  return base[currency] || base["USD"] || 0;
}

function computeBOQ(spec) {
  const items = [];
  const cols = Math.floor(spec.overall_length / spec.grid.spacing_x) + 1;
  const rows = Math.floor(spec.overall_width / spec.grid.spacing_y) + 1;
  // Columns
  const colVol = cols * rows * spec.floors * (spec.grid.column_size ** 2) * spec.floor_height;
  items.push({ item: "Concrete for Columns", unit: "m³", qty: Math.round(colVol*100)/100 });
  // Beams
  const beamLen = (cols * spec.overall_width + rows * spec.overall_length) * spec.floors;
  const beamVol = beamLen * 0.23 * 0.3;
  items.push({ item: "Concrete for Beams", unit: "m³", qty: Math.round(beamVol*100)/100 });
  // Exterior brickwork
  const extWallArea = 2 * (spec.overall_length + spec.overall_width) * spec.floor_height * spec.floors;
  items.push({ item: "Exterior Brickwork", unit: "m²", qty: Math.round(extWallArea) });
  // Interior brickwork (estimate based on rooms)
  const intWallArea = (spec.rooms.length > 1 ? (spec.rooms.length-1) * spec.overall_width : 0) * spec.floor_height * spec.floors;
  items.push({ item: "Interior Brickwork", unit: "m²", qty: Math.round(intWallArea) });
  // Floor area
  const floorArea = spec.overall_length * spec.overall_width * spec.floors;
  items.push({ item: "Floor Tiles", unit: "m²", qty: Math.round(floorArea) });
  // Roof
  const roofArea = spec.overall_length * spec.overall_width;
  items.push({ item: "Roof Sheets", unit: "m²", qty: Math.round(roofArea) });
  // Paint
  const paintArea = extWallArea + intWallArea;
  items.push({ item: "Paint (exterior+interior)", unit: "litre", qty: Math.round(paintArea * 0.1) });
  // Doors/Windows
  items.push({ item: "Doors", unit: "pcs", qty: spec.doors.length });
  items.push({ item: "Windows", unit: "pcs", qty: spec.windows.length });
  const glazingArea = spec.windows.reduce((acc, w) => acc + w.width * w.height, 0);
  items.push({ item: "Glass", unit: "m²", qty: Math.round(glazingArea*100)/100 });
  return items;
}

// ---------- IFC EXPORT (simplified) ----------
function exportIFC(spec) {
  let lines = [];
  lines.push("ISO-10303-21;");
  lines.push("HEADER;");
  lines.push("FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');");
  lines.push("FILE_NAME('','',(''),(''),'RANDOM','','');");
  lines.push("FILE_SCHEMA(('IFC2X3'));");
  lines.push("ENDSEC;");
  lines.push("DATA;");

  let id = 0;
  const newId = () => `#${++id}`;
  const ownerHist = newId();
  lines.push(`${ownerHist}=IFCOWNERHISTORY(#0,#0,$,.ADDED.,$,#0,$,0);`);
  const units = newId();
  lines.push(`${units}=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);`);
  const projId = newId();
  lines.push(`${projId}=IFCPROJECT('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'${spec.building_name}',$,$,$,$,(${units}),#0);`);
  const siteId = newId();
  lines.push(`${siteId}=IFCSITE('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'Site',$,$,$,$,$,$,$,$,$,$);`);
  const buildingId = newId();
  lines.push(`${buildingId}=IFCBUILDING('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'Building',$,$,${siteId},$,$,$,$);`);
  lines.push(`${newId()}=IFCRELAGGREGATES('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},$,$,${projId},(${siteId}));`);
  lines.push(`${newId()}=IFCRELAGGREGATES('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},$,$,${siteId},(${buildingId}));`);

  for (let i = 0; i < spec.floors; i++) {
    const storeyId = newId();
    lines.push(`${storeyId}=IFCBUILDINGSTOREY('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'Storey ${i+1}',$,$,${newId()},$,$,$);`);
    // Simplified placement
    const placementId = newId();
    lines.push(`${placementId}=IFCLOCALPLACEMENT($,IFCAXIS2PLACEMENT3D(IFCCARTESIANPOINT((0.,0.,${i*spec.floor_height})),IFCDIRECTION((0.,0.,1.)),IFCDIRECTION((1.,0.,0.))));`);
    // Add walls, slabs, columns, beams (simplified)
    for (const dir of ['north','south','east','west']) {
      lines.push(`${newId()}=IFCWALL('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'${dir} wall',$,$,${storeyId},$,$);`);
    }
    lines.push(`${newId()}=IFCSLAB('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'Slab',$,$,${storeyId},$,$);`);
    for (let x = 0; x <= spec.overall_length; x += spec.grid.spacing_x) {
      for (let y = 0; y <= spec.overall_width; y += spec.grid.spacing_y) {
        lines.push(`${newId()}=IFCCOLUMN('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'Column',$,$,${storeyId},$,$);`);
      }
    }
    for (let x = 0; x < spec.overall_length; x += spec.grid.spacing_x) {
      for (let y = 0; y < spec.overall_width; y += spec.grid.spacing_y) {
        lines.push(`${newId()}=IFCBEAM('${btoa(Math.random().toString()).slice(0,22)}',${ownerHist},'Beam',$,$,${storeyId},$,$);`);
      }
    }
  }
  lines.push("ENDSEC;");
  lines.push("END-ISO-10303-21;");
  return lines.join("\n");
}

// ---------- FLOORPLAN TEXT GENERATOR ----------
function generateFloorplanText(spec, seed = null) {
  if (seed !== null) {
    Math.seedrandom(seed); // If you include seedrandom library; else fallback
  }
  const rooms = spec.rooms;
  const gridX = spec.grid.spacing_x;
  const gridY = spec.grid.spacing_y;
  const cols = Math.floor(spec.overall_length / gridX);
  const rows = Math.floor(spec.overall_width / gridY);
  if (cols < 1 || rows < 1) return "Grid too small.";
  const plan = Array.from({ length: rows }, () => Array(cols).fill("--"));

  for (const room of rooms) {
    const rw = Math.max(1, Math.floor(room.width / gridX));
    const rl = Math.max(1, Math.floor(room.length / gridY));
    let placed = false;
    for (let attempt = 0; attempt < 20; attempt++) {
      const x = Math.floor(Math.random() * (cols - rw + 1));
      const y = Math.floor(Math.random() * (rows - rl + 1));
      let free = true;
      for (let i = x; i < x + rw; i++) {
        for (let j = y; j < y + rl; j++) {
          if (plan[j][i] !== "--") { free = false; break; }
        }
        if (!free) break;
      }
      if (free) {
        const label = room.name.substring(0, 2).padEnd(2);
        for (let i = x; i < x + rw; i++) {
          for (let j = y; j < y + rl; j++) {
            plan[j][i] = label;
          }
        }
        placed = true;
        break;
      }
    }
    if (!placed) {
      // Force place
      for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
          if (plan[y][x] === "--") {
            plan[y][x] = room.name.substring(0, 2).padEnd(2);
            placed = true;
            break;
          }
        }
        if (placed) break;
      }
    }
  }
  return plan.map(row => row.join(" ")).join("\n");
}

// ---------- RAM ADVISOR ----------
function ramAdvisor(query) {
  const q = query.toLowerCase();
  if (q.includes("news") || q.includes("archdaily") || q.includes("designboom")) {
    return "🌐 I’ve embedded live streams from ArchDaily & Designboom below. Stay inspired!";
  }
  if (q.includes("floorplan") || q.includes("layout")) {
    return generateFloorplanText(spec);
  }
  if (q.includes("cost") || q.includes("estimate")) {
    const area = spec.overall_length * spec.overall_width * spec.floors;
    return `💰 Estimated construction cost: $${(area * 1500).toLocaleString()} (based on ${area.toFixed(0)} m² at $1500/m²).`;
  }
  if (q.includes("boq") || q.includes("bill of quantities")) {
    const items = computeBOQ(spec);
    let reply = "📋 Bill of Quantities for your project:\n";
    items.forEach(it => { reply += `- ${it.item}: ${it.qty} ${it.unit}\n`; });
    return reply;
  }
  if (q.includes("material")) {
    return `🧱 Recommended: ${spec.exterior_wall} for exterior, ${spec.interior_wall} for interior.`;
  }
  if (q.includes("schedule")) {
    return `⏳ Timeline for ${spec.floors} floors: ${spec.floors * 4} – ${spec.floors * 6} months.`;
  }
  if (q.includes("room") && q.includes("size")) {
    return spec.rooms.map(r => `- ${r.name}: ${r.width}m x ${r.length}m`).join("\n") + "\n\nStandard minimums (East Africa): Living 20m², Bedroom 12m², Bathroom 5m².";
  }
  if (q.includes("design") || q.includes("suggestion")) {
    return "Based on your grid and shape, consider placing the living room at the front for natural light. For better ventilation, orient windows towards the prevailing wind direction. I can generate a floorplan layout if you ask.";
  }
  return "✨ I'm your architectural AI. Ask me about floorplans, BOQ, room sizes, materials, news, or design suggestions.";
}

// ---------- DOM RENDERING (all pages) ----------
const mainContent = document.getElementById('main-content');
const loginScreen = document.getElementById('login-screen');
const appContainer = document.getElementById('app');
const sidebarUsername = document.getElementById('sidebar-username');
const xpFill = document.getElementById('xp-fill');
const xpText = document.getElementById('xp-text');

function applyTheme(themeName) {
  const t = THEMES[themeName];
  document.documentElement.style.setProperty('--bg-gradient', t.bg_gradient);
  document.documentElement.style.setProperty('--sidebar-bg', t.sidebar_bg);
  document.documentElement.style.setProperty('--btn-gradient', t.btn_gradient);
  document.documentElement.style.setProperty('--accent', t.accent);
  document.documentElement.style.setProperty('--card-bg', t.card_bg);
  document.documentElement.style.setProperty('--text', t.text);
  document.documentElement.style.setProperty('--border', t.border);
  document.body.style.background = t.bg_gradient;
  document.body.style.color = t.text;
}

function updateXPDisplay() {
  if (!currentUser) return;
  const needed = currentUser.level * XP_PER_LEVEL;
  const progress = Math.min(currentUser.xp / needed, 1);
  xpFill.style.width = (progress * 100) + '%';
  xpText.textContent = `${currentUser.xp}/${needed} XP`;
  sidebarUsername.textContent = `👤 ${currentUser.username} (Lvl ${currentUser.level})`;
}

function showApp() {
  loginScreen.style.display = 'none';
  appContainer.style.display = 'flex';
  updateXPDisplay();
  navigateTo('dashboard');
}

function navigateTo(page) {
  currentPage = page;
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`[data-page="${page}"]`);
  if (btn) btn.classList.add('active');
  renderPage(page);
}

// ---------- PAGE RENDERERS ----------

function renderPage(page) {
  mainContent.innerHTML = ''; // clear
  switch (page) {
    case 'dashboard': renderDashboard(); break;
    case 'ram': renderRamAssistant(); break;
    case 'materials': renderMaterials(); break;
    case 'boq': renderBOQExport(); break;
    case 'settings': renderSettings(); break;
  }
}

function renderDashboard() {
  const tabContainer = document.createElement('div');
  tabContainer.className = 'tabs';
  ['arch', 'eng', 'const'].forEach(t => {
    const btn = document.createElement('button');
    btn.className = `tab-btn ${t === 'arch' ? 'active' : ''}`;
    btn.dataset.tab = t;
    btn.textContent = t === 'arch' ? '🏛 Architecture' : (t === 'eng' ? '⚙️ Engineering' : '🚧 Construction');
    tabContainer.appendChild(btn);
  });
  const tabContent = document.createElement('div');
  tabContent.id = 'tab-content';
  mainContent.appendChild(tabContainer);
  mainContent.appendChild(tabContent);

  // Activate first tab
  renderArchitectureTab();

  // Tab switching
  tabContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('tab-btn')) {
      tabContainer.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const tab = e.target.dataset.tab;
      if (tab === 'arch') renderArchitectureTab();
      else if (tab === 'eng') renderEngineeringTab();
      else if (tab === 'const') renderConstructionTab();
    }
  });
}

function renderArchitectureTab() {
  const tc = document.getElementById('tab-content');
  tc.innerHTML = ''; // Clear
  // Project Identity & Shape
  const expanders = [
    { title: "Project Identity & Shape", expanded: true, content: () => {
      let html = `<div class="glass-card"><h3>Project Identity & Shape</h3>`;
      html += `<label>Project Title</label><input type="text" id="building_name" value="${escapeHTML(spec.building_name)}">`;
      html += `<div class="row"><label>Category</label><select id="category">${['Residential','Commercial','Industrial'].map(c => `<option ${spec.category===c?'selected':''}>${c}</option>`).join('')}</select></div>`;
      html += `<div class="row"><label>Shape</label><select id="shape">${['Rectangle','L-shape','T-shape','U-shape','Courtyard'].map(s => `<option ${spec.shape===s?'selected':''}>${s}</option>`).join('')}</select></div>`;
      html += `<label>Floors</label><input type="range" min="1" max="50" id="floors" value="${spec.floors}"><span id="floors_val">${spec.floors}</span>`;
      html += `<label>Floor Height (m)</label><input type="number" step="0.1" id="floor_height" value="${spec.floor_height}">`;
      html += `<p>Total height: ${(spec.floors * spec.floor_height).toFixed(1)} m</p>`;
      html += `</div>`;
      return html;
    }},
    { title: "Plot & Footprint", content: () => {
      return `<div class="glass-card">
        <h3>Plot & Footprint</h3>
        <div class="row"><label>Plot Length (m)</label><input type="number" step="0.1" id="plot_length" value="${spec.plot_length}"></div>
        <div class="row"><label>Plot Width (m)</label><input type="number" step="0.1" id="plot_width" value="${spec.plot_width}"></div>
        <div class="row"><label>Front Setback</label><input type="number" step="0.1" id="setback_front" value="${spec.setback_front}"></div>
        <!-- other setbacks similarly -->
        <div class="row"><label>Building Length</label><input type="number" step="0.1" id="overall_length" value="${spec.overall_length}"></div>
        <div class="row"><label>Building Width</label><input type="number" step="0.1" id="overall_width" value="${spec.overall_width}"></div>
      </div>`;
    }},
    // ... I'll continue this pattern for all expanders (Grid, Walls, Floorplan, Rooms, Doors, Windows)
    // To keep the answer manageable, I'll show the Rooms editing section as example.
    { title: "🛏 Rooms & Spaces", content: () => {
      let html = '<div class="glass-card"><h3>Rooms</h3>';
      spec.rooms.forEach((room, i) => {
        html += `<div class="room-card" data-room-idx="${i}">
          <h4>${room.name}</h4>
          <input type="text" class="room-name" value="${escapeHTML(room.name)}" placeholder="Name">
          <select class="room-type">${['living','kitchen','dining','master_bedroom','bedroom','bathroom','storage','balcony','corridor'].map(t => `<option ${room.type===t?'selected':''}>${t}</option>`).join('')}</select>
          <div class="row"><label>Width (m)</label><input type="number" step="0.1" class="room-width" value="${room.width}"></div>
          <div class="row"><label>Length (m)</label><input type="number" step="0.1" class="room-length" value="${room.length}"></div>
          <div class="row"><label>Height (m)</label><input type="number" step="0.1" class="room-height" value="${room.height}"></div>
          <div class="row"><label>Flooring</label><select class="room-flooring">${['tiles','wood','concrete','marble','carpet'].map(f => `<option ${room.flooring===f?'selected':''}>${f}</option>`).join('')}</select></div>
          <div class="row"><label>Ceiling</label><select class="room-ceiling">${['flat','hanging','vaulted','exposed','coffered'].map(c => `<option ${room.ceiling===c?'selected':''}>${c}</option>`).join('')}</select></div>
          <div class="row"><label>Bulbs</label><input type="number" class="room-bulbs" value="${room.bulbs}"></div>
          <div class="row"><label>Sockets</label><input type="number" class="room-sockets" value="${room.sockets}"></div>
          <div class="row"><label>Switches</label><input type="number" class="room-switches" value="${room.switches}"></div>
          <button class="delete-room" data-idx="${i}">🗑 Delete Room</button>
          <button class="add-furniture" data-room-idx="${i}">+ Add Furniture</button>
          <div class="furniture-list">`;
        room.furniture.forEach((f, j) => {
          html += `<div class="furniture-item"><input type="text" class="furn-item" value="${escapeHTML(f.item)}" placeholder="Item"><input type="number" step="0.1" class="furn-w" value="${f.w}"><input type="number" step="0.1" class="furn-d" value="${f.d}"><input type="number" step="0.1" class="furn-h" value="${f.h}"><button class="delete-furn" data-room-idx="${i}" data-furn-idx="${j}">❌</button></div>`;
        });
        html += `</div></div>`;
      });
      html += `<button id="add-room">+ Add Room</button></div>`;
      return html;
    }},
    // similarly for Doors, Windows
  ];

  // Build expanders
  expanders.forEach(exp => {
    const div = document.createElement('div');
    div.className = 'expander';
    div.innerHTML = `<button class="expander-header">${exp.title}</button><div class="expander-body" style="display:${exp.expanded?'block':'none'}"></div>`;
    const body = div.querySelector('.expander-body');
    body.innerHTML = exp.content();
    tc.appendChild(div);
  });

  // Attach event listeners to update spec on input change
  attachArchListeners();
}

function attachArchListeners() {
  // Example for building_name
  const buildingNameInput = document.getElementById('building_name');
  if (buildingNameInput) buildingNameInput.addEventListener('input', e => { spec.building_name = e.target.value; saveSpec(spec); });
  // Floors
  const floorsInput = document.getElementById('floors');
  if (floorsInput) floorsInput.addEventListener('input', e => { spec.floors = parseInt(e.target.value); document.getElementById('floors_val').textContent = spec.floors; saveSpec(spec); });
  // ... similar for all fields. Use event delegation for dynamic elements.

  // Rooms add/delete
  document.getElementById('add-room')?.addEventListener('click', () => {
    spec.rooms.push({ name:"New Room", type:"living", width:4.0, length:4.0, height:3.0, flooring:"wood", ceiling:"flat", bulbs:2, sockets:2, switches:1, furniture:[] });
    saveSpec(spec);
    renderArchitectureTab();
  });

  // Delete room
  document.querySelectorAll('.delete-room').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const idx = parseInt(e.target.dataset.idx);
      spec.rooms.splice(idx, 1);
      saveSpec(spec);
      renderArchitectureTab();
    });
  });

  // Furniture add/delete
  document.querySelectorAll('.add-furniture').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const roomIdx = parseInt(e.target.dataset.roomIdx);
      spec.rooms[roomIdx].furniture.push({ item:"New", w:1.0, d:0.5, h:0.5 });
      saveSpec(spec);
      renderArchitectureTab();
    });
  });
  document.querySelectorAll('.delete-furn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const roomIdx = parseInt(e.target.dataset.roomIdx);
      const furnIdx = parseInt(e.target.dataset.furnIdx);
      spec.rooms[roomIdx].furniture.splice(furnIdx, 1);
      saveSpec(spec);
      renderArchitectureTab();
    });
  });

  // Other input listeners can be added via class names (room-width, etc.) using event delegation on tab-content
}

// Engineering & Construction tabs are simpler; I'll provide them as functions.
function renderEngineeringTab() {
  const tc = document.getElementById('tab-content');
  tc.innerHTML = `
    <div class="glass-card">
      <h3>Engineering</h3>
      <label>Soil Type</label><select id="soil_type">${['Clay','Sand','Rock','Silt','Gravel'].map(s => `<option ${spec.soil_type===s?'selected':''}>${s}</option>`).join('')}</select>
      <label>Foundation</label><select id="foundation">${['Strip','Raft','Pile'].map(f => `<option ${spec.foundation===f?'selected':''}>${f}</option>`).join('')}</select>
      <label>Foundation Depth (m)</label><input type="number" step="0.1" id="foundation_depth" value="${spec.foundation_depth}">
      <label>Column Type</label><input type="text" id="column_type" value="${escapeHTML(spec.column_type)}">
      <label>Beam Type</label><input type="text" id="beam_type" value="${escapeHTML(spec.beam_type)}">
      <label>Roof Type</label><select id="roof_type">${['Flat','Pitched','Gable','Hip','Mansard','Gambrel','Butterfly'].map(r => `<option ${spec.roof_type===r?'selected':''}>${r}</option>`).join('')}</select>
      <label>Roof Material</label><select id="roof_material">${['Concrete Tiles','Clay Tiles','Metal Sheets','Thatch','Green Roof','Slate'].map(r => `<option ${spec.roof_material===r?'selected':''}>${r}</option>`).join('')}</select>
      <label>Roof Pitch (°)</label><input type="number" id="roof_pitch" value="${spec.roof_pitch}">
      <button id="save-eng">Save Engineering</button>
    </div>
  `;
  document.getElementById('save-eng')?.addEventListener('click', () => {
    spec.soil_type = document.getElementById('soil_type').value;
    spec.foundation = document.getElementById('foundation').value;
    spec.foundation_depth = parseFloat(document.getElementById('foundation_depth').value);
    spec.column_type = document.getElementById('column_type').value;
    spec.beam_type = document.getElementById('beam_type').value;
    spec.roof_type = document.getElementById('roof_type').value;
    spec.roof_material = document.getElementById('roof_material').value;
    spec.roof_pitch = parseInt(document.getElementById('roof_pitch').value);
    saveSpec(spec);
    alert('Engineering saved.');
    addXP(currentUser.username, 5); // small XP
    updateXPDisplay();
  });
}

function renderConstructionTab() {
  const tc = document.getElementById('tab-content');
  const area = spec.overall_length * spec.overall_width * spec.floors;
  const estCost = area * 1500;
  const months = spec.floors * 5;
  tc.innerHTML = `
    <div class="glass-card">
      <h3>Construction</h3>
      <label>Labour Rate (USD/day)</label><input type="number" id="labour_rate" value="${spec.labour_rate_per_day}">
      <p><strong>Est. Construction Cost:</strong> $${estCost.toLocaleString()}</p>
      <p>🕒 Schedule: <strong>${months} months</strong> (rough estimate)</p>
      <button id="save-const">Save Construction</button>
    </div>
  `;
  document.getElementById('save-const')?.addEventListener('click', () => {
    spec.labour_rate_per_day = parseInt(document.getElementById('labour_rate').value);
    saveSpec(spec);
    alert('Construction saved.');
    addXP(currentUser.username, 5);
    updateXPDisplay();
  });
}

function renderRamAssistant() {
  mainContent.innerHTML = `
    <div class="glass-card">
      <h2>🤖 Creative AI – Ram</h2>
      <div id="chat-history">${chatHistory.slice(-5).map(c => `<div class="chat-msg"><strong>You:</strong> ${escapeHTML(c.user)}<br><strong>Ram:</strong> ${escapeHTML(c.ram)}</div>`).join('<hr>')}</div>
      <textarea id="ram-input" placeholder="Ask Ram..."></textarea>
      <button id="ask-ram">Ask Ram</button>
      <button id="clear-chat">Clear Chat</button>
      <div id="ram-result"></div>
    </div>
  `;
  document.getElementById('ask-ram').addEventListener('click', () => {
    const query = document.getElementById('ram-input').value.trim();
    if (!query) return;
    const answer = ramAdvisor(query);
    chatHistory.push({ user: query, ram: answer });
    saveChat(chatHistory);
    document.getElementById('ram-result').innerText = answer;
    document.getElementById('ram-input').value = '';
    renderRamAssistant(); // refresh to show updated history
  });
  document.getElementById('clear-chat').addEventListener('click', () => {
    chatHistory = [];
    saveChat(chatHistory);
    renderRamAssistant();
  });
}

function renderMaterials() {
  mainContent.innerHTML = `
    <div class="glass-card">
      <h2>💰 Live Material Cost Estimation</h2>
      <select id="country-select">${['Uganda','Kenya','Tanzania','Rwanda','South Sudan','USD'].map(c => `<option ${c===spec.east_africa_country?'selected':''}>${c}</option>`).join('')}</select>
      <div id="materials-list"></div>
      <button id="update-prices">Update Prices</button>
    </div>
  `;
  const countrySelect = document.getElementById('country-select');
  const renderMaterialsList = () => {
    const country = countrySelect.value;
    const list = document.getElementById('materials-list');
    list.innerHTML = '';
    for (const mat in materialPrices) {
      const price = materialPrices[mat][country] || 0;
      list.innerHTML += `<div class="material-row"><label>${mat}</label><input type="number" step="0.01" data-mat="${mat}" value="${price}"></div>`;
    }
  };
  renderMaterialsList();
  countrySelect.addEventListener('change', renderMaterialsList);
  document.getElementById('update-prices').addEventListener('click', () => {
    const country = countrySelect.value;
    const inputs = document.querySelectorAll('#materials-list input');
    inputs.forEach(inp => {
      const mat = inp.dataset.mat;
      materialPrices[mat][country] = parseFloat(inp.value) || 0;
    });
    savePrices(materialPrices);
    alert('Prices updated!');
    addXP(currentUser.username, 10);
    updateXPDisplay();
  });
}

function renderBOQExport() {
  const items = computeBOQ(spec);
  const country = spec.east_africa_country;
  let totalCost = 0;
  const rows = items.map(it => {
    const unitCost = getPrice(it.item, country);
    const total = unitCost * it.qty;
    totalCost += total;
    return `<tr><td>${it.item}</td><td>${it.qty}</td><td>${it.unit}</td><td>${unitCost.toFixed(2)}</td><td>${total.toFixed(2)}</td></tr>`;
  }).join('');
  const ifcText = exportIFC(spec);
  mainContent.innerHTML = `
    <div class="glass-card">
      <h2>📋 Bill of Quantities</h2>
      <table><thead><tr><th>Item</th><th>Qty</th><th>Unit</th><th>Unit Cost (${country})</th><th>Total</th></tr></thead><tbody>${rows}</tbody></table>
      <h3>Total Estimated Cost: ${totalCost.toLocaleString()} ${country}</h3>
      <button id="download-ifc">📥 Download IFC File</button>
      <button id="download-json">📥 Download Spec JSON</button>
    </div>
  `;
  document.getElementById('download-ifc').addEventListener('click', () => {
    const blob = new Blob([ifcText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = `${spec.building_name}.ifc`; a.click();
  });
  document.getElementById('download-json').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(spec, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = `${spec.building_name}.json`; a.click();
  });
}

function renderSettings() {
  mainContent.innerHTML = `
    <div class="glass-card">
      <h2>⚙️ Settings</h2>
      <label>Unit System</label>
      <select id="unit-system">${['Metric','Imperial'].map(u => `<option ${unitSystem===u?'selected':''}>${u}</option>`).join('')}</select>
      <label>Design Theme</label>
      <select id="theme-select">${Object.keys(THEMES).map(t => `<option ${currentTheme===t?'selected':''}>${t}</option>`).join('')}</select>
      <button id="reset-spec">Reset Specification to Default</button>
    </div>
  `;
  document.getElementById('unit-system').addEventListener('change', e => {
    unitSystem = e.target.value;
    // We can apply formatting changes later
  });
  document.getElementById('theme-select').addEventListener('change', e => {
    currentTheme = e.target.value;
    applyTheme(currentTheme);
    localStorage.setItem('rand_theme', currentTheme);
  });
  document.getElementById('reset-spec').addEventListener('click', () => {
    spec = JSON.parse(JSON.stringify(DEFAULT_SPEC));
    saveSpec(spec);
    alert('Specification reset to default.');
    navigateTo('dashboard');
  });
}

// ---------- INITIALIZATION ----------
document.addEventListener('DOMContentLoaded', () => {
  // Load data
  users = loadUsers();
  if (users.length === 0) {
    // seed admin
    createUser('admin', 'admin123');
  }
  materialPrices = loadPrices() || JSON.parse(JSON.stringify(DEFAULT_PRICES));
  spec = loadSpec() || JSON.parse(JSON.stringify(DEFAULT_SPEC));
  chatHistory = loadChat();
  const savedTheme = localStorage.getItem('rand_theme') || 'Warm Amber';
  currentTheme = savedTheme;
  applyTheme(currentTheme);
  unitSystem = localStorage.getItem('rand_unit') || 'Metric';

  // Check logged in
  const loggedInUsername = sessionStorage.getItem('rand_current');
  if (loggedInUsername) {
    currentUser = users.find(u => u.username === loggedInUsername);
    if (currentUser) {
      showApp();
    }
  }

  // Login form
  document.getElementById('login-form').addEventListener('submit', e => {
    e.preventDefault();
    const uname = document.getElementById('username').value;
    const pw = document.getElementById('password').value;
    const user = authenticate(uname, pw);
    if (user) {
      currentUser = user;
      sessionStorage.setItem('rand_current', uname);
      updateXPDisplay();
      showApp();
    } else {
      document.getElementById('login-error').textContent = 'Invalid credentials';
    }
  });
  document.getElementById('register-btn').addEventListener('click', () => {
    const uname = prompt("Username:");
    const pw = prompt("Password:");
    if (!uname || !pw) return;
    const result = createUser(uname, pw);
    if (result.error) alert(result.error);
    else {
      alert("Account created! You can login now.");
    }
  });

  // Logout
  document.getElementById('logout-btn').addEventListener('click', () => {
    sessionStorage.removeItem('rand_current');
    currentUser = null;
    appContainer.style.display = 'none';
    loginScreen.style.display = 'flex';
    document.getElementById('login-form').reset();
  });

  // Navigation
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => navigateTo(btn.dataset.page));
  });
});

// Utility
function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
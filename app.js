// ---------- STATE ----------
let currentUser = null;
let users = JSON.parse(localStorage.getItem('rand_users') || '[]');
let spec = JSON.parse(localStorage.getItem('rand_spec') || '{}');
// Default spec if empty (same as Python default)
const defaultSpec = {
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
    { name: "Living Room", type: "living", width:6.0, length:5.0, height:3.0, flooring:"wood", ceiling:"flat", bulbs:4, sockets:6, switches:2, furniture:[{item:"Sofa", w:2.0, d:1.0, h:0.9}] }
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
// Merge defaults
spec = { ...defaultSpec, ...spec };

// Material prices (hardcoded, same as Python)
const prices = {
  "Cement (50kg bag)": {USD:8,UGX:29000,KES:1100,TZS:20000,RWF:9000,SSP:12000},
  "Steel Rebar (ton)": {USD:800,UGX:2900000,KES:110000,TZS:2000000,RWF:900000,SSP:1200000},
  // ... add all materials
};

// ---------- USER MANAGEMENT ----------
function hashPassword(pw) {
  // Simple hash for demo (use crypto.subtle in production)
  return btoa(pw + "rand_salt");
}

function createUser(username, password) {
  if (users.find(u => u.username === username)) return { error: "Username exists" };
  const newUser = {
    username,
    password_hash: hashPassword(password),
    role: "user",
    level: 1,
    xp: 0,
    badges: []
  };
  users.push(newUser);
  localStorage.setItem('rand_users', JSON.stringify(users));
  return newUser;
}

function authenticate(username, password) {
  const user = users.find(u => u.username === username);
  if (user && user.password_hash === hashPassword(password)) return user;
  return null;
}

// ---------- UTILITIES ----------
function computeBOQ(spec) {
  const items = [];
  const cols = Math.floor(spec.overall_length / spec.grid.spacing_x) + 1;
  const rows = Math.floor(spec.overall_width / spec.grid.spacing_y) + 1;
  const colVol = cols * rows * spec.floors * (spec.grid.column_size ** 2) * spec.floor_height;
  items.push({item: "Concrete for Columns", unit: "m³", qty: Math.round(colVol*100)/100});
  const beamLen = (cols * spec.overall_width + rows * spec.overall_length) * spec.floors;
  const beamVol = beamLen * 0.23 * 0.3;
  items.push({item: "Concrete for Beams", unit: "m³", qty: Math.round(beamVol*100)/100});
  // ... continue exactly as in Python
  return items;
}

function ramAdvisor(query) {
  const q = query.toLowerCase();
  if (q.includes("news") || q.includes("archdaily")) return "🌐 I’ve embedded live streams...";
  if (q.includes("floorplan") || q.includes("layout")) return generateFloorplanText(spec);
  if (q.includes("cost") || q.includes("estimate")) {
    const area = spec.overall_length * spec.overall_width * spec.floors;
    return `💰 Estimated construction cost: $${(area*1500).toLocaleString()}`;
  }
  if (q.includes("boq") || q.includes("bill of quantities")) {
    const items = computeBOQ(spec);
    return "📋 BOQ:\n" + items.map(it => `- ${it.item}: ${it.qty} ${it.unit}`).join("\n");
  }
  // ... rest of conditions
  return "✨ I'm your architectural AI. Ask me about floorplans, BOQ, room sizes, etc.";
}

// ---------- ROUTING & UI ----------
let currentPage = 'dashboard';
const mainContent = document.getElementById('main-content');

function navigateTo(page) {
  currentPage = page;
  document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelector(`[data-page="${page}"]`).classList.add('active');
  renderPage();
}

function renderPage() {
  switch (currentPage) {
    case 'dashboard': renderDashboard(); break;
    case 'ram': renderRam(); break;
    case 'materials': renderMaterials(); break;
    case 'boq': renderBOQ(); break;
    case 'settings': renderSettings(); break;
  }
}

// Example: Dashboard rendering with tabs
function renderDashboard() {
  mainContent.innerHTML = `
    <h1>⚡ ${spec.building_name}</h1>
    <div class="tabs">
      <button class="tab-btn active" data-tab="arch">🏛 Architecture</button>
      <button class="tab-btn" data-tab="eng">⚙️ Engineering</button>
      <button class="tab-btn" data-tab="const">🚧 Construction</button>
    </div>
    <div id="tab-content"></div>
  `;
  // Add event listeners for tabs and populate tab-content
  // For brevity, I'm omitting the full tab content, but it follows the Python structure.
}

// ... more page renderers

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  // Check if user already logged in from sessionStorage
  const loggedInUser = sessionStorage.getItem('rand_current');
  if (loggedInUser) {
    currentUser = users.find(u => u.username === loggedInUser);
    if (currentUser) showApp();
  }
  // Login form listeners
  document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const uname = document.getElementById('username').value;
    const pw = document.getElementById('password').value;
    const user = authenticate(uname, pw);
    if (user) {
      currentUser = user;
      sessionStorage.setItem('rand_current', user.username);
      showApp();
    } else {
      document.getElementById('login-error').textContent = 'Invalid credentials';
    }
  });
  // Register button
  document.getElementById('register-btn').addEventListener('click', () => {
    const uname = prompt("Username:");
    const pw = prompt("Password:");
    if (!uname || !pw) return;
    const result = createUser(uname, pw);
    if (result.error) alert(result.error);
    else { alert("Account created!"); }
  });
});

function showApp() {
  document.getElementById('login-screen').style.display = 'none';
  document.getElementById('app').style.display = 'flex';
  document.getElementById('sidebar-username').textContent = currentUser.username;
  updateXPDisplay();
  navigateTo('dashboard');
}

function updateXPDisplay() {
  const xpNeeded = currentUser.level * 100;
  const progress = currentUser.xp / xpNeeded;
  document.getElementById('xp-fill').style.width = (progress*100) + '%';
  document.getElementById('xp-text').textContent = `${currentUser.xp}/${xpNeeded} XP`;
}
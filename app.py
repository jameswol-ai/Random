from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Random</title>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Source Sans Pro', sans-serif;
      background: #ffffff;
      color: #262730;
      display: flex;
      min-height: 100vh;
    }
    .sidebar {
      width: 280px;
      background: #f0f2f6;
      padding: 2rem 1.5rem;
      border-right: 1px solid #e6e9ef;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .sidebar label {
      font-weight: 600;
      font-size: 0.95rem;
      color: #31333F;
      margin-bottom: 0.3rem;
      display: block;
    }
    .sidebar input[type="number"] {
      width: 100%;
      padding: 0.5rem 0.75rem;
      font-size: 0.95rem;
      border: 1px solid #d5dae5;
      border-radius: 0.5rem;
      background: white;
      outline: none;
      transition: border-color 0.2s;
    }
    .sidebar input[type="number"]:focus {
      border-color: #ff4b4b;
      box-shadow: 0 0 0 1px #ff4b4b;
    }
    .main {
      flex: 1;
      padding: 3rem 4rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
      max-width: 900px;
    }
    h1 {
      font-size: 2.5rem;
      font-weight: 700;
      color: #0e1117;
      line-height: 1.2;
    }
    p {
      font-size: 1.1rem;
      line-height: 1.6;
      color: #3a3d4a;
    }
    .stButton > button {
      background: #ff4b4b;
      color: white;
      border: none;
      padding: 0.6rem 1.8rem;
      font-size: 1rem;
      font-weight: 600;
      border-radius: 0.5rem;
      cursor: pointer;
      transition: background 0.2s;
      font-family: inherit;
    }
    .stButton > button:hover { background: #e04343; }
    .result-box {
      background: #fafafa;
      border: 1px solid #e6e9ef;
      border-radius: 0.5rem;
      padding: 1.5rem;
      font-size: 1.2rem;
      word-break: break-word;
    }
    @media (max-width: 768px) {
      .sidebar {
        position: fixed;
        top: 0;
        left: -100%;
        height: 100vh;
        z-index: 999;
        transition: left 0.3s;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
      }
      .sidebar.open { left: 0; }
      .menu-toggle { display: flex; }
      .main { padding: 2rem 1.5rem; padding-top: 4rem; }
      h1 { font-size: 2rem; }
    }
    .menu-toggle {
      display: none;
      position: fixed;
      top: 1rem;
      left: 1rem;
      z-index: 1000;
      background: #ff4b4b;
      color: white;
      border: none;
      border-radius: 0.5rem;
      width: 40px;
      height: 40px;
      font-size: 1.5rem;
      cursor: pointer;
      align-items: center;
      justify-content: center;
    }
    .overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.3);
      z-index: 998;
    }
    .overlay.active { display: block; }
  </style>
</head>
<body>
  <button class="menu-toggle" id="menuToggle" aria-label="Toggle sidebar">☰</button>
  <div class="overlay" id="overlay"></div>

  <aside class="sidebar" id="sidebar">
    <div>
      <label for="numCount">Number of random numbers</label>
      <input type="number" id="numCount" value="5" min="1" max="100">
    </div>
  </aside>

  <main class="main">
    <h1>AI Random 🎲</h1>
    <p>
      This advanced AI uses a state‑of‑the‑art neural network to generate
      truly random numbers. Just set the desired count in the sidebar and
      click the button below.
    </p>
    <div class="stButton">
      <button id="generateBtn">Generate Random Numbers</button>
    </div>
    <div class="result-box" id="result">
      Your random numbers will appear here...
    </div>
  </main>

  <script>
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');
    const overlay = document.getElementById('overlay');
    function openSidebar() {
      sidebar.classList.add('open');
      overlay.classList.add('active');
    }
    function closeSidebar() {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
    }
    menuToggle.addEventListener('click', () => {
      sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
    });
    overlay.addEventListener('click', closeSidebar);

    document.getElementById('generateBtn').addEventListener('click', () => {
      const count = parseInt(document.getElementById('numCount').value, 10);
      const resultDiv = document.getElementById('result');
      if (isNaN(count) || count < 1) {
        resultDiv.textContent = 'Please enter a valid number (≥ 1).';
        return;
      }
      const numbers = Array.from({ length: count }, () => Math.floor(Math.random() * 100) + 1);
      resultDiv.textContent = numbers.join(', ');
    });

    // initial generation on load
    window.addEventListener('load', () => {
      document.getElementById('generateBtn').click();
    });
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# Vercel requires a callable named `app` (or you can configure in vercel.json)
# The above Flask app will be detected automatically.
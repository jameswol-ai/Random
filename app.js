// ---------- Clear any existing content ----------
document.body.innerHTML = '';

// ---------- Inject Streamlit-style CSS ----------
const style = document.createElement('style');
style.textContent = `
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Source Sans Pro', sans-serif;
    background: #ffffff;
    color: #262730;
    display: flex;
    min-height: 100vh;
    position: relative;
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
    z-index: 2;
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
  .stButton > button:hover {
    background: #e04343;
  }
  .result-box {
    background: #fafafa;
    border: 1px solid #e6e9ef;
    border-radius: 0.5rem;
    padding: 1.5rem;
    font-size: 1.2rem;
    word-break: break-word;
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
    .sidebar.open {
      left: 0;
    }
    .menu-toggle {
      display: flex;
    }
    .main {
      padding: 2rem 1.5rem;
      padding-top: 4rem;
    }
    h1 { font-size: 2rem; }
  }
  .overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.3);
    z-index: 998;
  }
  .overlay.active {
    display: block;
  }
`;
document.head.appendChild(style);

// ---------- Add Google Font (Source Sans Pro) if not already loaded ----------
const fontLink = document.createElement('link');
fontLink.href = 'https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap';
fontLink.rel = 'stylesheet';
document.head.appendChild(fontLink);

// ---------- Create sidebar ----------
const sidebar = document.createElement('aside');
sidebar.className = 'sidebar';
sidebar.id = 'sidebar';

const sidebarLabel = document.createElement('label');
sidebarLabel.htmlFor = 'numCount';
sidebarLabel.textContent = 'Number of random numbers';

const numInput = document.createElement('input');
numInput.type = 'number';
numInput.id = 'numCount';
numInput.value = '5';
numInput.min = '1';
numInput.max = '100';

sidebar.appendChild(sidebarLabel);
sidebar.appendChild(numInput);

// ---------- Create main content ----------
const main = document.createElement('main');
main.className = 'main';

const title = document.createElement('h1');
title.textContent = 'AI Random 🎲';

const description = document.createElement('p');
description.textContent = 'This advanced AI uses a state‑of‑the‑art neural network to generate truly random numbers. Just set the desired count in the sidebar and click the button below.';

const buttonDiv = document.createElement('div');
buttonDiv.className = 'stButton';
const generateBtn = document.createElement('button');
generateBtn.textContent = 'Generate Random Numbers';
buttonDiv.appendChild(generateBtn);

const resultBox = document.createElement('div');
resultBox.className = 'result-box';
resultBox.id = 'result';
resultBox.textContent = 'Your random numbers will appear here...';

main.appendChild(title);
main.appendChild(description);
main.appendChild(buttonDiv);
main.appendChild(resultBox);

// ---------- Create mobile menu toggle & overlay ----------
const menuToggle = document.createElement('button');
menuToggle.className = 'menu-toggle';
menuToggle.id = 'menuToggle';
menuToggle.setAttribute('aria-label', 'Toggle sidebar');
menuToggle.textContent = '☰';

const overlay = document.createElement('div');
overlay.className = 'overlay';
overlay.id = 'overlay';

// ---------- Append everything to body ----------
document.body.appendChild(menuToggle);
document.body.appendChild(overlay);
document.body.appendChild(sidebar);
document.body.appendChild(main);

// ---------- Functionality ----------
function generateNumbers() {
  const count = parseInt(numInput.value, 10);
  if (isNaN(count) || count < 1) {
    resultBox.textContent = 'Please enter a valid number (≥ 1).';
    return;
  }
  const numbers = Array.from({ length: count }, () => Math.floor(Math.random() * 100) + 1);
  resultBox.textContent = numbers.join(', ');
}

generateBtn.addEventListener('click', generateNumbers);

// Mobile sidebar toggle
function openSidebar() {
  sidebar.classList.add('open');
  overlay.classList.add('active');
}
function closeSidebar() {
  sidebar.classList.remove('open');
  overlay.classList.remove('active');
}
menuToggle.addEventListener('click', () => {
  if (sidebar.classList.contains('open')) {
    closeSidebar();
  } else {
    openSidebar();
  }
});
overlay.addEventListener('click', closeSidebar);

// Generate on page load (like Streamlit initial state)
window.addEventListener('load', generateNumbers);
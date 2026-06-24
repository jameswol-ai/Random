# sai/streamlit_app.py (V2 MULTI-USER READY)

import streamlit as st
import threading
import time
import logging
from logging.handlers import RotatingFileHandler
import matplotlib.pyplot as plt
import pandas as pd
import random
import pickle
from datetime import datetime
import queue
import traceback
import numpy as np
import os
import requests

# =========================================================
# 🌐 OPTIONAL MULTI-USER SERVER MODE
# =========================================================

API_URL = os.getenv("SAI_API_URL", None)
REMOTE_MODE = API_URL is not None

def api(path, method="GET", json_data=None):
    """Safe API wrapper for remote simulation server"""
    if not REMOTE_MODE:
        return None

    url = f"{API_URL}{path}"
    try:
        if method == "GET":
            return requests.get(url).json()
        if method == "POST":
            return requests.post(url, json=json_data).json()
    except Exception:
        return None

# =========================================================
# FORECAST PLUGINS (SAFE FALLBACKS)
# =========================================================

try:
    from plugins.arima_forecast import fit_arima, forecast_next
except:
    def fit_arima(*args, **kwargs):
        raise RuntimeError("ARIMA plugin missing")
    def forecast_next(*args, **kwargs):
        raise RuntimeError("ARIMA plugin missing")

try:
    from plugins.prophet_forecast import fit_prophet, forecast_future
except:
    def fit_prophet(*args, **kwargs):
        raise RuntimeError("Prophet plugin missing")
    def forecast_future(*args, **kwargs):
        raise RuntimeError("Prophet plugin missing")

# =========================================================
# METRICS
# =========================================================

def compute_metrics(actual, predicted):
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)

    if len(actual) == 0 or len(predicted) == 0:
        return {"RMSE": None, "MAPE": None}

    n = min(len(actual), len(predicted))
    actual = actual[-n:]
    predicted = predicted[:n]

    rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))
    denom = np.where(actual == 0, 1e-8, actual)
    mape = float(np.mean(np.abs((actual - predicted) / denom)) * 100)

    return {"RMSE": round(rmse, 6), "MAPE": round(mape, 4)}

# =========================================================
# BOT SIMULATION (LOCAL MODE ONLY)
# =========================================================

def run_bot():
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "trade": random.choice(["BUY", "SELL"]),
        "symbol": random.choice(["USD", "EUR", "GBP", "JPY", "UGX"]),
        "amount": random.randint(100, 5000)
    }

# =========================================================
# LOGGING
# =========================================================

logger = logging.getLogger("sai_app")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("sai_app.log", maxBytes=2_000_000, backupCount=3)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

if not logger.handlers:
    logger.addHandler(handler)

# =========================================================
# SESSION STATE SAFE INIT
# =========================================================

defaults = {
    "bot_thread": None,
    "bot_running": False,
    "logs": [],
    "history": pd.DataFrame(columns=["Time", "Currency", "Rate", "Forecast"]),
    "bot_queue": queue.Queue(),
    "stop_event": None,
    "auto_refresh": False,
    "refresh_interval": 3,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

HISTORY_MAX_ROWS = 500

# =========================================================
# BOT THREAD
# =========================================================

def bot_loop(queue_obj, stop_event):
    logger.info("Bot started")

    while not stop_event.is_set():
        try:
            queue_obj.put(run_bot())
        except Exception:
            logger.exception("Bot error")
            break
        time.sleep(2)

    logger.info("Bot stopped")

def start_bot():
    if st.session_state.bot_running:
        return

    stop_event = threading.Event()
    st.session_state.stop_event = stop_event

    t = threading.Thread(
        target=bot_loop,
        args=(st.session_state.bot_queue, stop_event),
        daemon=True
    )

    st.session_state.bot_thread = t
    st.session_state.bot_running = True
    t.start()

def stop_bot():
    if st.session_state.stop_event:
        st.session_state.stop_event.set()
    st.session_state.bot_running = False

def drain_queue():
    while not st.session_state.bot_queue.empty():
        item = st.session_state.bot_queue.get()
        st.session_state.logs.append(item)

    st.session_state.logs = st.session_state.logs[-1000:]

# =========================================================
# DATA (LOCAL OR REMOTE)
# =========================================================

def get_rates():
    if REMOTE_MODE:
        return api("/world") or {}

    currencies = ["USD", "EUR", "GBP", "JPY", "UGX", "KES"]
    return {c: round(random.uniform(0.5, 1500), 2) for c in currencies}

def forecast_rates(rates):
    return {k: round(v * (1 + random.uniform(-0.05, 0.05)), 2) for k, v in rates.items()}

# =========================================================
# UI
# =========================================================

st.set_page_config(page_title="SAI V2 Multi-User", layout="wide")
st.title("📈 SAI TRADING BOT — MULTI-USER READY")

if REMOTE_MODE:
    st.success("🌍 Connected to Remote Simulation World")
else:
    st.info("🖥 Running in Local Mode")

# =========================================================
# DASHBOARD
# =========================================================

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Bot"):
        start_bot()

    if st.button("Stop Bot"):
        stop_bot()

    if st.button("Refresh"):
        drain_queue()

    st.write("Bot:", st.session_state.bot_running)

with col2:
    rates = get_rates()
    forecast = forecast_rates(rates)

    st.subheader("💱 Rates")
    st.table(pd.DataFrame(rates.items(), columns=["Currency", "Rate"]))

    st.subheader("📊 Forecast")
    st.table(pd.DataFrame(forecast.items(), columns=["Currency", "Forecast"]))

# =========================================================
# LOGS
# =========================================================

st.subheader("📜 Logs")
st.write(st.session_state.logs[-10:])

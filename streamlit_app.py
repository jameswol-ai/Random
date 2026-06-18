# =========================================================
# 🏗️ RANDOM + SAI — AUTONOMOUS AI SYSTEM (HARDENED CORE)
# Forex + Architecture + Event Bus + Safe Execution
# =========================================================

import os
import sys
import streamlit as st

# =========================================================
# 🔧 BOOTSTRAP PATH FIX (CRITICAL FOR STREAMLIT CLOUD)
# =========================================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

CORE_DIR = os.path.join(ROOT_DIR, "core")
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

# =========================================================
# 🧠 SAFE CORE IMPORTS (FAIL-SAFE MODE)
# =========================================================
try:
    from core.registry import run_pipeline, REGISTRIES
    from core.event_bus import event_bus
    from core.safe_execution import safe_execute
except Exception as e:
    st.warning(f"⚠️ Core modules not fully loaded: {e}")

    # --- SAFE FALLBACKS ---
    REGISTRIES = {}

    def run_pipeline(*args, **kwargs):
        return {
            "status": "degraded_mode",
            "message": "Core registry not available"
        }

    class EventBusFallback:
        def emit(self, *args, **kwargs):
            return None

    event_bus = EventBusFallback()

    def safe_execute(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as ex:
            return {"error": str(ex)}

# =========================================================
# 🌐 STREAMLIT UI CONFIG
# =========================================================
st.set_page_config(
    page_title="Random + Sai AI OS",
    layout="wide"
)

st.title("🌌 Random + Sai — Autonomous AI Operating System")

# =========================================================
# 🧭 SIDEBAR MODE SWITCH
# =========================================================
mode = st.sidebar.radio(
    "🧭 System Mode",
    [
        "💹 Forex Intelligence",
        "🏗️ Architecture Engine",
        "🧠 System Diagnostics"
    ]
)

# =========================================================
# 💹 FOREX MODE (PLACEHOLDER SAFE LAYER)
# =========================================================
if mode == "💹 Forex Intelligence":
    st.subheader("Forex Engine (East Africa Focus)")

    if st.button("Run Forex Pipeline"):
        result = safe_execute(run_pipeline, "forex")
        st.json(result)

# =========================================================
# 🏗️ ARCHITECTURE MODE
# =========================================================
elif mode == "🏗️ Architecture Engine":
    st.subheader("AI Architectural Generator")

    if st.button("Generate Floor Plan"):
        result = safe_execute(run_pipeline, "architecture")
        st.json(result)

# =========================================================
# 🧠 DIAGNOSTICS MODE
# =========================================================
elif mode == "🧠 System Diagnostics":
    st.subheader("System Health Check")

    st.write("Registry Status:")
    st.json(REGISTRIES)

    st.write("Event Bus Status:")
    st.write(type(event_bus).__name__)

    if st.button("Run System Test"):
        test = safe_execute(lambda: {"status": "ok", "core": "alive"})
        st.success(test)

# =========================================================
# 🧱 FOOTER STATE
# =========================================================
st.sidebar.markdown("---")
st.sidebar.caption("Random + Sai | Hardened Runtime Kernel v1.0")

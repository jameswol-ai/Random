# =========================================================
# 🏗️ RANDOM OS — AUTONOMOUS ARCHITECTURE STREAMLIT KERNEL
# Plugin-driven AI Civilization System
# =========================================================

import streamlit as st
import os
import sys
import traceback

# =========================================================
# BOOT KERNEL (SAFE PATH SETUP)
# =========================================================
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# =========================================================
# SAFE CORE IMPORTS (NO CRASH MODE)
# =========================================================
CORE_AVAILABLE = True
BOOT_ERRORS = []

try:
    from core.registry import REGISTRY, register, get, list_modules
    from core.pipeline import run_pipeline
    from core.autoload import auto_load
except Exception as e:
    CORE_AVAILABLE = False
    BOOT_ERRORS.append(str(e))

    # fallback registry
    REGISTRY = {"engines": {}, "agents": {}, "pipelines": {}}

    def auto_load(x):
        pass

    def run_pipeline(*args, **kwargs):
        return {"status": "fallback", "message": "Core system missing"}

# =========================================================
# APP CONFIG
# =========================================================
st.set_page_config(page_title="Random OS — Autonomous Kernel", layout="wide")
st.title("🏗️ RANDOM OS — Autonomous Architecture Kernel")

# =========================================================
# AUTO LOAD PLUGINS
# =========================================================
auto_load("modules")

# =========================================================
# SYSTEM HEALTH PANEL
# =========================================================
st.sidebar.header("🧱 System Status")

if CORE_AVAILABLE:
    st.sidebar.success("Core Online")
else:
    st.sidebar.error("Core Missing (Fallback Mode)")

if BOOT_ERRORS:
    st.sidebar.warning("Boot Errors")
    st.sidebar.text("\n".join(BOOT_ERRORS))

# =========================================================
# REGISTRY VIEW
# =========================================================
st.sidebar.header("🛰️ Registry")
st.sidebar.json(REGISTRY)

# =========================================================
# MAIN UI
# =========================================================
mode = st.sidebar.selectbox(
    "System Mode",
    [
        "🧠 Engine Runtime",
        "🧩 Module Explorer",
        "🚀 Pipeline Runner"
    ]
)

# =========================================================
# 🧠 ENGINE RUNTIME
# =========================================================
if mode == "🧠 Engine Runtime":

    st.header("🧠 Autonomous Engine Runtime")

    engines = list(REGISTRY.get("engines", {}).keys())

    if not engines:
        st.warning("No engines loaded. Add modules to /modules folder.")
    else:
        selected = st.selectbox("Select Engine", engines)
        input_text = st.text_area("Input")

        if st.button("Run Engine"):

            try:
                result = run_pipeline(selected, input_text)
                st.success("Execution Complete")
                st.json(result)

            except Exception:
                st.error(traceback.format_exc())

# =========================================================
# 🧩 MODULE EXPLORER
# =========================================================
elif mode == "🧩 Module Explorer":

    st.header("🧩 Discovered Modules")

    st.subheader("Engines")
    st.json(REGISTRY.get("engines", {}))

    st.subheader("Agents")
    st.json(REGISTRY.get("agents", {}))

    st.subheader("Pipelines")
    st.json(REGISTRY.get("pipelines", {}))

# =========================================================
# 🚀 PIPELINE RUNNER
# =========================================================
elif mode == "🚀 Pipeline Runner":

    st.header("🚀 Dynamic Pipeline Execution")

    engine = st.text_input("Engine Name")
    payload = st.text_area("Payload")

    if st.button("Execute Pipeline"):

        try:
            result = run_pipeline(engine, payload)
            st.json(result)

        except Exception:
            st.error(traceback.format_exc())

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("Random OS — Autonomous Plugin Architecture Kernel v1")

import streamlit as st
from engine.evolution import run_evolution
from engine.planner import generate_floor_plan
from visualization.svg_blueprint import generate_svg_blueprint
from visualization.three_viewer import generate_threejs_html

def render_design_lab(mem, log_event, state):
    st.title("🏗️ Design Lab")
    
    # Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        building_type = st.selectbox("Building Type", ["Residential", "Commercial"], key="type")
    with col2:
        bedrooms = st.slider("Bedrooms", 1, 5, 3, key="bedrooms")
    with col3:
        if st.button("🚀 Evolve!", type="primary", use_container_width=True):
            with st.spinner("Evolving designs..."):
                best, history = run_evolution(
                    btype=building_type,
                    bedrooms=bedrooms,
                    gens=5,
                    pop_size=20
                )
                # Generate floor plan
                best["plan"] = generate_floor_plan(best)
                mem["designs"].append(best)
                state["active"] = best
                state["history"] = history
                log_event(mem, f"Generated design {best['id']}")
                st.rerun()
    
    # Active design display
    if state.get("active"):
        d = state["active"]
        
        # Metrics
        st.subheader(f"📐 Design {d['id']}")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Score", f"{d.get('score', 0):.1f}")
        m2.metric("Area", f"{d['area_sqm']} m²")
        m3.metric("Cost", f"${d.get('cost', 0):,}")
        m4.metric("Rooms", len(d.get("plan", [])))
        
        # 2D Blueprint + 3D Viewer side by side
        st.subheader("📊 2D Blueprint")
        if d.get("plan"):
            svg = generate_svg_blueprint(d["plan"])
            st.markdown(svg, unsafe_allow_html=True)
        
        st.subheader("🏛️ 3D Viewer")
        if d.get("plan"):
            three_html = generate_threejs_html(d["plan"])
            st.components.v1.html(three_html, height=450)
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Export as IFC"):
                # Placeholder for IFC export
                st.info("IFC export coming soon!")
        with col2:
            if st.button("📤 Export as glTF"):
                st.info("glTF export coming soon!")
    
    else:
        st.info("👈 Click 'Evolve!' to generate your first design.")

import streamlit as st
from engine.evolution import run_evolution
from engine.planner import generate_floor_plan
from visualization.svg_blueprint import generate_svg_blueprint
from visualization.three_viewer import generate_threejs_html
from engine.export_ifc import export_ifc
from engine.export_gltf import generate_gltf

def render_design_lab(mem, log_event, state):
    st.title("🏗️ Design Lab")
    
    # ... (keep existing controls and metrics code) ...
    
    # After displaying 2D and 3D, add export section
    if state.get("active"):
        d = state["active"]
        
        # Export section
        st.subheader("📤 Export")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export IFC", use_container_width=True):
                if d.get("plan"):
                    ifc_data = export_ifc(d["plan"])
                    st.download_button(
                        label="⬇️ Download IFC",
                        data=ifc_data,
                        file_name=f"{d['id']}.ifc",
                        mime="application/x-ifc",
                        key="ifc_download"
                    )
                else:
                    st.warning("No plan data to export.")
        
        with col2:
            if st.button("🔷 Export glTF", use_container_width=True):
                if d.get("plan"):
                    glb_data = generate_gltf(d["plan"])
                    if glb_data and glb_data != b"GLB export requires trimesh. pip install trimesh":
                        st.download_button(
                            label="⬇️ Download glTF",
                            data=glb_data,
                            file_name=f"{d['id']}.glb",
                            mime="model/gltf-binary",
                            key="gltf_download"
                        )
                    else:
                        st.warning("glTF export requires trimesh. pip install trimesh")
                else:
                    st.warning("No plan data to export.")
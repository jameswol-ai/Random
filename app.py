elif page == "Random Copilot":
    st.markdown("## 🧠 Random Copilot – Full Design Control")
    
    category = st.radio("Building Category", list(ARCHITECTURE_TYPES.keys()), horizontal=True)
    building = st.selectbox("Building Type", ARCHITECTURE_TYPES[category])
    
    col1, col2 = st.columns(2)
    with col1:
        num_floors = st.slider("Floors", 1, 5, 2)
        total_rooms = st.slider("Total Rooms", num_floors, num_floors*8, num_floors*2,
                                help="Total across all floors")
    with col2:
        total_doors = st.slider("Total Doors", total_rooms, total_rooms*3, total_rooms+num_floors)
        total_windows = st.slider("Total Windows", max(0, total_rooms - num_floors), total_rooms*2, total_rooms)
    
    modules = st.slider("Complexity (Modules)", 1, 10, 4)
    generations = st.slider("Evolution Cycles", 2, 30, 8)
    population = st.slider("Population", 4, 40, 12)
    
    enforce_standards = st.checkbox("Enforce Architectural Standards (room sizes, daylight, grid)", value=True)
    
    if st.button("🚀 Generate Design"):
        with st.spinner("Evolving with standards..."):
            best, history, all_designs = evolve_design_multi(
                building=building,
                modules=modules,
                generations=generations,
                population_size=population,
                num_floors=num_floors,
                total_rooms=total_rooms,
                total_doors=total_doors,
                total_windows=total_windows,
                enforce_standards=enforce_standards
            )
            st.success(f"Design {best['id']} created!")
            # ... rest of handling (save to session, XP, etc.) unchanged ...

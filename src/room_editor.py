import streamlit as st
from .rendering_2d import generate_floor_plan

def render_room_editor(design):
    if "floors" not in design:
        st.warning("No floor data.")
        return
    floor_idx = st.slider("Floor to edit", 0, len(design["floors"])-1, 0, key="room_editor_floor")
    floor = design["floors"][floor_idx]
    room_names = [f"{r['name']} ({r['type']})" for r in floor["rooms"]]
    selected_room = st.selectbox("Select room", room_names)
    room_idx = room_names.index(selected_room)
    room = floor["rooms"][room_idx]
    
    col1, col2 = st.columns(2)
    with col1:
        new_width = st.number_input("New width (m)", min_value=1.0, max_value=20.0, value=float(room["polygon"][1][0] - room["polygon"][0][0]))
    with col2:
        room_types = ["living","kitchen","dining","bedroom","bathroom","corridor","office","meeting","reception","hall","storage","study"]
        new_type = st.selectbox("Room type", room_types, index=room_types.index(room["type"]) if room["type"] in room_types else 0)
    
    if st.button("Update Room"):
        old_width = room["polygon"][1][0] - room["polygon"][0][0]
        scale = new_width / old_width
        for i in range(len(room["polygon"])):
            x, y = room["polygon"][i]
            room["polygon"][i] = (x * scale, y)
        for op in room["openings"]:
            op["start"] = (op["start"][0] * scale, op["start"][1])
            op["end"] = (op["end"][0] * scale, op["end"][1])
        room["type"] = new_type
        st.success("Room updated!")
        st.image(generate_floor_plan(design, floor_idx), caption="Updated Floor Plan", use_column_width=True)

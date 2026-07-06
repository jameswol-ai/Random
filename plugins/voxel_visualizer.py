import streamlit as st

def slice_view(world, y):
    grid = world[:, y, :]
    out = ""

    for z in range(grid.shape[1]):
        row = ""
        for x in range(grid.shape[0]):
            v = grid[x, z]
            row += "⬛" if v==0 else "🟦" if v==1 else "🟨"
        out += row + "\n"

    st.code(out)
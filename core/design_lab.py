st.subheader("🧠 AI Structural Critic Report")

crit = d.get("critique", None)

if crit:
    st.metric("Overall Verdict Score", crit["scores"]["overall"])
    st.write("### Verdict")
    st.success(crit["verdict"])

    st.write("### Structural Notes")
    st.info(crit["notes"]["structural"])

    st.write("### Cost Notes")
    st.warning(crit["notes"]["cost"])

    st.write("### Spatial Notes")
    st.info(crit["notes"]["spatial"])
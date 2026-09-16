import streamlit as st

st.set_page_config(
    page_title="ContextLock",
    page_icon="🛡️",
    layout="wide",
)

st.sidebar.title("🛡️ ContextLock")

selected_page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Protected Chat",
        "Memory Explorer",
        "Quarantine",
        "Memory Graph",
        "Incidents",
    ],
)

st.sidebar.divider()
st.sidebar.success("System status: Starting development")

if selected_page == "Dashboard":
    st.title("🛡️ ContextLock")
    st.subheader("Self-Healing Memory Firewall for AI Agents")

    st.info(
        "ContextLock protects an AI agent from storing and using "
        "dangerous or untrusted information."
    )

    column1, column2, column3, column4 = st.columns(4)

    column1.metric("Total memories", 0)
    column2.metric("Active memories", 0)
    column3.metric("Quarantined", 0)
    column4.metric("Threats blocked", 0)

    st.divider()

    st.subheader("Development status")

    st.write("✅ Project environment created")
    st.write("✅ Basic dashboard created")
    st.write("⏳ Memory database not implemented")
    st.write("⏳ Security engine not implemented")
    st.write("⏳ AI agent not implemented")
    st.write("⏳ Self-healing system not implemented")

elif selected_page == "Protected Chat":
    st.title("Protected AI Chat")
    st.warning("This feature will be implemented later.")

elif selected_page == "Memory Explorer":
    st.title("Memory Explorer")
    st.warning("The memory database will be implemented later.")

elif selected_page == "Quarantine":
    st.title("Quarantine")
    st.warning("The quarantine system will be implemented later.")

elif selected_page == "Memory Graph":
    st.title("Memory Relationship Graph")
    st.warning("The relationship graph will be implemented later.")

elif selected_page == "Incidents":
    st.title("Security Incidents")
    st.warning("The incident system will be implemented later.")
import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database.database import (
    initialize_database, save_memory, get_all_memories,
    get_active_memories, get_quarantined_memories,
    update_memory_status, delete_memory, get_memory_counts
)
from security.risk_engine import analyze_memory

# Initialize database on startup
initialize_database()

st.set_page_config(
    page_title="ContextLock",
    page_icon="🛡️",
    layout="wide",
)

st.sidebar.title("🛡️ ContextLock")
selected_page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Memory", "Memory Explorer", "Quarantine", "Memory Graph", "Incidents"],
)
st.sidebar.divider()

counts = get_memory_counts()
if counts["quarantined"] > 0:
    st.sidebar.error(f"⚠️ {counts['quarantined']} quarantined memories")
else:
    st.sidebar.success("✅ System status: Protected")

# ─── DASHBOARD ───────────────────────────────────────────────
if selected_page == "Dashboard":
    st.title("🛡️ ContextLock")
    st.subheader("Self-Healing Memory Firewall for AI Agents")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Memories", counts["total"])
    col2.metric("Active", counts["active"])
    col3.metric("Quarantined", counts["quarantined"])
    col4.metric("Pending Approval", counts["pending"])

    st.divider()

    st.subheader("Recent Memories")
    memories = get_all_memories()
    if memories:
        for m in memories[:5]:
            status_icon = {"active": "🟢", "quarantined": "🔴", 
                           "pending_approval": "🟠", "restricted": "🟡"}.get(m["status"], "⚪")
            st.write(f"{status_icon} **{m['content'][:80]}** | Source: `{m['source_type']}` | "
                     f"Risk: `{m['risk_score']}/100` | Status: `{m['status']}`")
    else:
        st.info("No memories stored yet. Go to 'Add Memory' to begin.")

    st.divider()
    st.subheader("Development Status")
    st.write("✅ Project environment created")
    st.write("✅ Basic dashboard created")
    st.write("✅ Memory database implemented")
    st.write("✅ Risk scoring engine implemented")
    st.write("⏳ Protected AI chat — coming Week 3")
    st.write("⏳ Memory relationship graph — coming Week 5")
    st.write("⏳ Self-healing recovery — coming Week 6")

# ─── ADD MEMORY ──────────────────────────────────────────────
elif selected_page == "Add Memory":
    st.title("🧠 Add / Test Memory")
    st.write("Enter information below. ContextLock will analyze it before storing.")

    with st.form("add_memory_form"):
        content = st.text_area("Information to store", placeholder="e.g. My project deadline is 20 October")
        
        col1, col2 = st.columns(2)
        with col1:
            source_type = st.selectbox("Source", [
                "user_direct", "uploaded_document", "agent_generated",
                "website", "unknown_email", "quarantined_source"
            ])
        with col2:
            context = st.selectbox("Current task context", [
                "general", "project_management", "email_communication",
                "document_summary", "task_creation", "security_settings"
            ])

        submitted = st.form_submit_button("🔍 Analyze & Save")

    if submitted and content.strip():
        analysis = analyze_memory(content, source_type, context)

        st.divider()
        st.subheader("🛡️ ContextLock Analysis")

        col1, col2, col3 = st.columns(3)
        col1.metric("Trust Score", f"{analysis['trust_score']}/100")
        col2.metric("Risk Score", f"{analysis['risk_score']}/100")
        col3.write(f"**Decision:** {analysis['decision_text']}")

        st.write("**Risk reasons:**")
        for reason in analysis["reasons"]:
            st.write(f"- {reason}")

        memory_id = save_memory(
            content=content,
            source_type=source_type,
            source_reference="manual_entry",
            context=context,
            trust_score=analysis["trust_score"],
            risk_score=analysis["risk_score"],
            status=analysis["status"],
            allowed_contexts=analysis["allowed_contexts"],
            allowed_actions=analysis["allowed_actions"],
            content_hash=analysis["content_hash"],
        )
        st.success(f"Memory #{memory_id} saved with status: **{analysis['status']}**")
    elif submitted:
        st.warning("Please enter some information to analyze.")

# ─── MEMORY EXPLORER ─────────────────────────────────────────
elif selected_page == "Memory Explorer":
    st.title("🔍 Memory Explorer")

    memories = get_all_memories()
    if not memories:
        st.info("No memories stored yet.")
    else:
        df = pd.DataFrame(memories)
        display_cols = ["id", "content", "source_type", "trust_score", "risk_score", "status", "created_at"]
        available = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True)

        st.divider()
        st.subheader("Manage a Memory")
        memory_ids = [m["id"] for m in memories]
        selected_id = st.selectbox("Select memory ID", memory_ids)

        selected_memory = next((m for m in memories if m["id"] == selected_id), None)
        if selected_memory:
            st.json(selected_memory)
            col1, col2, col3 = st.columns(3)
            if col1.button("✅ Mark Active"):
                update_memory_status(selected_id, "active")
                st.rerun()
            if col2.button("🔴 Quarantine"):
                update_memory_status(selected_id, "quarantined")
                st.rerun()
            if col3.button("🗑️ Delete"):
                delete_memory(selected_id)
                st.rerun()

# ─── QUARANTINE ──────────────────────────────────────────────
elif selected_page == "Quarantine":
    st.title("🔴 Quarantine")
    st.write("These memories were flagged as dangerous and blocked from active use.")

    quarantined = get_quarantined_memories()
    if not quarantined:
        st.success("No quarantined memories. The system is clean.")
    else:
        for m in quarantined:
            with st.expander(f"Memory #{m['id']}: {m['content'][:60]}..."):
                st.write(f"**Content:** {m['content']}")
                st.write(f"**Source:** {m['source_type']}")
                st.write(f"**Risk Score:** {m['risk_score']}/100")
                st.write(f"**Created:** {m['created_at']}")
                if st.button(f"Restore Memory #{m['id']}", key=f"restore_{m['id']}"):
                    update_memory_status(m["id"], "active")
                    st.rerun()

# ─── PLACEHOLDERS ────────────────────────────────────────────
elif selected_page == "Memory Graph":
    st.title("📊 Memory Relationship Graph")
    st.warning("This will be implemented in Week 5.")

elif selected_page == "Incidents":
    st.title("🚨 Security Incidents")
    st.warning("This will be implemented in Week 6.")
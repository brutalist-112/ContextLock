elif page == "💬 Protected Chat":
    st.title("💬 Protected Chat")
    st.caption("This chatbot only uses memories with Active security status.")

    from agent.memory_agent import MemoryAgent
    agent = MemoryAgent()

    safe_memories = agent.get_safe_memories()
    st.info(f"🔒 {len(safe_memories)} trusted memories loaded into context.")

    if len(safe_memories) == 0:
        st.warning("No active memories found. Add some safe memories first.")
    else:
        with st.expander("👁️ View loaded memory context"):
            st.text(agent.build_context())

    st.divider()
    st.subheader("Ask a Question")

    user_input = st.text_input("Your question:", placeholder="e.g. What do you know about my project?")

    if st.button("Ask") and user_input:
        with st.spinner("Thinking..."):
            response = agent.respond(user_input)
        st.markdown("**ContextLock says:**")
        st.success(response)
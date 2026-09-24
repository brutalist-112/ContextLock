### ✅ Week 3 — Protected AI Chatbot
**Aim:** Build an AI chat interface that only uses memories with Active security status — quarantined memories are completely blocked from influencing the chatbot.

**Completed:**
- Built `💬 Protected Chat` page directly inside `app.py`
- Chatbot loads **only active memories** as context — quarantined memories are never used
- Implemented keyword-based memory retrieval to answer user questions
- Used `st.chat_message` for proper chat bubble UI
- Used `st.chat_input` for a clean chat bar at the bottom
- Added persistent chat history within a session using `st.session_state`
- Live stats bar shows trusted memories loaded vs. quarantined memories blocked
- Expandable memory context viewer so user can see what the chatbot knows
- Clear chat history button to reset the conversation

**Output:** A working memory-protected chatbot. Ask it anything — it answers only from safe memories, and dangerous/quarantined memories can never influence its responses.
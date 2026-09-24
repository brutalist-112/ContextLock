# agent/memory_agent.py
from database.database import DatabaseManager

class MemoryAgent:
    def __init__(self):
        self.db = DatabaseManager()

    def get_safe_memories(self):
        """Retrieve only memories with 'active' status."""
        conn = self.db.get_connection()
        cursor = conn.execute(
            "SELECT content, source, trust_score FROM memories WHERE security_status = 'active'"
        )
        memories = cursor.fetchall()
        conn.close()
        return memories

    def build_context(self):
        """Build a context string from safe memories only."""
        memories = self.get_safe_memories()
        if not memories:
            return "No trusted memories available."
        
        context_lines = []
        for mem in memories:
            content, source, trust = mem
            context_lines.append(f"[Source: {source} | Trust: {trust}%] {content}")
        
        return "\n".join(context_lines)

    def respond(self, user_question: str) -> str:
        """Generate a response using only safe memory context."""
        context = self.build_context()
        
        # Simple keyword-based response (no external AI API needed)
        question_lower = user_question.lower()
        memories = self.get_safe_memories()

        matched = []
        for mem in memories:
            content, source, trust = mem
            # Check if any words from the question appear in the memory
            words = question_lower.split()
            if any(word in content.lower() for word in words if len(word) > 3):
                matched.append(f"• {content} *(from {source}, trust: {trust}%)*")

        if matched:
            answer = "Based on my trusted memories:\n\n" + "\n".join(matched)
        else:
            answer = "I don't have any trusted memories relevant to that question."

        return answer
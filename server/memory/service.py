import json
from database.db import (
    get_working_memory,
    save_working_memory,
    get_chat_history,
    save_chat_message
)
from tools.memory_tool import save_semantic_memory, search_semantic_memories

class MemoryService:
    @staticmethod
    def read_working_memory(session_id: str) -> dict:
        """Reads the short term working memory context for this active session."""
        try:
            raw = get_working_memory(session_id)
            return json.loads(raw)
        except Exception:
            return {}

    @staticmethod
    def write_working_memory(session_id: str, context: dict):
        """Updates the short term working memory context for this active session."""
        try:
            save_working_memory(session_id, json.dumps(context))
        except Exception as e:
            print(f"MemoryService write_working_memory error: {e}")

    @staticmethod
    def read_session_history(session_id: str) -> list:
        """Loads structured message lists from PostgreSQL/SQLite for this session."""
        return get_chat_history(session_id)

    @staticmethod
    def save_session_message(session_id: str, role: str, content: str, input_type="text", output_type="both"):
        """Saves a single message entry into session storage."""
        save_chat_message(session_id, role, content, input_type, output_type)

    @staticmethod
    def read_long_term_memory(query: str, limit=3) -> list:
        """Queries semantic Vector embeddings from ChromaDB."""
        return search_semantic_memories(query, limit)

    @staticmethod
    def save_long_term_memory(content: str, doc_id: str):
        """Indexes key facts or summaries into ChromaDB long-term memory."""
        return save_semantic_memory(content, doc_id)

    @staticmethod
    def get_agent_memory(session_id: str, agent_id: str) -> dict:
        """Retrieves agent-specific contextual memory from session state."""
        session_mem = MemoryService.read_working_memory(session_id)
        return session_mem.get(f"agent_ctx_{agent_id}", {})

    @staticmethod
    def save_agent_memory(session_id: str, agent_id: str, key: str, value):
        """Updates agent-specific contextual memory values in session state."""
        session_mem = MemoryService.read_working_memory(session_id)
        agent_key = f"agent_ctx_{agent_id}"
        if agent_key not in session_mem:
            session_mem[agent_key] = {}
        session_mem[agent_key][key] = value
        MemoryService.write_working_memory(session_id, session_mem)

    @staticmethod
    def get_shared_memory(session_id: str) -> dict:
        """Retrieves shared memory profile data accessible by all agents."""
        session_mem = MemoryService.read_working_memory(session_id)
        return session_mem.get("shared_profile", {
            "operator": "Surya",
            "voice_enabled": True,
            "system_mode": "production"
        })

    @staticmethod
    def save_shared_memory(session_id: str, profile_updates: dict):
        """Appends/updates shared memory parameters."""
        session_mem = MemoryService.read_working_memory(session_id)
        if "shared_profile" not in session_mem:
            session_mem["shared_profile"] = {}
        session_mem["shared_profile"].update(profile_updates)
        MemoryService.write_working_memory(session_id, session_mem)

"""Persistent Conversation History and Memory Manager.
Synchronizes in-memory active cache with permanent SQLite persistence.
"""

from typing import Dict, List, Any, Optional
import time
from app.db.database import db_manager, DatabaseManager

class PersistentMessageStore:
    def __init__(self, db: Optional[DatabaseManager] = None, max_history_per_session: int = 25):
        self.db = db or db_manager
        self.max_history = max_history_per_session
        self._cache: Dict[str, List[Dict[str, Any]]] = {}

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieve conversation history from cache or fallback to SQLite."""
        if session_id in self._cache:
            return list(self._cache[session_id])

        # Load from SQLite
        db_rows = self.db.get_conversation_history(session_id, limit=self.max_history)
        history = [{"role": r["role"], "content": r["content"]} for r in db_rows]
        self._cache[session_id] = history
        return history

    def add_message(
        self,
        session_id: str,
        message: Dict[str, Any],
        tools_called: Optional[List[str]] = None
    ) -> None:
        """Persist message in SQLite and update memory cache."""
        role = message.get("role", "user")
        content = message.get("content", "")

        # 1. Persist to SQLite
        try:
            self.db.save_conversation_message(
                session_id=session_id,
                role=role,
                content=content,
                tools_called=tools_called
            )
        except Exception as e:
            pass

        # 2. Update local session cache
        if session_id not in self._cache:
            self._cache[session_id] = []
        self._cache[session_id].append({"role": role, "content": content})

        # Keep cache bounded
        if len(self._cache[session_id]) > self.max_history * 2:
            self._cache[session_id] = self._cache[session_id][-self.max_history:]

    def clear_session(self, session_id: str) -> None:
        """Clear session from cache and delete from SQLite."""
        self._cache.pop(session_id, None)
        try:
            self.db.clear_conversation_history(session_id)
        except Exception:
            pass

    def list_active_sessions(self) -> List[str]:
        """Return all sessions active in memory or SQLite."""
        db_sessions = set(self.db.list_persisted_sessions())
        cached_sessions = set(self._cache.keys())
        return list(db_sessions.union(cached_sessions))

message_store = PersistentMessageStore()
MessageStore = PersistentMessageStore

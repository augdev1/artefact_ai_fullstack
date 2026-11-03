import os
import pytest
from app.db.database import DatabaseManager

@pytest.fixture
def memory_db():
    """Provides an isolated, in-memory SQLite database populated with challenge data."""
    manager = DatabaseManager(db_path=":memory:")
    manager.init_database(force_reload=True)
    yield manager
    manager.close()

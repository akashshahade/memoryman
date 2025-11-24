"""
Unit tests for Memory Man module
"""

import pytest
import tempfile
import os
from datetime import datetime
from memoryman import MemoryManager


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        yield db_path


@pytest.fixture
def memory_manager(temp_db):
    """Create a memory manager for testing"""
    manager = MemoryManager(storage_type="sqlite", db_path=temp_db)
    yield manager
    manager.close()


class TestMemoryManager:
    """Test MemoryManager basic functionality"""

    def test_initialization(self, memory_manager):
        """Test memory manager initialization"""
        assert memory_manager is not None
        assert memory_manager.storage_type == "sqlite"

    def test_store_and_retrieve_short_term(self, memory_manager):
        """Test storing and retrieving short-term memory"""
        data = {"role": "user", "content": "Hello"}
        memory_manager.store("short_term", data, key="msg_1")

        retrieved = memory_manager.retrieve("short_term", "msg_1")
        assert retrieved is not None
        assert retrieved["role"] == "user"
        assert retrieved["content"] == "Hello"

    def test_store_string_data(self, memory_manager):
        """Test storing string data (should be converted to dict)"""
        key = memory_manager.store("short_term", "Simple message")
        retrieved = memory_manager.retrieve("short_term", key)

        assert retrieved is not None
        assert retrieved["content"] == "Simple message"

    def test_store_long_term(self, memory_manager):
        """Test long-term memory storage"""
        data = {
            "title": "Important Fact",
            "content": "This is important",
            "category": "facts"
        }
        memory_manager.store("long_term", data, key="fact_1")

        retrieved = memory_manager.retrieve("long_term", "fact_1")
        assert retrieved["title"] == "Important Fact"
        assert retrieved["category"] == "facts"

    def test_store_episodic(self, memory_manager):
        """Test episodic memory storage"""
        data = {
            "event": "User asked a question",
            "outcome": "Answered",
        }
        memory_manager.store("episodic", data, key="episode_1")

        retrieved = memory_manager.retrieve("episodic", "episode_1")
        assert retrieved["event"] == "User asked a question"

    def test_store_semantic(self, memory_manager):
        """Test semantic memory storage"""
        data = {
            "title": "Knowledge",
            "content": "Interesting fact",
            "tags": ["learning", "ai"]
        }
        memory_manager.store("semantic", data, key="knowledge_1")

        retrieved = memory_manager.retrieve("semantic", "knowledge_1")
        assert retrieved["tags"] == ["learning", "ai"]

    def test_query_with_filters(self, memory_manager):
        """Test querying with filters"""
        memory_manager.store("short_term", {"role": "user", "content": "Hi"}, key="msg_1")
        memory_manager.store("short_term", {"role": "assistant", "content": "Hello"}, key="msg_2")
        memory_manager.store("short_term", {"role": "user", "content": "How are you?"}, key="msg_3")

        user_msgs = memory_manager.query("short_term", role="user")
        assert len(user_msgs) == 2
        assert all(msg["role"] == "user" for msg in user_msgs)

    def test_search_query(self, memory_manager):
        """Test text search"""
        memory_manager.store("short_term", {"content": "Hello world"}, key="msg_1")
        memory_manager.store("short_term", {"content": "Goodbye world"}, key="msg_2")
        memory_manager.store("short_term", {"content": "Hello there"}, key="msg_3")

        results = memory_manager.query("short_term", search_query="Hello")
        assert len(results) == 2

    def test_get_recent(self, memory_manager):
        """Test getting recent items"""
        for i in range(5):
            memory_manager.store("short_term", {"content": f"Message {i}"}, key=f"msg_{i}")

        recent = memory_manager.get_recent("short_term", limit=2)
        assert len(recent) == 2

    def test_delete(self, memory_manager):
        """Test deleting items"""
        memory_manager.store("short_term", {"content": "Test"}, key="msg_1")

        assert memory_manager.retrieve("short_term", "msg_1") is not None

        deleted = memory_manager.delete("short_term", "msg_1")
        assert deleted is True
        assert memory_manager.retrieve("short_term", "msg_1") is None

    def test_clear(self, memory_manager):
        """Test clearing memory"""
        memory_manager.store("short_term", {"content": "Message 1"}, key="msg_1")
        memory_manager.store("short_term", {"content": "Message 2"}, key="msg_2")

        assert memory_manager.count("short_term") == 2

        memory_manager.clear("short_term")
        assert memory_manager.count("short_term") == 0

    def test_count(self, memory_manager):
        """Test counting items"""
        for i in range(3):
            memory_manager.store("short_term", {"content": f"Message {i}"}, key=f"msg_{i}")

        count = memory_manager.count("short_term")
        assert count == 3

    def test_count_all(self, memory_manager):
        """Test counting all memories"""
        memory_manager.store("short_term", {"content": "Message"}, key="msg_1")
        memory_manager.store("long_term", {"title": "Fact"}, key="fact_1")
        memory_manager.store("episodic", {"event": "Event"}, key="ep_1")
        memory_manager.store("semantic", {"title": "Knowledge"}, key="know_1")

        counts = memory_manager.count()
        assert counts["short_term"] == 1
        assert counts["long_term"] == 1
        assert counts["episodic"] == 1
        assert counts["semantic"] == 1

    def test_list_all(self, memory_manager):
        """Test listing all keys"""
        memory_manager.store("short_term", {"content": "Message 1"}, key="msg_1")
        memory_manager.store("short_term", {"content": "Message 2"}, key="msg_2")

        keys = memory_manager.list_all("short_term")
        assert len(keys) == 2
        assert "msg_1" in keys
        assert "msg_2" in keys

    def test_export_json(self, memory_manager):
        """Test JSON export"""
        memory_manager.store("short_term", {"content": "Message"}, key="msg_1")

        json_str = memory_manager.export_json("short_term")
        assert "Message" in json_str
        assert len(json_str) > 0

    def test_search_cross_memory(self, memory_manager):
        """Test searching across memory types"""
        memory_manager.store("short_term", {"content": "Hello world"}, key="msg_1")
        memory_manager.store("long_term", {"title": "Hello fact"}, key="fact_1")
        memory_manager.store("episodic", {"event": "Hello event"}, key="ep_1")

        results = memory_manager.search("Hello", limit=5)
        assert "short_term" in results
        assert "long_term" in results
        assert "episodic" in results

    def test_invalid_memory_type(self, memory_manager):
        """Test error handling for invalid memory type"""
        with pytest.raises(ValueError):
            memory_manager.store("invalid_type", {"data": "test"})

        with pytest.raises(ValueError):
            memory_manager.query("invalid_type")

    def test_context_manager(self, temp_db):
        """Test using memory manager as context manager"""
        with MemoryManager(storage_type="sqlite", db_path=temp_db) as memory:
            memory.store("short_term", {"content": "Test"}, key="msg_1")
            assert memory.count("short_term") == 1


class TestMemoryTypes:
    """Test specific memory type features"""

    def test_short_term_recent(self, memory_manager):
        """Test short-term memory get_recent"""
        for i in range(5):
            memory_manager.store("short_term", {"content": f"Message {i}"}, key=f"msg_{i}")

        recent = memory_manager.short_term.get_recent(limit=3)
        assert len(recent) == 3

    def test_long_term_category(self, memory_manager):
        """Test long-term memory by category"""
        memory_manager.store("long_term", {"title": "AI Fact", "category": "ai"}, key="fact_1")
        memory_manager.store("long_term", {"title": "Python Fact", "category": "programming"}, key="fact_2")

        ai_facts = memory_manager.long_term.get_by_category("ai")
        assert len(ai_facts) == 1
        assert ai_facts[0]["title"] == "AI Fact"

    def test_episodic_date_range(self, memory_manager):
        """Test episodic memory date range query"""
        start_date = "2025-01-01T00:00:00"
        end_date = "2025-12-31T23:59:59"

        memory_manager.store("episodic", {
            "event": "Event 1",
            "timestamp": "2025-06-15T10:00:00"
        }, key="ep_1")

        results = memory_manager.episodic.get_by_date_range(start_date, end_date)
        assert len(results) == 1

    def test_semantic_tags(self, memory_manager):
        """Test semantic memory search by tags"""
        memory_manager.store("semantic", {
            "title": "Knowledge 1",
            "tags": ["ai", "learning"]
        }, key="know_1")

        memory_manager.store("semantic", {
            "title": "Knowledge 2",
            "tags": ["python", "programming"]
        }, key="know_2")

        results = memory_manager.semantic.search_by_tags(["ai"])
        assert len(results) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

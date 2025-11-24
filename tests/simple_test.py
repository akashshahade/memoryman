"""
Simple test script to verify Memory Man functionality
"""

import sys
import os
import tempfile
from datetime import datetime

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memoryman import MemoryManager


def test_basic_operations():
    """Test basic memory operations"""
    print("Testing AI Memory Module...")
    print("=" * 60)

    # Create temporary database
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        memory = MemoryManager(storage_type="sqlite", db_path=db_path)

        # Test 1: Store and retrieve short-term
        print("\n✓ Test 1: Short-term Memory (Store & Retrieve)")
        memory.store("short_term", {"role": "user", "content": "Hello"}, key="msg_1")
        data = memory.retrieve("short_term", "msg_1")
        assert data is not None, "Failed to retrieve data"
        assert data["content"] == "Hello", "Content mismatch"
        print("  PASSED - Stored and retrieved message")

        # Test 2: Long-term memory
        print("\n✓ Test 2: Long-term Memory")
        memory.store("long_term", {
            "title": "Python",
            "content": "A programming language",
            "category": "programming"
        }, key="fact_1")
        data = memory.retrieve("long_term", "fact_1")
        assert data["title"] == "Python", "Title mismatch"
        print("  PASSED - Stored and retrieved fact")

        # Test 3: Episodic memory
        print("\n✓ Test 3: Episodic Memory")
        memory.store("episodic", {
            "event": "User asked question",
            "outcome": "Answered"
        }, key="ep_1")
        data = memory.retrieve("episodic", "ep_1")
        assert data["event"] == "User asked question", "Event mismatch"
        print("  PASSED - Stored and retrieved episode")

        # Test 4: Semantic memory
        print("\n✓ Test 4: Semantic Memory")
        memory.store("semantic", {
            "title": "AI",
            "content": "Artificial Intelligence",
            "tags": ["ai", "tech"]
        }, key="know_1")
        data = memory.retrieve("semantic", "know_1")
        assert "ai" in data["tags"], "Tags mismatch"
        print("  PASSED - Stored and retrieved knowledge")

        # Test 5: Query with filters
        print("\n✓ Test 5: Query with Filters")
        memory.store("short_term", {"role": "user", "content": "Hi"}, key="msg_2")
        memory.store("short_term", {"role": "assistant", "content": "Hello"}, key="msg_3")
        user_msgs = memory.query("short_term", role="user")
        assert len(user_msgs) == 2, "Filter query failed"
        print(f"  PASSED - Found {len(user_msgs)} user messages")

        # Test 6: Text search
        print("\n✓ Test 6: Text Search")
        memory.store("long_term", {"title": "JavaScript", "content": "A web language"}, key="fact_2")
        results = memory.query("long_term", search_query="language")
        assert len(results) >= 1, "Text search failed"
        print(f"  PASSED - Text search found {len(results)} results")

        # Test 7: Get recent
        print("\n✓ Test 7: Get Recent")
        recent = memory.get_recent("short_term", limit=2)
        assert len(recent) == 2, "Get recent failed"
        print(f"  PASSED - Retrieved {len(recent)} recent items")

        # Test 8: Delete
        print("\n✓ Test 8: Delete")
        deleted = memory.delete("short_term", "msg_1")
        assert deleted, "Delete failed"
        data = memory.retrieve("short_term", "msg_1")
        assert data is None, "Item not deleted"
        print("  PASSED - Successfully deleted item")

        # Test 9: Count
        print("\n✓ Test 9: Count Statistics")
        counts = memory.count()
        assert isinstance(counts, dict), "Count failed"
        print(f"  PASSED - Memory stats: {counts}")

        # Test 10: Search cross-memory
        print("\n✓ Test 10: Cross-Memory Search")
        results = memory.search("learning", limit=5)
        assert isinstance(results, dict), "Cross-memory search failed"
        print(f"  PASSED - Found results in {len(results)} memory types")

        # Test 11: Clear
        print("\n✓ Test 11: Clear Memory")
        memory.clear("short_term")
        count = memory.count("short_term")
        assert count == 0, "Clear failed"
        print("  PASSED - Successfully cleared memory")

        # Test 12: Export
        print("\n✓ Test 12: Export JSON")
        json_str = memory.export_json("long_term")
        assert len(json_str) > 0, "Export failed"
        print(f"  PASSED - Exported {len(json_str)} bytes")

        memory.close()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_basic_operations()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

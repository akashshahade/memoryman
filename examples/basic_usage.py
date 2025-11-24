"""
Comprehensive example usage of Memory Man module
"""

from memoryman import MemoryManager
from datetime import datetime


def main():
    # Initialize memory manager
    print("=" * 60)
    print("AI Memory Module - Usage Examples")
    print("=" * 60)
    print()

    # Create memory manager with SQLite backend
    memory = MemoryManager(storage_type="sqlite", db_path="./demo_memory.db")

    # ============ SHORT-TERM MEMORY ============
    print("1. SHORT-TERM MEMORY (Recent Conversations)")
    print("-" * 60)

    # Store conversation messages
    memory.store("short_term", {
        "role": "user",
        "content": "What is machine learning?",
        "timestamp": datetime.now().isoformat()
    }, key="msg_1")

    memory.store("short_term", {
        "role": "assistant",
        "content": "Machine learning is a subset of AI...",
        "timestamp": datetime.now().isoformat()
    }, key="msg_2")

    memory.store("short_term", {
        "role": "user",
        "content": "Can you explain neural networks?",
        "timestamp": datetime.now().isoformat()
    }, key="msg_3")

    # Get recent messages
    recent = memory.get_recent("short_term", limit=2)
    print(f"Recent messages (last 2):")
    for msg in recent:
        print(f"  - {msg['role']}: {msg['content'][:50]}...")
    print()

    # Query by role
    user_msgs = memory.query("short_term", role="user")
    print(f"User messages: {len(user_msgs)}")
    for msg in user_msgs:
        print(f"  - {msg['content'][:50]}...")
    print()

    # ============ LONG-TERM MEMORY ============
    print("2. LONG-TERM MEMORY (Persistent Facts)")
    print("-" * 60)

    # Store facts/knowledge
    memory.store("long_term", {
        "title": "Python Basics",
        "content": "Python is a high-level programming language",
        "category": "programming",
        "timestamp": datetime.now().isoformat()
    }, key="fact_python")

    memory.store("long_term", {
        "title": "AI Definition",
        "content": "Artificial Intelligence refers to machine intelligence",
        "category": "ai",
        "timestamp": datetime.now().isoformat()
    }, key="fact_ai")

    # Get by category
    ai_facts = memory.query("long_term", category="ai")
    print(f"AI-related facts: {len(ai_facts)}")
    for fact in ai_facts:
        print(f"  - {fact['title']}: {fact['content'][:40]}...")
    print()

    # ============ EPISODIC MEMORY ============
    print("3. EPISODIC MEMORY (Events & Episodes)")
    print("-" * 60)

    # Store episodes/events
    memory.store("episodic", {
        "event": "User asked about ML",
        "duration": "2 minutes",
        "outcome": "Question answered",
        "timestamp": datetime.now().isoformat()
    }, key="episode_1")

    memory.store("episodic", {
        "event": "User learned about neural networks",
        "duration": "5 minutes",
        "outcome": "Concept explained",
        "timestamp": datetime.now().isoformat()
    }, key="episode_2")

    # Get all episodes
    episodes = memory.query("episodic")
    print(f"Total episodes: {len(episodes)}")
    for ep in episodes:
        print(f"  - {ep['event']} ({ep['duration']})")
    print()

    # ============ SEMANTIC MEMORY ============
    print("4. SEMANTIC MEMORY (General Knowledge)")
    print("-" * 60)

    # Store semantic knowledge
    memory.store("semantic", {
        "title": "What is Deep Learning",
        "content": "Deep Learning uses neural networks with multiple layers",
        "tags": ["AI", "machine learning", "neural networks"],
        "timestamp": datetime.now().isoformat()
    }, key="knowledge_dl")

    memory.store("semantic", {
        "title": "Types of Neural Networks",
        "content": "CNN, RNN, Transformer are common types",
        "tags": ["neural networks", "architecture", "AI"],
        "timestamp": datetime.now().isoformat()
    }, key="knowledge_types")

    # Search by tags
    nn_knowledge = memory.query("semantic", search_query="neural")
    print(f"Results for 'neural': {len(nn_knowledge)}")
    for know in nn_knowledge:
        print(f"  - {know['title']}")
    print()

    # ============ CROSS-MEMORY SEARCH ============
    print("5. CROSS-MEMORY SEARCH")
    print("-" * 60)

    # Search across all memory types
    results = memory.search("machine learning", limit=3)
    for mem_type, items in results.items():
        if items:
            print(f"  {mem_type}: {len(items)} results")
            for item in items:
                content = item.get('content', item.get('title', 'N/A'))[:40]
                print(f"    - {content}...")
    print()

    # ============ STATISTICS ============
    print("6. MEMORY STATISTICS")
    print("-" * 60)

    # Get counts
    counts = memory.count()
    print("Items per memory type:")
    for mem_type, count in counts.items():
        print(f"  - {mem_type}: {count} items")
    print()

    # Total items
    total = sum(counts.values())
    print(f"Total items stored: {total}")
    print()

    # ============ DATA EXPORT ============
    print("7. EXPORT DATA")
    print("-" * 60)

    # Export conversation
    json_data = memory.export_json("short_term")
    print(f"Exported {len(json_data)} bytes of conversation data")
    print()

    # ============ CLEANUP ============
    print("8. CLEANUP")
    print("-" * 60)

    # Delete specific item
    deleted = memory.delete("short_term", "msg_1")
    print(f"Deleted message: {deleted}")

    # Clear memory type
    remaining = memory.count("short_term")
    print(f"Remaining short-term items: {remaining}")
    print()

    # Close connection
    memory.close()
    print("Memory connection closed!")
    print()
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

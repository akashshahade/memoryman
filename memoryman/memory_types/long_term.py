"""
Memory type implementations
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from memoryman.core.memory_base import Memory
from memoryman.core.retrieval import SimpleRetriever


class ShortTermMemory(Memory):
    """Short-term/working memory for recent conversation context"""

    def store(self, key: str, data: Dict[str, Any]) -> None:
        """Store data in short-term memory"""
        # Add metadata
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        if "memory_type" not in data:
            data["memory_type"] = "short_term"

        self.storage.store(self.memory_id, key, data)

    def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data from short-term memory"""
        return self.storage.retrieve(self.memory_id, key)

    def query(self, query: str = "", **kwargs) -> List[Dict[str, Any]]:
        """
        Query short-term memory

        Args:
            query: Optional text search query
            **kwargs: Additional filters (role, etc.)

        Returns:
            List of matching items
        """
        # Get all data for this memory
        all_keys = self.storage.list_keys(self.memory_id)
        all_data = [self.retrieve(key) for key in all_keys if self.retrieve(key)]

        # Apply filters
        result = SimpleRetriever.filter_by_multiple(all_data, kwargs) if kwargs else all_data

        # Text search if query provided
        if query:
            result = SimpleRetriever.search_text(result, query)

        # Sort by timestamp (most recent first)
        result = SimpleRetriever.sort_by_field(result, "timestamp", reverse=True)

        return result

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent messages"""
        all_keys = self.storage.list_keys(self.memory_id)
        all_data = [self.retrieve(key) for key in all_keys if self.retrieve(key)]
        return SimpleRetriever.get_recent(all_data, limit=limit)

    def delete(self, key: str) -> bool:
        """Delete data from short-term memory"""
        return self.storage.delete(self.memory_id, key)

    def clear(self) -> None:
        """Clear all short-term memory"""
        self.storage.delete_memory(self.memory_id)


class LongTermMemory(Memory):
    """Long-term memory for persistent storage and facts"""

    def store(self, key: str, data: Dict[str, Any]) -> None:
        """Store data in long-term memory"""
        # Add metadata
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        if "memory_type" not in data:
            data["memory_type"] = "long_term"
        if "category" not in data:
            data["category"] = "general"

        self.storage.store(self.memory_id, key, data)

    def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data from long-term memory"""
        return self.storage.retrieve(self.memory_id, key)

    def query(self, query: str = "", **kwargs) -> List[Dict[str, Any]]:
        """
        Query long-term memory

        Args:
            query: Optional text search query
            **kwargs: Additional filters (category, etc.)

        Returns:
            List of matching items
        """
        # Get all data
        all_keys = self.storage.list_keys(self.memory_id)
        all_data = [self.retrieve(key) for key in all_keys if self.retrieve(key)]

        # Apply filters
        result = SimpleRetriever.filter_by_multiple(all_data, kwargs) if kwargs else all_data

        # Text search if query provided
        if query:
            result = SimpleRetriever.search_text(result, query)

        return result

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all data in a category"""
        return self.query(category=category)

    def delete(self, key: str) -> bool:
        """Delete data from long-term memory"""
        return self.storage.delete(self.memory_id, key)

    def clear(self) -> None:
        """Clear all long-term memory"""
        self.storage.delete_memory(self.memory_id)


class EpisodicMemory(Memory):
    """Episodic memory for specific events and conversations"""

    def store(self, key: str, data: Dict[str, Any]) -> None:
        """Store event/episode in episodic memory"""
        # Add metadata
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        if "memory_type" not in data:
            data["memory_type"] = "episodic"
        if "episode_id" not in data:
            data["episode_id"] = key

        self.storage.store(self.memory_id, key, data)

    def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve episode from episodic memory"""
        return self.storage.retrieve(self.memory_id, key)

    def query(self, query: str = "", **kwargs) -> List[Dict[str, Any]]:
        """
        Query episodic memory

        Args:
            query: Optional text search query
            **kwargs: Additional filters

        Returns:
            List of matching episodes
        """
        # Get all data
        all_keys = self.storage.list_keys(self.memory_id)
        all_data = [self.retrieve(key) for key in all_keys if self.retrieve(key)]

        # Apply filters
        result = SimpleRetriever.filter_by_multiple(all_data, kwargs) if kwargs else all_data

        # Text search if query provided
        if query:
            result = SimpleRetriever.search_text(result, query)

        # Sort by timestamp (most recent first)
        result = SimpleRetriever.sort_by_field(result, "timestamp", reverse=True)

        return result

    def get_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get episodes within a date range"""
        all_keys = self.storage.list_keys(self.memory_id)
        all_data = [self.retrieve(key) for key in all_keys if self.retrieve(key)]

        result = [
            item for item in all_data
            if start_date <= item.get("timestamp", "") <= end_date
        ]
        return SimpleRetriever.sort_by_field(result, "timestamp", reverse=True)

    def delete(self, key: str) -> bool:
        """Delete episode from episodic memory"""
        return self.storage.delete(self.memory_id, key)

    def clear(self) -> None:
        """Clear all episodic memory"""
        self.storage.delete_memory(self.memory_id)


class SemanticMemory(Memory):
    """Semantic memory for general knowledge and facts"""

    def store(self, key: str, data: Dict[str, Any]) -> None:
        """Store fact/knowledge in semantic memory"""
        # Add metadata
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        if "memory_type" not in data:
            data["memory_type"] = "semantic"
        if "tags" not in data:
            data["tags"] = []

        self.storage.store(self.memory_id, key, data)

    def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve fact from semantic memory"""
        return self.storage.retrieve(self.memory_id, key)

    def query(self, query: str = "", **kwargs) -> List[Dict[str, Any]]:
        """
        Query semantic memory

        Args:
            query: Optional text search query
            **kwargs: Additional filters

        Returns:
            List of matching facts
        """
        # Get all data
        all_keys = self.storage.list_keys(self.memory_id)
        all_data = [self.retrieve(key) for key in all_keys if self.retrieve(key)]

        # Apply filters
        result = SimpleRetriever.filter_by_multiple(all_data, kwargs) if kwargs else all_data

        # Text search if query provided
        if query:
            result = SimpleRetriever.search_text(result, query, fields=["title", "content", "tags"])

        return result

    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Search facts by tags"""
        all_keys = self.storage.list_keys(self.memory_id)
        all_data = [self.retrieve(key) for key in all_keys if self.retrieve(key)]

        result = [
            item for item in all_data
            if any(tag in item.get("tags", []) for tag in tags)
        ]
        return result

    def delete(self, key: str) -> bool:
        """Delete fact from semantic memory"""
        return self.storage.delete(self.memory_id, key)

    def clear(self) -> None:
        """Clear all semantic memory"""
        self.storage.delete_memory(self.memory_id)

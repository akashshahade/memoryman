"""
Main Memory Manager - unified interface for all memory types
"""

from typing import Dict, List, Optional, Any, Union
from memoryman.storage.sqlite_backend import SQLiteStorage
from memoryman.memory_types.long_term import (
    ShortTermMemory,
    LongTermMemory,
    EpisodicMemory,
    SemanticMemory,
)


class MemoryManager:
    """
    Unified interface for managing all types of AI memory

    Example:
        >>> memory = MemoryManager(storage_type="sqlite", db_path="./memory.db")
        >>> memory.store("conversation", "Hello AI!")
        >>> memory.get_recent("conversation", limit=5)
    """

    def __init__(
        self,
        storage_type: str = "sqlite",
        db_path: str = "./ai_memory.db",
    ):
        """
        Initialize MemoryManager

        Args:
            storage_type: Type of storage backend ("sqlite")
            db_path: Path to database file
        """
        self.storage_type = storage_type
        self.db_path = db_path

        # Initialize storage backend
        if storage_type == "sqlite":
            self.storage = SQLiteStorage(db_path)
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

        # Initialize memory types
        self.short_term = ShortTermMemory("short_term", self.storage)
        self.long_term = LongTermMemory("long_term", self.storage)
        self.episodic = EpisodicMemory("episodic", self.storage)
        self.semantic = SemanticMemory("semantic", self.storage)

        # Memory type mapping
        self.memory_types = {
            "short_term": self.short_term,
            "long_term": self.long_term,
            "episodic": self.episodic,
            "semantic": self.semantic,
        }

    def store(
        self,
        memory_type: str,
        data: Union[str, Dict[str, Any]],
        key: Optional[str] = None,
    ) -> str:
        """
        Store data in specified memory type

        Args:
            memory_type: Type of memory ("short_term", "long_term", "episodic", "semantic")
            data: Data to store (string or dict)
            key: Optional key (auto-generated if not provided)

        Returns:
            The key used to store data

        Example:
            >>> memory.store("conversation", {"role": "user", "content": "Hi!"})
            >>> memory.store("facts", "The sky is blue", key="fact_1")
        """
        if memory_type not in self.memory_types:
            raise ValueError(f"Unknown memory type: {memory_type}")

        # Convert string to dict if needed
        if isinstance(data, str):
            data = {"content": data}

        # Generate key if not provided
        if key is None:
            key = f"{memory_type}_{self.memory_types[memory_type].count()}"

        # Store
        self.memory_types[memory_type].store(key, data)
        return key

    def retrieve(self, memory_type: str, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from memory

        Args:
            memory_type: Type of memory
            key: Key to retrieve

        Returns:
            Data if found, None otherwise

        Example:
            >>> data = memory.retrieve("conversation", "msg_1")
        """
        if memory_type not in self.memory_types:
            raise ValueError(f"Unknown memory type: {memory_type}")

        return self.memory_types[memory_type].retrieve(key)

    def query(
        self,
        memory_type: str,
        search_query: Optional[str] = None,
        **filters,
    ) -> List[Dict[str, Any]]:
        """
        Query memory with optional search and filters

        Args:
            memory_type: Type of memory to query
            search_query: Optional text to search for
            **filters: Additional filters (e.g., role="user")

        Returns:
            List of matching items

        Example:
            >>> results = memory.query("conversation", role="user")
            >>> results = memory.query("facts", search_query="weather")
        """
        if memory_type not in self.memory_types:
            raise ValueError(f"Unknown memory type: {memory_type}")

        return self.memory_types[memory_type].query(search_query or "", **filters)

    def get_recent(self, memory_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent items from memory

        Args:
            memory_type: Type of memory
            limit: Maximum number of items to return

        Returns:
            List of recent items (most recent first)

        Example:
            >>> recent = memory.get_recent("conversation", limit=5)
        """
        if memory_type not in self.memory_types:
            raise ValueError(f"Unknown memory type: {memory_type}")

        if hasattr(self.memory_types[memory_type], "get_recent"):
            return self.memory_types[memory_type].get_recent(limit)
        else:
            # Fallback for memory types without get_recent
            all_keys = self.memory_types[memory_type].list_keys()
            all_data = [
                self.memory_types[memory_type].retrieve(k) for k in all_keys
                if self.memory_types[memory_type].retrieve(k)
            ]
            # Sort by timestamp and limit
            from memoryman.core.retrieval import SimpleRetriever
            sorted_data = SimpleRetriever.sort_by_field(all_data, "timestamp", reverse=True)
            return sorted_data[:limit]

    def search(
        self,
        query: str,
        memory_types: Optional[List[str]] = None,
        limit: int = 10,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search across memory types

        Args:
            query: Search query
            memory_types: Which memory types to search (default: all)
            limit: Max results per memory type

        Returns:
            Dictionary with results per memory type

        Example:
            >>> results = memory.search("AI concepts", limit=5)
            >>> results = memory.search("weather", memory_types=["long_term", "semantic"])
        """
        if memory_types is None:
            memory_types = list(self.memory_types.keys())

        results = {}
        for mem_type in memory_types:
            if mem_type in self.memory_types:
                search_results = self.query(mem_type, search_query=query)
                results[mem_type] = search_results[:limit]

        return results

    def delete(self, memory_type: str, key: str) -> bool:
        """
        Delete data from memory

        Args:
            memory_type: Type of memory
            key: Key to delete

        Returns:
            True if deleted, False if not found

        Example:
            >>> memory.delete("conversation", "msg_1")
        """
        if memory_type not in self.memory_types:
            raise ValueError(f"Unknown memory type: {memory_type}")

        return self.memory_types[memory_type].delete(key)

    def clear(self, memory_type: str) -> None:
        """
        Clear all data from a memory type

        Args:
            memory_type: Type of memory to clear

        Example:
            >>> memory.clear("short_term")
        """
        if memory_type not in self.memory_types:
            raise ValueError(f"Unknown memory type: {memory_type}")

        self.memory_types[memory_type].clear()

    def clear_all(self) -> None:
        """Clear all memories"""
        for mem_type in self.memory_types:
            self.clear(mem_type)

    def count(self, memory_type: Optional[str] = None) -> Union[int, Dict[str, int]]:
        """
        Count items in memory

        Args:
            memory_type: Specific type to count (None = all)

        Returns:
            Count or dict of counts per type

        Example:
            >>> total = memory.count("conversation")
            >>> all_counts = memory.count()
        """
        if memory_type:
            if memory_type not in self.memory_types:
                raise ValueError(f"Unknown memory type: {memory_type}")
            return self.memory_types[memory_type].count()
        else:
            return {
                mem_type: self.memory_types[mem_type].count()
                for mem_type in self.memory_types
            }

    def list_all(self, memory_type: Optional[str] = None) -> Union[List[str], Dict[str, List[str]]]:
        """
        List all keys in memory

        Args:
            memory_type: Specific type to list (None = all)

        Returns:
            List of keys or dict of keys per type

        Example:
            >>> keys = memory.list_all("conversation")
            >>> all_keys = memory.list_all()
        """
        if memory_type:
            if memory_type not in self.memory_types:
                raise ValueError(f"Unknown memory type: {memory_type}")
            return self.memory_types[memory_type].list_keys()
        else:
            return {
                mem_type: self.memory_types[mem_type].list_keys()
                for mem_type in self.memory_types
            }

    def export_json(self, memory_type: Optional[str] = None) -> str:
        """
        Export memory as JSON

        Args:
            memory_type: Specific type to export (None = all)

        Returns:
            JSON string

        Example:
            >>> json_str = memory.export_json("conversation")
        """
        import json

        if memory_type:
            if memory_type not in self.memory_types:
                raise ValueError(f"Unknown memory type: {memory_type}")
            keys = self.memory_types[memory_type].list_keys()
            data = [
                self.memory_types[memory_type].retrieve(k)
                for k in keys
                if self.memory_types[memory_type].retrieve(k)
            ]
            return json.dumps({memory_type: data}, indent=2, default=str)
        else:
            all_data = {}
            for mem_type in self.memory_types:
                keys = self.memory_types[mem_type].list_keys()
                all_data[mem_type] = [
                    self.memory_types[mem_type].retrieve(k)
                    for k in keys
                    if self.memory_types[mem_type].retrieve(k)
                ]
            return json.dumps(all_data, indent=2, default=str)

    def close(self) -> None:
        """Close storage connection"""
        self.storage.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

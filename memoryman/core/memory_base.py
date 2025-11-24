"""
Base classes for memory implementations
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class Memory(ABC):
    """Abstract base class for all memory types"""

    def __init__(self, memory_id: str, storage_engine):
        """
        Initialize memory

        Args:
            memory_id: Unique identifier for this memory
            storage_engine: Storage backend to use
        """
        self.memory_id = memory_id
        self.storage = storage_engine
        self.created_at = datetime.now()

    @abstractmethod
    def store(self, key: str, data: Dict[str, Any]) -> None:
        """Store data in memory"""
        pass

    @abstractmethod
    def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data from memory"""
        pass

    @abstractmethod
    def query(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """Query memory with custom logic"""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete data from memory"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all data from memory"""
        pass

    def list_keys(self) -> List[str]:
        """List all keys in this memory"""
        return self.storage.list_keys(self.memory_id)

    def count(self) -> int:
        """Count total items in memory"""
        return len(self.list_keys())


class StorageEngine(ABC):
    """Abstract base class for storage backends"""

    @abstractmethod
    def store(self, memory_id: str, key: str, data: Dict[str, Any]) -> None:
        """Store data with memory_id:key"""
        pass

    @abstractmethod
    def retrieve(self, memory_id: str, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data by memory_id:key"""
        pass

    @abstractmethod
    def query(self, memory_id: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query data in a memory"""
        pass

    @abstractmethod
    def delete(self, memory_id: str, key: str) -> bool:
        """Delete data by memory_id:key"""
        pass

    @abstractmethod
    def delete_memory(self, memory_id: str) -> None:
        """Delete entire memory"""
        pass

    @abstractmethod
    def list_keys(self, memory_id: str) -> List[str]:
        """List all keys in a memory"""
        pass

    @abstractmethod
    def list_memories(self) -> List[str]:
        """List all memory IDs"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close storage connection"""
        pass

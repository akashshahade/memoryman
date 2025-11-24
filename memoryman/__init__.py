"""
Memory Man - A lightweight memory layer for AI models and chatbots
"""

from memoryman.core.memory_manager import MemoryManager
from memoryman.memory_types.long_term import (
    ShortTermMemory,
    LongTermMemory,
    SemanticMemory,
    EpisodicMemory,
)

__version__ = "0.1.0"
__author__ = "Memory Team"

__all__ = [
    "MemoryManager",
    "ShortTermMemory",
    "LongTermMemory",
    "SemanticMemory",
    "EpisodicMemory",
]

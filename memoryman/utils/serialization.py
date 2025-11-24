"""
Utility functions for data serialization and deserialization
"""

import json
from typing import Any, Dict


def serialize_data(data: Dict[str, Any]) -> str:
    """
    Serialize data to JSON string

    Args:
        data: Dictionary to serialize

    Returns:
        JSON string
    """
    return json.dumps(data, default=str)


def deserialize_data(data_str: str) -> Dict[str, Any]:
    """
    Deserialize JSON string to dictionary

    Args:
        data_str: JSON string to deserialize

    Returns:
        Dictionary
    """
    return json.loads(data_str)

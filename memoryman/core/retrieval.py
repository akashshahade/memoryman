"""
Retrieval and search utilities
"""

from typing import Any, Dict, List, Optional
import json


class SimpleRetriever:
    """Simple retrieval engine with basic filtering and searching"""

    @staticmethod
    def filter_by_field(items: List[Dict[str, Any]], field: str, value: Any) -> List[Dict[str, Any]]:
        """Filter items by a field value"""
        return [item for item in items if item.get(field) == value]

    @staticmethod
    def filter_by_multiple(items: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter items by multiple field values"""
        result = items
        for field, value in filters.items():
            result = SimpleRetriever.filter_by_field(result, field, value)
        return result

    @staticmethod
    def search_text(items: List[Dict[str, Any]], search_term: str, fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search items by text content in specified fields
        
        Args:
            items: List of items to search
            search_term: Text to search for (case-insensitive)
            fields: Fields to search in (default: all string fields)
        
        Returns:
            List of matching items
        """
        search_term_lower = search_term.lower()
        results = []

        for item in items:
            if fields:
                # Search only in specified fields
                for field in fields:
                    if field in item:
                        value = str(item[field]).lower()
                        if search_term_lower in value:
                            results.append(item)
                            break
            else:
                # Search all string fields
                for key, value in item.items():
                    if isinstance(value, str) and search_term_lower in value.lower():
                        results.append(item)
                        break

        return results

    @staticmethod
    def sort_by_field(items: List[Dict[str, Any]], field: str, reverse: bool = False) -> List[Dict[str, Any]]:
        """Sort items by field"""
        try:
            return sorted(items, key=lambda x: x.get(field, ""), reverse=reverse)
        except TypeError:
            # Handle mixed types
            return items

    @staticmethod
    def limit_results(items: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Limit results to N items"""
        return items[:limit]

    @staticmethod
    def get_recent(items: List[Dict[str, Any]], timestamp_field: str = "timestamp", limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent items by timestamp"""
        sorted_items = SimpleRetriever.sort_by_field(items, timestamp_field, reverse=True)
        return SimpleRetriever.limit_results(sorted_items, limit)

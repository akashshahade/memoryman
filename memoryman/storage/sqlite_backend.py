"""
SQLite storage backend
"""

import sqlite3
import json
from typing import Any, Dict, List, Optional
from memoryman.core.memory_base import StorageEngine
from memoryman.utils.serialization import serialize_data, deserialize_data


class SQLiteStorage(StorageEngine):
    """SQLite-based storage backend"""

    def __init__(self, db_path: str):
        """
        Initialize SQLite storage

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        """Initialize database tables"""
        cursor = self.conn.cursor()

        # Create memories table to track memory instances
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                memory_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT NOT NULL,
                key TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(memory_id, key),
                FOREIGN KEY(memory_id) REFERENCES memories(memory_id)
            )
        """)

        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memory_id 
            ON memory_data(memory_id)
        """)

        self.conn.commit()

    def store(self, memory_id: str, key: str, data: Dict[str, Any]) -> None:
        """Store data"""
        cursor = self.conn.cursor()

        # Ensure memory exists
        cursor.execute("INSERT OR IGNORE INTO memories (memory_id) VALUES (?)", (memory_id,))

        # Serialize data
        serialized = serialize_data(data)

        # Insert or update data
        cursor.execute("""
            INSERT INTO memory_data (memory_id, key, data)
            VALUES (?, ?, ?)
            ON CONFLICT(memory_id, key) DO UPDATE SET 
                data=excluded.data,
                updated_at=CURRENT_TIMESTAMP
        """, (memory_id, key, serialized))

        self.conn.commit()

    def retrieve(self, memory_id: str, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT data FROM memory_data WHERE memory_id = ? AND key = ?",
            (memory_id, key)
        )
        row = cursor.fetchone()

        if row:
            return deserialize_data(row["data"])
        return None

    def query(self, memory_id: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query data by filters"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT data FROM memory_data WHERE memory_id = ?",
            (memory_id,)
        )
        rows = cursor.fetchall()

        # Deserialize all data
        all_data = [deserialize_data(row["data"]) for row in rows]

        # Apply filters
        result = all_data
        for field, value in filters.items():
            result = [item for item in result if item.get(field) == value]

        return result

    def delete(self, memory_id: str, key: str) -> bool:
        """Delete data"""
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM memory_data WHERE memory_id = ? AND key = ?",
            (memory_id, key)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_memory(self, memory_id: str) -> None:
        """Delete entire memory"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM memory_data WHERE memory_id = ?", (memory_id,))
        cursor.execute("DELETE FROM memories WHERE memory_id = ?", (memory_id,))
        self.conn.commit()

    def list_keys(self, memory_id: str) -> List[str]:
        """List all keys in a memory"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT key FROM memory_data WHERE memory_id = ? ORDER BY created_at",
            (memory_id,)
        )
        return [row["key"] for row in cursor.fetchall()]

    def list_memories(self) -> List[str]:
        """List all memory IDs"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT memory_id FROM memories")
        return [row["memory_id"] for row in cursor.fetchall()]

    def close(self) -> None:
        """Close database connection"""
        self.conn.close()

    def __del__(self):
        """Cleanup on deletion"""
        try:
            self.close()
        except:
            pass

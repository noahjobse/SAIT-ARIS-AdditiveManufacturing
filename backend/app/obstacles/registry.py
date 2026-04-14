"""
In-memory obstacle registry.

MVP: global dict keyed by obstacle_id.
Future: swap to Supabase per-user storage.
"""
import logging
import os
import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime

logger = logging.getLogger(__name__)


@dataclass
class ObstacleRecord:
    obstacle_id: str
    filename: str
    file_path: str
    position: list[float]
    rotation: list[float]
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class ObstacleRegistry:
    """In-memory obstacle store. Thread-safe: uses RLock for concurrent register/get/list/delete operations."""

    def __init__(self):
        self._obstacles: dict[str, ObstacleRecord] = {}
        self._lock = threading.RLock()

    def register(self, record: ObstacleRecord):
        with self._lock:
            self._obstacles[record.obstacle_id] = record
        logger.info("Registered obstacle '%s' (%s)", record.obstacle_id, record.filename)

    def get(self, obstacle_id: str) -> ObstacleRecord | None:
        with self._lock:
            return self._obstacles.get(obstacle_id)

    def list_all(self) -> list[ObstacleRecord]:
        with self._lock:
            return list(self._obstacles.values())

    def delete(self, obstacle_id: str) -> bool:
        with self._lock:
            record = self._obstacles.pop(obstacle_id, None)
        if record is None:
            return False
        # Clean up the temp file (outside lock — I/O should not hold locks)
        if os.path.exists(record.file_path):
            os.remove(record.file_path)
            logger.info("Deleted obstacle file '%s'", record.file_path)
        return True


# Global singleton — will be replaced by Supabase-backed store later
obstacle_registry = ObstacleRegistry()

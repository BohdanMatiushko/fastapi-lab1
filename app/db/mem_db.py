from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Dict, Any


@dataclass
class InMemoryDB:
    users: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    next_id: int = 1
    lock: Lock = field(default_factory=Lock)


db = InMemoryDB()
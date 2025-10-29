from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class Relationship:
    name: str
    value: float = 0.0

    def clamp(self) -> None:
        self.value = max(0.0, min(100.0, self.value))


@dataclass(slots=True)
class GameTime:
    week: int = 1
    day: str = "Mon"
    slot: str = "morning"


@dataclass(slots=True)
class ScheduleEvent:
    passage_id: str
    week: int
    day: str
    slot: str


@dataclass(slots=True)
class GameState:
    stats: Dict[str, float] = field(default_factory=dict)
    flags: Dict[str, object] = field(default_factory=dict)
    relationships: Dict[str, Relationship] = field(default_factory=dict)
    time: GameTime = field(default_factory=GameTime)
    schedule: List[ScheduleEvent] = field(default_factory=list)
    unlocked_tags: set[str] = field(default_factory=set)
    current_passage: Optional[str] = None
    return_stack: List[str] = field(default_factory=list)
    rng_seed: Optional[int] = None

    def ensure_relationship(self, name: str) -> Relationship:
        if name not in self.relationships:
            self.relationships[name] = Relationship(name=name)
        return self.relationships[name]

    def add_schedule(self, event: ScheduleEvent) -> None:
        self.schedule.append(event)
        self.schedule.sort(key=lambda e: (e.week, e.day, e.slot))


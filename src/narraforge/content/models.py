from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Optional, Sequence


@dataclass(slots=True)
class PackManifest:
    """Represents the manifest metadata that every content pack must provide."""

    id: str
    name: str
    version: str
    author: str
    licence: str
    engine_compat: str
    dependencies: Sequence[dict] = field(default_factory=list)
    soft_dependencies: Sequence[dict] = field(default_factory=list)
    provides: Sequence[str] = field(default_factory=list)
    conflicts: Sequence[dict] = field(default_factory=list)
    assets: Sequence[str] = field(default_factory=list)
    strings: Sequence[str] = field(default_factory=list)


@dataclass(slots=True)
class ChoiceEffect:
    """Atomic effect applied after selecting a choice or entering a passage."""

    type: str
    params: Dict[str, object]


@dataclass(slots=True)
class Choice:
    text: str
    to: str
    condition: Optional[str] = None
    effects: Sequence[ChoiceEffect] = field(default_factory=list)
    weight: Optional[float] = None


@dataclass(slots=True)
class Passage:
    id: str
    title: str
    tags: Sequence[str]
    body: str
    media: Dict[str, Optional[str]] = field(default_factory=dict)
    choices: Sequence[Choice] = field(default_factory=list)
    on_enter: Sequence[ChoiceEffect] = field(default_factory=list)
    time_cost: Optional[str] = None


@dataclass(slots=True)
class Pack:
    manifest: PackManifest
    passages: Dict[str, Passage]
    assets_root: Optional[Path] = None
    strings_root: Optional[Path] = None

    def passage_ids(self) -> Iterable[str]:
        return self.passages.keys()


@dataclass(slots=True)
class SaveSlot:
    name: str
    created_at: datetime
    description: str
    thumbnail_path: Optional[Path]


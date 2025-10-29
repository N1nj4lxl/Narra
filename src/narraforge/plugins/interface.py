from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from ..runtime.state import GameState


class ConditionRegistry(Protocol):
    def register(self, name: str, func: Callable[..., object]) -> None: ...


class EffectRegistry(Protocol):
    def register(self, name: str, handler: Callable[[GameState, dict], None]) -> None: ...


@dataclass(slots=True)
class PluginContext:
    root: str
    mode: str


class Plugin(Protocol):
    def on_engine_start(self, context: PluginContext) -> None: ...

    def on_game_start(self, state: GameState) -> None: ...

    def on_passage_enter(self, passage_id: str, state: GameState) -> None: ...

    def on_choice_selected(self, passage_id: str, choice_index: int, state: GameState) -> None: ...

    def register_conditions(self, registry: ConditionRegistry) -> None: ...

    def register_effects(self, registry: EffectRegistry) -> None: ...


class SafePlugin:
    """Default no-op implementation used when plugins are disabled."""

    def on_engine_start(self, context: PluginContext) -> None:  # pragma: no cover - trivial
        return

    def on_game_start(self, state: GameState) -> None:  # pragma: no cover - trivial
        return

    def on_passage_enter(self, passage_id: str, state: GameState) -> None:  # pragma: no cover - trivial
        return

    def on_choice_selected(self, passage_id: str, choice_index: int, state: GameState) -> None:  # pragma: no cover - trivial
        return

    def register_conditions(self, registry: ConditionRegistry) -> None:  # pragma: no cover - trivial
        return

    def register_effects(self, registry: EffectRegistry) -> None:  # pragma: no cover - trivial
        return


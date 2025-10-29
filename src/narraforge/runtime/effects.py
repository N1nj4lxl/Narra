from __future__ import annotations

from typing import Iterable

from ..content.models import ChoiceEffect
from .state import GameState, ScheduleEvent


class EffectError(Exception):
    """Raised when applying an effect fails."""


def apply_effect(effect: ChoiceEffect, state: GameState) -> None:
    effect_type = effect.type
    params = effect.params

    if effect_type == "add_stat":
        name = params["name"]
        amount = float(params.get("amount", 0))
        state.stats[name] = float(state.stats.get(name, 0)) + amount
    elif effect_type == "set_stat":
        name = params["name"]
        state.stats[name] = float(params.get("value", 0))
    elif effect_type == "set_flag":
        name = params["name"]
        state.flags[name] = params.get("value")
    elif effect_type == "add_rel":
        rel = state.ensure_relationship(params["name"])
        rel.value += float(params.get("amount", 0))
        rel.clamp()
    elif effect_type == "schedule":
        event = ScheduleEvent(
            passage_id=params["passage_id"],
            week=int(params.get("week", state.time.week)),
            day=str(params.get("day", state.time.day)),
            slot=str(params.get("slot", state.time.slot)),
        )
        state.add_schedule(event)
    elif effect_type == "unlock_tag":
        state.unlocked_tags.add(params["name"])
    elif effect_type == "lock_tag":
        state.unlocked_tags.discard(params["name"])
    elif effect_type == "goto":
        state.current_passage = params["passage_id"]
    else:
        raise EffectError(f"Unknown effect type: {effect_type}")


def apply_effects(effects: Iterable[ChoiceEffect], state: GameState) -> None:
    for effect in effects:
        apply_effect(effect, state)


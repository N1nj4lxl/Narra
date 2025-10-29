from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from ..content.models import Pack
from ..loader.packs import PackLoadError, load_pack
from ..runtime.conditions import ConditionError, ConditionContext, build_rng, evaluate_condition
from ..runtime.state import GameState


@dataclass(slots=True)
class ValidationMessage:
    level: str
    location: str
    message: str


@dataclass(slots=True)
class ValidationReport:
    messages: List[ValidationMessage]

    @property
    def errors(self) -> List[ValidationMessage]:
        return [msg for msg in self.messages if msg.level == "error"]

    @property
    def warnings(self) -> List[ValidationMessage]:
        return [msg for msg in self.messages if msg.level == "warning"]

    def ok(self) -> bool:
        return not self.errors


class Validator:
    """Runs static checks against a set of packs."""

    def __init__(self) -> None:
        self._messages: List[ValidationMessage] = []

    def validate_paths(self, paths: Iterable[str]) -> ValidationReport:
        self._messages = []
        packs: List[Pack] = []
        for path in paths:
            pack_path = str(path)
            try:
                pack = load_pack(Path(pack_path))
            except PackLoadError as exc:
                self._messages.append(ValidationMessage("error", pack_path, str(exc)))
                continue
            packs.append(pack)
        if not packs:
            return ValidationReport(messages=self._messages)
        self._check_duplicate_passages(packs)
        self._check_conditions(packs)
        return ValidationReport(messages=self._messages)

    def _check_duplicate_passages(self, packs: Iterable[Pack]) -> None:
        seen: dict[str, str] = {}
        for pack in packs:
            for pid in pack.passages:
                if pid in seen:
                    self._messages.append(
                        ValidationMessage(
                            "warning",
                            f"{pack.manifest.id}:{pid}",
                            f"Passage overrides previously defined in {seen[pid]}",
                        )
                    )
                else:
                    seen[pid] = pack.manifest.id

    def _check_conditions(self, packs: Iterable[Pack]) -> None:
        state = GameState()
        context = ConditionContext(state=state, rng=build_rng(0))
        for pack in packs:
            for passage in pack.passages.values():
                for choice in passage.choices:
                    if not choice.condition:
                        continue
                    try:
                        evaluate_condition(choice.condition, context)
                    except ConditionError as exc:
                        self._messages.append(
                            ValidationMessage(
                                "error",
                                f"{pack.manifest.id}:{passage.id}",
                                f"Invalid condition '{choice.condition}': {exc}",
                            )
                        )


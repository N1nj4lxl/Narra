from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

from ..content.models import Choice, Pack, Passage
from .conditions import ConditionContext, ConditionError, build_rng, evaluate_condition
from .effects import apply_effects
from .state import GameState


@dataclass(slots=True)
class PassageResult:
    passage: Passage
    available_choices: List[Choice]


class RuntimeEngine:
    """Loads packs, manages state, and evaluates passages."""

    def __init__(self, packs: Sequence[Pack], seed: int = 42) -> None:
        self.packs = list(packs)
        self.seed = seed
        self.state = GameState(rng_seed=seed)
        self._passage_index: Dict[str, Passage] = {}
        self._build_index()
        self._rng_gate = build_rng(seed)

    def _build_index(self) -> None:
        for pack in self.packs:
            for pid, passage in pack.passages.items():
                self._passage_index[pid] = passage

    def start(self, passage_id: str) -> PassageResult:
        self.state.current_passage = passage_id
        return self.enter_passage(passage_id)

    def enter_passage(self, passage_id: str) -> PassageResult:
        passage = self._passage_index.get(passage_id)
        if passage is None:
            raise KeyError(f"Unknown passage id: {passage_id}")
        self.state.current_passage = passage_id
        if passage.on_enter:
            apply_effects(passage.on_enter, self.state)
        choices = self._filter_choices(passage)
        return PassageResult(passage=passage, available_choices=choices)

    def choose(self, choice: Choice) -> PassageResult:
        apply_effects(choice.effects, self.state)
        target = choice.to
        if target == "return":
            if not self.state.return_stack:
                raise KeyError("Return stack is empty; cannot return")
            target = self.state.return_stack.pop()
        elif self.state.current_passage:
            self.state.return_stack.append(self.state.current_passage)
        return self.enter_passage(target)

    def _filter_choices(self, passage: Passage) -> List[Choice]:
        available: List[Choice] = []
        for choice in passage.choices:
            if choice.condition:
                ctx = ConditionContext(state=self.state, rng=self._rng_gate)
                try:
                    if not evaluate_condition(choice.condition, ctx):
                        continue
                except ConditionError:
                    continue
            available.append(choice)
        return available

    def get_passage(self, passage_id: str) -> Passage:
        return self._passage_index[passage_id]

    def list_passages(self) -> Iterable[str]:
        return self._passage_index.keys()


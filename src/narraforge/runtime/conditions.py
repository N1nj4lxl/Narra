from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Callable

from .state import GameState

_ALLOWED_NODES = (
    ast.Expression,
    ast.BoolOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Call,
    ast.List,
    ast.Tuple,
    ast.Attribute,
    ast.In,
    ast.NotIn,
)

_ALLOWED_FUNCTIONS = {"stat", "flag", "rel", "chance"}
_ALLOWED_TIME_ATTRS = {"week", "day", "slot"}


class ConditionError(Exception):
    """Raised when a condition expression fails validation or evaluation."""


@dataclass(slots=True)
class ConditionContext:
    state: GameState
    rng: Callable[[float], bool]

    def stat(self, name: str) -> float:
        return float(self.state.stats.get(name, 0))

    def flag(self, name: str) -> Any:
        return self.state.flags.get(name)

    def rel(self, name: str) -> float:
        return self.state.ensure_relationship(name).value

    def chance(self, probability: float) -> bool:
        return self.rng(probability)


class _Validator(ast.NodeVisitor):
    def generic_visit(self, node: ast.AST) -> None:
        if not isinstance(node, _ALLOWED_NODES):
            raise ConditionError(f"Unsupported expression: {ast.dump(node, include_attributes=False)}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: D401 - short override
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
            raise ConditionError("Only stat, flag, rel, and chance calls are permitted")
        super().generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name) and node.value.id == "time":
            if node.attr not in _ALLOWED_TIME_ATTRS:
                raise ConditionError("Invalid time attribute access")
        else:
            raise ConditionError("Attribute access is only allowed on the time object")
        super().generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        raise ConditionError("Indexing is not permitted in conditions")


def evaluate_condition(expression: str, context: ConditionContext) -> bool:
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:  # pragma: no cover - syntax error branch
        raise ConditionError(f"Invalid expression: {expression}") from exc

    _Validator().visit(parsed)

    env: dict[str, Any] = {
        "stat": context.stat,
        "flag": context.flag,
        "rel": context.rel,
        "chance": context.chance,
        "time": context.state.time,
    }

    try:
        return bool(eval(compile(parsed, "<condition>", "eval"), {"__builtins__": {}}, env))
    except Exception as exc:  # noqa: BLE001
        raise ConditionError(f"Failed to evaluate expression: {expression}") from exc


def build_rng(seed: int) -> Callable[[float], bool]:
    import random

    rng = random.Random(seed)

    def gate(probability: float) -> bool:
        if probability <= 0:
            return False
        if probability >= 1:
            return True
        return rng.random() < probability

    return gate


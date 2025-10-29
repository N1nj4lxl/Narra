from __future__ import annotations

from pathlib import Path

from narraforge.loader.packs import load_pack
from narraforge.runtime.engine import RuntimeEngine


def load_sample_pack() -> Path:
    return Path(__file__).parent.parent / "examples" / "sample_pack"


def test_engine_advances_passages() -> None:
    pack_path = load_sample_pack()
    pack = load_pack(pack_path)
    engine = RuntimeEngine([pack], seed=1234)

    result = engine.start("demo.start")
    assert result.passage.id == "demo.start"
    assert len(result.available_choices) == 2
    assert engine.state.stats["Grades"] == 75

    breakfast = next(choice for choice in result.available_choices if choice.to == "demo.breakfast")
    next_result = engine.choose(breakfast)
    assert next_result.passage.id == "demo.breakfast"
    assert engine.state.stats["Energy"] == 5

    return_choice = next_result.available_choices[0]
    home_result = engine.choose(return_choice)
    assert home_result.passage.id == "demo.start"


def test_inspect_lists_passages() -> None:
    pack_path = load_sample_pack()
    pack = load_pack(pack_path)
    engine = RuntimeEngine([pack])
    passages = list(engine.list_passages())
    assert set(passages) == {"demo.start", "demo.breakfast", "demo.room"}


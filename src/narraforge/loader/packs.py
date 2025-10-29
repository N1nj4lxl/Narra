from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

from ..content.models import Choice, ChoiceEffect, Pack, PackManifest, Passage


class PackLoadError(Exception):
    pass


def _load_manifest(manifest_path: Path) -> PackManifest:
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PackLoadError(f"Invalid manifest: {manifest_path}") from exc

    required = {"id", "name", "version", "author", "licence", "engine_compat"}
    missing = required - data.keys()
    if missing:
        raise PackLoadError(f"Manifest missing required fields: {sorted(missing)}")

    return PackManifest(
        id=data["id"],
        name=data["name"],
        version=data["version"],
        author=data["author"],
        licence=data["licence"],
        engine_compat=data["engine_compat"],
        dependencies=data.get("dependencies", []),
        soft_dependencies=data.get("soft_dependencies", []),
        provides=data.get("provides", []),
        conflicts=data.get("conflicts", []),
        assets=data.get("assets", []),
        strings=data.get("strings", []),
    )


def _load_choice_effect(effect: dict) -> ChoiceEffect:
    if "type" not in effect:
        raise PackLoadError("Effect missing type")
    return ChoiceEffect(type=effect["type"], params=effect.get("params", {}))


def _load_choice(choice: dict) -> Choice:
    required = {"text", "to"}
    missing = required - choice.keys()
    if missing:
        raise PackLoadError(f"Choice missing fields: {missing}")
    effects = [_load_choice_effect(eff) for eff in choice.get("effects", [])]
    return Choice(
        text=choice["text"],
        to=choice["to"],
        condition=choice.get("condition"),
        effects=effects,
        weight=choice.get("weight"),
    )


def _load_passage(passage: dict) -> Passage:
    required = {"id", "title", "tags", "body"}
    missing = required - passage.keys()
    if missing:
        raise PackLoadError(f"Passage missing fields: {missing}")
    choices = [_load_choice(choice) for choice in passage.get("choices", [])]
    on_enter = [_load_choice_effect(effect) for effect in passage.get("on_enter", [])]
    return Passage(
        id=passage["id"],
        title=passage["title"],
        tags=passage.get("tags", []),
        body=passage["body"],
        media=passage.get("media", {}),
        choices=choices,
        on_enter=on_enter,
        time_cost=passage.get("time_cost"),
    )


def _load_content(content_root: Path) -> Dict[str, Passage]:
    passages: Dict[str, Passage] = {}
    for file in sorted(content_root.glob("*.json")):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise PackLoadError(f"Invalid content file: {file}") from exc
        for passage in data.get("passages", []):
            loaded = _load_passage(passage)
            passages[loaded.id] = loaded
    return passages


def load_pack(path: Path) -> Pack:
    if not path.exists():
        raise PackLoadError(f"Pack path does not exist: {path}")
    manifest_path = path / "manifest.json"
    if not manifest_path.exists():
        raise PackLoadError("manifest.json is missing")
    manifest = _load_manifest(manifest_path)
    content_root = path / "content"
    if not content_root.exists():
        raise PackLoadError("Content directory missing")
    passages = _load_content(content_root)
    return Pack(
        manifest=manifest,
        passages=passages,
        assets_root=path / "assets" if (path / "assets").exists() else None,
        strings_root=path / "strings" if (path / "strings").exists() else None,
    )


def load_packs(paths: Iterable[Path]) -> List[Pack]:
    return [load_pack(path) for path in paths]


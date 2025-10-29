# NarraForge Overview

## Name and Vision

NarraForge is a mod-friendly, data-driven narrative engine designed for image-on-top, text-below, choice-based experiences. The engine prioritises approachable authoring workflows by letting writers and modders add content via structured files rather than code. NarraForge ships with a control panel desktop application that validates content packs and launches the runtime, positioning the tooling as a management console rather than a scene editor.

## High-Level Architecture

The platform is organised into five cooperating pillars:

1. **Runtime Core** – Loads and evaluates content packs, advances passages, renders the standard VN-inspired UI, orchestrates state, persistence, and deterministic random number generation.
2. **Control Panel UI** – A standalone desktop app that manages projects, pack configuration, validation runs, build output, and launching the runtime with selected profiles and seeds.
3. **Content Packs** – File-based bundles containing manifests, story files, assets, localisation data, tests, and documentation. Pack load order is explicit and validation is strict to maintain compatibility.
4. **Plugin Layer** – Optional Python plug-ins with limited hooks for advanced behaviours. Plug-ins are disabled by default and can only interact with the engine through a curated surface of safe APIs.
5. **Validator** – A CLI tool integrated into the Control Panel that performs schema, link, asset, tag, and performance checks before content ships.

## Engine Feature Themes

- **Rendering Contract** – Standard layout with a top image region, prose body, and bottom-aligned choice buttons. A collapsible right sidebar exposes time, stats, relationships, schedule previews, save/load controls, options, and mods toggles. Skins theme the runtime and can be swapped without altering content.
- **Persistence and Accessibility** – Named save slots with thumbnails, autosaves, gzipped JSON save files, text scaling, dyslexic-friendly fonts, high-contrast themes, image opacity controls, keyboard navigation, screen reader support, and tag-driven content filters.
- **Localisation** – Per-pack string tables keyed by stable identifiers, right-to-left text support, and per-language font overrides.
- **Performance Budgets** – Enforced limits on asset dimensions and sizes, lazy media loading, caching, and validation to catch hot loops or heavy resources.

## Mod Support Philosophy

NarraForge embraces community-created content through:

- Strict pack structure with manifests that declare compatibility, dependencies, provided namespaces, and licensing.
- Deterministic load order with conflict warnings and soft dependency support.
- Tools for packaging packs into distributable archives and installing zips safely with path traversal protections.
- Migration tooling to keep packs viable across engine versions using semantic versioning.

## Testing and Quality Assurance

The development workflow leans on:

- Golden path scripts that run deterministic playthroughs.
- Seeded runs to reproduce RNG-dependent bugs.
- Snapshot rendering of passage bodies with substitutions.
- Save migration exercises that confirm backward compatibility.

## Security and Privacy

By default, the engine operates offline with no telemetry. Plug-ins run in safe or restricted sandboxes unless the user explicitly enables trusted mode. All imported zips are scanned for traversal attacks before installation.

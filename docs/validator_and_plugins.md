# Validation, Plugins, and Tooling

## Validator

The validator exists both as a CLI tool and as an embedded service within the Control Panel. Its responsibilities include:

- **Schema Checks** – Validate manifests, passages, choices, and auxiliary data files against the published schemas.
- **Link Integrity** – Ensure all choice targets and scheduled passages resolve; detect loops that could create hot transitions.
- **Asset Verification** – Confirm referenced media exists, meets dimension and file size budgets, and adheres to naming conventions.
- **Tag Catalogue Enforcement** – Highlight unknown or misspelled tags and reference the canonical catalogue for correction.
- **Condition Parsing** – Parse and type-check condition expressions, including random gates in allowed contexts.
- **Performance Budgets** – Flag passages or packs that exceed resource budgets, with escalating severity for critical failures.
- **Strict Mode** – Optional release build profile that escalates certain warnings to errors.

Validator results surface in the Control Panel with grouped errors and quick links to offending files, and can be exported as reports for CI pipelines.

## Plugin Layer

### Philosophy

Content creators should not need Python scripts; plug-ins are reserved for advanced behaviours, analytics, or extending the condition/effect vocabulary. Plug-ins are disabled by default to maintain safety.

### Hook Surface

Plug-ins can implement:

- `on_engine_start(context)`
- `on_game_start(state)`
- `on_passage_enter(passage_id, state)`
- `on_choice_selected(passage_id, choice_index, state)`
- `register_conditions(registry)` – Add pure, side-effect-free condition helpers.
- `register_effects(registry)` – Introduce new effect types that map to validated state mutations.

### Safety Modes

- **Safe Mode** – Plug-ins disabled entirely. Default for fresh installs.
- **Restricted Mode** – Plug-ins execute with a whitelist of modules, no file or network I/O, and enforced timeouts.
- **Trusted Mode** – Full Python access, off by default and clearly labelled.

## Content Pack Structure and Distribution

Each content pack is a folder containing:

- `manifest` – Metadata (name, version, author, licence), engine compatibility, dependencies, soft dependencies, provided namespaces, conflicts, asset folders, and localisation support.
- `content` – Story files, typically partitioned by arc or area.
- `assets` – Images and audio referenced by passages.
- `strings` – Localisation files per locale.
- `data` – Optional stat presets or relationship templates.
- `tests` – Optional golden path scripts for CI.
- `docs` – Optional modder-facing notes.

### Load Order and Overrides

- Base game loads first, followed by packs in configured order.
- Later packs override earlier passages if IDs collide; the validator warns about overrides.
- Soft dependencies allow optional enhancements without runtime crashes when missing.
- Namespaces reduce collision risk and promote clarity.

### Compatibility and Migration

- The engine follows semantic versioning; minor updates strive to retain compatibility.
- Packs declare supported engine ranges (e.g. `>=1.2 <2.0`).
- Migration tools assist with schema changes, such as renaming fields or tags.

### Distribution Workflow

- Control Panel packages selected packs into zipped bundles with manifest stamps.
- Zipped packs install via drag-and-drop into the `mods` directory; the installer verifies and unpacks safely, guarding against path traversal.
- Licence metadata is required; missing licences default to permissive but flagged as unknown.

## Tooling and Documentation

NarraForge ships with documentation and utilities tailored for writers, modders, and plug-in developers:

- **Writer’s Guide** – Explains passage formats, tag usage, and accessibility guidance.
- **Modder’s Handbook** – Covers manifests, load order management, validation workflows, and distribution packaging.
- **Plugin API Reference** – Details hook contracts, safety expectations, and examples for restricted mode.
- **Style Guide** – Establishes tone, stat naming conventions, and inclusive language best practices.
- **Examples** – Includes a reference content pack and sample restricted-mode plug-in to accelerate onboarding.

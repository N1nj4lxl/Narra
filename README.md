# NarraForge

NarraForge is a data-driven narrative engine for visual novel-style games with an emphasis on moddable content packs and strict validation. This repository currently tracks the product vision, high-level architecture, and design contracts that guide future development of the runtime engine, control panel, and tooling ecosystem.

## Documentation

- [Product Vision and Architecture](docs/overview.md)
- [Content Model and Data Contracts](docs/content_model.md)
- [Runtime and Control Panel Experience](docs/runtime_control_panel.md)
- [Validation, Plugins, and Tooling](docs/validator_and_plugins.md)

## Status

The repository now includes a Python reference implementation of the NarraForge runtime core, loader, validator, and command line tooling. The implementation focuses on the data-driven systems outlined in the design documents:

- Typed data models for manifests, passages, choices, and effects.
- A deterministic runtime engine that evaluates conditions, applies effects, and advances passages.
- A strict pack loader that reads JSON manifests and story files from content packs.
- A validator that surfaces duplicate passages and condition syntax issues.
- A `narraforge` CLI with `validate` and `inspect` subcommands for day-to-day workflows.
- An `examples/sample_pack` directory that demonstrates the expected pack layout.

Future work will expand on the control panel UI, additional validator rules, persistence, and plug-in sandboxes described in the specs.

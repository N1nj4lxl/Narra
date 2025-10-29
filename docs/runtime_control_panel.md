# Runtime and Control Panel Experience

## Control Panel UI

The Control Panel is a desktop management console without live scene preview. It comprises the following sections:

- **Home** – Project selector, recent projects list, open-folder shortcut, and a prominent **Launch Game** button that starts the runtime with a chosen profile and RNG seed.
- **Content Packs** – Displays built-in and installed packs with enable/disable toggles, load order controls, dependency visualisation, and per-pack validation badges. Users can install packs from folders or zips.
- **Tags and Stats** – Read-only catalogue of canonical stats and tags, with export tools for writers.
- **Validation** – Runs the validator across enabled packs, presenting grouped errors and warnings with file path shortcuts.
- **Build and Export** – Packages selected packs into distributable zips, stamps manifests, generates changelog excerpts, and reports size and hash budgets.
- **Settings** – Controls for engine version pinning, default runtime skin, accessibility defaults for test runs, and plug-in safety mode selection.
- **Tools** – Utilities for link graph exports (image or JSON), golden path runner configuration, and save migrator dry runs.

## Runtime Game UI

The runtime renders content in a standard VN-inspired layout:

- **Top** – Image banner representing the current passage.
- **Middle** – Prose body supporting inline substitutions for stats, relationships, and time.
- **Bottom** – Two to four choice buttons, optionally weighted for random choice menus.
- **Sidebar** – Collapsible right panel exposing:
  - Current time, stats, relationships, and a schedule preview.
  - Control buttons: Save, Load, Restart, Options, Mods.
  - Accessibility toggles (text scaling, font selection, contrast, image opacity).

A developer overlay is available in test builds when launched with a flag, revealing condition evaluations, hidden choices, and stat deltas.

## Flow and Persistence

- Deterministic RNG seeds each save file, with optional per-passage sub-seeds.
- Return stack supports modal sub-passages.
- Autosaves occur at day starts or when content flags a passage.
- Save slots are named and include thumbnails, timestamps, and version metadata for migration.

## Accessibility and Localisation Hooks

- Text scaling, dyslexia-friendly fonts, high-contrast mode, and adjustable image opacity support readability.
- Keyboard navigation and screen reader labels ensure inclusive play.
- Content filters driven by tags allow players to hide sensitive material.
- Right-to-left languages and per-language font or line-height adjustments are supported via localisation packs.

## Performance Considerations

- Media is lazily loaded with caching of recently used assets.
- Validators enforce maximum image dimensions and file sizes, warning or blocking problematic assets.
- Static analysis prevents hot loop transitions and highlights expensive passages before runtime issues arise.

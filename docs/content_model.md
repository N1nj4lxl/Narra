# Content Model and Data Contracts

## Passages

All interactive story moments in NarraForge are represented as **passages** with the following fields:

| Field | Description |
| --- | --- |
| `id` | Unique identifier, recommended to be namespaced (e.g. `club.robodrama.week2.intro`). |
| `title` | Human-friendly display name. |
| `tags` | List of strings for classification and filtering (e.g. `location:library`, `menu:start`). |
| `media` | Keys for primary image and optional ambient audio. |
| `body` | Rich text with lightweight markup and inline variables (e.g. `{stat:Grades}`, `{time:slot}`). |
| `choices` | List of player options with text, target passage id, optional condition, effects, and optional random weight. |
| `on_enter` | Effects triggered when entering the passage. |
| `time_cost` | Optional time slot or scheduling cost when the passage resolves. |

### Choices

Each choice supports:

- `text` – Display text.
- `to` – Target passage id.
- `condition` – Optional expression gate.
- `effects` – Declarative state changes (see Effects below).
- `weight` – Optional weight for randomised selection in weighted choice menus.

### Supporting Entities

- **Stats** – Named integers or floats with optional min and max bounds (e.g. Grades, Energy, Stress).
- **Flags** – Booleans or enums representing story state.
- **Relationships** – Meters from 0 to 100 with soft thresholds at 25, 50, and 75.
- **Time** – Week number, day of week, and time slot (morning, afternoon, evening, night).
- **Schedule** – Queued events targeted at future time points.

## Condition Grammar

NarraForge uses a small, safe expression language. Expressions support literals, comparison operators, boolean operators (`and`, `or`, `not`), and namespaced functions such as `stat("Grades")`, `flag("JoinedDrama")`, `rel("Alex")`, `time.week`, and `time.slot`. Enum membership checks use `in` (e.g. `time.day in ["Sat", "Sun"]`). Random gates via `chance(probability)` are only allowed in `on_enter` blocks or explicitly marked randomised choices.

## Effects Model

Effects are atomic, declarative mutations:

- `add_stat(name, amount)`
- `set_stat(name, value)`
- `set_flag(name, value)`
- `add_rel(name, amount)`
- `schedule(passage_id, when=...)`
- `unlock_tag(name)` / `lock_tag(name)`
- `goto(passage_id)` – Reserved for safeguards in `on_enter`.

Effects can be chained inside `on_enter` or per-choice lists, and complex results are achieved by combining small operations rather than scripting.

## Flow and Randomness

- Deterministic seeded RNG per save enables reproducible bug reports.
- Optional per-passage sub-seeds support localised randomness without affecting the wider run.
- A return stack permits temporary sub-passages, enabling modal mini-scenes or detours.

## Rendering Contract

Content authors rely on the standard runtime layout:

- Top: primary image area.
- Middle: prose body with inline substitutions.
- Bottom: two to four choice buttons, optionally weighted.
- Right: collapsible sidebar for time, stats, relationships, schedule preview, and control buttons (Save, Load, Restart, Options, Mods).

Skins define theming for the runtime. The Control Panel does not preview skins, but runtime skin swapping is supported.

## Persistence

- Save slots are named and include thumbnails and timestamps.
- Autosaves occur on flagged passages or day transitions.
- Save files are gzipped JSON with version metadata and migration support for backwards compatibility.

## Accessibility

- Adjustable text scaling and font selection (including dyslexia-friendly options).
- High contrast theme and image opacity slider to enhance readability.
- Full keyboard navigation and screen reader friendly labels.
- Tag-driven content filters (e.g. `theme:alcohol`, `theme:exam_anxiety`).

## Localisation

- Packs ship string tables per locale, keyed by stable identifiers.
- Runtime supports right-to-left rendering and per-language font overrides or line-height adjustments.

## Tag Catalogue

Baseline tags include:

- **Locations**: dorm, classroom, library, cafeteria, gym, theatre.
- **Clubs**: robotics, drama, debate, athletics, radio.
- **Courses**: compsci, drama, history, business, biology.
- **Themes**: alcohol, exam_anxiety, romance, rivalry.
- **Menu Types**: menu:start, menu:options, menu:mods, menu:saves, menu:character_creator.
- **Time**: morning, afternoon, evening, night.

Packs can extend the catalogue using namespaced tags such as `club:quidditch`.

## Stats Contract

Core stats ship with the base game, but packs may declare additional stats along with their min and max bounds. Writers always reference stats by name and never by index.

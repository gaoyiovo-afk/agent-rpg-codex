# Changelog

## 1.1.0 — 2026-10-05

Based on upstream `agent-rpg` 1.0.1 by xhrisfu.

### Added

- Cross-process and in-process campaign locking.
- Monotonic `world.json.revision` values.
- Explicit untrusted-campaign-data boundaries in tool output and skill instructions.
- GM and player state views with secret-field redaction.
- JSON, journal, string, collection, and nesting safety limits.
- Strict schema checks with controlled user-facing errors.
- Windows reserved-name validation.
- Symlink and Windows reparse-point checks for core save files.
- Atomic journal writes and bounded streaming journal-tail reads.
- Automatic pre-force snapshots and exact campaign confirmation.
- Security, concurrency, redaction, malformed-save, and portability regression tests.
- Portable and Codex-compatible plugin manifests.

### Changed

- Non-standard JSON constants such as `NaN` are stored as plain text rather than emitted as invalid JSON.
- Journal entries are normalized to one Markdown line.
- Hidden NPCs, quests, and clocks can be excluded from player view.
- Provenance and licensing are documented at repository and skill level.

### Removed

- Unused icon demonstration with insufficiently documented third-party provenance.
- ClawHub-specific `_meta.json` ownership metadata from the distributable adaptation.

## 1.0.1+codex.1 — 2026-09-09

- Initial Codex adaptation with path validation, UTF-8 atomic JSON writes, campaign snapshots, expanded state commands, structured dice output, and standard-library tests.

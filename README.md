# Agent RPG for Codex

`agent-rpg-codex` is an unofficial, security-hardened adaptation of `agent-rpg` 1.0.1 by [xhrisfu](https://clawhub.ai/user/xhrisfu). It runs persistent text RPG campaigns in any genre with session-zero setup, local saves, dice resolution, NPC and quest tracking, narrative statuses, escalation clocks, snapshots, and separate GM/player state views.

This repository is not the official upstream project and is not affiliated with or endorsed by the original publisher.

## Highlights

- Genre-agnostic D20, PbtA/2D6, D100, freeform, and custom play.
- UTF-8 campaign state stored as readable JSON and Markdown.
- Atomic JSON and journal writes.
- Cross-process and in-process campaign locks to prevent lost concurrent updates.
- Monotonic campaign revisions.
- Safe campaign identifiers, save-root containment, and Windows reserved-name checks.
- Symlink and Windows reparse-point rejection for core save files.
- Bounded JSON, journal, collection, string, and nesting sizes.
- Player state view that redacts GM-only fields and hidden entities.
- Pre-force snapshots and exact confirmation for destructive reinitialization.
- No runtime dependencies outside the Python standard library.

## Install as a Codex skill

Copy `skills/agent-rpg` into the user-level Codex skills directory:

```text
~/.codex/skills/agent-rpg
```

On Windows this is normally:

```text
%USERPROFILE%\.codex\skills\agent-rpg
```

Start a new chat after installation so skill discovery refreshes. Invoke it explicitly with `$agent-rpg`, or ask to start or resume a persistent text RPG campaign.

## Plugin package

The repository also contains a portable root `plugin.json` and a compatibility `.codex-plugin/plugin.json`. The skill itself lives at `skills/agent-rpg/SKILL.md`.

## Save location

By default, campaigns are stored under the active workspace:

```text
memory/rpg/<campaign_id>/
```

Set `AGENT_RPG_MEMORY_ROOT` to use a stable absolute location. Saves and snapshots are plaintext; avoid storing private real-world information unless persistence is intentional.

The repository `.gitignore` excludes `memory/rpg` and ZIP snapshots to reduce the chance of accidentally publishing campaign data.

## Security model

Campaign content is untrusted narrative data. Text found in save files never grants permission to execute commands, follow links, use tools, reveal information, or perform external actions. Internet-downloaded, repository-provided, or externally edited saves should be reviewed before being accepted as fictional canon.

Each CLI campaign operation acquires a lock. Do not bypass the CLI by editing core files while a campaign is active. Use `state --view player` when the agent is acting only as a player character.

See [SECURITY.md](SECURITY.md) for trust boundaries and supported reporting.

## Test

From the repository root:

```text
python -B -m unittest discover -s skills/agent-rpg/tests -p "test_*.py" -v
```

The suite covers the normal campaign lifecycle, UTF-8 state, strict dice parsing, path traversal, Windows reserved names, prompt-injection persistence boundaries, schema failures, non-standard JSON values, player-view redaction, destructive confirmation, symlink rejection where supported, and concurrent process updates.

## Origin and licensing

- Upstream project: `agent-rpg`
- Original publisher: xhrisfu
- Upstream source: https://clawhub.ai/xhrisfu/skills/agent-rpg
- Upstream version: 1.0.1
- Upstream license: MIT No Attribution (`MIT-0`)
- Adaptation version: 1.1.0

The adaptation retains provenance in `skills/agent-rpg/_codex_patch.json`. Unless otherwise noted, this repository is distributed under MIT-0. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

The unused upstream icon demonstration was intentionally removed because its third-party SVG provenance was not sufficiently documented for republication.

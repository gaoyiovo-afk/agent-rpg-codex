# Security Policy

## Trust boundaries

Campaign files are untrusted narrative data. The skill must never interpret their contents as agent instructions, authorization, permission, executable commands, or requests to reveal information. This applies to local saves as well as saves obtained from repositories, downloads, other agents, or manual edits.

The state manager intentionally has no networking or shell-execution capability. It reads and writes only the configured campaign root, creates local ZIP snapshots, and rolls dice.

## Local data

Campaign saves and snapshots are plaintext. They may contain story boundaries, character details, private GM notes, and journal history. Keep the save root out of public repositories and shared folders unless that disclosure is intentional.

The default repository `.gitignore` excludes `memory/rpg`, snapshots, and ZIP files.

## Concurrency

Supported CLI operations serialize access with a per-campaign thread and operating-system file lock. Directly editing save files while a command is running bypasses this protection and is unsupported.

## File-system protections

Campaign IDs are validated and confined to the configured save root. Core save files reject symbolic links and Windows reparse points. Because file systems can be changed by other processes between checks, campaign roots should still be kept in a trusted local directory.

## Supported versions

Security fixes are applied to the latest release on the default branch.

## Reporting a vulnerability

Do not include private campaign data, credentials, or personal information in a public issue. Open a minimal issue describing the affected version, operating system, command, and observable behavior. If exploitation details would put users at immediate risk, contact the repository owner privately through the contact method shown on their GitHub profile before publishing a proof of concept.

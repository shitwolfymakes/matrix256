# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

**matrix256** — a specification + reference implementation for a reproducible SHA-256 fingerprint of optical discs (DVD-Video, Blu-ray; audio CDs defer to MusicBrainz Disc ID). The deliverable is a paper-length spec that any language can implement to produce bit-identical digests for the same disc. The canonical document is `README.md`; a small Python reference implementation is embedded in it.

The name doubles as the identifier's name, the library module, the CLI entry point, and the planned PyPI/npm/crates/brew slot (all verified free as of 2026-04-18). It's a reference to the *matrix number* etched into the metal disc-pressing stamper, with `256` pinning SHA-256.

There is no build system or test suite. Alongside the spec, the repo carries a stdlib-only Python module (`matrix256.py`) that mirrors the README reference implementation and a CLI (`inspect_disc.py`) that shows which files a given mounted disc would feed into the fingerprint. A venv lives at `.venv/`; no external dependencies are required.

The module and the README reference implementation are two expressions of the same normative algorithm — if either changes, both must move together and produce byte-identical digests on the same input.

## Load-bearing invariants

When editing the spec or the reference implementation, these properties must hold — violating any of them breaks the whole point of the project:

- **Determinism across implementations.** The digest must depend only on bytes on the disc and on choices fixed in the spec (file list, ordering, chunking is irrelevant to the hash). Never introduce anything that depends on the reader, OS, filesystem driver, locale, or library version. If a change could make two correct implementations disagree, it is wrong.
- **Fixed file list and fixed order.** DVD: `VIDEO_TS.IFO`, then `VTS_NN_0.IFO` for `NN` in `01..99` ascending. Blu-ray: `BDMV/index.bdmv`, `BDMV/MovieObject.bdmv`, then `BDMV/PLAYLIST/*.mpls` lexicographic, then `BDMV/CLIPINF/*.clpi` lexicographic. No separators, no length prefixes, no framing.
- **Exclusions are intentional.** `.BUP` files, `BDMV/BACKUP/*`, VOB/M2TS payload, `BDMV/STREAM`, `BDMV/AUXDATA`, `BDMV/BDJO`, `BDMV/JAR`, `BDMV/META` are deliberately excluded. Proposals to add them must explain why they don't either double-count (backups) or force whole-disc reads (payloads).
- **Audio CD = MusicBrainz Disc ID, unchanged.** Do not propose an ARM-specific SHA-256 for audio CDs; the spec explicitly adopts MusicBrainz to avoid ecosystem fragmentation.
- **No `format_version` field or other implementation-choice knobs.** A prior draft had one; it was removed because optional behavior destroys reproducibility. Future revisions are separate algorithms (e.g. `v2`), not parameters of this one.

## Editing guidance

- When revising the spec, keep the DVD/Blu-ray/audio-CD sections symmetric in structure (collect → sort → concatenate → SHA-256) — the paper's readability depends on that parallelism.
- The reference implementation in `README.md` is part of the normative spec: if you change file-selection or ordering logic in prose, update the Python too (and vice versa), and verify they still match.
- Filenames in DVD-Video are uppercase; UDF is case-insensitive but case-sensitive views must select uppercase. Don't "fix" this to be case-insensitive in the reference code.
- The `Rationale` and `Limitations` sections carry the argumentative weight of the paper — prefer extending them over inlining justification into the algorithm section.

## Unrelated files

`sqlite_mcp_server.db` is a scratch file from an MCP server, not part of the spec. Ignore it.

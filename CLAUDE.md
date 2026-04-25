# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

**matrix256** — a specification family for reproducible SHA-256 fingerprints of optical discs and, more generally, of rooted filesystem trees. The deliverable is paper-length normative spec(s) that any language can implement to produce bit-identical digests for the same input. Audio CDs defer to MusicBrainz Disc ID and are not in scope for either matrix256 version.

Two algorithm versions coexist in this repo:

- **v0 (initial, frozen):** structural hash over a fixed list of named metadata files. DVD: `VIDEO_TS.IFO`, `VTS_NN_0.IFO`. Blu-ray: `index.bdmv`, `MovieObject.bdmv`, MPLS, CLPI. The normative spec is `README.md` and the reference implementation is `matrix256/v0.py`. v0 is under active evaluation against the real-disc corpus in `CORPUS.md`; published v0 digests must remain stable.
- **v1 (draft, filesystem-agnostic):** walk the entire filesystem at the provided root and serialize `(path, size)` records. The normative spec is `SPEC.md`. There is no v1 reference implementation yet — `matrix256/v1.py` is the planned home.

Companion (non-normative) documents:

- `IMPLEMENTERS.md` — practical guidance for v1 implementers (bridge discs, encoding, mount handling).
- `RATIONALE.md` — design rationale and prior-art comparison.
- `VENUES.md` — candidate publication venues.
- `PUBLICATION_TARGETS.md` — earlier journal scouting; partially superseded by `VENUES.md` but still in tree.

The name doubles as the identifier's name, the library module, the CLI entry point, and the planned PyPI/npm/crates/brew slot (all verified free as of 2026-04-18). It's a reference to the *matrix number* etched into the metal disc-pressing stamper, with `256` pinning SHA-256.

There is no build system or test suite. Alongside the specs, the repo carries a stdlib-only Python package (`matrix256/`, with each algorithm version as a submodule — currently only `matrix256.v0`) and a CLI (`inspect_disc.py`) that shows which files a v0 fingerprint of a mounted disc would consume. A venv lives at `.venv/`; no external dependencies are required.

The `matrix256.v0` submodule and the README v0 reference implementation are two expressions of the same normative v0 algorithm — if either changes, both must move together and produce byte-identical digests on the same input.

## Load-bearing invariants (v0)

When editing the spec or the reference implementation, these properties must hold — violating any of them breaks the whole point of the project:

- **Determinism across implementations.** The digest must depend only on bytes on the disc and on choices fixed in the spec (file list, ordering, chunking is irrelevant to the hash). Never introduce anything that depends on the reader, OS, filesystem driver, locale, or library version. If a change could make two correct implementations disagree, it is wrong.
- **Fixed file list and fixed order (v0).** DVD: `VIDEO_TS.IFO`, then `VTS_NN_0.IFO` for `NN` in `01..99` ascending. Blu-ray: `BDMV/index.bdmv`, `BDMV/MovieObject.bdmv`, then `BDMV/PLAYLIST/*.mpls` lexicographic, then `BDMV/CLIPINF/*.clpi` lexicographic. No separators, no length prefixes, no framing.
- **Exclusions are intentional (v0).** `.BUP` files, `BDMV/BACKUP/*`, VOB/M2TS payload, `BDMV/STREAM`, `BDMV/AUXDATA`, `BDMV/BDJO`, `BDMV/JAR`, `BDMV/META` are deliberately excluded. Proposals to add them must either stay inside v0 with a compelling reason why they don't double-count or force whole-disc reads, or be factored out as a v1+ algorithm.
- **Audio CD = MusicBrainz Disc ID, unchanged.** Do not propose an ARM-specific SHA-256 for audio CDs; the spec explicitly adopts MusicBrainz to avoid ecosystem fragmentation.
- **No `format_version` field or other implementation-choice knobs.** A prior draft had one; it was removed because optional behavior destroys reproducibility. Future revisions are separate algorithms (e.g. `matrix256v1`), not parameters of v0.
- **v0 digests are immutable.** Once a hash is in `CORPUS.md`, it must keep matching. Any change that would cause a previously-recorded corpus digest to differ is a v0 regression and should instead be scoped to a future version.

## Version labeling conventions

- In running text: "matrix256 v0", "matrix256 v1" (or just "matrix256" where the context makes the version unambiguous, e.g. inside `README.md` or `CORPUS.md` after the introduction has established scope).
- In structured contexts (database columns, API fields, file headers): `matrix256v0`, `matrix256v1`, or a separate `version: 0` / `version: 1` field.
- In the v0 reference implementation: `matrix256.v0.VERSION = "0"`.
- Never embed the version in the digest string itself — the digest is a 64-character lowercase hex SHA-256, nothing else.

## Editing guidance

- The v0 normative spec is `README.md`; the v1 normative spec is `SPEC.md`. Keep them clearly separated: don't blur v0 prose with v1 framing or vice versa.
- v0 has two synchronized expressions: the prose+code in `README.md` and the submodule `matrix256/v0.py`. If file-selection or ordering logic changes in one, update the other and verify they still produce byte-identical digests on the corpus.
- v1 has no reference implementation yet. The planned home is `matrix256/v1.py`; if you add one, treat it the same way as v0 (prose in `SPEC.md` and code must match), and any future v1 corpus digests are immutable from the moment they're published.
- When revising v0 prose, keep the DVD/Blu-ray/audio-CD sections symmetric (collect → sort → concatenate → SHA-256) — the paper's readability depends on that parallelism. v1 is filesystem-agnostic, so the parallelism rule does not apply there.
- Filenames in DVD-Video are uppercase; UDF is case-insensitive but case-sensitive views must select uppercase. Don't "fix" this to be case-insensitive in v0 reference code.
- Argumentative content belongs in `RATIONALE.md`; practical implementer concerns (mounting, encoding, bridge-disc resolution) belong in `IMPLEMENTERS.md`. Both are non-normative and must not contradict the specs they accompany.
- If a proposed change would alter an existing v0 corpus digest, it is by definition a v1+ change, not a v0 revision. Open a design doc for the new version; leave v0 frozen. The same rule applies once v1 digests are published.

## Unrelated files

`sqlite_mcp_server.db` is a scratch file from an MCP server, not part of the spec. Ignore it.

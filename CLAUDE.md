# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

**matrix256** — a specification for reproducible SHA-256 fingerprints of rooted filesystem trees, with optical discs as the primary intended use case. The deliverable is a paper-length normative spec that any language can implement to produce bit-identical digests for the same input. Audio CDs have no filesystem and are out of scope; MusicBrainz Disc ID is the recommended complementary identifier for them.

The algorithm walks the entire filesystem at the provided root and serializes `(path, size)` records in a canonical form, hashed with SHA-256. The normative spec is `SPEC.md`; the reference implementation is `matrix256/v1.py`. The spec is labeled **matrix256v1**: there is no v0 in active service. An earlier `matrix256v0` algorithm was retired before publication; its corpus, code, and prose are gone from this tree (still recoverable from git history if ever needed).

Companion (non-normative) documents:

- `README.md` — project landing page: motivation, quickstart, links into the rest of the tree.
- `IMPLEMENTERS.md` — practical guidance for implementers (bridge discs, encoding, mount handling).
- `RATIONALE.md` — design rationale and prior-art comparison.
- `CORPUS.md` — evaluation corpus of real discs and their published `matrix256v1` digests.
- `VENUES.md` — candidate publication venues.
- `PUBLICATION_TARGETS.md` — earlier journal scouting; partially superseded by `VENUES.md` but still in tree.

The name doubles as the identifier's name, the library module, the CLI entry point, and the planned PyPI/npm/crates/brew slot (all verified free as of 2026-04-18). It's a reference to the *matrix number* etched into the metal disc-pressing stamper, with `256` pinning SHA-256.

There is no build system or test suite. Alongside the spec, the repo carries a stdlib-only Python package (`matrix256/`, with the algorithm in `matrix256.v1`) and a CLI (`inspect_disc.py`) that walks a mounted disc, surfaces metadata, and prints the matrix256v1 digest. A venv lives at `.venv/`; no external dependencies are required.

The `matrix256.v1` submodule and the `SPEC.md` prose are two expressions of the same normative algorithm — if either changes, both must move together and produce byte-identical digests on the same input.

## Load-bearing invariants

When editing the spec or the reference implementation, these properties must hold — violating any of them breaks the whole point of the project:

- **Determinism across implementations.** The digest must depend only on the filesystem view exposed at the provided root and on choices fixed in the spec (path normalization, size source, sort order, serialization). Never introduce anything that depends on the reader, OS, filesystem driver, locale, or library version. If a change could make two correct implementations disagree on the same input view, it is wrong.
- **Path normalization is fixed.** Forward slash separator, no leading slash, NFC, UTF-8 with U+FFFD substitution for invalid units. Sort order is byte-wise lexicographic over the UTF-8 encoded relative paths.
- **Size comes from filesystem metadata, not from reading file contents.** Implementations must not seek through or read file bytes to verify size.
- **Audio CDs out of scope.** Audio CDs have no filesystem and the spec applies to filesystem-rooted inputs. MusicBrainz Disc ID is the established community identifier.
- **No `format_version` field or other implementation-choice knobs inside the digest.** Spec versions, when added, are separate algorithms (e.g. a hypothetical `matrix256v2`), not parameters of v1. The 64-character lowercase hex SHA-256 is the entire digest string.
- **v1 digests are immutable.** Once a hash is in `CORPUS.md`, it must keep matching. Any change that would cause a previously-recorded corpus digest to differ is a v1 regression and should instead be scoped to a future version.

## Version labeling conventions

- The version-bearing label is `matrix256v1` — no space between the family name and the version, in running prose and in structured contexts alike (database columns, API fields, file headers, table headers, bold field names). Bare `matrix256` is fine where the version is unambiguous from context (e.g. inside `SPEC.md` or `CORPUS.md` after the introduction has established scope).
- A separate `version: 1` field is acceptable as an alternative when the carrier already names matrix256 elsewhere.
- In the reference implementation: `matrix256.v1.VERSION = "1"`.
- Never embed the version in the digest string itself — the digest is a 64-character lowercase hex SHA-256, nothing else.

## Editing guidance

- The normative spec is `SPEC.md`; `README.md` is a friendly landing page and must not contradict the spec. If `SPEC.md` and `README.md` disagree, `SPEC.md` wins and `README.md` is the bug.
- The spec and the submodule must agree: `SPEC.md` and `matrix256/v1.py` must produce byte-identical digests on the same input. If walk/sort/serialization logic changes in one, update the other and verify against `CORPUS.md`.
- Argumentative content belongs in `RATIONALE.md`; practical implementer concerns (mounting, encoding, bridge-disc resolution) belong in `IMPLEMENTERS.md`. Both are non-normative and must not contradict `SPEC.md`.
- If a proposed change would alter an existing v1 corpus digest, it is by definition a v2+ change, not a v1 revision. Open a design doc for the new version; leave v1 frozen.
- v0 is retired. Do not reintroduce v0 prose, code, or corpus columns. If a historical v0 digest is needed (e.g. for cross-referencing a third-party catalog), recover it from git history rather than re-adding columns to the active corpus.

## Unrelated files

`sqlite_mcp_server.db` is a scratch file from an MCP server, not part of the spec. Ignore it.

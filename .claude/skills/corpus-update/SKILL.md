---
name: corpus-update
description: Run inspect_disc.py against the disc currently loaded in the optical drive, look up its existing matrix256v0 entry in CORPUS.md, and add the matrix256v1 digest plus the IMPLEMENTERS.md §5 filesystem-view fields. Aborts without editing if no matching v0 entry is found.
---

# corpus-update

Companion to `corpus-add`. Used when a disc whose v0 digest is already in `CORPUS.md` gets re-inspected and we want to record the v1 digest plus the per-digest filesystem-view metadata IMPLEMENTERS.md §5 recommends. Stops short of committing — changes are left in the working tree for the user to review.

## 1. Locate the optical drive

Find the block device for the currently-loaded disc with a single `lsblk` call covering the four conventional optical-drive nodes:

```
lsblk -o NAME,LABEL,FSTYPE /dev/sr0 /dev/sr1 /dev/sr2 /dev/sr3
```

Missing nodes print a one-line error to stderr and are skipped; present nodes appear in the table. Pick the device with a non-empty `LABEL` (and usually `udf` or `iso9660` as `FSTYPE`).

If no loaded optical disc is found, stop and tell the user — do not modify `CORPUS.md`.

## 2. Inspect the disc

Use `--json` for clean parsing; skip metadata extraction (lsdvd / bd_info / makemkv aren't needed for an update):

```
python inspect_disc.py <device> --no-metadata --json
```

Read these from the JSON:

- `fingerprints.v0` — used to look up the existing entry
- `fingerprints.v1` — the new digest to record
- `submission.source_kind`
- `submission.filesystem`
- `submission.mount_device`
- `submission.mount_options`
- `submission.reader.{tool, python, os}`

## 3. Find the matching v0 entry

Grep `CORPUS.md` for the bullet line containing the computed v0:

```
grep -nF "**matrix256v0:** \`<full v0 hash>\`" CORPUS.md
```

Walk back from that line to the nearest `## N. <title>` heading to identify which entry it belongs to.

**If no entry matches, stop. Do not edit `CORPUS.md`.** Report which v0 hash was computed and that no entry references it. Adding a brand-new entry is `corpus-add`'s job, not this one.

## 4. Check for an existing v1 record

If the matched entry already has a `**matrix256v1:**` bullet:

- **Recorded v1 matches the computed v1**: the entry is already up to date. Report and exit without edits.
- **Recorded v1 differs**: this is a regression — v1 digests are immutable once published, just like v0. Report which entry mismatched and the two hashes, then stop. **Do not overwrite.**

If the entry has no v1 bullet, proceed to step 5.

## 5. Edit the entry

Insert three bullets immediately after the existing `**matrix256v0:**` bullet (preserving everything else):

```
- **matrix256v1:** `<full 64-char hash>`
- **Filesystem view:** <filesystem> on <mount_device> (<source_kind>); options `<mount_options>`
- **Reader:** <reader.tool> · python <reader.python> · <reader.os>
```

Notes on formatting:

- Use the middle dot (`·`, U+00B7) as the reader-field separator — that's what `inspect_disc.py` prints.
- Wrap `mount_options` in backticks; the comma-separated `key=value` form reads better as code.
- Don't update the summary table at the top of `CORPUS.md`. Its `matrix256v0 (first 16)` column is v0-only by design.

## 6. Report

One short message covering:

1. Which entry number + title was updated.
2. The full new v1 hash.
3. The captured view in one line (e.g. `udf on /dev/sr0, source_kind=physical_disc`).

Then stop. **Do not commit.** The user reviews the working-tree diff and commits explicitly when they're ready.

## Notes and constraints

- Use the device path (`/dev/srN`), not a mount point — `inspect_disc.py` handles mount/unmount internally.
- If `inspect_disc.py` fails (unreadable disc, missing tool, unexpected structure), report the error and leave `CORPUS.md` untouched.
- v1 immutability mirrors v0's: once recorded for a corpus disc, that v1 value must keep matching. A mismatch on rerun is grounds to investigate, not to overwrite.
- The skill is idempotent on a happy path: re-running on a disc whose entry already has a matching v1 + view should report "already up to date" and make no changes.

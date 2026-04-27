---
name: corpus-update
description: Re-inspect the disc currently loaded in the optical drive, look up its existing entry in CORPUS.md by matrix256v1 fingerprint, and refresh or backfill the IMPLEMENTERS.md §5 filesystem-view fields. Refuses to overwrite a recorded matrix256v1 with a different value (immutability check).
---

# corpus-update

Companion to `corpus-add`. Re-inspects a disc that's already in the corpus and refreshes the captured filesystem view, or backfills missing v1 / view fields on a stale entry. Stops short of committing — changes are left in the working tree for the user to review.

The two normal use cases:

1. **Stale entry** — an entry pre-dates the v1 / submission-view roll-out and is missing one or more of `**matrix256v1:**`, `**Filesystem view:**`, `**Reader:**`.
2. **View change** — the disc has been re-inspected from a different reader, OS, or filesystem driver, and the captured submission view should be refreshed.

If the disc isn't in the corpus at all, this is `corpus-add`'s job; report and stop.

## 1. Locate the optical drive

Find the block device for the currently-loaded disc with a single `lsblk` call covering the four conventional optical-drive nodes:

```
lsblk -o NAME,LABEL,FSTYPE /dev/sr0 /dev/sr1 /dev/sr2 /dev/sr3
```

Missing nodes print a one-line error to stderr and are skipped; present nodes appear in the table. Pick the device with a non-empty `LABEL` (and usually `udf` or `iso9660` as `FSTYPE`).

If no loaded optical disc is found, stop and tell the user — do not modify `CORPUS.md`.

## 2. Inspect the disc

Use `--json` for clean parsing; metadata extraction is optional for an update, so `--no-metadata` keeps the run fast:

```
python inspect_disc.py <device> --no-metadata --json
```

Read these from the JSON:

- `fingerprint` — the matrix256v1 digest, used to look up the entry.
- `submission.source_kind`
- `submission.filesystem`
- `submission.mount_device`
- `submission.mount_options`
- `submission.reader.{tool, python, os}`

## 3. Find the matching entry

First try a direct hash match:

```
grep -nF "**matrix256v1:** \`<full v1 hash>\`" CORPUS.md
```

If found, walk back from that line to the nearest `## N. <title>` heading. The entry is current; jump to step 5 if you want to refresh its view fields, or stop if not.

If the hash isn't recorded, the entry might still exist with a missing or different v1. Look up by disc identity instead:

- For Blu-rays, match `**AACS Disc ID:** \`<id>\`` against the JSON's metadata if available, or by the disc title in the entry heading.
- For DVDs and data discs, match by udisks label, libbluray/lsdvd disc name, or the title used in the heading.

If a candidate entry is found but already carries a *different* matrix256v1 hash, this is a regression — v1 digests are immutable once published. Report the entry, the recorded hash, and the freshly computed hash, and stop. **Do not overwrite.**

If no candidate entry is found at all, report the computed hash and recommend `corpus-add` for a brand-new entry. Stop.

## 4. Backfill or refresh fields

Within the matched entry's bullet list, ensure the three view bullets exist in this order, immediately after the heading:

```
- **matrix256v1:** `<full 64-char hash>`
- **Filesystem view:** <filesystem> on <mount_device> (<source_kind>); options `<mount_options>`
- **Reader:** <reader.tool> · python <reader.python> · <reader.os>
```

Cases:

- **Backfill** (entry has none of these): insert all three at the top of the bullet list.
- **Partial backfill** (entry has matrix256v1 but lacks Filesystem view / Reader, or vice versa): add only the missing bullets in the canonical order.
- **Refresh** (all three present, view differs from JSON): replace the existing Filesystem view + Reader bullets with the new values. Do **not** modify the matrix256v1 line — if the hash differs, you should already have stopped at step 3.

Notes on formatting:

- Use the middle dot (`·`, U+00B7) as the reader-field separator — that's what `inspect_disc.py` prints.
- Wrap `mount_options` in backticks; the comma-separated `key=value` form reads better as code.
- If you backfill a v1 hash, also update the entry's row in the summary table at the top of `CORPUS.md`: replace the placeholder hash cell with the first 16 chars of the new digest in backticks.

## 5. Report

One short message covering:

1. Which entry number + title was updated, and which case applied (backfill, partial backfill, refresh).
2. The matrix256v1 hash on file (and confirm it matched the recompute).
3. The captured view in one line (e.g. `udf on /dev/sr0, source_kind=physical_disc`).

Then stop. **Do not commit.** The user reviews the working-tree diff and commits explicitly when they're ready.

## Notes and constraints

- Use the device path (`/dev/srN`), not a mount point — `inspect_disc.py` handles mount/unmount internally.
- If `inspect_disc.py` fails (unreadable disc, missing tool, unexpected structure), report the error and leave `CORPUS.md` untouched.
- v1 immutability: once recorded for a corpus disc, that v1 value must keep matching. A mismatch on rerun is grounds to investigate, not to overwrite.
- The skill is idempotent on a happy path: re-running on a disc whose entry already has the matching v1 + view should report "already up to date" and make no changes.

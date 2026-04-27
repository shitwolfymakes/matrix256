---
name: corpus-add
description: Inspect the optical disc currently loaded in the system's optical drive, compute its matrix256v1 fingerprint via inspect_disc.py, and append a new entry to CORPUS.md. Accepts an optional one-or-two-sentence "why it's here" rationale as arguments; if omitted, derives one from the disc's observable properties.
---

# corpus-add

Automates the workflow we use when the user loads a new disc and asks to add it to the corpus. Stops short of committing — changes are left in the working tree for the user to review.

The optional arguments (`$ARGUMENTS`) are the **"Why it's here"** rationale for the new corpus entry. If the user provided them, use them verbatim. If they're empty, write a short one-to-two-sentence rationale yourself based on what the disc's properties reveal (new axis covered, unusual structure, pair with an existing entry, etc.).

## 1. Locate the optical drive

Find the block device representing the currently-loaded disc. Kernel enumeration can skip numbers after eject/reinsert cycles, so don't assume `/dev/sr0` is always correct.

List what's connected with a single call:

```
lsblk -o NAME,LABEL,FSTYPE /dev/sr0 /dev/sr1 /dev/sr2 /dev/sr3
```

Missing nodes print a one-line error to stderr and are skipped; present nodes appear in the table. Pick the device that reports a non-empty `LABEL` (and usually `udf` or `iso9660` as `FSTYPE`). Do **not** wrap this in a `for … do` shell loop — a single `lsblk` invocation with all four paths is cleaner and avoids one subshell per device.

If no loaded optical disc is found, stop and tell the user — do not modify `CORPUS.md`.

## 2. Inspect the disc

A single invocation produces the fingerprint, the submission view, and the metadata summary in one go:

```
python inspect_disc.py <device>
```

Extract these fields:

- **Disc name** (from `Disc name:` in the Metadata block; for DVDs, use `Disc title:` or fall back to the udisks label if neither is helpful).
- **Disc type** — "Blu-ray", "DVD-Video", or "Data disc" (derive from the `Disc type:` line plus the filesystem; non-DVD/non-BD discs report `Disc type: unknown` and are conventionally labeled "Data disc" in the entry heading).
- **matrix256v1 fingerprint** (full 64-char SHA-256 from the `Fingerprint (matrix256v1, SHA-256):` line).
- **Filesystem view** (from the `Submission metadata` block: `Filesystem`, `Mount device`, `Source kind`, `Mount options`).
- **Reader** (from the `Reader:` line in the same block).
- **AACS Disc ID** (from `Disc ID:` in the Metadata block; Blu-rays only; omit if absent).
- **Protection flags** (from `Protection:`; Blu-rays only — AACS/BD+/BD-J yes-or-no).
- **Title counts** (from `Title counts:`; Blu-rays only).
- **Main title** (from `Main title:`; Blu-rays only).

## 3. Find the next entry number

Read `CORPUS.md`, find the summary table, and identify the highest existing entry number in the first column. The new entry is that number + 1.

## 4. Append a row to the summary table

Add a new row at the bottom of the table in the format used by existing rows:

```
| N | <short title> | <type> | `<first-16-chars-of-hash>` |
```

For the short title, use the disc name, but abbreviate/annotate when useful — match the style of existing rows. Examples from the corpus:

- `Silicon Valley Season 1 Disc 1` → `Silicon Valley S1 — Disc 1`
- `Suicide Squad` → `Suicide Squad (theatrical)` (only when disambiguation is needed; otherwise leave the name alone).

Use 16 hex chars of the matrix256v1 fingerprint (first 8 bytes).

## 5. Append a full entry section

Insert a new `## N. <Disc Name> (<Type>)` section immediately **before** the `## Reproducing a fingerprint` heading. Use the full disc name in the heading.

### Common bullet ordering

Every entry leads with the same three bullets (the digest and the captured filesystem view):

```
- **matrix256v1:** `<64-char SHA-256>`
- **Filesystem view:** <filesystem> on <mount_device> (<source_kind>); options `<mount_options>`
- **Reader:** <reader.tool> · python <reader.python> · <reader.os>
```

Then the disc-type-specific bullets follow.

### Blu-ray layout

```markdown
## N. <Full Disc Name> (Blu-ray)

- **matrix256v1:** `<64-char SHA-256>`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python <X.Y.Z> · Linux <release>
- **AACS Disc ID:** `<40-char hex>`
- **Protection:** AACS <✓ or ✗>, BD+ <✓ or ✗>, BD-J <✓ or ✗>
- **Titles:** N HDMV + M BD-J (K "unsupported"); main title #X
- **Why it's here:** <verbatim $ARGUMENTS, or an inferred rationale>
```

Omit the `AACS Disc ID` bullet if the disc didn't report one.

### DVD layout

DVDs produce much less metadata, so use a trimmed template. Look at entry 2 (Sintel) for reference:

```markdown
## N. <Full Disc Name> (DVD-Video)

- **matrix256v1:** `<64-char SHA-256>`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python <X.Y.Z> · Linux <release>
- **Source:** <if known, otherwise omit>
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** <verbatim $ARGUMENTS, or an inferred rationale>
```

### Data disc layout

For non-DVD/non-BD discs (Digital Copy data discs, ISO 9660 carriers, etc.), use the bare common bullets plus a `**Structure:**` description and the rationale. Entry 47 (Rio Digital Copy) is the model.

## 6. Sibling cross-references (when applicable)

If the disc is obviously part of a set with an existing entry (multi-disc TV box, theatrical/extended pair, region variants of the same film), add a `**See also:**` bullet to *both* entries pointing at each other. Only do this when the connection is unambiguous — don't invent siblings from naming coincidence alone.

Existing examples:

- Entries 6 and 7 reference each other as the Suicide Squad theatrical/extended pair.
- Entries 8 and 9 reference each other as the Silicon Valley S1 Disc 1/Disc 2 pair.

## 7. Report to the user

Write one short message covering:

1. The new entry number and disc name.
2. The full matrix256v1 fingerprint.
3. The captured filesystem view in one line (e.g. `udf on /dev/sr0, source_kind=physical_disc`).
4. Anything notable: new-axis coverage in the corpus, unusual structure (pure BD-J, heavy decoys, etc.), or a pair/sibling link to an existing entry.

Then stop. **Do not commit.** The user reviews the working-tree diff and commits explicitly when they're ready.

## Notes and constraints

- `inspect_disc.py` is read-only against the disc. Don't `dd` or image the disc unless explicitly requested — the fingerprint doesn't need a local copy.
- Don't run `udisksctl loop-delete` or other teardown operations manually — `inspect_disc.py` handles mount/unmount internally.
- If `inspect_disc.py` fails (unreadable disc, missing tools, unexpected structure), report the error and leave `CORPUS.md` untouched.
- If the disc's matrix256v1 fingerprint already appears in `CORPUS.md`, point that out and ask the user whether to add a duplicate entry (a legitimate case if they're verifying reproducibility) or abort.
- Preserve the exact formatting of existing entries: checkmarks (✓/✗), em-dashes (—), middle dots (·), and bullet structure.

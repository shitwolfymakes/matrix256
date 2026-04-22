---
name: corpus-add
description: Inspect the optical disc currently loaded in the system's optical drive, compute its matrix256 fingerprint via inspect_disc.py, and append a new entry to CORPUS.md. Accepts an optional one-or-two-sentence "why it's here" rationale as arguments; if omitted, derives one from the disc's observable properties.
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

Run the project's existing inspection tool twice — once for metadata, once for fingerprint + file accounting:

```
python inspect_disc.py <device> --no-fingerprint
python inspect_disc.py <device> --no-metadata
```

Extract these fields:

- **Disc name** (from `Disc name:` in the Metadata block; for DVDs, use `Disc title:` or fall back to the udisks label if neither is helpful).
- **Disc type** — "Blu-ray" or "DVD-Video" (derive from the `Disc type:` line).
- **matrix256 fingerprint** (full 64-char SHA-256 from the `Fingerprint (SHA-256):` line).
- **AACS Disc ID** (from `Disc ID:` in the Metadata block; Blu-rays only; omit if absent).
- **Protection flags** (from `Protection:`; Blu-rays only — AACS/BD+/BD-J yes-or-no).
- **Title counts** (from `Title counts:`; Blu-rays only).
- **Main title** (from `Main title:`; Blu-rays only).
- **Files hashed** (the last numbered file in the "Files included in fingerprint" list — that count is also printed on the section header line as "N files").
- **Payload sizes** (from the "Files present but excluded by spec" block: the `STREAM/` size, and for Blu-rays also the `JAR/` and `BDJO/` sizes if non-zero and interesting).

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

Use 16 hex chars of the fingerprint (first 8 bytes).

## 5. Append a full entry section

Insert a new `## N. <Disc Name> (<Type>)` section immediately **before** the `## Reproducing a fingerprint` heading. Use the full disc name in the heading.

### Blu-ray layout

```markdown
## N. <Full Disc Name> (Blu-ray)

- **matrix256:** `<64-char SHA-256>`
- **AACS Disc ID:** `<40-char hex>`
- **Protection:** AACS <✓ or ✗>, BD+ <✓ or ✗>, BD-J <✓ or ✗>
- **Titles:** N HDMV + M BD-J (K "unsupported"); main title #X
- **Files hashed:** N
- **Payload:** NN GB STREAM[, M MB JAR][, P KB BDJO]  ← only list non-zero contributors
- **Why it's here:** <verbatim $ARGUMENTS, or an inferred rationale>
```

Omit the `AACS Disc ID` bullet if the disc didn't report one. Round payload sizes as shown in the script's output (the script already formats them sensibly).

### DVD layout

DVDs produce much less metadata, so use a trimmed template. Look at entry 2 (Sintel) for reference:

```markdown
## N. <Full Disc Name> (DVD-Video)

- **Source:** <if known, otherwise omit>
- **matrix256:** `<64-char SHA-256>`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** <verbatim $ARGUMENTS, or an inferred rationale>
```

## 6. Sibling cross-references (when applicable)

If the disc is obviously part of a set with an existing entry (multi-disc TV box, theatrical/extended pair, region variants of the same film), add a `**See also:**` bullet to *both* entries pointing at each other. Only do this when the connection is unambiguous — don't invent siblings from naming coincidence alone.

Existing examples:

- Entries 6 and 7 reference each other as the Suicide Squad theatrical/extended pair.
- Entries 8 and 9 reference each other as the Silicon Valley S1 Disc 1/Disc 2 pair.

## 7. Report to the user

Write one short message covering:

1. The new entry number and disc name.
2. The full fingerprint.
3. Anything notable: new-axis coverage in the corpus, unusual structure (pure BD-J, heavy decoys, etc.), or a pair/sibling link to an existing entry.

Then stop. **Do not commit.** The user reviews the working-tree diff and commits explicitly when they're ready.

## Notes and constraints

- `inspect_disc.py` is read-only against the disc. Don't `dd` or image the disc unless explicitly requested — the fingerprint doesn't need a local copy.
- Don't run `udisksctl loop-delete` or other teardown operations manually — `inspect_disc.py` handles mount/unmount internally.
- If `inspect_disc.py` fails (unreadable disc, missing tools, unexpected structure), report the error and leave `CORPUS.md` untouched.
- If the disc's fingerprint already appears in `CORPUS.md`, point that out and ask the user whether to add a duplicate entry (a legitimate case if they're verifying reproducibility) or abort.
- Preserve the exact formatting of existing entries: checkmarks (✓/✗), em-dashes (—), and bullet structure.

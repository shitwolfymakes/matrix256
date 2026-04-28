# matrix256: Reproducible Fingerprints for Optical Discs

**matrix256** is a reproducible SHA-256 fingerprint for optical discs and, more generally, for rooted filesystem trees. Given the same disc and the same filesystem view, any correct implementation produces a bit-identical digest regardless of operating system, reader hardware, or language runtime.

The name is an homage to the *matrix number* — the identifier etched into the metal stamper that presses every disc — with the `256` suffix pinning the hash function.

The current and only active version of the algorithm is **matrix256v1**. The normative specification is [`SPEC.md`](SPEC.md); the reference implementation is [`matrix256/v1.py`](matrix256/v1.py).

## Motivation

Metadata lookup services (TMDB, OMDB) key on titles and years entered by humans, which are lossy, language-specific, and ambiguous (region variants, extended editions, double-dips). Existing disc-level identifiers address parts of this:

- **MusicBrainz Disc ID** — SHA-1 of a normalized audio-CD TOC. A community standard for audio CDs.
- **pydvdid** — a CRC64 over DVD track layout. CRC64 has a small collision space; different pressings with identical track layouts collide.
- **AACS Disc ID / BD-J organization ID** — assigned identifiers stored on some Blu-ray discs. Identify a licensing or authoring group, not a specific structural encoding, and may be absent on homemade or open-content discs.

matrix256 defines a uniform SHA-256 fingerprint over a disc's filesystem layout — every regular file's path and size, canonically serialized — and produces the same digest for any standards-compliant filesystem view of that disc. The goal is a stable, reproducible identifier that:

- Is computed from filesystem metadata the disc itself carries, so the same disc always hashes to the same digest under the same view.
- Depends on no implementation choices that could change over time.
- Permits a many-to-one mapping from fingerprints to logical titles. Region variants, language variants, and special editions of the same title are expected to produce different fingerprints. That is a feature, not a bug: a community mapping layer resolves fingerprints to titles.

## Scope and non-goals

matrix256 applies to any optical disc that exposes a readable filesystem (DVD-Video, DVD-ROM, HD DVD, Blu-ray, UHD Blu-ray, Video CD, data discs, combo-pack supplementary discs) and to any rooted filesystem tree more generally. **Audio CDs** carry no filesystem and are out of scope; MusicBrainz Disc ID is the recommended companion identifier for catalogs that handle both.

Non-goals: tamper detection, per-byte content verification, robustness to disc damage, copy-protection bypass. matrix256 hashes filesystem metadata, not file contents — two discs with identical filesystem layouts but different bit-level video encodings produce the same fingerprint. In practice, mastering changes are almost always accompanied by structural changes, but the collision is possible and should be understood.

## Quickstart

Clone the repository and inspect a mounted disc, an ISO image, or a block device:

```
$ python inspect_disc.py /dev/sr0
Source:    /dev/sr0
Mount:     /media/user/MY_DISC
Disc type: bluray

Fingerprint (matrix256v1, SHA-256): 652e8189d14d260ea73e0e8e08848a455139e110b0655c56dd0cf42886f1499d

Submission metadata (filesystem view):
  Source kind:    physical_disc
  Filesystem:     udf
  Mount device:   /dev/sr0
  Mount options:  ro,nosuid,nodev,relatime,iocharset=utf8
  Reader:         inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic

Metadata (libbluray):
  Disc name:      BIG_BUCK_BUNNY
  ...
```

`inspect_disc.py` accepts a mount-point directory, an ISO file (loop-mounted via `udisksctl`), or a block device (e.g. `/dev/sr0`). Anything it mounts itself, it unmounts on exit. Flags: `--no-fingerprint` to skip hashing, `--no-metadata` to skip the lsdvd / bd_info / makemkv summary, `--json` for a machine-readable report.

For audio CDs, use a MusicBrainz Disc ID implementation (`libdiscid`, `python-discid`, or equivalent).

## Reference implementation (Python)

The full reference implementation is in [`matrix256/v1.py`](matrix256/v1.py). The core is small:

```python
import hashlib
import unicodedata
from pathlib import Path


def fingerprint(root: Path) -> str:
    records = []
    for p in root.rglob("*"):
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(root).as_posix()
        rel_nfc = unicodedata.normalize("NFC", rel)
        records.append((rel_nfc.encode("utf-8"), p.stat().st_size))
    records.sort(key=lambda r: r[0])
    h = hashlib.sha256()
    for path_bytes, size in records:
        h.update(path_bytes)
        h.update(b"\x00")
        h.update(str(size).encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()
```

The actual module handles symlinks, non-Unicode bytes, and error reporting per the spec — see `matrix256/v1.py` and [`SPEC.md`](SPEC.md) for the normative behavior.

## Documents in this repository

- [`SPEC.md`](SPEC.md) — **normative specification.** This is the source of truth.
- [`RATIONALE.md`](RATIONALE.md) — design rationale, prior-art comparison, why-not-X.
- [`IMPLEMENTERS.md`](IMPLEMENTERS.md) — practical guidance for implementers (bridge discs, encoding, mount handling, submission metadata).
- [`CORPUS.md`](CORPUS.md) — evaluation corpus of real discs with published `matrix256v1` digests.
- [`CONFORMANCE_FIXTURES.md`](CONFORMANCE_FIXTURES.md) — synthetic test suite for implementations: deterministic filesystem fixtures with expected digests, runnable in CI without external data.
- [`VENUES.md`](VENUES.md) — candidate publication venues for the spec.

## Repository tooling

The repo carries two stdlib-only Python files:

- [`matrix256/v1.py`](matrix256/v1.py) — the reference implementation, factored into a reusable submodule. Importing code addresses it as `from matrix256 import v1`.
- [`inspect_disc.py`](inspect_disc.py) — a CLI that mounts a disc (if needed), computes the matrix256v1 digest, and renders a MakeMKV-style metadata summary alongside the IMPLEMENTERS.md §5 submission view (source kind, filesystem driver, mount options, reader info). Useful for verifying spec compliance on real discs and for building an evaluation corpus.

## Copyright and DRM

matrix256 reads only filesystem metadata — file paths and file sizes — which are functional facts about how the disc is laid out. The video, audio, subtitle, and menu payloads are never read. AACS, CSS, BD+, and similar protection layers are never decrypted; no keys, libaacs, or libdvdcss are required to compute a fingerprint, because the filesystem layer that matrix256 reads is plaintext on every conformant optical disc by spec — the player itself needs that information to locate what to decrypt.

That distinction is the one that matters for DMCA §1201 and its international counterparts. matrix256 does not bypass any technological protection measure: the metadata it reads is the metadata the disc explicitly publishes to anyone who mounts it. The output is a one-way SHA-256 digest that cannot be reversed to reconstruct the disc, and the pre-hash records (paths like `VTS_01_1.VOB` and integer file sizes) are mechanical artifacts of the authoring tools rather than authored works.

This category of identifier has long-standing precedent. MusicBrainz Disc ID has computed and published TOC-derived hashes of audio CDs internationally for over two decades. AcoustID and Chromaprint do comparable things on the audio side. matrix256 sits in the same family: a hash of factual layout data, used as a stable key for community-curated metadata.

A catalog keyed on matrix256 digests can record and exchange information *about* a pressing — title, year, region, edition notes, errata — without reproducing or transmitting the disc itself. The fingerprint provides no path to playback, copying, or DRM defeat: knowing a disc's digest grants no access to its contents that the holder did not already have.

This section describes algorithm behavior, not legal conclusions. Operators of public lookup services should consult counsel for their jurisdiction.

## License

TBD. The specification and reference implementation will be released under a permissive open-source license once the spec is frozen.

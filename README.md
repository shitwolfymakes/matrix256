# matrix256: Reproducible Fingerprints for Optical Discs

**matrix256** is a reproducible SHA-256 fingerprint for optical discs (DVD-Video, Blu-ray) computed from disc-native bytes only. Given the same disc, any correct implementation of this specification produces the same digest, regardless of operating system, reader hardware, or language runtime. For audio CDs, matrix256 defers to the existing MusicBrainz Disc ID unchanged.

The name is an homage to the *matrix number* — the identifier etched into the metal stamper that presses every disc — with the `256` suffix pinning the hash function.

## Motivation

Metadata lookup services (TMDB, OMDB) key on titles and years entered by humans, which are lossy, language-specific, and ambiguous (region variants, extended editions, double-dips). Existing disc-level identifiers address parts of this:

- **MusicBrainz Disc ID** — SHA-1 of a normalized audio-CD TOC. A community standard for audio CDs.
- **pydvdid** — a CRC64 over DVD track layout. Fingerprint of the TOC structure, not of disc bytes. CRC64 has a small collision space; different pressings with identical track layouts collide.
- **VIDEO_TS / BDMV content hashes** — no widely-adopted standard exists.

This specification defines a uniform SHA-256 fingerprint over disc-native metadata bytes for DVD-Video and Blu-ray discs, and pins the existing MusicBrainz Disc ID for audio CDs. The goal is a stable, reproducible identifier that:

- Is computed from bytes the disc itself carries, so the same disc always hashes to the same digest.
- Depends on no implementation choices that could change over time.
- Permits a many-to-one mapping from fingerprints to logical titles. Region variants, language variants, and special editions of the same title are expected to produce different fingerprints. That is a feature, not a bug: a community mapping layer resolves fingerprints to titles.

## Goals and non-goals

**Goals**

- **Reproducibility.** A correct implementation in any language produces bit-identical digests for the same disc.
- **Disc-only input.** The fingerprint is a function of bytes on the disc; it does not depend on the reader, the host OS, the filesystem driver, or the implementing software version.
- **Structural identity, not content identity.** The fingerprint covers metadata structures (IFO, MPLS, CLPI, index.bdmv, MovieObject.bdmv), not the video payload itself. Hashing the full video payload is outside scope.
- **Publishable spec.** The algorithm is small enough to fit on one page and be reimplemented in an afternoon.

**Non-goals**

- Tamper detection. This fingerprint is not a cryptographic proof of disc contents; it is an identifier.
- Per-frame or per-byte content verification.
- Robustness to disc damage. A disc with unreadable sectors in a metadata file will not produce a meaningful fingerprint.
- Copy-protection bypass. The algorithm reads only unencrypted metadata structures that any standards-compliant reader can access.

## Algorithm

The fingerprint is the lowercase hex encoding of the SHA-256 digest of a byte stream assembled from specific files on the mounted disc, concatenated in a specified order with no separators.

### DVD-Video

Input: a DVD-Video disc with a readable `VIDEO_TS` directory.

1. Collect the following files from the `VIDEO_TS` directory, if present:
   - `VIDEO_TS.IFO`
   - `VTS_NN_0.IFO` for each title set, where `NN` ranges from `01` to `99`.
2. Sort the collected files in this exact order:
   - `VIDEO_TS.IFO` first.
   - Then `VTS_NN_0.IFO` in ascending numeric order of `NN`.
3. Concatenate the raw bytes of each file into a single byte stream. No separators, no framing, no length prefixes.
4. Compute the SHA-256 of the concatenated stream.

Files that do not exist on the disc are skipped. `.BUP` backup files are **not** included; they duplicate the IFO bytes and their inclusion would double-count identical content. VOB video payload files are **not** included; this is a structural fingerprint.

Filenames in the DVD-Video specification are uppercase. UDF is case-insensitive, but implementations that read the filesystem via a case-sensitive view must select uppercase filenames.

### Blu-ray

Input: a Blu-ray disc with a readable `BDMV` directory.

1. Collect the following files, if present:
   - `BDMV/index.bdmv`
   - `BDMV/MovieObject.bdmv`
   - All `BDMV/PLAYLIST/*.mpls`
   - All `BDMV/CLIPINF/*.clpi`
2. Sort in this exact order:
   - `BDMV/index.bdmv` first.
   - Then `BDMV/MovieObject.bdmv`.
   - Then every `.mpls` file in `BDMV/PLAYLIST`, lexicographically by filename.
   - Then every `.clpi` file in `BDMV/CLIPINF`, lexicographically by filename.
3. Concatenate the raw bytes of each file. No separators.
4. Compute the SHA-256 of the concatenated stream.

Blu-ray playlist and clip info files are zero-padded numeric filenames (`00000.mpls`, `00001.mpls`, …), so lexicographic ordering is equivalent to numeric ordering. No files from `BDMV/STREAM`, `BDMV/AUXDATA`, `BDMV/BDJO`, `BDMV/JAR`, or `BDMV/META` are included. Files in `BDMV/BACKUP` are not included; like DVD `.BUP` files, they duplicate primary data.

### Audio CD

Input: a Red Book audio CD.

The fingerprint **is** the MusicBrainz Disc ID, computed per the [MusicBrainz Disc ID Calculation specification](https://musicbrainz.org/doc/Disc_ID_Calculation). No ARM-specific hash is computed for audio CDs.

Rationale: audio CDs have no metadata files to hash. The MusicBrainz Disc ID is a SHA-1 of a canonical TOC layout, is already published as a community standard, and is already the key used by the largest community database for audio CDs. Introducing a parallel SHA-256 would fragment the ecosystem with no gain.

### Data discs and other optical media

Out of scope. Data discs carry arbitrary filesystem content and have no fixed metadata structure to fingerprint. Applications wishing to identify data discs can compute file-level hashes using conventional tools.

## Reference implementation (Python)

```python
import hashlib
from pathlib import Path


def dvd_fingerprint(mountpoint: Path) -> str:
    video_ts = mountpoint / "VIDEO_TS"
    files = []
    vmg = video_ts / "VIDEO_TS.IFO"
    if vmg.is_file():
        files.append(vmg)
    for nn in range(1, 100):
        vts = video_ts / f"VTS_{nn:02d}_0.IFO"
        if vts.is_file():
            files.append(vts)
    h = hashlib.sha256()
    for path in files:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 16), b""):
                h.update(chunk)
    return h.hexdigest()


def bluray_fingerprint(mountpoint: Path) -> str:
    bdmv = mountpoint / "BDMV"
    files = []
    for name in ("index.bdmv", "MovieObject.bdmv"):
        p = bdmv / name
        if p.is_file():
            files.append(p)
    files.extend(sorted((bdmv / "PLAYLIST").glob("*.mpls")))
    files.extend(sorted((bdmv / "CLIPINF").glob("*.clpi")))
    h = hashlib.sha256()
    for path in files:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 16), b""):
                h.update(chunk)
    return h.hexdigest()
```

For audio CDs, use any conforming implementation of MusicBrainz Disc ID (`libdiscid`, `python-discid`, or equivalent) and store the returned identifier verbatim.

## Rationale

**Why SHA-256.** SHA-256 is cryptographically sound, universally available in standard libraries, and produces a 256-bit digest with no realistic collision risk for any scale of disc catalog. CRC64 (as used by `pydvdid`) has a 64-bit space that is adequate for small catalogs but inappropriate for a community identifier. MD5 and SHA-1 are omitted; they carry collision risk with no offsetting benefit here.

**Why these files and not others.** The chosen files are the structural, disc-mastered metadata that define the playback experience: program chains, cell tables, stream attributes, region flags, playlist definitions, clip descriptors. They are small (a few hundred kilobytes total), present on every standards-compliant disc, and stable across playback software. Video payload files (VOB, M2TS) are deliberately excluded: they are large, their presence or absence in a hash would force implementations to read the entire disc, and their bit-level identity is captured indirectly through the structural metadata that references them.

**Why exclude backup files.** `VIDEO_TS.BUP`, `VTS_NN_0.BUP`, and `BDMV/BACKUP/*` are duplicates of the primary metadata files. Including them in the hash would double-count identical bytes and add nothing to the identifier's specificity.

**Why exclude format versioning.** An earlier draft of this specification included a `format_version` field alongside the digest so that the algorithm could be updated later without invalidating existing hashes. That field was removed: if the hash ever depends on implementation choices, the reproducibility property is lost. The file list and ordering are fixed for this version of the specification. Future revisions, if needed, will be defined as separate algorithms (e.g., a hypothetical `DiscFingerprint/v2`) and published alongside this one, not as a modification of it.

**Why many fingerprints per title is expected.** A theatrical release, a region A Blu-ray, a region B Blu-ray, a director's cut, and a special edition of the same film will typically each produce a distinct fingerprint. This is the intended behavior: the fingerprint identifies a specific disc edition, not an abstract title. The mapping from fingerprint to title is a separate, mutable, community-curated layer.

## Limitations

- **Disc damage.** Unreadable sectors inside a metadata file will either cause the read to fail or produce a digest over corrupted bytes. Implementations should fail loudly rather than silently emit a digest from partial data.
- **Non-standard discs.** Some homemade or non-commercial discs omit `MovieObject.bdmv`, include unusual file layouts, or use non-standard filename conventions. The algorithm produces a deterministic digest for any input that matches the shape defined here; discs that do not match this shape will produce digests that cannot be meaningfully compared to commercial disc fingerprints.
- **UHD Blu-ray.** This specification covers Blu-ray (BDMV) as commonly authored. UHD Blu-ray layouts are a superset; the algorithm as specified covers the files that exist in both formats and should produce stable digests for UHD discs, but formal coverage is pending verification against a range of UHD titles.
- **Not a content hash.** Two discs with identical metadata but different video encodings (different mastering passes of the same structural layout) would produce the same fingerprint. In practice this collision is rare because mastering changes are almost always accompanied by structural changes, but it is possible and should be understood.
- **Box sets and TV series.** Sibling discs in a TV-series box set often share title counts and generic per-title names (e.g. unnamed or numeric-only titles). The hashed metadata (IFO for DVD; index/MovieObject/MPLS/CLPI for Blu-ray) encodes per-disc sector offsets, chapter timings, and durations, so sibling discs are expected to produce distinct digests; empirical verification against a range of multi-disc box sets is pending.

## Prior art and related identifiers

- **MusicBrainz Disc ID** ([spec](https://musicbrainz.org/doc/Disc_ID_Calculation)) — SHA-1 of a normalized audio-CD TOC. This specification adopts it unchanged for audio CDs.
- **pydvdid** ([project](https://github.com/sjwood/pydvdid)) — CRC64 of DVD track layout derived from `VIDEO_TS.IFO`. Demonstrates the utility of a structural hash but uses a hash function with too small a collision space for a community-wide identifier.
- **libdvdread / libbluray** — the canonical open-source libraries for parsing DVD and Blu-ray metadata. Either can be used to implement the file reads in this specification, though direct filesystem access is sufficient.

## Repository tooling

Alongside the specification, this repository carries two small Python files that depend only on the standard library:

- `matrix256.py` — the reference implementation above, factored into a reusable module. The file-selection and hashing logic is byte-for-byte equivalent to the code block in [Reference implementation](#reference-implementation-python); either can be used to verify a third-party implementation.
- `inspect_disc.py` — a command-line tool that reports, for a mounted disc, which files would be fed into the fingerprint (in spec order, with sizes), which files are present but excluded (with the reason), and the resulting matrix256 digest. Intended for sanity-checking implementations and for surveying real discs.

Example:

```
$ python inspect_disc.py /media/user/MY_DISC
Mount:     /media/user/MY_DISC
Disc type: bluray

Files included in fingerprint (6 files, 1.2 MB):
    1. BDMV/index.bdmv               92 B
    2. BDMV/MovieObject.bdmv        256 B
    3. BDMV/PLAYLIST/00000.mpls   1.4 KB
    ...

Fingerprint (SHA-256): 647f526d79439f2cc13b0516ebed57a18dc0a6ceb8d985db99b7a52748375cd4
```

Flags: `--no-fingerprint` to skip hashing (selection only), `--json` for machine-readable output. Audio CDs are out of scope for this tool; use a MusicBrainz Disc ID implementation (`libdiscid`, `python-discid`, or equivalent).

## License

TBD. The specification and reference implementation will be released under a permissive open-source license once the first-version spec is frozen.

# matrix256 Specification

**Version:** 1
**Status:** Draft

matrix256 is a reproducible cryptographic fingerprint for optical discs. Given the same disc, any correct implementation of this specification produces a bit-identical SHA-256 digest regardless of operating system, reader, optical drive, or language runtime.

The name is an homage to the *matrix number* — the identifier etched into the metal stamper that presses every disc — with the `256` suffix pinning the hash function.

## 1. Scope

### 1.1 In scope

matrix256 applies to any optical disc that exposes a readable filesystem, including:

- DVD-Video and DVD-ROM
- HD DVD
- Blu-ray and UHD Blu-ray
- Video CD and Super Video CD
- Data discs on any of the above media
- Combo-pack supplementary discs (digital copy DVDs, bonus data discs)

More broadly, matrix256 applies to any rooted filesystem tree. The optical-disc framing reflects the primary intended use case, but nothing in the algorithm is specific to optical media or to any particular filesystem.

### 1.2 Out of scope

matrix256 does not apply to:

- **Audio CDs** (Red Book CDDA). Audio CDs carry no filesystem. The MusicBrainz Disc ID specification (https://musicbrainz.org/doc/Disc_ID_Calculation) is the established community identifier for audio CDs and is recommended as a complementary identifier alongside matrix256 in catalogs that handle both.
- **LaserDisc** and other analog optical media. These formats have no filesystem and cannot be fingerprinted by this specification.

### 1.3 Relationship to other identifiers

matrix256 does not replace or subsume:

- AACS Disc IDs (cryptographic, stored on some commercial Blu-ray discs)
- BD-J organization IDs (authored, stored in `CERTIFICATE/id.bdmv`)
- DVD catalog numbers, ISBNs, UPCs (assigned, printed on packaging)
- MusicBrainz Disc IDs (derived from audio CD TOCs)

These identifiers serve different purposes and may be recorded alongside matrix256 in any catalog.

### 1.4 Input precondition

matrix256 operates on a filesystem rooted at a path provided by the caller. The specification assumes the provided root is a successfully mounted, readable filesystem in which all file entries can be enumerated and have retrievable paths and sizes. Mounting, filesystem-view selection on multi-filesystem media (e.g., UDF/ISO 9660 bridge discs), and error handling for mount failures are outside the scope of this specification. Two implementations that walk different filesystem views of the same physical media will produce different (and individually correct) digests; reconciling such variation is the responsibility of the lookup or catalog layer that consumes matrix256 digests, not the algorithm itself.

## 2. Algorithm

The matrix256 digest of an optical disc is the SHA-256 hash of a canonically serialized listing of the disc's filesystem entries. The output is encoded as 64 lowercase hexadecimal characters.

### 2.1 Enumerate filesystem entries

Starting at the provided root, walk the filesystem and collect every **regular file** entry. Exclude:

- Directories (their presence is implicit in the paths of contained files).
- Symbolic links (not followed, not emitted).
- Other non-file entries (devices, sockets, FIFOs).

Include all regular file entries regardless of filesystem flags (hidden, system, archive).

### 2.2 Normalize paths

For each file entry, compute its path relative to the provided root. Each relative path:

1. Uses the forward slash `/` (U+002F) as the directory separator.
2. Contains no leading slash.
3. Preserves the case as presented by the filesystem.
4. Is normalized to Unicode Normalization Form C (NFC).
5. Is encoded as UTF-8 for serialization.

Paths that cannot be represented as valid Unicode are encoded as UTF-8 with the Unicode replacement character (U+FFFD, bytes `EF BF BD`) substituted for each invalid code unit.

### 2.3 Determine file size

For each file entry, use the size as reported by the filesystem. Implementations **must not** verify the size by reading or seeking through file contents; the reported size is authoritative.

### 2.4 Sort

Sort file entries by their UTF-8 encoded relative paths using byte-wise lexicographic comparison (equivalent to `memcmp`). No locale-aware, case-folded, or Unicode-collation-aware ordering is permitted.

### 2.5 Serialize

For each file entry in sorted order, emit:

```
<path-bytes> 0x00 <size-ascii> 0x0A
```

where:

- `<path-bytes>` is the UTF-8 encoded relative path from §2.2.
- `0x00` is a single null byte separator (one byte).
- `<size-ascii>` is the file size in bytes, written as base-10 ASCII digits (`0`–`9`) with no leading zeros. A size of zero is written as the single byte `0x30` (ASCII `0`).
- `0x0A` is a single line feed byte (one byte).

No other framing, length prefixes, or metadata are emitted. The concatenation of these per-entry records is the hash input.

### 2.6 Hash

Compute the SHA-256 digest of the concatenated serialization from §2.5.

Encode the digest as 64 lowercase hexadecimal characters with no whitespace, prefix, or suffix. This is the matrix256 digest.

### 2.7 Empty filesystems

A disc with a readable filesystem containing zero regular file entries produces a digest over an empty input:

```
matrix256(empty) = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

This is a valid digest. Implementations must not special-case empty filesystems as errors.

## 3. Error handling

Implementations must fail explicitly and must not produce a digest under any of the following conditions:

- A directory's contents cannot be read.
- A file entry's size or path cannot be retrieved from filesystem metadata.

matrix256 represents the full filesystem or no digest at all. Implementations must not produce a digest from a partial enumeration.

Damage to the bytes of a file's *contents* does not affect the digest, because file contents are not read.

## 4. Conformance

An implementation is conformant if, for every disc or disc image in the matrix256 conformance corpus, it produces a digest bit-identical to the corpus's published value.

The conformance corpus is published alongside this specification and includes:

- Open-content discs (Big Buck Bunny, Sintel, and others) with ISO images freely downloadable from their publishers.
- Test vectors for filesystem edge cases: Unicode filenames, UDF/ISO 9660 bridge discs, AACS-protected Blu-rays, HD DVD layouts.

Third-party implementations are encouraged to publish their own test vectors and cross-validate against other implementations.

## 5. Versioning

This specification is **matrix256 version 1**. The version number identifies this specification; it is not embedded in the digest.

Future specification versions, if defined, will be given distinct names (e.g., `matrix256v2`) and will produce distinct digests. This specification's digests remain stable regardless of future versions.

Implementations that must disambiguate between specification versions should do so at the application or protocol layer (database column, API response field, URI path), not within the digest string itself.

## 6. Reference implementation

A Python reference implementation is distributed alongside this specification. It depends only on the Python standard library and operates on any filesystem path the host OS can present.

The reference implementation is authoritative for conformance testing: an implementation is conformant if and only if it produces identical digests to the reference for every disc in the conformance corpus.

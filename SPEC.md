# matrix256 Specification

**Version:** 1.0
**Status:** Draft

matrix256 is a reproducible cryptographic fingerprint for optical discs. Given the same disc, any correct implementation of this specification produces a bit-identical SHA-256 digest regardless of operating system, reader, optical drive, or language runtime.

The name is an homage to the *matrix number* — the identifier etched into the metal stamper that presses every disc — with the `256` suffix pinning the hash function.

## 1. Scope

### 1.1 In scope

matrix256 applies to any optical disc that exposes a readable filesystem, including:

- DVD-Video and DVD-ROM (UDF, ISO 9660, or UDF/ISO bridge)
- HD DVD (UDF 2.50)
- Blu-ray and UHD Blu-ray (UDF 2.50)
- Video CD and Super Video CD (ISO 9660)
- Data discs on any of the above media
- Combo-pack supplementary discs (digital copy DVDs, bonus data discs)

### 1.2 Out of scope

matrix256 does not apply to:

- **Audio CDs** (Red Book CDDA). Audio CDs carry no filesystem. The MusicBrainz Disc ID specification (https://musicbrainz.org/doc/Disc_ID_Calculation) is the established community identifier for audio CDs and is recommended as a complementary identifier alongside matrix256 in catalogs that handle both.
- **LaserDisc** and other analog optical media. These formats have no filesystem and cannot be fingerprinted by this specification.
- **Non-optical storage.** matrix256 is defined for optical discs only.

### 1.3 Relationship to other identifiers

matrix256 does not replace or subsume:

- AACS Disc IDs (cryptographic, stored on some commercial Blu-ray discs)
- BD-J organization IDs (authored, stored in `CERTIFICATE/id.bdmv`)
- DVD catalog numbers, ISBNs, UPCs (assigned, printed on packaging)
- MusicBrainz Disc IDs (derived from audio CD TOCs)

These identifiers serve different purposes and may be recorded alongside matrix256 in any catalog.

## 2. Algorithm

The matrix256 digest of an optical disc is the SHA-256 hash of a canonically serialized listing of the disc's filesystem entries. The output is encoded as 64 lowercase hexadecimal characters.

### 2.1 Enumerate filesystem entries

Walk the disc's filesystem starting at the mount root. Collect every **regular file** entry. Exclude:

- Directories (directory entries are not emitted; their presence is implicit in the paths of contained files).
- Symbolic links (not followed, not emitted as entries).
- Other non-file entries (devices, sockets, FIFOs).

Include all regular file entries regardless of filesystem flags (hidden, system, archive).

**Bridge discs.** On discs that expose both UDF and ISO 9660 views of the same underlying data, use the UDF view. On ISO 9660 discs with Joliet or Rock Ridge extensions, use the extended view that surfaces full-length filenames.

### 2.2 Normalize paths

For each file entry, compute its path relative to the mount root.

Each relative path:

1. Uses the forward slash `/` (U+002F) as the directory separator.
2. Contains no leading slash.
3. Preserves the case as stored in the filesystem.
4. Is decoded from the filesystem's native encoding to Unicode per the applicable filesystem specification (ECMA-167 / OSTA UDF for UDF filesystems; ISO 9660 with Joliet or Rock Ridge extensions as applicable).
5. Is normalized to Unicode Normalization Form C (NFC).
6. Is encoded as UTF-8 for serialization.

Filesystem-native filenames that cannot be decoded as valid Unicode are encoded as UTF-8 with the Unicode replacement character (U+FFFD, bytes `EF BF BD`) substituted for each invalid code unit.

### 2.3 Determine file size

For each file entry, use the size as stored in the filesystem metadata:

- UDF: the Information Length field of the File Entry or Extended File Entry descriptor.
- ISO 9660: the Data Length field of the directory record.

Implementations **must not** verify the size by reading or seeking through file contents. The declared size is authoritative.

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

- The disc's filesystem cannot be mounted or enumerated.
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

This specification is **matrix256 version 2**. The version number identifies this specification; it is not embedded in the digest.

Future specification versions, if defined, will be given distinct names (e.g., `matrix256/3`) and will produce distinct digests. This specification's digests remain stable regardless of future versions.

Implementations that must disambiguate between specification versions should do so at the application or protocol layer (database column, API response field, URI path), not within the digest string itself.

## 6. Reference implementation

A Python reference implementation is distributed alongside this specification. It depends only on the Python standard library and on a user-selected UDF/ISO 9660 reader.

The reference implementation is authoritative for conformance testing: an implementation is conformant if and only if it produces identical digests to the reference for every disc in the conformance corpus.

## 7. Test vector

For a hypothetical disc whose filesystem contains exactly two files:

```
BDMV/index.bdmv                92 bytes
BDMV/MovieObject.bdmv         256 bytes
```

The serialized input to SHA-256 is (hex):

```
42 44 4D 56 2F 69 6E 64 65 78 2E 62 64 6D 76     "BDMV/index.bdmv"
00                                                NUL
39 32                                             "92"
0A                                                LF
42 44 4D 56 2F 4D 6F 76 69 65 4F 62 6A 65 63     "BDMV/MovieObjec
74 2E 62 64 6D 76                                 t.bdmv"
00                                                NUL
32 35 36                                          "256"
0A                                                LF
```

Total: 48 bytes. Conforming implementations are expected to verify the SHA-256 of this input as part of their test suite.

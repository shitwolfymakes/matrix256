# matrix256v1 Conformance Fixtures

**Status:** non-normative companion to [`SPEC.md`](SPEC.md). The specification is the source of truth. Where this document and the spec disagree, this document is the bug.

This file defines a portable test suite for matrix256v1 implementations. Each fixture is a deterministic filesystem state that any implementation can construct locally at test time, then hash with its own `fingerprint` function. The expected digest is published here. An implementation passes the suite if it produces the documented digest for every fixture it can construct on its target platform.

The fixtures cover the algorithmic surface area of matrix256v1 — path normalization, byte-wise sort, serialization, edge cases — without depending on real optical media. Together with the two open-content corpus entries (Sintel and Big Buck Bunny in [`CORPUS.md`](CORPUS.md)) they form the publishable conformance bar that runs in continuous integration without external data dependencies.

## Conformance tiers

The conformance architecture has three tiers, in increasing order of fidelity to real-world inputs and decreasing order of portability:

- **Tier 1 — synthetic fixtures (this document).** Constructed in a temporary directory by the test runner. No external data. Runs unattended in CI on any platform that supports the fixture's filesystem features. Exercises the algorithm in isolation.
- **Tier 2 — open-content corpus entries.** The Sintel and Big Buck Bunny ISO images published by the Blender Foundation under permissive open-content licenses, with their digests recorded in [`CORPUS.md`](CORPUS.md). Downloadable in CI; verifies that the algorithm composes correctly with a real ISO 9660/UDF filesystem walk.
- **Tier 3 — full corpus.** The complete [`CORPUS.md`](CORPUS.md) entries, the bulk of which are commercial pressings whose ISO images cannot be redistributed. Runs only on machines that own the physical media. Verifies the algorithm against the full diversity of real-world disc structures.

A new implementation should reach Tier 1 first (this document), then Tier 2 (the two open-content discs), and only then reach for Tier 3 if the implementer has access to the relevant pressings.

## How to use this document

For each fixture listed below:

1. Construct the described filesystem state in an empty directory.
2. Run your implementation's `fingerprint` function against that directory.
3. Compare the output to the expected digest in this document.

Equality (case-insensitive over hex characters, though the spec mandates lowercase) is the pass criterion. Any deviation indicates a divergence from the spec.

Fixture construction is also implemented end-to-end in [`generate_fixtures.py`](generate_fixtures.py), which runs the Python reference implementation against each fixture and reports pass/fail. Implementers in other languages can read that script as the canonical specification of fixture construction, since the prose construction descriptions below are necessarily less precise than executable code.

## Portability requirements

Every fixture is designed to be reproducible across operating systems and filesystems. Specifically:

- **Paths.** Forward slashes and POSIX semantics. Implementations on filesystems that disallow specific path characters (e.g., NTFS forbids `:` and `<` in filenames) should construct fixtures using the documented codepoints; if a codepoint is unrepresentable on the target filesystem, the fixture is incompatible with that platform and should be skipped.
- **File contents.** Specified as exact byte sequences (in hex) where they matter. Filenames are specified as exact codepoint sequences with explicit `U+XXXX` notation. No ambiguity from glyph rendering or text-editor normalization.
- **Filesystem feature dependencies.** Some fixtures depend on platform features that are not universally available — symlinks (Windows requires elevated permissions), case sensitivity (HFS+ default is case-insensitive), non-UTF-8 filenames (POSIX-only). These dependencies are called out per fixture; an implementation may skip an incompatible fixture without forfeiting conformance, but the skip must be reported.
- **Cleanup.** Each fixture should be constructed in a fresh, empty directory. Re-using a directory across fixtures will produce wrong digests because residual state contributes records.

## Fixtures

Twenty-five fixtures, every digest produced by the Python reference implementation in [`matrix256-py`](https://github.com/shitwolfymakes/matrix256-py) at `matrix256.v1`.

### Fixture 1 — empty directory

**Purpose.** Verify empty-input handling per [`SPEC.md`](SPEC.md) §2.7.

**Construction.** A directory with no entries.

**Expected matrix256v1 digest.**

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

**Notes.** This is the SHA-256 of the empty byte string. The fixture confirms that an implementation does not special-case empty filesystems as errors.

### Fixture 2 — single zero-byte file

**Purpose.** Single-record digest with size 0.

**Construction.** One regular file at relative path `a` (one byte: `0x61`) with size zero.

**Expected matrix256v1 digest.**

```
576ada568edb673473287643d06ca9b763d81b712a080388fbf445bf580dab3d
```

**Notes.** Verifies that size 0 is serialized as the single ASCII byte `0` (`0x30`), not as an empty string and not as `00`. The hash input is exactly `61 00 30 0A` (four bytes).

### Fixture 3 — single small ASCII file

**Purpose.** Single-record digest with non-zero size.

**Construction.** One regular file at relative path `hello.txt` with contents `68 65 6C 6C 6F 0A` (the ASCII string `hello\n`, 6 bytes).

**Expected matrix256v1 digest.**

```
00c8e12fff1075e74071d424a34ec9e89e2ffc96c5c4ec6a5bf7a3b5941b3324
```

**Notes.** Only the size matters to the digest, not the content. Implementations that hash file bytes are out of spec.

### Fixture 4 — two files at root

**Purpose.** Trivial sort over two empty files.

**Construction.** Two zero-byte regular files at relative paths `a` and `b`.

**Expected matrix256v1 digest.**

```
a7cde029efe3b62bb536d2eead4b0900409eea281230c0e1146dd0db645a2042
```

### Fixture 5 — case-sensitive sort

**Purpose.** Verify ASCII sort treats uppercase and lowercase as distinct.

**Construction.** Two zero-byte regular files at relative paths `A` (`0x41`) and `a` (`0x61`).

**Expected matrix256v1 digest.**

```
e99dec2b961d71942f740d942301fdb9e1268eeca6b21161dfaf5b7c253ed660
```

**Notes.** On case-insensitive filesystems (legacy HFS+, NTFS in default mode, FAT32) only one of the two files can exist; the fixture is undefined there. Run on a case-sensitive filesystem (ext4, APFS, NTFS configured case-sensitive, ZFS) or skip.

### Fixture 6 — slash vs dash sort edge case

**Purpose.** Verify byte-wise sort places `a-b` before `a/b`. The hyphen byte (`0x2D`) is less than the forward-slash byte (`0x2F`).

**Construction.** Two zero-byte regular files: one named `a-b` at the root, and one named `b` inside a subdirectory `a` (relative path `a/b`).

**Expected matrix256v1 digest.**

```
82d1301cbc45799e538f19a52840b9ff5a9ca797d80c5e52b4d98c4750d2b5e3
```

**Notes.** A naive implementation that sorts on path components rather than on the full UTF-8 byte string will get this wrong: per-component sorting groups `a/b` under the `a` subtree before any sibling at the root, which is incorrect under matrix256v1.

### Fixture 7 — nested directories

**Purpose.** Verify directories themselves are not emitted, but their paths are implicit in the relative paths of contained files.

**Construction.** One zero-byte regular file at relative path `dir1/dir2/file.txt`.

**Expected matrix256v1 digest.**

```
8f2c64be52e682809a97f2e370a2638c10e3c3f9071eaa0bda3f7fc4c6c6eccb
```

**Notes.** Implementations that emit a record for `dir1` or `dir1/dir2` will diverge.

### Fixture 8 — sibling directories sort by full path

**Purpose.** Verify the sort key is the full UTF-8 path, not per-component or per-depth.

**Construction.** Two zero-byte regular files at relative paths `a/z` and `b/a`.

**Expected matrix256v1 digest.**

```
ab44545fa7095c239cd8e9fa36eff237b1cc8e32c5126e98591b24250aa11871
```

**Notes.** `a/z` (UTF-8: `61 2F 7A`) sorts before `b/a` (UTF-8: `62 2F 61`) because the first byte differs. An implementation that sorts by directory and then by leaf name will agree by coincidence here, but a careful implementer should still verify the sort key is the full byte string.

### Fixture 9 — only an empty subdirectory

**Purpose.** Verify that a tree containing directories but no files produces the empty digest.

**Construction.** A directory containing exactly one entry: an empty subdirectory at relative path `empty/`.

**Expected matrix256v1 digest.**

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

**Notes.** Should match Fixture 1 exactly. Empty subdirectories alone produce no records.

### Fixture 10 — file plus an empty subdirectory

**Purpose.** Verify empty subdirectories alongside files do not perturb the digest.

**Construction.** Same as Fixture 3 (`hello.txt` with `hello\n` content), plus an empty subdirectory at relative path `empty/`.

**Expected matrix256v1 digest.**

```
00c8e12fff1075e74071d424a34ec9e89e2ffc96c5c4ec6a5bf7a3b5941b3324
```

**Notes.** Should match Fixture 3 exactly. The empty subdirectory contributes no record and must not change the result. Implementations that emit a record for `empty/` (or even just keep it in the sort) will diverge.

### Fixture 11 — only a symlink

**Purpose.** Verify symlinks are skipped per [`SPEC.md`](SPEC.md) §2.1, not followed.

**Construction.** A directory containing exactly one entry: a symbolic link `link` whose target is the literal string `nonexistent` (a dangling symlink).

**Expected matrix256v1 digest.**

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

**Notes.** Should match Fixture 1's empty digest. The symlink target is intentionally nonexistent so that any implementation that mistakenly follows the link will fail loudly with a stat error rather than silently re-hash the symlink target. **Platform requirement:** symlinks. POSIX implementations have them by default; Windows requires elevated permissions or developer mode. Skip on platforms without symlink support.

### Fixture 12 — symlink alongside a file

**Purpose.** Verify a symlink is skipped while a sibling regular file is hashed normally.

**Construction.** A directory containing two entries: a regular file at relative path `real.txt` with contents `78` (one byte, ASCII `x`), and a symbolic link `link` whose target is the literal string `real.txt`.

**Expected matrix256v1 digest.**

```
1f99a83be1c9ac0d243b7937f15908a03ede98ffa24c18fcf6100fca66506df4
```

**Notes.** The symlink target exists; an implementation that follows symlinks will emit a second record (for `link`, with size 1) and produce a different digest. **Platform requirement:** symlinks.

### Fixture 13 — Latin diacritics, NFC source

**Purpose.** Non-ASCII filename in already-NFC form.

**Construction.** One zero-byte regular file at relative path `café.txt`, where the filename codepoints are `U+0063 U+0061 U+0066 U+00E9 U+002E U+0074 U+0078 U+0074` (precomposed `é`).

**Expected matrix256v1 digest.**

```
afd2f606ae4f4e4d644cbb28ab2f1c5d46d6f98130304efd9941db17d6a91dcd
```

### Fixture 14 — Latin diacritics, NFD source

**Purpose.** Verify normalization to NFC before sorting and hashing.

**Construction.** One zero-byte regular file at relative path `café.txt`, where the filename codepoints are `U+0063 U+0061 U+0066 U+0065 U+0301 U+002E U+0074 U+0078 U+0074` — that is, `c` `a` `f` `e` followed by combining acute (`U+0301`), then `.txt`. NFD form.

**Expected matrix256v1 digest.**

```
afd2f606ae4f4e4d644cbb28ab2f1c5d46d6f98130304efd9941db17d6a91dcd
```

**Notes.** Should produce **the same digest as Fixture 13.** This is the central NFC-normalization test: filesystems that store the bytes as written (APFS, ext4, NTFS) will hand the implementation the NFD form, and the implementation must normalize to NFC before hashing. **Platform exception:** legacy HFS+ auto-normalizes on write and cannot host this fixture as written; the file as stored will already be NFC. APFS, ext4, and NTFS are all suitable.

### Fixture 15 — Cyrillic filename

**Purpose.** Non-Latin script in filename.

**Construction.** One zero-byte regular file at relative path `привет.txt`, where the filename codepoints are `U+043F U+0440 U+0438 U+0432 U+0435 U+0442 U+002E U+0074 U+0078 U+0074`.

**Expected matrix256v1 digest.**

```
c044182349eea94dff66a1ce2764e6f809cbf8893b2071d5906203b41fea21c0
```

### Fixture 16 — Han filename

**Purpose.** CJK ideographs in filename.

**Construction.** One zero-byte regular file at relative path `你好.txt`, where the filename codepoints are `U+4F60 U+597D U+002E U+0074 U+0078 U+0074`.

**Expected matrix256v1 digest.**

```
339e0893d9d4aa8df81e9e7d671983f7befa124bd86416dc69697c32d8112787
```

### Fixture 17 — Arabic filename

**Purpose.** RTL script in filename.

**Construction.** One zero-byte regular file at relative path `مرحبا.txt`, where the filename codepoints are `U+0645 U+0631 U+062D U+0628 U+0627 U+002E U+0074 U+0078 U+0074`.

**Expected matrix256v1 digest.**

```
9ec64191ddf011278744183c8830b3b7e7c6f35fbff37c66122f0ae0e7add033
```

**Notes.** The stored byte order on disk is logical, not visual. The matrix256v1 sort operates on the logical byte order. Glyph rendering of the filename in a terminal or text editor is irrelevant.

### Fixture 18 — emoji filename

**Purpose.** Supplementary-plane codepoint in filename, exercising four-byte UTF-8.

**Construction.** One zero-byte regular file at relative path `🎵.txt`, where the filename codepoints are `U+1F3B5 U+002E U+0074 U+0078 U+0074`. The `U+1F3B5` codepoint encodes as four UTF-8 bytes (`F0 9F 8E B5`).

**Expected matrix256v1 digest.**

```
7c547ce5b89040b67d9cbf5c2ec5556090fdcfa8f3120b48a856c054769b7816
```

### Fixture 19 — multi-script directory

**Purpose.** Stable sort across mixed scripts.

**Construction.** Four zero-byte regular files at the following relative paths, each a single component:

- `ascii.txt` (UTF-8 first byte: `0x61`)
- `café.txt` in NFC form (UTF-8 first byte: `0x63`)
- `你好.txt` (UTF-8 first byte: `0xE4`)
- `🎵.txt` (UTF-8 first byte: `0xF0`)

**Expected matrix256v1 digest.**

```
b7ce4f0d4e8cde3698b11edc79c49639b3f04cf88e128b0f1c3f0951843f7966
```

**Notes.** The sort order under matrix256v1 byte-wise comparison is `ascii.txt`, `café.txt`, `你好.txt`, `🎵.txt`, governed by the first differing UTF-8 byte. A locale-aware sort (e.g., `strcoll`) will produce a different order on most systems and will fail this fixture.

### Fixture 20 — size boundaries

**Purpose.** Verify ASCII size encoding across decimal-digit count boundaries.

**Construction.** Seven regular files, all at the root, each filled with null bytes (`0x00` repeated). The relative path of each file embeds its size in zero-padded form so sort order is fully deterministic regardless of size:

| Relative path     | Size (bytes) |
|-------------------|-------------:|
| `size_0000000`    | 0            |
| `size_0000001`    | 1            |
| `size_0000255`    | 255          |
| `size_0000256`    | 256          |
| `size_0065535`    | 65535        |
| `size_0065536`    | 65536        |
| `size_1000000`    | 1000000      |

**Expected matrix256v1 digest.**

```
ac2ee75612a4d578fe365711b2f8aef71e40b2f8c2abf212fa26308d857160e6
```

**Notes.** The serialization writes sizes as decimal ASCII with no leading zeros. Each digit-count boundary (1→2, 2→3, 3→4 digits, etc.) is exercised. File contents are null bytes for reproducibility, but only sizes affect the digest.

### Fixture 21 — many small files

**Purpose.** Sort stability under volume.

**Construction.** 100 zero-byte regular files at the root, named `f000`, `f001`, …, `f099` (three-digit zero-padded suffix).

**Expected matrix256v1 digest.**

```
a164865515f0f66b25cc4aff36e558a602d3db6caf62d41d1e830f9283b3dc8f
```

**Notes.** Catches implementations that rely on filesystem-return order (which is unspecified across filesystems) or that use a sort whose results depend on input order (an unstable sort is fine here because keys are unique, but an order-dependent comparator would fail).

### Fixture 22 — deeply nested file

**Purpose.** Verify deep recursion.

**Construction.** One zero-byte regular file at relative path `a/b/c/d/e/f/g/h/i/j/file.txt` — ten directory levels above the file. Path is 28 bytes UTF-8.

**Expected matrix256v1 digest.**

```
35997ed41f132aad8afc1e08a577090dff4aaa7bb23ffe5f874e879fbc38475f
```

**Notes.** Catches implementations with a shallow recursion limit or that track depth in a way that overflows on real disc structures (commercial Blu-rays nest several layers under `BDMV/`).

### Fixture 23 — long filename

**Purpose.** Verify long-name encoding.

**Construction.** One zero-byte regular file at the root whose filename is `a` (`U+0061`) repeated 200 times.

**Expected matrix256v1 digest.**

```
31013f1f14b4c55273b923a96047c43e157423625160c53dad1f7971de44db58
```

**Notes.** Stays within the 255-byte component limit on ext4, APFS (NAME_MAX 255), and NTFS (255 UTF-16 units). Filesystems that impose tighter limits (FAT32 short name without LFN, ISO 9660 Level 1) cannot host this fixture.

### Fixture 24 — surrogate-escape filename byte

**Purpose.** Verify U+FFFD substitution per [`SPEC.md`](SPEC.md) §2.2 for paths that cannot be represented as valid Unicode.

**Construction.** One zero-byte regular file at the root whose filename, as raw bytes, is `62 61 64 FF 2E 74 78 74` — the ASCII string `bad`, then the byte `0xFF`, then `.txt`. The byte `0xFF` is not a valid UTF-8 start byte, so the filename is not valid UTF-8 as stored.

**Expected matrix256v1 digest.**

```
8392ec1f2dec1510d58ade51d070394768a4fbbe917c677387901f1147dd439a
```

**Notes.** When the implementation walks the filesystem, the invalid byte must be replaced with the U+FFFD replacement character (UTF-8: `EF BF BD`) before hashing. The hashed path bytes are therefore `62 61 64 EF BF BD 2E 74 78 74` (10 bytes). **Platform requirement:** Linux. The fixture depends on filesystems that store filenames as raw byte strings (POSIX) and on the convention that a path byte outside valid UTF-8 should be substituted (rather than error). macOS APFS rejects non-UTF-8 filenames at creation time, and Windows uses UTF-16 throughout; on those platforms this fixture cannot be constructed and should be skipped.

### Fixture 25 — prefix and trailing-character sort

**Purpose.** Verify shorter-prefix-first byte-wise sort.

**Construction.** Three zero-byte regular files at the root with the relative paths `foo`, `foo.txt`, and `foobar`.

**Expected matrix256v1 digest.**

```
599b5d5fd9d52740c6b40f134b260b52de60bed70ee60aa0536ee8474fc65bcc
```

**Notes.** Sort order under byte-wise comparison: `foo` (a prefix of the others, sorts first), then `foo.txt` (next byte after `foo` is `.` = `0x2E`), then `foobar` (next byte after `foo` is `b` = `0x62`). Catches implementations that sort component-wise (treating `.txt` as a separate token), that strip extensions, or that use a comparison function that misorders proper prefixes.

## Implementation guidance

To wire this suite into a non-Python implementation:

1. **Implement a fixture-construction helper in your language.** It should produce the same on-disk state as the corresponding entry in [`generate_fixtures.py`](generate_fixtures.py). The Python script is the canonical reference for any case where this document's prose is ambiguous.
2. **Run your `fingerprint` function against each constructed fixture.**
3. **Compare each produced digest against the expected digest in this document.** Equality is the pass criterion.
4. **Wire the suite into your CI.** This becomes the implementation's Tier 1 conformance test: it runs unattended on every commit, has no external data dependencies, and proves the algorithmic core matches the spec without needing access to the full corpus.
5. **Skip rather than work around incompatible fixtures.** If a fixture depends on a platform feature your CI environment doesn't have (Windows symlinks, Linux-only surrogate-escape, case-sensitive filesystems on default macOS), report a skip rather than mutate the fixture. A skip is a known limitation; a silent workaround is a divergence.

After Tier 1 passes, add the two open-content corpus entries (Sintel, Big Buck Bunny) from [`CORPUS.md`](CORPUS.md) as Tier 2 tests if your CI can download Blender Foundation ISO images. Tier 3 is local-only.

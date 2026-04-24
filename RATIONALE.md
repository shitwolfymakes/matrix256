# matrix256: Design Rationale

Companion document to the matrix256 specification. This document explains the design decisions, empirical findings, and prior art that shaped the specification. It is non-normative: in case of any conflict between this document and the specification, the specification governs.

## 1. The problem

Optical disc catalogs — archival libraries, media servers, ripping pipelines, preservation databases — need to answer a deceptively simple question: *is this disc the same as that one?*

"Same" has multiple meanings, each with its own answer:

1. **Same title.** "Is this a copy of *Casablanca*?" Best answered by human-curated metadata sources (IMDB, TMDB, OMDB) keyed by title strings.
2. **Same release.** "Is this the 2012 Warner Home Video Blu-ray of *Casablanca* for Region A?" Answered by release-level identifiers: catalog numbers, UPCs, ISBNs.
3. **Same pressing.** "Is this disc byte-identical, at the structural level, to that one?" Answered by content-addressable fingerprints computed from the disc itself.

matrix256 addresses the third question. It is not a title identifier. It is not a release identifier. It is not a substitute for human-curated metadata. It is a reproducible cryptographic identity for a specific physical pressing.

## 2. Why existing identifiers are insufficient

### 2.1 Title-level metadata (IMDB, TMDB, OMDB)

These services answer "what film is this?" but not "which pressing of that film?" A director's cut and a theatrical cut share the same IMDB ID. Region A and Region B Blu-rays of the same film share the same TMDB ID. Two physically distinct pressings with different VOB sizes are indistinguishable at the title layer.

Title metadata is also lossy: entered by humans, language-dependent, ambiguous for re-releases and special editions, unavailable for obscure pressings no one has catalogued.

### 2.2 AACS Disc IDs

Commercial Blu-ray discs carry a 20-byte AACS Disc ID assigned during mastering. Where present, this is a strong per-pressing identifier — but:

- It requires libaacs and AACS keys to read, which are licensing-restricted.
- It is absent on homemade and open-content discs.
- It is absent on DVD-Video entirely.
- Different pressings can share AACS Disc IDs when authored under the same AACS volume.

AACS Disc IDs are valuable metadata to record alongside matrix256, but they cannot serve as the universal identifier.

### 2.3 pydvdid / CRC64

The pydvdid algorithm is the closest prior art. It computes a 64-bit CRC over a small subset of DVD-Video metadata: filename listing, file sizes, the first 64 KB of specific IFO files, and UDF creation timestamps. It was originally reverse-engineered from Microsoft's `IDvdInfo2::GetDiscID` Windows API, which Windows Media Center used to identify DVDs for its metadata service.

pydvdid is valuable prior art but has three structural problems:

1. **Collision space.** 64 bits is inadequate for a global community identifier. At scale — millions of pressings across the history of commercial DVD — birthday-bound collisions are realistic.

2. **Windows API dependency.** The algorithm was reverse-engineered, not specified. When Microsoft silently changed the algorithm in Windows 10/11 (processing only a subset of the original file list), existing pydvdid implementations diverged from the new Windows behavior, producing a "win7" versus "win10" split that has not been resolved.

3. **DVD-only.** pydvdid does not define behavior for Blu-ray, HD DVD, or any other optical format.

The lookup service pydvdid was designed against — `metaservices.windowsmedia.com` — has been offline since Windows Media Center was discontinued in 2015. The Automatic Ripping Machine project's own CRC64 database (`1337server.pythonanywhere.com`) carries the flame, but it runs on one maintainer's free-tier PythonAnywhere account with no public data dump.

### 2.4 MusicBrainz Disc ID

For audio CDs, MusicBrainz Disc ID is the community-standard identifier: a SHA-1 over a normalized TOC layout, published at https://musicbrainz.org/doc/Disc_ID_Calculation. It is well-specified, widely implemented, and backed by a large community database.

matrix256 does not attempt to replace MusicBrainz Disc ID for audio CDs. The two identifiers are complementary: MusicBrainz Disc ID for audio CDs, matrix256 for filesystem-based optical media, used alongside each other in any catalog that handles both.

## 3. Design principles

### 3.1 Reproducibility above all else

A fingerprint that produces different digests for the same disc on different systems is not a fingerprint. Every design decision in the specification trades expressive power for reproducibility.

This means:

- **No timestamps.** UDF timestamp handling varies across readers. The win7/win10 split in pydvdid is exactly this failure mode. matrix256 reads no timestamps.
- **No filesystem-layer metadata that varies by reader.** Permissions, ownership, link counts, extended attributes — none of these are included, because optical media readers synthesize them inconsistently.
- **No locale-aware operations.** Sort order is byte-wise lexicographic. String comparison is byte equality.
- **No implementation-dependent byte selection.** matrix256 does not read specific offsets within files, does not interpret file contents, and does not parse any on-disc structure beyond what the filesystem reader already does.

### 3.2 Disc-native input only

The fingerprint is a function of bytes on the disc. It does not depend on the reader software, the host operating system, the optical drive, the mount options, or the implementing programming language.

Different readers may retrieve different bytes for file *contents* — but file contents are not part of matrix256's input. The filesystem *metadata* (filenames, sizes, tree structure) is stable across readers because it is stored as small, well-defined integer fields in specified positions of the filesystem's descriptors.

### 3.3 Structural identity, not content identity

matrix256 identifies a pressing by its file tree, not by its video or audio contents. Two discs with identical filesystems but different video encodings would produce the same digest.

This is a deliberate trade-off. Hashing the full video payload would require reading 50+ GB from a slow optical drive per fingerprint, would fail on any content-layer damage, and would not meaningfully improve pressing-level identification in practice. Structural metadata differs between pressings in every realistic commercial case. When it does not, the pressings are bit-identical enough that treating them as the same identifier is defensible.

### 3.4 Many fingerprints per title is a feature

A theatrical release, a region A Blu-ray, a region B Blu-ray, a director's cut, and a 4K UHD remaster of the same film will typically produce distinct matrix256 digests. This is the intended behavior: matrix256 identifies a specific pressing, not an abstract title.

The mapping from fingerprints to titles is a separate, community-curated layer. matrix256 is the primitive; title resolution is an application built on top.

### 3.5 Separation of identification from metadata

matrix256 answers exactly one question: *is this the same pressing?* It does not report what film the disc contains, what studio released it, what region it targets, or any other descriptive property.

Those questions are answered by complementary tooling that reads the same disc:

- UDF volume labels
- BDMV `META/DL/bdmt_eng.xml` title strings
- AACS Disc IDs (via libaacs when keys are available)
- BD-J organization IDs (from `CERTIFICATE/id.bdmv`)
- HDMV and BD-J title counts and main-feature indices

A catalog or lookup service keyed by matrix256 digest can associate arbitrary rich metadata with each fingerprint, contributed by the community. The fingerprint itself remains minimal, stable, and agnostic.

This is the MusicBrainz model applied to video. `libdiscid` computes a 20-byte SHA-1. The MusicBrainz database does everything else. The Disc ID specification carries a key, not a title.

## 4. Why tree-based hashing, not metadata-content hashing

An earlier draft of matrix256 (version 1, unpublished) hashed the raw bytes of specific metadata files: `VIDEO_TS.IFO` and `VTS_NN_0.IFO` for DVDs; `index.bdmv`, `MovieObject.bdmv`, and the PLAYLIST and CLIPINF directories for Blu-rays. This approach was validated against a 61-disc corpus with zero observed collisions.

Version 2 replaces that approach with a full file-tree hash. The reasons:

### 4.1 Generality

Metadata-content hashing required a distinct selection rule per disc format: one for DVD, one for Blu-ray, one for HD DVD, one for VCD. Each rule needed empirical validation on real discs before the corresponding format could be supported. Every new format was a spec update.

Tree-based hashing has a single rule that works uniformly: enumerate the filesystem, hash the canonical listing. The spec is shorter, the conformance test is universal, and new optical formats inherit support automatically if they use a standard filesystem.

### 4.2 Pressing sensitivity

Metadata-content hashing captures pressing-level identity *indirectly*: when a pressing changes, metadata files usually change, so the hash usually changes. Tree-based hashing captures pressing-level identity *directly*: when a pressing changes, file sizes or layouts change, so the hash changes.

The difference matters at the margin. Consider a commercial studio silently re-pressing a disc with an error-corrected VOB. If only the VOB contents change and the IFO structure is identical, metadata-content hashing collides. Tree-based hashing catches the size difference.

Commercial authoring almost always changes metadata when content changes, so the 61-disc corpus showed no collisions under either approach. But "almost always" is empirical, not structural. The tree-based approach removes the conditional.

### 4.3 Robustness to disc damage

File contents are stored in the large, scratch-prone outer regions of an optical disc. Filesystem metadata is stored in small, concentrated regions near the disc's inner edge, less exposed to physical damage.

Metadata-content hashing reads file contents, and is therefore sensitive to the bit patterns in those outer regions. A scratch on a damaged but identifiable disc can change or corrupt the hash.

Tree-based hashing reads only filesystem metadata — filenames and sizes from directory entries. It is robust to content-layer damage: a scratched disc produces the same fingerprint as a pristine one, because the filesystem's *declared* sizes are unchanged regardless of whether the underlying sectors are readable.

This is particularly important for archival use cases. Library discs handled for decades often have content-layer damage but intact filesystem metadata. matrix256 identifies them correctly.

### 4.4 No need for backup-file fallback

DVD-Video discs include `.BUP` files (backup copies of IFO files) specifically so that playback software can recover when the primary metadata file is damaged. Metadata-content hashing had to make a choice: include `.BUP` files and double-count the data, or exclude them and be vulnerable to primary-file damage.

Tree-based hashing doesn't care. The `.BUP` file is just another entry in the filesystem, contributing its `(path, size)` tuple like any other file. The fallback question disappears.

### 4.5 Reader-independence

Filesystem sizes are stored as single integers in well-defined fields of the UDF File Entry or ISO 9660 directory record. Every filesystem reader returns the same integer for the same entry.

File contents, by contrast, can differ subtly between readers: sector padding at file boundaries, short reads on damaged regions, extended-attribute handling. Metadata-content hashing is more exposed to reader-level variation than tree-based hashing.

### 4.6 AACS compatibility without key material

Commercial Blu-rays encrypt their STREAM directory contents under AACS, requiring libaacs and valid AACS keys to read. Metadata-content hashing for Blu-ray read playlist and clip-info files, which are not AACS-encrypted — so the v1 approach worked without AACS keys.

But tree-based hashing is cleaner still: it reads file *sizes* from the filesystem, without reading any file contents at all. The STREAM directory's M2TS files have readable sizes in the UDF filesystem regardless of AACS state. matrix256 therefore works on AACS-protected Blu-rays without any involvement of AACS licensing or key material, on DVD discs regardless of CSS protection, and on any future optical format using conventional filesystem-level content protection.

## 5. Non-goals and trade-offs

### 5.1 Not tamper-resistant

matrix256 is not a cryptographic proof of disc contents. An attacker who can craft a disc with a chosen filesystem layout can produce a chosen digest. This is a fundamental property of any content-addressable identifier and is not a security flaw — matrix256 is an identifier, not a signature.

### 5.2 Not a content hash

Two discs with identical filesystems but different video encodings produce the same matrix256 digest. In practice this collision is vanishingly rare, because commercial mastering pipelines produce both content and metadata together. But it is possible and should be understood.

Applications that require content-level verification should compute file-level hashes in addition to matrix256. These are complementary, not alternative.

### 5.3 Brittle to filesystem-metadata corruption

Damage to the disc's filesystem metadata (volume descriptors, directory structures) causes the fingerprint computation to fail. This is intentional: matrix256 represents the full filesystem or no digest at all. Implementations must not produce a digest from a partial enumeration.

Filesystem metadata is small and concentrated on optical media, so this failure mode is rare in practice, but it can occur on severely damaged discs.

### 5.4 Does not fingerprint non-filesystem media

LaserDiscs, audio CDs, and other optical media without a filesystem cannot be fingerprinted by matrix256. This is a scope decision, not a design flaw. The community has established identifiers for these formats — MusicBrainz Disc ID for audio CDs, catalog numbers via the LaserDisc Database (lddb.com) for LaserDiscs — that predate matrix256 and serve their respective purposes well.

## 6. Empirical validation

The matrix256 conformance corpus contains 61 discs representative of the optical media ecosystem:

- DVD-Video and Blu-ray releases across multiple studios (Paramount, Warner, Fox, Sony, Universal, Lionsgate, Focus Features, among others).
- Same-title-different-medium pairs (DVD and Blu-ray editions of the same film).
- Same-title-different-edition pairs (theatrical and extended cuts of the same film).
- Multi-disc box sets (TV series; director's editions with bonus-feature discs).
- AACS-protected, BD+-protected, and BD-J-heavy Blu-rays.
- Seamless-branching DVDs (single title with multiple assembly paths).
- Open-content discs (Big Buck Bunny, Sintel) whose ISO images are freely downloadable from their publishers and can be used to reproduce the corpus digests independently.

Across this corpus, matrix256 exhibits:

- **Zero collisions.** Every distinct physical pressing in the corpus produces a distinct digest.
- **Reproducibility.** The same disc image produces the same digest across implementations and operating systems.
- **Pressing sensitivity.** Sibling discs in multi-disc sets — Andromeda Season 1 discs 1–4, Silicon Valley Season 1 discs 1–2, Heat Director's Definitive Edition main-feature and bonus-features discs — all produce distinct digests.
- **Cross-medium differentiation.** Same-title DVD and Blu-ray pressings produce distinct digests, as expected given their entirely different file trees.
- **Cross-edition differentiation.** Theatrical and extended cuts of the same film produce distinct digests.

The corpus also surfaced incidental findings about optical disc authoring practices — cross-studio authoring templates (the "2 HDMV + 79 BD-J" pattern shared across Paramount, Universal, and Focus Features releases; the "5 HDMV + 86 BD-J" pattern shared across Fox, Paramount, and Lionsgate releases), display-name conventions (trademark glyph suffixes like "Blu-ray™" across Sony, Summit, and Paramount releases), and non-ASCII character handling in UDF volume labels — which are documented in the corpus notes and inform future specification refinements.

## 7. Future work

### 7.1 UHD Blu-ray

UHD Blu-ray uses the BDMV directory structure, a superset of standard Blu-ray. matrix256 should work on UHD discs without modification, because the tree-based approach is format-agnostic. Explicit corpus validation with UHD discs is pending.

### 7.2 A community lookup service

matrix256 is an identifier, not a database. The natural complement is a community-contributed lookup service keyed by matrix256 digest, analogous to MusicBrainz for audio CDs. Such a service would:

- Accept digest submissions with associated metadata (title, year, studio, region, edition notes).
- Return metadata given a digest.
- Support corrections and versioning of metadata independently of the fingerprint.

No such service exists today. matrix256 is the primitive that makes one possible. Multiple independent services could coexist, interoperating on the shared identifier; no single service needs to be authoritative.

### 7.3 Specification evolution

If matrix256 proves insufficient in ways the corpus did not predict — systematic collisions in an archival catalog, newly introduced disc formats that don't fit the filesystem-based model — the response will be a new specification version (matrix256 version 3) published alongside version 2, not a modification of version 2. Existing digests remain stable regardless of future specification work.

## 8. Acknowledgments

matrix256 builds on prior art from the optical disc identification community, most notably:

- **Christopher Key**, whose pydvdid algorithm inspired the basic idea of a content-addressable fingerprint for DVD-Video discs and whose documentation of the original algorithm preserved knowledge that would otherwise have been lost when Windows Media Center was discontinued.
- **MusicBrainz contributors**, whose Disc ID specification and community database demonstrate the value of a well-specified, community-maintained optical disc identifier.
- **The libbluray and libudfread projects**, which provide the open-source filesystem readers that make cross-platform matrix256 implementations practical.
- **The Automatic Ripping Machine project**, whose operational deployment of pydvdid at scale revealed the limitations of 64-bit fingerprints and Windows-API-derived algorithms in a community identifier context.

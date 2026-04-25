# matrix256: Implementer's Guidance

Companion document to the matrix256 specification. This document is **non-normative**: nothing here is part of the algorithm. The specification (`SPEC.md`) is the single source of truth for what a matrix256 digest is. This document collects practical guidance for implementations that compute matrix256 digests against optical discs and other filesystem sources.

In case of any conflict between this document and the specification, the specification governs.

## 1. Scope of this document

The matrix256 algorithm operates on a rooted filesystem tree. It does not specify how an implementation arrives at that tree — mounting, filesystem-view selection, encoding handling, error recovery, and similar concerns are deliberately outside the normative algorithm so that the same digest can be computed from a mounted optical disc, a loop-mounted ISO image, an in-memory directory, a tar archive, or any other tree-shaped data source.

This document collects the operational concerns that fall outside the spec but matter in practice if you want your implementation's digests to agree with other implementations' digests on real-world media.

## 2. Bridge discs and filesystem-view selection

Many commercial DVDs and some Blu-ray discs are mastered as **bridge discs** that expose the same underlying data through more than one filesystem — most commonly UDF and ISO 9660. The two filesystems can differ in trivially observable ways (case of filenames, presence of synthetic entries, directory ordering as enumerated by the reader) without any difference in the underlying pressing.

Because matrix256 walks "the filesystem at the provided root", it produces a different digest for each filesystem view of the same physical media. Both digests are correct outputs of the algorithm against different inputs.

For cross-implementation digest agreement on bridge discs:

- **Prefer the UDF view when both UDF and ISO 9660 are available.** This is the view that common operating systems (Linux desktops, macOS, Windows) default to when mounting a commercial DVD or Blu-ray, and it is the view used to generate the matrix256 corpus values.
- **On ISO 9660 discs with Joliet or Rock Ridge extensions, use the extended view that surfaces full-length filenames.** The plain ISO 9660 view truncates names to 8.3 form and will diverge from any extended view.

Implementations that catalog or submit digests should record which filesystem view was used (e.g., `"UDF"`, `"ISO 9660"`, `"ISO 9660 + Joliet"`) so a downstream lookup service can reconcile multiple fingerprints from the same physical pressing.

## 3. Reference environment for the matrix256 corpus

The corpus values published alongside this specification were generated under the following environment:

- Ubuntu 24.04 LTS
- `udisksctl` (udisks2) for mount management
- Linux kernel UDF and ISO 9660 drivers as shipped with the distribution

Implementations should expect bit-identical digest agreement with the published corpus when reading the same physical media under similar conditions. Differences in mount behavior across operating systems, distributions, or kernel versions are exactly what §1.4 of the specification places outside the algorithm — but in practice the major desktop platforms agree on UDF view selection for commercial discs, and corpus reproduction has been verified across reasonable Linux configurations.

If you observe a digest mismatch against the corpus on a disc you can read cleanly, the most likely causes are, in rough order of frequency:

1. Reading a different filesystem view than the corpus generator did (see §2 above).
2. A filesystem reader that synthesizes additional entries (e.g., a `.Trashes` or `System Volume Information` directory injected by an operating system that has touched the medium).
3. A path-decoding bug in the implementation (NFD vs. NFC, or a non-Unicode filename handled differently).
4. A genuine discrepancy in the physical media — distinct pressings of the same title with subtly different file layouts.

## 4. Non-disc filesystems

matrix256 is filesystem-agnostic. Implementations targeting USB drives, archive files, in-memory directory trees, or other rooted filesystem inputs need no special handling — the algorithm is the same. The optical-disc framing in `SPEC.md` reflects the primary intended use case, not a constraint on inputs.

For non-disc inputs, the same caveats apply:

- The filesystem-view choice (and any extension layer such as Joliet, Rock Ridge, or NTFS short-name policy) determines what gets enumerated. Two different views of the same underlying data will produce two different digests.
- The caller is responsible for ensuring the root is a successfully mounted, readable filesystem before invoking matrix256. Mount or open failures are not part of the algorithm's error model.

## 5. Submitting digests to a lookup service

Lookup services keyed by matrix256 digest should accept and store filesystem-view metadata alongside each submitted digest, so that:

- Multiple fingerprints from the same physical pressing (one per filesystem view that the pressing exposes) can be associated with a single logical pressing record.
- Future implementations that prefer a different default view (e.g., a future operating system that mounts ISO 9660 instead of UDF on bridge discs) can be reconciled against the existing catalog without losing prior submissions.

Recommended submission fields, in addition to the digest itself:

- Filesystem identifier as observed at mount time (e.g., `"udf"`, `"iso9660"`, `"iso9660+joliet"`, `"iso9660+rockridge"`, `"ntfs"`, `"ext4"`, `"fat32"`).
- Whether the source was a physical disc, an ISO image, or another filesystem source.
- Optionally, the operating system and reader software used to enumerate the filesystem, for audit purposes.

The catalog layer — not the algorithm — is responsible for collapsing multiple per-view fingerprints into a single logical-pressing identity.

# Evaluation corpus

Discs inspected with `inspect_disc.py` to exercise matrix256 against real-world inputs. Each entry records the computed fingerprint so any reproducer can verify their implementation against a known digest.

The corpus is not normative — matrix256's specification is the source of truth. These are illustrative fixtures covering open-content and commercial pressings, DVD and Blu-ray, HDMV-only and BD-J-heavy, protected and unprotected.

## Summary

| # | Title | Type | matrix256 (first 16) |
|---|---|---|---|
| 1 | Big Buck Bunny | Blu-ray | `38d3330a06917cbc` |
| 2 | Sintel | DVD-Video | `4bba5d860a2e61b7` |
| 3 | The Martian | Blu-ray | `0c4c94044c3309c0` |
| 4 | The Boondock Saints | Blu-ray | `fe37e0802e514cfd` |
| 5 | La La Land | Blu-ray | `364381f64015e1c3` |
| 6 | Suicide Squad (theatrical) | Blu-ray | `c12f9c146f49fc43` |
| 7 | Suicide Squad: Extended Cut | Blu-ray | `48dad7a2a1514eca` |
| 8 | Silicon Valley S1 — Disc 1 | Blu-ray | `765a3c735a1f2a48` |
| 9 | Silicon Valley S1 — Disc 2 | Blu-ray | `c891cc3db59097f0` |
| 10 | Silicon Valley S2 — Disc 1 | DVD-Video | `a712a945fc6a406e` |
| 11 | Silicon Valley S2 — Disc 2 | DVD-Video | `c4fff4d76b300ad0` |
| 12 | Andromeda S1 — Disc 1 | DVD-Video | `a36d79234597315a` |
| 13 | Andromeda S1 — Disc 2 | DVD-Video | `a67241ef1da2ea9a` |
| 14 | Andromeda S1 — Disc 3 | DVD-Video | `d08a3e5bba2d4568` |
| 15 | Andromeda S1 — Disc 4 | DVD-Video | `7459e8c79c55f3ac` |
| 16 | No Country for Old Men / Gone Baby Gone (double feature) | Blu-ray | `795d32f567b931b1` |
| 17 | Afro Samurai | Blu-ray | `f1e1bd8385e39c39` |
| 18 | Four Brothers | DVD-Video | `b9b566fa01ce0730` |
| 19 | Munich | DVD-Video | `49ff13400488f1e0` |
| 20 | Argo | DVD-Video | `3b04b8bab8c7c50d` |
| 21 | American Gangster (seamless branching) | DVD-Video | `50426f73dbc0eb3b` |
| 22 | Casablanca | DVD-Video | `8ef7dba2bdbf4ac9` |
| 23 | Pitch Perfect (Aca-Awesome Sing-Along) | DVD-Video | `0766b920ec352286` |

## 1. Big Buck Bunny (Blu-ray)

- **Source:** Blender Foundation, open content (https://peach.blender.org/)
- **matrix256:** `38d3330a06917cbc1b66ec2d4c36942809071d3ee8b5c920bcc1c399a11ae3a4`
- **AACS Disc ID:** `69C41314710953D5C34CBF0E01F20BC870CF704A`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 599 HDMV + 4 BD-J (4 "unsupported")
- **Payload:** ~7.9 GB STREAM
- **Why it's here:** Open content baseline. Ships an AACS directory (so libaacs surfaces a Disc ID) but isn't actually encrypted — a useful test for confirming matrix256 works identically whether or not decryption would be possible. Rich `BDMV/META/DL/bdmt_eng.xml` with named TOC entries, exercising the XML dump path in `inspect_disc.py`.

## 2. Sintel (DVD-Video)

- **Source:** Blender Foundation, open content (https://durian.blender.org/)
- **matrix256:** `4bba5d860a2e61b7b93778a97c65da01347416645f6eb971a27c17000d20880d`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** The DVD counterpart to Big Buck Bunny. Exercises the DVD path of the algorithm (VIDEO_TS.IFO + VTS_NN_0.IFO selection). Open content, so the ISO can be redistributed as a test fixture.

## 3. The Martian (Blu-ray)

- **matrix256:** `0c4c94044c3309c077beeb7a092b8dc405de7195512cf89aaf89a9a22f96bb89`
- **AACS Disc ID:** `C803CB1A9B5484B1B970378ED7E1D531DDB3276C`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 5 HDMV + 86 BD-J (86 "unsupported"); main title #70
- **Files hashed:** 174 (≈290 KB)
- **Payload:** 44.51 GB STREAM, 47 MB JAR
- **Why it's here:** Commercial AACS+BD+ reference. Dozens of 7-second BD-J decoy playlists around the real movie (main title #70) — classic anti-rip pattern. Validates that matrix256 fingerprints are reproducible on fully protected discs without needing libaacs or any decrypt pass.

## 4. The Boondock Saints (Blu-ray)

- **matrix256:** `fe37e0802e514cfd76543fce0aaed51d2d655787b4b0235e1258ecea5a2dc287`
- **AACS Disc ID:** `AF3FA2FD3D2BCF0FF199D97C3BBA4EFE9BCCBB84`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 0 HDMV + 81 BD-J (81 "unsupported"); main title #36
- **Files hashed:** 78 (≈150 KB)
- **Payload:** 41.22 GB STREAM, 48 MB JAR
- **Why it's here:** Pure BD-J disc — zero HDMV titles, playback is entirely Java-driven. Unusual authoring pattern; useful for confirming matrix256 doesn't depend on having any HDMV Movie Object content (the file is hashed because it exists, but its semantic role is minimal).

## 5. La La Land (Blu-ray)

- **matrix256:** `364381f64015e1c3f22ae1b945c4f380e0ff3d2a418a654b878377666153ce05`
- **AACS Disc ID:** `A4E972BDF029F7E4CB48D75C96B2E5FC601D5229`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 93 HDMV + 10 BD-J (10 "unsupported"); main title #193
- **Files hashed:** 514
- **Payload:** 45.96 GB STREAM, 25 MB JAR
- **Why it's here:** Heavy-decoy HDMV disc — main title numbered #193 but only 103 titles exist, meaning the playlist/clip ID space is sparse (00001.mpls … 02756.clpi) with many filler entries. Largest file count in the corpus by ~3×; stress-tests ordering stability under a big, sparse numeric space. AACS without BD+ (Lionsgate).

## 6. Suicide Squad (Blu-ray)

- **matrix256:** `c12f9c146f49fc4352bed581f76652493697ebd6e67dff09f107c0c7995ca57d`
- **AACS Disc ID:** `85D565E111B07F774191EF7D82E579F61D62A94C`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 12 HDMV + 0 BD-J (0 "unsupported"); main title #27
- **Files hashed:** 88
- **Payload:** 41.63 GB STREAM, 0 B JAR, 0 B BDJO
- **Why it's here:** Pure HDMV authoring — zero bytes in `BDMV/JAR/` and `BDMV/BDJO/`. Together with The Boondock Saints (0 HDMV + 81 BD-J) it brackets the commercial authoring spectrum, confirming matrix256 is stable across both extremes. AACS only, no BD+ (Warner).
- **See also:** entry 7, the Extended Cut pressing from the same 2-disc combo pack, for a direct theatrical-vs-extended comparison.

## 7. Suicide Squad: Extended Cut (Blu-ray)

- **matrix256:** `48dad7a2a1514ecadaee160a5782562560810d37dda2c727359d3c33fc088482`
- **AACS Disc ID:** `C4C849323E97963B49014C6F5C12159F54182B21`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 12 HDMV + 0 BD-J (0 "unsupported"); main title #26
- **Files hashed:** 86
- **Payload:** 40.89 GB STREAM, 0 B JAR, 0 B BDJO
- **Why it's here:** The second disc of the Suicide Squad 2-disc combo pack — same studio, same authoring house, same protection profile, same pure-HDMV style as entry 6, but carrying the extended cut. matrix256 produces a digest completely distinct from the theatrical disc (`48dad7a2…` vs `c12f9c14…`), and Warner's AACS Disc ID also differs. This is the corpus's empirical demonstration of the README's "many fingerprints per title is expected" rationale: a fingerprint identifies a specific edition, not an abstract title. Structural differences that propagate into the hashed bytes include a shifted main title index (#26 vs #27), a different file count (86 vs 88), and a 750 MB smaller payload distribution across differently-sized clips.

## 8. Silicon Valley Season 1 — Disc 1 (Blu-ray)

- **matrix256:** `765a3c735a1f2a486de96bdcb0f98cad314ba78c08e05eed0e3b7320ecbae248`
- **AACS Disc ID:** `57163EBEC59D05A4A71F70723D0D6492EC5BC64A`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #12
- **Files hashed:** 56 — smallest BD in the corpus
- **Payload:** 43.5 GB STREAM, 1.4 MB JAR
- **Why it's here:** First TV-series disc in the corpus, addressing the README's "Box sets and TV series — empirical verification pending" Limitation. HBO-style authoring: mixed HDMV+BD-J with a lightweight Java menu layer over HDMV-driven episode playback, contrasting with Warner's pure-HDMV and Fox's pure-BD-J approaches. Many very-short (1s) playlist entries likely serve as per-episode intro cards or chapter-selection stubs.
- **See also:** entry 9, the Disc 2 sibling from the same set, for a box-set sibling-distinction data point.

## 9. Silicon Valley Season 1 — Disc 2 (Blu-ray)

- **matrix256:** `c891cc3db59097f006bfdbca09fef42035898235b6e16ab5434610a1efb47d79`
- **AACS Disc ID:** `D3915434FDCABA94F5E16BB9E5018EB7CC309F22`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #14
- **Files hashed:** 58
- **Payload:** 22.6 GB STREAM, 1.4 MB JAR
- **Why it's here:** The sibling of entry 8 from the same HBO box set. A single data point rather than empirical proof, but a useful one: two discs authored by the same house with identical title counts (2 HDMV + 79 BD-J both) and identical protection profile still produce cleanly distinct matrix256 digests. Structural differences that propagate into the hash: shifted main title index (#14 vs #12), slightly different clip mix (58 files vs 56), and different per-episode MPLS/CLPI content. Disc 2 carries a smaller payload (22.6 GB vs 43.5 GB), consistent with an uneven episode split across the set. More box sets would be needed to treat the "sibling discs produce distinct digests" property as confirmed rather than observed.

## 10. Silicon Valley Season 2 — Disc 1 (DVD-Video)

- **matrix256:** `a712a945fc6a406e70d4c5dc8da03e9ff554c8a045748766b70f04a329a3bbc3`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 1 of the Silicon Valley season 2 DVD box set.
- **See also:** entry 11, the Disc 2 sibling from the same set.

## 11. Silicon Valley Season 2 — Disc 2 (DVD-Video)

- **matrix256:** `c4fff4d76b300ad00001f82871a6cd9914331612553f073e7f2cff43b1c6fe04`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 2 of the Silicon Valley season 2 DVD box set.
- **See also:** entry 10, the Disc 1 sibling from the same set.

## 12. Andromeda Season 1 — Disc 1 (DVD-Video)

- **matrix256:** `a36d79234597315a41681a494d63b56aa820db531168d2906e024f4c3da277d9`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 1 of the Andromeda season 1 DVD box set.
- **See also:** entries 13, 14, and 15 — the Disc 2, Disc 3, and Disc 4 siblings from the same set.

## 13. Andromeda Season 1 — Disc 2 (DVD-Video)

- **matrix256:** `a67241ef1da2ea9af53c09396ca029537012cb5d20272095747d3d8ca18b2501`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 2 of the Andromeda season 1 DVD box set.
- **See also:** entries 12, 14, and 15 — the Disc 1, Disc 3, and Disc 4 siblings from the same set.

## 14. Andromeda Season 1 — Disc 3 (DVD-Video)

- **matrix256:** `d08a3e5bba2d4568646b8f7d0518aac7a7dd390c8b127e705adbd87492acdcd5`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 3 of the Andromeda season 1 DVD box set.
- **See also:** entries 12, 13, and 15 — the Disc 1, Disc 2, and Disc 4 siblings from the same set.

## 15. Andromeda Season 1 — Disc 4 (DVD-Video)

- **matrix256:** `7459e8c79c55f3ac8963447b9a04bdf738dff6cad677c833cc60f8b85f9316ee`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 4 of the Andromeda season 1 DVD box set.
- **See also:** entries 12, 13, and 14 — the Disc 1, Disc 2, and Disc 3 siblings from the same set.

## 16. No Country For Old Men / Gone Baby Gone BD (Blu-ray)

- **matrix256:** `795d32f567b931b1a4d4912db10a3191ef3b2faf203283470480e13c07794241`
- **AACS Disc ID:** `7BFBDC2177C6E3139FDE37AAF2FB424049BB654B`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 26 HDMV + 0 BD-J (0 "unsupported"); main title #8
- **Files hashed:** 28
- **Payload:** 38.06 GB STREAM, 0 B JAR, 0 B BDJO
- **Why it's here:** this is a double-feature bluray containing No Country for Old Men and Gone Baby Gone.

## 17. Afro Samurai (Blu-ray)

- **matrix256:** `f1e1bd8385e39c397dd980b7acd745d410dfdedad7adb7b3dcce8072f3a3be9e`
- **AACS Disc ID:** `F2A6F9BBE8A7060FF0FEF1D5F9623C8D8EB20EB4`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 29 HDMV + 0 BD-J (0 "unsupported"); main title #9
- **Files hashed:** 81
- **Payload:** 23.21 GB STREAM, 0 B JAR, 0 B BDJO
- **Why it's here:** This is the full series of Afro Samurai.

## 18. Four Brothers (DVD-Video)

- **matrix256:** `b9b566fa01ce0730783d3b051d7618db16da96b4a680ff069e6cb3f04198cf13`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** First commercial feature-film DVD in the corpus (prior commercial DVDs were TV-series box sets). Has the most VTSes (8) and the largest `VIDEO_TS.IFO` (22 KB) of any DVD in the corpus so far, exercising a broader slice of the DVD-Video navigation layout than the leaner box-set discs.

## 19. Munich (DVD-Video)

- **matrix256:** `49ff13400488f1e0a79c2a5360eb64abb9841c21b87999043bf5af2f79c444e9`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Minimal-VTS commercial feature-DVD — a dual-layer (DVD9) pressing where the entire 2h43m feature plus a short trailer live in just 3 VTSes, with `VTS_01_0.IFO` at 104 KB (second-largest IFO in the DVD corpus). Contrasts with Four Brothers (entry 18, 8 VTSes) as the simple-authoring end of the commercial-feature-DVD spectrum.

## 20. Argo (DVD-Video)

- **matrix256:** `3b04b8bab8c7c50d54e57e06a734b2f00df4a77927c898dff389fadf5d950478`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Second minimal-VTS commercial feature DVD in the corpus: like Munich (entry 19), a DVD9 Warner pressing with 3 VTSes and the entire feature (2h00m) living in `VTS_01`. Different `VTS_01_0.IFO` size (94 KB vs 104 KB) and different fingerprint despite the shared authoring pattern — another per-edition distinction data point. Title #5 / #6 audio-language fields carry non-UTF-8 bytes from the disc's raw IFO strings, which prompted a `errors="replace"` hardening in `inspect_disc.py`'s lsdvd subprocess decoding.

## 21. American Gangster (DVD-Video)

- **matrix256:** `50426f73dbc0eb3b29366e73e54c76e9925944819840be6a5bccd93db51d4618`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** First seamless-branching disc in the corpus. A single VTS_01 carries the video payload for two distinct DVD titles — the 2h55m40s extended cut and the 2h36m49s theatrical cut — stitched together from different cell orderings (MakeMKV reports 30 segments per title, the classic seamless-branching signature). Exercises a DVD authoring pattern the corpus previously lacked: two alternate cuts co-resident on one disc via shared VOBs rather than separate VTSes (contrast with Suicide Squad theatrical/extended at entries 6-7, which ship on two discs).
- **Why the tools report it as "ASDF":** Neither lsdvd, MakeMKV, nor udisksctl surface the film title — they all fall back to "ASDF" because both the VMG disc-title field (inside `VIDEO_TS.IFO`) and the UDF volume name were left as that placeholder by Universal's authoring team. DVD-Video's VMG disc-title is a studio-populated string with no functional role in playback, so it's frequently shipped blank or placeholder — which is why `inspect_disc.py` can't recover the film title from the disc alone for this pressing.

## 22. Casablanca (DVD-Video)

- **matrix256:** `8ef7dba2bdbf4ac926a6faedc2ad22e5bcf29e6050988f53a543e3a9b89ff04e`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Minimum-VTS commercial feature DVD — 2 IFOs hashed (`VIDEO_TS.IFO` + one `VTS_01_0.IFO`), the fewest of any commercial feature in the corpus. The 1h42m feature, a 36m44s bonus documentary, and ~10 short supplements all live in a single `VTS_01` with a dense `VTS_01_0.IFO` (116 KB) carrying the navigation for 14 chapter-addressed titles. Warner Home Video authoring, DVD9 payload. Sharpens the sparse end of the commercial-feature-DVD structural spectrum below Munich (entry 19, 3 VTSes) and Argo (entry 20, 3 VTSes).

## 23. Pitch Perfect (Aca-Awesome Sing-Along) (DVD-Video)

- **matrix256:** `0766b920ec352286950fb972eddf59f2695ebfc8c698838f3a8537b209e40c81`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is the Aca-Awesome release of Pitch Perfect. Second seamless-branching disc in the corpus, but a different flavor than American Gangster (entry 21): both branches have identical duration (1h51m38s), same source VTS, same 35-segment map — the two titles are the same film played back with different default audio/subtitle selections (regular track vs sing-along). Confirms matrix256 handles seamless-branching authoring identically regardless of whether the branches differ in runtime or only in default stream picks.

## Reproducing a fingerprint

For discs with an `.iso` available, the fingerprint is deterministic from the disc image alone:

```
python inspect_disc.py <path-to-iso>
```

For physical discs, pass the optical drive block device (`/dev/sr0`, `/dev/sr1`, …). The script loop-mounts the ISO or uses `udisksctl` to mount the block device read-only, runs selection and SHA-256, and unmounts on exit.

Open-content discs (Big Buck Bunny, Sintel) are freely downloadable from their respective project pages and should produce identical fingerprints to the values recorded here.

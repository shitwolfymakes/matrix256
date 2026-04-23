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
| 24 | Heat | DVD-Video | `1983932253e4116a` |
| 25 | Stonehenge Apocalypse | DVD-Video | `5e0e5f5de53fce79` |
| 26 | Madso's War | DVD-Video | `cbf05563e0fbf73e` |
| 27 | VANish | DVD-Video | `e90c7a1341c8ef43` |
| 28 | Treasure Guards | DVD-Video | `a75a01a298decf62` |
| 29 | The Reading Room | DVD-Video | `111878a8ecdcc09b` |
| 30 | The Secret | DVD-Video | `1dc7a2d76e69093e` |
| 31 | The Endless Summer | DVD-Video | `448a1cb79358460a` |
| 32 | Space Camp | DVD-Video | `310ac2bd337c2c73` |
| 33 | The Adventures of Milo and Otis | DVD-Video | `0005cb727f4851ec` |
| 34 | Space Odyssey: Voyage to the Planets | DVD-Video | `4ba6b0c730a105a1` |
| 35 | Five Fingers | DVD-Video | `0c28f606ac8b466b` |
| 36 | Whiskey Tango Foxtrot | DVD-Video | `68e1e31d648edc8d` |
| 37 | Whiskey Tango Foxtrot | Blu-ray | `7520a70f5d9646d5` |
| 38 | Cowboys & Aliens | DVD-Video | `44bb1b63ee48d1e8` |
| 39 | Cowboys & Aliens | Blu-ray | `04c192e9e34ee28d` |
| 40 | Life of Brian (Immaculate Edition) — Disc 1 | DVD-Video | `1391d48490beb787` |
| 41 | Life of Brian (Immaculate Edition) — Bonus Disc | DVD-Video | `8948ddb848b10920` |

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

## 24. Heat (DVD-Video)

- **matrix256:** `1983932253e4116af6606d4244256b1ce5d4ba0dc4cbb9686f22d8ae409ccab0`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Second minimum-VTS commercial feature DVD — same single-VTS Warner Home Video authoring pattern as Casablanca (entry 22), different feature (2h50m vs 1h42m), more chapters (52 vs 36), slightly smaller `VTS_01_0.IFO` (110 KB vs 116 KB), distinct fingerprint. Gives the "minimum-VTS" axis two data points across very different eras (1942 catalog release vs 1995 theatrical). Notable curiosity: the UDF volume label `HEAT_16X9LB_DUAL_LAYER_NA` encodes the aspect ratio (16:9 letterbox), disc type (DVD9 dual layer), and region (North America) directly — one of the most descriptive volume labels in the corpus.

## 25. Stonehenge Apocalypse (DVD-Video)

- **matrix256:** `5e0e5f5de53fce798cd9093df32051865fe452c2459cd09f257312caad1b5004`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Here's an obscure, D-Tier movie called Stonehenge Apocalypse. First single-layer (DVD5) commercial feature in the corpus — total VOB payload is ~4.5 GB across 4 VTSes, comfortably fitting DVD5 capacity, where every previous commercial feature in the corpus is DVD9. Also notable: MakeMKV reports the disc name as "Stonehenge Apocalypse" (proper capitalisation, with space) rather than the UDF volume label, confirming the VMG disc-title field *is* populated correctly when studios bother to set it — a clean counterpoint to American Gangster (entry 21) where that same field was left as "ASDF".

## 26. Madso's War (DVD-Video)

- **matrix256:** `cbf05563e0fbf73eba871d8f8cf94be685a7fdc59dadbc65a672679ba62fe8b9`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is called Madso's War. Second DVD5 commercial feature in the corpus (alongside Stonehenge Apocalypse, entry 25) — ~4.1 GB of VOB payload fitting single-layer capacity, a 1h25m feature, and five shallow VTSes with the feature material in `VTS_03`. Unlike Stonehenge Apocalypse, this pressing left the VMG disc-title field unset, so MakeMKV falls back to the UDF volume label `MADSOS_WAR` — another data point for the "VMG disc-title is studio-discretionary" observation (contrast entries 21 and 25).

## 27. VANish (DVD-Video)

- **matrix256:** `e90c7a1341c8ef43b01188b28fa335bad846dbe131b3e58768e43b8afe621943`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is VANish (2015).

## 28. Treasure Guards (DVD-Video)

- **matrix256:** `a75a01a298decf62788c7175cdea2e0aa91a3a9af02bd8da1fbee1ee2715a30c`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Treasure Guards (2011). Third DVD5 commercial feature in the corpus (alongside entries 25 and 26) — ~3.9 GB payload across just 2 VTSes, the minimum VTS count for any DVD5 entry here. Also notable for audio/subtitle language codes reported as `xx` (unset) by lsdvd, unusual compared to the properly-tagged `en/es/fr` of higher-budget pressings — consistent with lean authoring on low-budget releases.

## 29. The Reading Room (DVD-Video)

- **matrix256:** `111878a8ecdcc09b9dca5b1f889c76f986b703a3c24adf77c7d86c0dd68ad5b4`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Reading Room (2005). Fourth DVD5 commercial feature in the corpus and a near-identical structural twin of Treasure Guards (entry 28): same 3-IFO / 2-VTS layout, `VTS_01_0.IFO` within 2 KB of its match (70 KB vs 72 KB), both `xx` audio/subtitle language codes, both with `Provider ID` set to the volume label — yet the two fingerprints differ completely. Sharpens the sibling-distinction observation at the low-budget template-authoring end of the DVD spectrum.

## 30. The Secret (DVD-Video)

- **matrix256:** `1dc7a2d76e69093e63801922272f03aad9b6f70c4c97644a0cc622938770f340`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Secret (2006). Most VTSes of any DVD in the corpus — 12 VTSes and 13 IFOs hashed — yet still DVD5 (~4.2 GB total payload). Unusual authoring: the 1h30m feature lives in `VTS_05` (`VTS_05_0.IFO` 78 KB), while each short extra (from 30 seconds to 8 minutes) is isolated in its own dedicated VTS with an identical 18 KB IFO. Extends the high end of the DVD VTS-count axis (previous max was Four Brothers's 8 VTSes at entry 18).

## 31. The Endless Summer (DVD-Video)

- **matrix256:** `448a1cb79358460ac3304c065868d989f03ed85de907497daf3ed43162a42bf7`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Endless Summer (1966). Sixth DVD5 commercial feature in the corpus, and the first disc carrying a true **mono (1-channel) audio track** — a 1966 surf documentary preserving its original single-channel mix, where every previous corpus disc ships stereo (2ch) or 5.1 (6ch). Structurally aligned with the 3-IFO / 2-VTS template of entries 28-29 but with a larger `VTS_01_0.IFO` (80 KB, reflecting the feature's 20 chapters) and a properly-tagged `en` language code — a counter-example to the "xx" unset pattern seen on other low-budget pressings.

## 32. Space Camp (DVD-Video)

- **matrix256:** `310ac2bd337c2c73e03f324ee7d3514602babb2780d5f2f79af63bba875b6512`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Space Camp (1986). Seventh DVD5 commercial feature in the corpus — 3-IFO / 2-VTS layout shared with entries 28, 29, 31, but the first disc with a third-party authoring-house Provider ID (`LASERPACIFIC MEDIA CORPORATION`) rather than a studio name or a self-referential label. Minor but real axis: discs outsourced to a mastering vendor get the vendor's ID stamped into VMGI, distinct from the self-authored studio pattern (Warner Home Video etc.) and the "placeholder-equals-label" pattern of the very low-budget discs.

## 33. The Adventures of Milo and Otis (DVD-Video)

- **matrix256:** `0005cb727f4851ec9c6ab5467af51634d7a2c7a0ba803d06a4b9e251870ed70e`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Adventures of Milo and Otis (1986) — specifically the American release, which is Columbia's re-cut-and-redubbed version of the 1986 Japanese film *Koneko Monogatari* (*The Adventures of Chatran*), with a shorter runtime, Dudley Moore narration, and new credits. That makes this disc a new regional-release axis: the underlying work is Japanese but the pressed edition is a distinct American derivative, with its own authoring chain and its own matrix256 digest independent of any Japanese or international pressing.
- **Structural note:** Cleanest DVD authoring in the corpus — 2 IFOs hashed, a single VTS, a single title, no bonus/extras/menus VTS at all; just the 1h15m feature and the VMG entry. An unusual VMG-disc-title pattern too: properly populated as "The Adventures of Milo and Otis" despite the UDF volume label being a generic default `DVD_VIDEO` (contrast American Gangster at entry 21, where *both* were placeholder, and Stonehenge Apocalypse at entry 25, where both were meaningful). Ideal floor on the authoring-complexity axis.

## 34. Space Odyssey: Voyage to the Planets (DVD-Video)

- **matrix256:** `4ba6b0c730a105a1b2303c7b04e7d939a235939eebc1dffe3d1f43a4aec7227c`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is the dvd release of Space Odyssey: Voyage to the Planets (2004), a two-part docu-drama. Interesting play-all authoring: the disc exposes both the individual episodes (titles #9 and #10, ~59 minutes each) and a separate concatenated 1h57m "both episodes back-to-back" title (#8, exactly twice the episode runtime). `VTS_04_0.IFO` at 178 KB is unusually large, reflecting the extra navigation tables for this compound-title arrangement. Also a new label axis: the UDF volume name and VMG disc-title are both just `E2194`, a distributor catalog/SKU number — distinct from the studio, placeholder, title-as-label, and authoring-house patterns already in the corpus.

## 35. Five Fingers (DVD-Video)

- **matrix256:** `0c28f606ac8b466b2e5992c495ba843b545b2a98be23835c835b908eff92c10f`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Five Fingers (2006). Eighth DVD5 commercial feature in the corpus — 7 IFOs hashed, feature in `VTS_01` (~3.7 GB, `VTS_01_0.IFO` 70 KB — same size as entry 29), with five smaller VTSes carrying menus and short extras. Partial language-code tagging (feature is `en`, most bonus titles are `xx`) — a new pattern midway between the fully-tagged and fully-placeholder DVDs earlier in the corpus.

## 36. Whiskey Tango Foxtrot (DVD-Video)

- **matrix256:** `68e1e31d648edc8d1c943e4b21955227e0c336782a13e12e0529d8f1de0ac12d`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Whiskey Tango Foxtrot (2015), it is the DVD disk of a DVD/Blu-ray combo pack. First "combo-pack DVD side" data point in the corpus — a modern retail pattern where the same film ships on both formats in a single SKU, and the DVD side often has lighter authoring than a standalone DVD release. Structurally a standard DVD9 feature disc (6 IFOs, feature in `VTS_05` with a 72 KB IFO spanning 8 VOBs / ~6.4 GB), with MakeMKV reporting 3 segments on the main title — likely a layer-break cell split rather than seamless-branching.
- **See also:** entry 37, the Blu-ray side of the same combo pack — first cross-format sibling pair in the corpus.

## 37. Whiskey Tango Foxtrot (Blu-ray)

- **matrix256:** `7520a70f5d9646d5b9363c5001b918231a9af00e15b53e226649cde98d6ff571`
- **AACS Disc ID:** `33BBB49A812E43775553DD8B45083CE9482AE63B`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 3 HDMV + 78 BD-J (78 "unsupported"); main title #1
- **Files hashed:** 151
- **Payload:** 42.37 GB STREAM, 23.7 MB JAR, 4.4 KB BDJO
- **Why it's here:** This movie is Whiskey Tango Foxtrot (2015), it is the Blu-ray disk of a DVD/Blu-ray combo pack. Paramount-style heavy-decoy authoring (only 3 HDMV titles but 78 BD-J "unsupported" playlists salted around the real movie) matching the pattern seen at entry 3 (The Martian) and entry 4 (The Boondock Saints). Pairs with entry 36, the DVD side of the same retail SKU, to form the corpus's first cross-format sibling — same film, same release, same authoring team, two different media with completely distinct structural fingerprints.
- **See also:** entry 36, the DVD side of the same combo pack.

## 38. Cowboys & Aliens (DVD-Video)

- **matrix256:** `44bb1b63ee48d1e83fd902634923ace473cb862c030046536b71f75563b9a06d`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Cowboys & Aliens (2011), it is the DVD disk of a DVD/Blu-ray combo pack. Second combo-pack DVD side in the corpus (after Whiskey Tango Foxtrot at entry 36) — same DVD9 + combo-pack authoring family but with more VTSes (9 IFOs hashed vs 6), with the feature in `VTS_08` (`VTS_08_0.IFO` 26 KB, 6.8 GB VOB span) and a dense `VTS_07_0.IFO` at 82 KB carrying the bonus-feature navigation. MakeMKV again reports 2 segments on the main title — likely the layer-break cell split consistent with entry 36's pattern.
- **See also:** entry 39, the Blu-ray side of the same combo pack.

## 39. Cowboys & Aliens (Blu-ray)

- **matrix256:** `04c192e9e34ee28d765f1addb7d5268e39866e28c0634985c4fbff32a32090c5`
- **AACS Disc ID:** `9597816567B81882E27FE5321307D50630894626`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 6 HDMV + 75 BD-J (75 "unsupported"); main title #106
- **Files hashed:** 213
- **Payload:** 46.05 GB STREAM, 25.5 MB JAR, 4.9 KB BDJO
- **Why it's here:** This movie is Cowboys & Aliens (2011), it is the Blu-ray disk of a DVD/Blu-ray combo pack. Second cross-format sibling pair in the corpus — pairs with entry 38 (the DVD side of the same retail SKU) to reinforce that matrix256 distinguishes DVD and Blu-ray halves of combo packs even though the underlying film is identical. Heavy-decoy Universal-family authoring: only 6 HDMV titles but 75 BD-J "unsupported" playlists scattered throughout a sparse ID space (main title #106), echoing the pattern of entries 3 (The Martian), 4 (The Boondock Saints), and 37 (Whiskey Tango Foxtrot).
- **See also:** entry 38, the DVD side of the same combo pack.

## 40. Life of Brian (Immaculate Edition) — Disc 1 (DVD-Video)

- **matrix256:** `1391d48490beb787b88ab29a9ac70a94ce8bb05bc552d56173a9d0192b6dc5fd`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Immaculate Edition of Monty Python's Life of Brian (1979), it is the DVD disk of a DVD/Special Features combo pack. Introduces a third multi-disc-set flavor into the corpus: not a TV box (entries 8-9, 10-11, 12-15), not a cross-format combo pack (entries 36-37, 38-39), but a *main-feature + bonus-disc* two-disc pairing — both are DVDs, but only one carries the movie and the other is entirely extras. Feature in `VTS_01` (~6.4 GB, 8 VOB split, 32 chapters), DVD9. Notable label quirk: the UDF volume identifier is the multi-field string `LIFE_OF_BRIAN_DISC1` while the volume *label* read by `lsblk` is the space-containing `Life of Brian` — this surfaced a latent bug in `inspect_disc.py`'s `/dev/srN` path (udisksctl reports the mount point with `\x20` escapes for spaces, which the script currently takes literally, breaking VIDEO_TS detection; passing the already-mounted path directly works around it).
- **See also:** entry 41, the Bonus Disc from the same set.

## 41. Life of Brian (Immaculate Edition) — Bonus Disc (DVD-Video)

- **matrix256:** `8948ddb848b10920e3a121b861da36c665d5be9a4e62e0887160804fd0b1a2b4`
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Immaculate Edition of Monty Python's Life of Brian (1979), it is the Special Features of a DVD/Special Features combo pack. Pairs with entry 40 as the extras-only half of the main-feature + bonus-disc arrangement — and sets a new corpus record for DVD VTS count: **14 IFOs hashed across 13 VTSes**, beating The Secret (entry 30, 12 VTSes). Bonus/special-features discs are the natural high end of this axis because each featurette or segment commonly gets its own VTS. Provider ID `LIFE_OF_BRIAN_DISC2` confirms the disc's role within the set, and the VMG disc-title is set to the full "Life of Brian: Bonus Disc" — another example of a properly-authored VMG title field.
- **See also:** entry 40, the main feature Disc 1 from the same set.

## Reproducing a fingerprint

For discs with an `.iso` available, the fingerprint is deterministic from the disc image alone:

```
python inspect_disc.py <path-to-iso>
```

For physical discs, pass the optical drive block device (`/dev/sr0`, `/dev/sr1`, …). The script loop-mounts the ISO or uses `udisksctl` to mount the block device read-only, runs selection and SHA-256, and unmounts on exit.

Open-content discs (Big Buck Bunny, Sintel) are freely downloadable from their respective project pages and should produce identical fingerprints to the values recorded here.

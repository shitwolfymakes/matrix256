# Evaluation corpus

Discs inspected with `inspect_disc.py` to exercise matrix256 against real-world inputs. Each entry records the computed **matrix256v1** fingerprint so any reproducer can verify their implementation against a known digest. The corpus is also where the IMPLEMENTERS.md §5 submission view (filesystem driver, mount options, reader info) is captured for each disc — two correct implementations walking different filesystem views of the same physical media will produce different (and individually correct) digests, so the view is part of the recorded fingerprint.

The corpus is not normative — matrix256's specification is the source of truth. These are illustrative fixtures covering open-content and commercial pressings, DVD and Blu-ray, HDMV-only and BD-J-heavy, protected and unprotected, plus a handful of data-disc combo-pack sides that the algorithm fingerprints alongside the more conventional video discs.

**Reference environment.** All fingerprints in this corpus were computed on Ubuntu 24.04.4 LTS (noble), using `inspect_disc.py` with the system's default UDF and ISO 9660 drivers and `udisksctl` for mount handling. The spec's reproducibility property guarantees the same digests on any correct implementation walking the same view, but the corpus values themselves are empirical artifacts of this specific environment. Divergence between a new implementation's output and a corpus value, on the same view, is evidence of either a spec bug or an environmental issue, not a property of the disc.

**About v0.** An earlier `matrix256v0` algorithm — a structural hash over a fixed list of named DVD/Blu-ray metadata files — was retired before publication; the corpus carried both v0 and v1 digests during the transition. v0 is no longer recorded here. Historical v0 digests remain recoverable from this repository's git history if cross-referencing a third-party catalog requires them.

## Summary

| # | Title | Type | matrix256v1 (first 16) |
|---|---|---|---|
| 1 | Big Buck Bunny | Blu-ray | `652e8189d14d260e` |
| 2 | Sintel | DVD-Video | `ee3ac7007f0854a3` |
| 3 | The Martian | Blu-ray | `202d14c8a8f22a16` |
| 4 | The Boondock Saints | Blu-ray | `16aed31722591f8c` |
| 5 | La La Land | Blu-ray | `a8493743e418c15d` |
| 6 | Suicide Squad (theatrical) | Blu-ray | `1c3290e7dbe2f253` |
| 7 | Suicide Squad: Extended Cut | Blu-ray | `c86815687c944160` |
| 8 | Silicon Valley S1 — Disc 1 | Blu-ray | `9e4edd18781705e7` |
| 9 | Silicon Valley S1 — Disc 2 | Blu-ray | `8fccea4677fbc629` |
| 10 | Silicon Valley S2 — Disc 1 | DVD-Video | `b06947aa46bc927c` |
| 11 | Silicon Valley S2 — Disc 2 | DVD-Video | `92c4aeb0fa558dbc` |
| 12 | Andromeda S1 — Disc 1 | DVD-Video | `0dbab021fa4446f0` |
| 13 | Andromeda S1 — Disc 2 | DVD-Video | `3b87f16a7539abea` |
| 14 | Andromeda S1 — Disc 3 | DVD-Video | `479ed6ecdcef0e9d` |
| 15 | Andromeda S1 — Disc 4 | DVD-Video | `5cb204ec0a49967a` |
| 16 | No Country for Old Men / Gone Baby Gone (double feature) | Blu-ray | `619dda39e24e39aa` |
| 17 | Afro Samurai | Blu-ray | `d84410cd34299fb0` |
| 18 | Four Brothers | DVD-Video | `a77e33ca0c738026` |
| 19 | Munich | DVD-Video | `0760f9c709df6718` |
| 20 | Argo | DVD-Video | `47f42927f02d465a` |
| 21 | American Gangster (seamless branching) | DVD-Video | `c0f274226217b48d` |
| 22 | Casablanca | DVD-Video | `29db4a6accb47857` |
| 23 | Pitch Perfect (Aca-Awesome Sing-Along) | DVD-Video | `65b1c4e21b0fb6c8` |
| 24 | Heat | DVD-Video | `0d8a97f7308923cb` |
| 25 | Stonehenge Apocalypse | DVD-Video | `dbf83e45a121e8f5` |
| 26 | Madso's War | DVD-Video | `b6cdc167580c7244` |
| 27 | VANish | DVD-Video | `278f7f7c002b81fa` |
| 28 | Treasure Guards | DVD-Video | `83adcfa241ca84d9` |
| 29 | The Reading Room | DVD-Video | `5bd8aa43f01060aa` |
| 30 | The Secret | DVD-Video | `702cf99802d9c162` |
| 31 | The Endless Summer | DVD-Video | `4a64da80ed64f91c` |
| 32 | Space Camp | DVD-Video | `f07436197a30b71f` |
| 33 | The Adventures of Milo and Otis | DVD-Video | `3633a182f1f833e2` |
| 34 | Space Odyssey: Voyage to the Planets | DVD-Video | `7bc44e82f9e2c2b5` |
| 35 | Five Fingers | DVD-Video | `0dd4d0aa7612f1e3` |
| 36 | Whiskey Tango Foxtrot | DVD-Video | `2c6b66a50b9b912f` |
| 37 | Whiskey Tango Foxtrot | Blu-ray | `fda666d139227a48` |
| 38 | Cowboys & Aliens | DVD-Video | `2a984e0bd35bec83` |
| 39 | Cowboys & Aliens | Blu-ray | `7c3a12dd0a1ecefc` |
| 40 | Life of Brian (Immaculate Edition) — Disc 1 | DVD-Video | `1516583b7e3dc8c3` |
| 41 | Life of Brian (Immaculate Edition) — Bonus Disc | DVD-Video | `3ee2344cc794c08a` |
| 42 | Interstellar | Blu-ray | `25ca634dbcdc9adb` |
| 43 | Interstellar Bonus Disc | Blu-ray | `263efa6d97eee52f` |
| 44 | Hancock (theatrical + extended) | Blu-ray | `ef93c20e21d3de00` |
| 45 | Hancock — Digital Copy | DVD-Video | `5ef8beb9e3a17675` |
| 46 | Rio | Blu-ray | `1015aa690bbca540` |
| 47 | Rio — Digital Copy | Data disc | `c9c14e70e279f5ac` |
| 48 | The Perks of Being a Wallflower | Blu-ray | `7cdd87bcf81522d9` |
| 49 | Wall Street: Money Never Sleeps | Blu-ray | `307da4dc33c152a2` |
| 50 | Sherlock Holmes | Blu-ray | `6f4703d22731e06c` |
| 51 | Sherlock Holmes: A Game of Shadows | DVD-Video | `f5054d9cfd64a2f8` |
| 52 | Sherlock Holmes: A Game of Shadows | Blu-ray | `6eb6ed7546f58372` |
| 53 | Star Trek | Blu-ray | `6e0ac21f4d92e589` |
| 54 | Star Trek — Special Features | Blu-ray | `a465de7abf2273ab` |
| 55 | Kingsman: The Secret Service | Blu-ray | `1b2ede79f6704b24` |
| 56 | Inglourious Basterds | Blu-ray | `1ad3f19fe7d33dee` |
| 57 | 9 (2009) | Blu-ray | `fbd0fc6db5840c37` |
| 58 | Heat (Director's Definitive Edition) | Blu-ray | `434000af52c57c30` |
| 59 | Heat DDE — Bonus Features | Blu-ray | `b62cc9414ccf6a1a` |
| 60 | Venom (2018) | Blu-ray | `7535ef82a812cf5b` |
| 61 | Venom: Let There Be Carnage | Blu-ray | `85582cedde959ba7` |
| 62 | Andromeda S1 — Disc 5 | DVD-Video | `c57955e9951b9109` |
| 63 | Andromeda S2 — Disc 1 | DVD-Video | `2633ef627235fd2c` |
| 64 | Andromeda S2 — Disc 4 | DVD-Video | `b4c613fea1af47b6` |
| 65 | Andromeda S2 — Disc 5 | DVD-Video | `312632a769502b38` |
| 66 | Andromeda S5 — Disc 3 | DVD-Video | `165a39a117c11220` |
| 67 | Andromeda S5 — Disc 4 | DVD-Video | `67df7f03d11c86ac` |
| 68 | Andromeda S3 — Disc 3 | DVD-Video | `542701a3d6b16d5c` |
| 69 | Andromeda S4 — Disc 2 | DVD-Video | `fe8dafb8bfc89d74` |

## 1. Big Buck Bunny (Blu-ray)

- **Source:** Blender Foundation, open content (https://peach.blender.org/)
- **matrix256v1:** `652e8189d14d260ea73e0e8e08848a455139e110b0655c56dd0cf42886f1499d`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `69C41314710953D5C34CBF0E01F20BC870CF704A`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 599 HDMV + 4 BD-J (4 "unsupported")
- **Why it's here:** Open content baseline. Ships an AACS directory (so libaacs surfaces a Disc ID) but isn't actually encrypted — a useful test for confirming matrix256v1 works identically whether or not decryption would be possible. Rich `BDMV/META/DL/bdmt_eng.xml` with named TOC entries, exercising the XML dump path in `inspect_disc.py`.

## 2. Sintel (DVD-Video)

- **Source:** Blender Foundation, open content (https://durian.blender.org/)
- **matrix256v1:** `ee3ac7007f0854a3ea43cc0ecd5a9991df129aad7a6ee6e74f1d2fa5e984940d`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** The DVD counterpart to Big Buck Bunny. Exercises the DVD path of the algorithm (VIDEO_TS.IFO + VTS_NN_0.IFO selection). Open content, so the ISO can be redistributed as a test fixture.

## 3. The Martian (Blu-ray)

- **matrix256v1:** `202d14c8a8f22a16dd52ba6dfd42b766cfb89eb9a769e413572def041873fb0d`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `C803CB1A9B5484B1B970378ED7E1D531DDB3276C`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 5 HDMV + 86 BD-J (86 "unsupported"); main title #70
- **Why it's here:** Commercial AACS+BD+ reference. Dozens of 7-second BD-J decoy playlists around the real movie (main title #70) — classic anti-rip pattern. Validates that matrix256v1 fingerprints are reproducible on fully protected discs without needing libaacs or any decrypt pass.

## 4. The Boondock Saints (Blu-ray)

- **matrix256v1:** `16aed31722591f8cd4aec0a0282c135a49ac365a2434bf490ecfcff767d4200f`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `AF3FA2FD3D2BCF0FF199D97C3BBA4EFE9BCCBB84`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 0 HDMV + 81 BD-J (81 "unsupported"); main title #36
- **Why it's here:** Pure BD-J disc — zero HDMV titles, playback is entirely Java-driven. Unusual authoring pattern; useful for confirming matrix256v1 doesn't depend on having any HDMV Movie Object content (the file is hashed because it exists, but its semantic role is minimal).

## 5. La La Land (Blu-ray)

- **matrix256v1:** `a8493743e418c15d677ed32855765f0b7c40a06a35e959a360951fa295426f44`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `A4E972BDF029F7E4CB48D75C96B2E5FC601D5229`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 93 HDMV + 10 BD-J (10 "unsupported"); main title #193
- **Why it's here:** Heavy-decoy HDMV disc — main title numbered #193 but only 103 titles exist, meaning the playlist/clip ID space is sparse (00001.mpls … 02756.clpi) with many filler entries. Largest file count in the corpus by ~3×; stress-tests ordering stability under a big, sparse numeric space. AACS without BD+ (Lionsgate).

## 6. Suicide Squad (Blu-ray)

- **matrix256v1:** `1c3290e7dbe2f2538d37f707f168a5aa600d54f5bb7d9b2ab9046c0f43beb033`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `85D565E111B07F774191EF7D82E579F61D62A94C`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 12 HDMV + 0 BD-J (0 "unsupported"); main title #27
- **Why it's here:** Pure HDMV authoring — zero bytes in `BDMV/JAR/` and `BDMV/BDJO/`. Together with The Boondock Saints (0 HDMV + 81 BD-J) it brackets the commercial authoring spectrum. AACS only, no BD+ (Warner).
- **See also:** entry 7, the Extended Cut pressing from the same 2-disc combo pack, for a direct theatrical-vs-extended comparison.

## 7. Suicide Squad: Extended Cut (Blu-ray)

- **matrix256v1:** `c86815687c944160cb74079368b42bfb1dbe04375d5eb99fa4486ad53947840c`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `C4C849323E97963B49014C6F5C12159F54182B21`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 12 HDMV + 0 BD-J (0 "unsupported"); main title #26
- **Why it's here:** The second disc of the Suicide Squad 2-disc combo pack — same studio, same authoring house, same protection profile, same pure-HDMV style as entry 6, but carrying the extended cut. matrix256v1 produces a digest completely distinct from the theatrical disc (`48dad7a2…` vs `c12f9c14…`), and Warner's AACS Disc ID also differs. This is the corpus's empirical demonstration of the README's "many fingerprints per title is expected" rationale: a fingerprint identifies a specific edition, not an abstract title. Structural differences that propagate into the hashed bytes include a shifted main title index (#26 vs #27), a different file count (86 vs 88), and a 750 MB smaller payload distribution across differently-sized clips.

## 8. Silicon Valley Season 1 — Disc 1 (Blu-ray)

- **matrix256v1:** `9e4edd18781705e74e089ae299dedd86c75d6d30cd5505555522c8b899748671`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `57163EBEC59D05A4A71F70723D0D6492EC5BC64A`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #12
- **Why it's here:** First TV-series disc in the corpus, addressing the README's "Box sets and TV series — empirical verification pending" Limitation. HBO-style authoring: mixed HDMV+BD-J with a lightweight Java menu layer over HDMV-driven episode playback, contrasting with Warner's pure-HDMV and Fox's pure-BD-J approaches. Many very-short (1s) playlist entries likely serve as per-episode intro cards or chapter-selection stubs.
- **See also:** entry 9, the Disc 2 sibling from the same set, for a box-set sibling-distinction data point.

## 9. Silicon Valley Season 1 — Disc 2 (Blu-ray)

- **matrix256v1:** `8fccea4677fbc629ec982690b9ddaa3eaf08fa8ed27ff9c51c591fbb61e7712e`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `D3915434FDCABA94F5E16BB9E5018EB7CC309F22`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #14
- **Why it's here:** The sibling of entry 8 from the same HBO box set. A single data point rather than empirical proof, but a useful one: two discs authored by the same house with identical title counts (2 HDMV + 79 BD-J both) and identical protection profile still produce cleanly distinct matrix256v1 digests. Structural differences that propagate into the hash: shifted main title index (#14 vs #12), slightly different clip mix (58 files vs 56), and different per-episode MPLS/CLPI content. Disc 2 carries a smaller payload (22.6 GB vs 43.5 GB), consistent with an uneven episode split across the set. More box sets would be needed to treat the "sibling discs produce distinct digests" property as confirmed rather than observed.

## 10. Silicon Valley Season 2 — Disc 1 (DVD-Video)

- **matrix256v1:** `b06947aa46bc927c595eac46329518b06df7f0989c9371f479294fd16296d45f`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 1 of the Silicon Valley season 2 DVD box set.
- **See also:** entry 11, the Disc 2 sibling from the same set.

## 11. Silicon Valley Season 2 — Disc 2 (DVD-Video)

- **matrix256v1:** `92c4aeb0fa558dbc9bf6ceb1ddd1b894cb972efd1189cb5624e7ac8c6bd0f049`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 2 of the Silicon Valley season 2 DVD box set.
- **See also:** entry 10, the Disc 1 sibling from the same set.

## 12. Andromeda Season 1 — Disc 1 (DVD-Video)

- **matrix256v1:** `0dbab021fa4446f0070ef937956474a565ae5981f3b1d7f7c52f5af4a14d36fe`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 1 of Season 1 of the Andromeda full series box set
- **See also:** entries 13, 14, 15, and 62 — the Disc 2, Disc 3, Disc 4, and Disc 5 siblings from the same set.

## 13. Andromeda Season 1 — Disc 2 (DVD-Video)

- **matrix256v1:** `3b87f16a7539abea039747fa155070a886e63230a7c51f943f7e496978292b67`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 2 of Season 1 of the Andromeda full series box set
- **See also:** entries 12, 14, 15, and 62 — the Disc 1, Disc 3, Disc 4, and Disc 5 siblings from the same set.

## 14. Andromeda Season 1 — Disc 3 (DVD-Video)

- **matrix256v1:** `479ed6ecdcef0e9d3979f1808310547b5b0191951f60bde49ead3a80fc182181`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 3 of Season 1 of the Andromeda full series box set
- **See also:** entries 12, 13, 15, and 62 — the Disc 1, Disc 2, Disc 4, and Disc 5 siblings from the same set.

## 15. Andromeda Season 1 — Disc 4 (DVD-Video)

- **matrix256v1:** `5cb204ec0a49967a99c4ccfaf551b56fa1faacdc6c9f5b6cc05fd2060175db84`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 4 of Season 1 of the Andromeda full series box set
- **See also:** entries 12, 13, 14, and 62 — the Disc 1, Disc 2, Disc 3, and Disc 5 siblings from the same set.

## 16. No Country For Old Men / Gone Baby Gone BD (Blu-ray)

- **matrix256v1:** `619dda39e24e39aaf684db381087dc00a96f38a818974d73a62502e87214468f`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `7BFBDC2177C6E3139FDE37AAF2FB424049BB654B`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 26 HDMV + 0 BD-J (0 "unsupported"); main title #8
- **Why it's here:** this is a double-feature bluray containing No Country for Old Men and Gone Baby Gone.

## 17. Afro Samurai (Blu-ray)

- **matrix256v1:** `d84410cd34299fb0f19c98cfa1b068a8fe8a06eeb8623a5ebb61aef165762623`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `F2A6F9BBE8A7060FF0FEF1D5F9623C8D8EB20EB4`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✗
- **Titles:** 29 HDMV + 0 BD-J (0 "unsupported"); main title #9
- **Why it's here:** This is the full series of Afro Samurai.

## 18. Four Brothers (DVD-Video)

- **matrix256v1:** `a77e33ca0c738026ee5678dea046094ba0e06c47a4813d9a0907dd822ec8b7c4`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** First commercial feature-film DVD in the corpus (prior commercial DVDs were TV-series box sets). Has the most VTSes (8) and the largest `VIDEO_TS.IFO` (22 KB) of any DVD in the corpus so far, exercising a broader slice of the DVD-Video navigation layout than the leaner box-set discs.

## 19. Munich (DVD-Video)

- **matrix256v1:** `0760f9c709df671806bdf18367c0dd5b7d1059fb0536d47ce1f7461d8090596e`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Minimal-VTS commercial feature-DVD — a dual-layer (DVD9) pressing where the entire 2h43m feature plus a short trailer live in just 3 VTSes, with `VTS_01_0.IFO` at 104 KB (second-largest IFO in the DVD corpus). Contrasts with Four Brothers (entry 18, 8 VTSes) as the simple-authoring end of the commercial-feature-DVD spectrum.

## 20. Argo (DVD-Video)

- **matrix256v1:** `47f42927f02d465a3b5638c3b0368b8602e8b8f49c27c42444a64429bbc3eb7e`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Second minimal-VTS commercial feature DVD in the corpus: like Munich (entry 19), a DVD9 Warner pressing with 3 VTSes and the entire feature (2h00m) living in `VTS_01`. Different `VTS_01_0.IFO` size (94 KB vs 104 KB) and different fingerprint despite the shared authoring pattern — another per-edition distinction data point. Title #5 / #6 audio-language fields carry non-UTF-8 bytes from the disc's raw IFO strings, which prompted a `errors="replace"` hardening in `inspect_disc.py`'s lsdvd subprocess decoding.

## 21. American Gangster (DVD-Video)

- **matrix256v1:** `c0f274226217b48df1fe3e5832337b12a1f0f83da1af32199f71a05cb54f5795`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** First seamless-branching disc in the corpus. A single VTS_01 carries the video payload for two distinct DVD titles — the 2h55m40s extended cut and the 2h36m49s theatrical cut — stitched together from different cell orderings (MakeMKV reports 30 segments per title, the classic seamless-branching signature). Exercises a DVD authoring pattern the corpus previously lacked: two alternate cuts co-resident on one disc via shared VOBs rather than separate VTSes (contrast with Suicide Squad theatrical/extended at entries 6-7, which ship on two discs).
- **Why the tools report it as "ASDF":** Neither lsdvd, MakeMKV, nor udisksctl surface the film title — they all fall back to "ASDF" because both the VMG disc-title field (inside `VIDEO_TS.IFO`) and the UDF volume name were left as that placeholder by Universal's authoring team. DVD-Video's VMG disc-title is a studio-populated string with no functional role in playback, so it's frequently shipped blank or placeholder — which is why `inspect_disc.py` can't recover the film title from the disc alone for this pressing.

## 22. Casablanca (DVD-Video)

- **matrix256v1:** `29db4a6accb47857c466954db48a2ddb816078e8c4fa1c0c0b8eb5efe09b0868`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Minimum-VTS commercial feature DVD — 2 IFOs hashed (`VIDEO_TS.IFO` + one `VTS_01_0.IFO`), the fewest of any commercial feature in the corpus. The 1h42m feature, a 36m44s bonus documentary, and ~10 short supplements all live in a single `VTS_01` with a dense `VTS_01_0.IFO` (116 KB) carrying the navigation for 14 chapter-addressed titles. Warner Home Video authoring, DVD9 payload. Sharpens the sparse end of the commercial-feature-DVD structural spectrum below Munich (entry 19, 3 VTSes) and Argo (entry 20, 3 VTSes).

## 23. Pitch Perfect (Aca-Awesome Sing-Along) (DVD-Video)

- **matrix256v1:** `65b1c4e21b0fb6c8f003b76e5e7c6f35e4833643efb89e07acc29b030f0ea1bc`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is the Aca-Awesome release of Pitch Perfect. Second seamless-branching disc in the corpus, but a different flavor than American Gangster (entry 21): both branches have identical duration (1h51m38s), same source VTS, same 35-segment map — the two titles are the same film played back with different default audio/subtitle selections (regular track vs sing-along). Confirms matrix256v1 handles seamless-branching authoring identically regardless of whether the branches differ in runtime or only in default stream picks.

## 24. Heat (DVD-Video)

- **matrix256v1:** `0d8a97f7308923cbbe1ea2c03e90f72ca426a27b6f386d559548924d70466a5f`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Second minimum-VTS commercial feature DVD — same single-VTS Warner Home Video authoring pattern as Casablanca (entry 22), different feature (2h50m vs 1h42m), more chapters (52 vs 36), slightly smaller `VTS_01_0.IFO` (110 KB vs 116 KB), distinct fingerprint. Gives the "minimum-VTS" axis two data points across very different eras (1942 catalog release vs 1995 theatrical). Notable curiosity: the UDF volume label `HEAT_16X9LB_DUAL_LAYER_NA` encodes the aspect ratio (16:9 letterbox), disc type (DVD9 dual layer), and region (North America) directly — one of the most descriptive volume labels in the corpus.
- **See also:** entry 58, the 2017 "Director's Definitive Edition" Blu-ray re-release of the same film — a cross-medium and cross-edition sibling.

## 25. Stonehenge Apocalypse (DVD-Video)

- **matrix256v1:** `dbf83e45a121e8f55cea704d023f343e93250dfed9bcf64f5bfef223b86b6ea2`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Here's an obscure, D-Tier movie called Stonehenge Apocalypse. First single-layer (DVD5) commercial feature in the corpus — total VOB payload is ~4.5 GB across 4 VTSes, comfortably fitting DVD5 capacity, where every previous commercial feature in the corpus is DVD9. Also notable: MakeMKV reports the disc name as "Stonehenge Apocalypse" (proper capitalisation, with space) rather than the UDF volume label, confirming the VMG disc-title field *is* populated correctly when studios bother to set it — a clean counterpoint to American Gangster (entry 21) where that same field was left as "ASDF".

## 26. Madso's War (DVD-Video)

- **matrix256v1:** `b6cdc167580c724453191a91e907bf31c6b30e437888bd1842638efc19c05016`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is called Madso's War. Second DVD5 commercial feature in the corpus (alongside Stonehenge Apocalypse, entry 25) — ~4.1 GB of VOB payload fitting single-layer capacity, a 1h25m feature, and five shallow VTSes with the feature material in `VTS_03`. Unlike Stonehenge Apocalypse, this pressing left the VMG disc-title field unset, so MakeMKV falls back to the UDF volume label `MADSOS_WAR` — another data point for the "VMG disc-title is studio-discretionary" observation (contrast entries 21 and 25).

## 27. VANish (DVD-Video)

- **matrix256v1:** `278f7f7c002b81fa9b49f9dcb946318a5c61f1b3bcda9d3d7ce3e921c0ea21db`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is VANish (2015).

## 28. Treasure Guards (DVD-Video)

- **matrix256v1:** `83adcfa241ca84d9521c3e021eb7a17c597063cc04f7c5cc416bb7623f8c6ad0`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Treasure Guards (2011). Third DVD5 commercial feature in the corpus (alongside entries 25 and 26) — ~3.9 GB payload across just 2 VTSes, the minimum VTS count for any DVD5 entry here. Also notable for audio/subtitle language codes reported as `xx` (unset) by lsdvd, unusual compared to the properly-tagged `en/es/fr` of higher-budget pressings — consistent with lean authoring on low-budget releases.

## 29. The Reading Room (DVD-Video)

- **matrix256v1:** `5bd8aa43f01060aa5073fed1172d1963512ebdff0cd7986d59ab82028d48b20c`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Reading Room (2005). Fourth DVD5 commercial feature in the corpus and a near-identical structural twin of Treasure Guards (entry 28): same 3-IFO / 2-VTS layout, `VTS_01_0.IFO` within 2 KB of its match (70 KB vs 72 KB), both `xx` audio/subtitle language codes, both with `Provider ID` set to the volume label — yet the two fingerprints differ completely. Sharpens the sibling-distinction observation at the low-budget template-authoring end of the DVD spectrum.

## 30. The Secret (DVD-Video)

- **matrix256v1:** `702cf99802d9c162633afe44b789f3d209f238f124f448bc06177cfc7abba267`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Secret (2006). Most VTSes of any DVD in the corpus — 12 VTSes and 13 IFOs hashed — yet still DVD5 (~4.2 GB total payload). Unusual authoring: the 1h30m feature lives in `VTS_05` (`VTS_05_0.IFO` 78 KB), while each short extra (from 30 seconds to 8 minutes) is isolated in its own dedicated VTS with an identical 18 KB IFO. Extends the high end of the DVD VTS-count axis (previous max was Four Brothers's 8 VTSes at entry 18).

## 31. The Endless Summer (DVD-Video)

- **matrix256v1:** `4a64da80ed64f91c9ad480601ab3ce0696ae5c98c88ef081d6d76ab0687949c6`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Endless Summer (1966). Sixth DVD5 commercial feature in the corpus, and the first disc carrying a true **mono (1-channel) audio track** — a 1966 surf documentary preserving its original single-channel mix, where every previous corpus disc ships stereo (2ch) or 5.1 (6ch). Structurally aligned with the 3-IFO / 2-VTS template of entries 28-29 but with a larger `VTS_01_0.IFO` (80 KB, reflecting the feature's 20 chapters) and a properly-tagged `en` language code — a counter-example to the "xx" unset pattern seen on other low-budget pressings.

## 32. Space Camp (DVD-Video)

- **matrix256v1:** `f07436197a30b71f176df359f2eff05e68a66aafc78cd6a337adcae8403af7b0`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Space Camp (1986). Seventh DVD5 commercial feature in the corpus — 3-IFO / 2-VTS layout shared with entries 28, 29, 31, but the first disc with a third-party authoring-house Provider ID (`LASERPACIFIC MEDIA CORPORATION`) rather than a studio name or a self-referential label. Minor but real axis: discs outsourced to a mastering vendor get the vendor's ID stamped into VMGI, distinct from the self-authored studio pattern (Warner Home Video etc.) and the "placeholder-equals-label" pattern of the very low-budget discs.

## 33. The Adventures of Milo and Otis (DVD-Video)

- **matrix256v1:** `3633a182f1f833e27262a54443b83d2f7dd5e12c32ca49c56f47cfca5fd56b03`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Adventures of Milo and Otis (1986) — specifically the American release, which is Columbia's re-cut-and-redubbed version of the 1986 Japanese film *Koneko Monogatari* (*The Adventures of Chatran*), with a shorter runtime, Dudley Moore narration, and new credits. That makes this disc a new regional-release axis: the underlying work is Japanese but the pressed edition is a distinct American derivative, with its own authoring chain and its own matrix256v1 digest independent of any Japanese or international pressing.
- **Structural note:** Cleanest DVD authoring in the corpus — 2 IFOs hashed, a single VTS, a single title, no bonus/extras/menus VTS at all; just the 1h15m feature and the VMG entry. An unusual VMG-disc-title pattern too: properly populated as "The Adventures of Milo and Otis" despite the UDF volume label being a generic default `DVD_VIDEO` (contrast American Gangster at entry 21, where *both* were placeholder, and Stonehenge Apocalypse at entry 25, where both were meaningful). Ideal floor on the authoring-complexity axis.

## 34. Space Odyssey: Voyage to the Planets (DVD-Video)

- **matrix256v1:** `7bc44e82f9e2c2b55c79f1032c8f24299d8cde17ddf30cf8eff2f09f8126d0d2`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is the dvd release of Space Odyssey: Voyage to the Planets (2004), a two-part docu-drama. Interesting play-all authoring: the disc exposes both the individual episodes (titles #9 and #10, ~59 minutes each) and a separate concatenated 1h57m "both episodes back-to-back" title (#8, exactly twice the episode runtime). `VTS_04_0.IFO` at 178 KB is unusually large, reflecting the extra navigation tables for this compound-title arrangement. Also a new label axis: the UDF volume name and VMG disc-title are both just `E2194`, a distributor catalog/SKU number — distinct from the studio, placeholder, title-as-label, and authoring-house patterns already in the corpus.

## 35. Five Fingers (DVD-Video)

- **matrix256v1:** `0dd4d0aa7612f1e37a6841d1852d1211b5c65097fd40ae6395bad00955200292`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Five Fingers (2006). Eighth DVD5 commercial feature in the corpus — 7 IFOs hashed, feature in `VTS_01` (~3.7 GB, `VTS_01_0.IFO` 70 KB — same size as entry 29), with five smaller VTSes carrying menus and short extras. Partial language-code tagging (feature is `en`, most bonus titles are `xx`) — a new pattern midway between the fully-tagged and fully-placeholder DVDs earlier in the corpus.

## 36. Whiskey Tango Foxtrot (DVD-Video)

- **matrix256v1:** `2c6b66a50b9b912f3a74b85c4699df68dddc7bd4ede9001d48e17557aeef3d30`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Whiskey Tango Foxtrot (2015), it is the DVD disk of a DVD/Blu-ray combo pack. First "combo-pack DVD side" data point in the corpus — a modern retail pattern where the same film ships on both formats in a single SKU, and the DVD side often has lighter authoring than a standalone DVD release. Structurally a standard DVD9 feature disc (6 IFOs, feature in `VTS_05` with a 72 KB IFO spanning 8 VOBs / ~6.4 GB), with MakeMKV reporting 3 segments on the main title — likely a layer-break cell split rather than seamless-branching.
- **See also:** entry 37, the Blu-ray side of the same combo pack — first cross-format sibling pair in the corpus.

## 37. Whiskey Tango Foxtrot (Blu-ray)

- **matrix256v1:** `fda666d139227a480e1c10a7249f60cb3911487fe28f6cd10e140c3bc61cace8`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `33BBB49A812E43775553DD8B45083CE9482AE63B`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 3 HDMV + 78 BD-J (78 "unsupported"); main title #1
- **Why it's here:** This movie is Whiskey Tango Foxtrot (2015), it is the Blu-ray disk of a DVD/Blu-ray combo pack. Paramount-style heavy-decoy authoring (only 3 HDMV titles but 78 BD-J "unsupported" playlists salted around the real movie) matching the pattern seen at entry 3 (The Martian) and entry 4 (The Boondock Saints). Pairs with entry 36, the DVD side of the same retail SKU, to form the corpus's first cross-format sibling — same film, same release, same authoring team, two different media with completely distinct structural fingerprints.
- **See also:** entry 36, the DVD side of the same combo pack.

## 38. Cowboys & Aliens (DVD-Video)

- **matrix256v1:** `2a984e0bd35bec8326cc53379ac4ec54e4819f38a48ecadb480603834fb27584`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Cowboys & Aliens (2011), it is the DVD disk of a DVD/Blu-ray combo pack. Second combo-pack DVD side in the corpus (after Whiskey Tango Foxtrot at entry 36) — same DVD9 + combo-pack authoring family but with more VTSes (9 IFOs hashed vs 6), with the feature in `VTS_08` (`VTS_08_0.IFO` 26 KB, 6.8 GB VOB span) and a dense `VTS_07_0.IFO` at 82 KB carrying the bonus-feature navigation. MakeMKV again reports 2 segments on the main title — likely the layer-break cell split consistent with entry 36's pattern.
- **See also:** entry 39, the Blu-ray side of the same combo pack.

## 39. Cowboys & Aliens (Blu-ray)

- **matrix256v1:** `7c3a12dd0a1ecefce874a0f0475c8ebcf2ad1136aa986c4cd6b4ef540f638643`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `9597816567B81882E27FE5321307D50630894626`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 6 HDMV + 75 BD-J (75 "unsupported"); main title #106
- **Why it's here:** This movie is Cowboys & Aliens (2011), it is the Blu-ray disk of a DVD/Blu-ray combo pack. Second cross-format sibling pair in the corpus — pairs with entry 38 (the DVD side of the same retail SKU) to reinforce that matrix256v1 distinguishes DVD and Blu-ray halves of combo packs even though the underlying film is identical. Heavy-decoy Universal-family authoring: only 6 HDMV titles but 75 BD-J "unsupported" playlists scattered throughout a sparse ID space (main title #106), echoing the pattern of entries 3 (The Martian), 4 (The Boondock Saints), and 37 (Whiskey Tango Foxtrot).
- **See also:** entry 38, the DVD side of the same combo pack.

## 40. Life of Brian (Immaculate Edition) — Disc 1 (DVD-Video)

- **matrix256v1:** `1516583b7e3dc8c387adda5a79ec86111a76abf1dd290baea1ad91181328b919`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Immaculate Edition of Monty Python's Life of Brian (1979), it is the DVD disk of a DVD/Special Features combo pack. Introduces a third multi-disc-set flavor into the corpus: not a TV box (entries 8-9, 10-11, 12-15), not a cross-format combo pack (entries 36-37, 38-39), but a *main-feature + bonus-disc* two-disc pairing — both are DVDs, but only one carries the movie and the other is entirely extras. Feature in `VTS_01` (~6.4 GB, 8 VOB split, 32 chapters), DVD9. Notable label quirk: the UDF volume identifier is the multi-field string `LIFE_OF_BRIAN_DISC1` while the volume *label* read by `lsblk` is the space-containing `Life of Brian` — this surfaced a latent bug in `inspect_disc.py`'s `/dev/srN` path (udisksctl reports the mount point with `\x20` escapes for spaces, which the script currently takes literally, breaking VIDEO_TS detection; passing the already-mounted path directly works around it).
- **See also:** entry 41, the Bonus Disc from the same set.

## 41. Life of Brian (Immaculate Edition) — Bonus Disc (DVD-Video)

- **matrix256v1:** `3ee2344cc794c08ad86d03ce080f8fd64f2a702b1fc53136ac7d42e377d64564`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is The Immaculate Edition of Monty Python's Life of Brian (1979), it is the Special Features of a DVD/Special Features combo pack. Pairs with entry 40 as the extras-only half of the main-feature + bonus-disc arrangement — and sets a new corpus record for DVD VTS count: **14 IFOs hashed across 13 VTSes**, beating The Secret (entry 30, 12 VTSes). Bonus/special-features discs are the natural high end of this axis because each featurette or segment commonly gets its own VTS. Provider ID `LIFE_OF_BRIAN_DISC2` confirms the disc's role within the set, and the VMG disc-title is set to the full "Life of Brian: Bonus Disc" — another example of a properly-authored VMG title field.
- **See also:** entry 40, the main feature Disc 1 from the same set.

## 42. Interstellar (Blu-ray)

- **matrix256v1:** `25ca634dbcdc9adb19b42ce6d638b2322ce927faeb05e50b966d088b87691141`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `B7D228759201D315B2294F41388450849DF3A7C3`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #8
- **Why it's here:** This movie is Interstellar (2014), it is the Blu-ray disk of a Blu-ray/Special Features combo pack. Paramount heavy-decoy authoring: only 2 HDMV titles but 79 BD-J "unsupported" playlists salted around the real movie (main title #8), matching the pattern of entries 3 (The Martian), 4 (The Boondock Saints), 37 (Whiskey Tango Foxtrot), and 39 (Cowboys & Aliens). Includes a `BDMV/META/DL/bdmt_eng.xml` disc-library record with jacket thumbnails, exercising the XML dump path — one of the few discs in the corpus to do so alongside Big Buck Bunny (entry 1).
- **See also:** entry 43, the Bonus Disc from the same combo pack.

## 43. Interstellar Bonus Disc (Blu-ray)

- **matrix256v1:** `263efa6d97eee52fb573fa8ca5c08d7adcc601c582822878dd1a280463f545e5`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `67FE296CE298C6A5DAB8C3AB9263CB99EA3C0023`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #15
- **Why it's here:** This movie is Interstellar (2014), it is the Special Features disk of a Blu-ray/Special Features combo pack. First main-feature + bonus-disc pair on **Blu-ray** in the corpus — pairs with entry 42 to form the Blu-ray analogue of the Life of Brian DVD pairing at entries 40/41. The bonus disc shares the main feature's exact authoring skeleton (same 00002-00077 MPLS/CLPI decoy block, same 00100/00120 menu entries, same 01000/01001 18.9 KB playlists, identical 79 BD-J "unsupported" count) but appends a dedicated 00201-00219 range carrying the real special-features content: a 50m20s primary featurette (main title #15 → `00201.mpls`) plus 18 shorter segments ranging 2m-14m. Useful empirical data for the observation that studios ship the *same* BD-J menu skeleton across both discs of a set and let the BDMV payload differ — matrix256v1 cleanly distinguishes them (`644e3378…` vs `4de5afe5…`) because the extra MPLS/CLPI entries propagate into the hash.

## 44. Hancock (Blu-ray)

- **matrix256v1:** `ef93c20e21d3de00e13d79296a7f844b959aefb4c006c4559660a14e207e2ee0`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `358B99E382B0FA7AAEB2E45246AB96CD6803E961`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 495 HDMV + 5 BD-J (5 "unsupported"); main title #161
- **Why it's here:** This movie is Hancock (2008), it is the Blu-ray disk of a Blu-ray/Special Features combo pack. This disk contains both theatrical and extended editions. New axes for the corpus: (1) **theatrical + extended cut on the same disc** — unlike the Suicide Squad pair at entries 6-7, where the two cuts ship as separate pressings, Hancock carries both 1h32m (theatrical) and 1h42m (extended) as adjacent HDMV titles #160-163 (two duration-variants × two angle-variants), sharing VOB cells between them; and (2) **largest HDMV title count in the corpus by a wide margin** — 495 HDMV titles versus the prior max of 93 at La La Land (entry 5) — Sony Pictures extreme-decoy authoring with hundreds of 6-second MPLS stubs. Also the first corpus disc whose libbluray-reported name carries a **™** trademark glyph (`Hancock - Blu-ray™`), a Sony-specific display-name convention.
- **See also:** entry 45, the Digital Copy disc from the same combo pack.

## 45. Hancock Bonus Disc — Digital Copy (DVD-Video)

- **matrix256v1:** `5ef8beb9e3a17675f9298f2c434c65d24bb2c0d10f302d565a65782bcfd4a0ab`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout (stub) + `Movies/` directory carrying the real payload
- **Why it's here:** This movie is Hancock (2008), it is the Digital Copy bonus disk of a Blu-ray/Digital Copy combo pack. First **Digital Copy disc** in the corpus and the first **hybrid layout** captured here — a token DVD-Video facade hiding a sideload payload. The disc root carries an 874 MB `Movies/HancockBD_2008_PC.wmv` (PC sideloading), a 727 MB `Movies/MAQ00579.MGV` (portable devices), and a `bonuscopy.exe` Windows installer with autorun, while the `VIDEO_TS/` tree alongside it carries only a token 30 MB of menu/stub VOBs across 3 short titles (27s, 15s, 16s) — exactly enough to make the disc appear as a valid DVD to players that probe for `VIDEO_TS.IFO`. matrix256v1 walks the entire layout (the 4 stub IFOs *and* the `Movies/` payload), so the digest reflects the disc as it really ships, not just the DVD-Video facade. Smallest-IFO VIDEO_TS in the corpus (previous floor: Milo and Otis at entry 33, 2 IFOs but a 2.6 GB VOB feature).
- **See also:** entry 44, the main-feature Blu-ray side of the same combo pack.

## 46. Rio (Blu-ray)

- **matrix256v1:** `1015aa690bbca5403946a39e50d092cd8016a32769fb5757b0444b2c67438e60`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `2B04F0049EC70196BCFC2199A047A6E849B84A4F`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 5 HDMV + 86 BD-J (86 "unsupported"); main title #85
- **Why it's here:** This movie is Rio (2011), it is the Blu-ray disk of a Blu-ray/Digital Copy combo pack. Only the second AACS + BD+ + BD-J triple-protection disc in the corpus after The Martian (entry 3) — the full commercial-protection stack, not the AACS-only or AACS+BD-J flavors that dominate the rest. Also the **largest BD-J payload** in the corpus so far: 151.5 MB of `BDMV/JAR/` (previous max: The Martian at 47 MB), consistent with Fox/Blue Sky Studios' BD-Live-heavy authoring for animated releases. UDF volume label `RIO_FD` (likely "Rio Feature Disc") is another distributor-SKU-style label similar to entry 34.
- **See also:** entry 47, the Digital Copy disc from the same combo pack.

## 47. Rio Digital Copy (Data disc)

- **matrix256v1:** `c9c14e70e279f5ac0d03eb4ada2b581627576de1a0139207a8b757620eb65b33`
- **Filesystem view:** iso9660 on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,norock,check=r,map=n,blocksize=2048,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Filesystem:** ISO 9660 (not UDF), volume label `Fox Digital Copy`
- **Structure:** pure Windows/iTunes sideload layout — `Autorun.inf` + `Click to START.bat` at the root, a Windows-installer `DVDROM/menu.exe` (12 MB), a `DVDROM/iTunesInfo.xml` manifest, and a `DVDROM/Media/` directory carrying three video files: a 1.4 GB `FeatureMovie` (iTunes sideload), a 1.1 GB `Rio.wmv` (PC Windows Media), and a 488 MB `Rio - Portable.wmv` (portable-device Windows Media).
- **Why it's here:** This movie is Rio (2011), it is the Digital Copy disk of a Blu-ray/Digital Copy combo pack. **First non-DVD/non-BD optical disc in the corpus** — there is no `VIDEO_TS/` or `BDMV/` directory tree anywhere on the disc; it's a conventional iso9660 data carrier for a Windows sideloading installer and its accompanying media payload. matrix256v1 fingerprints it cleanly because the algorithm is filesystem-agnostic — the absence of a DVD-Video or Blu-ray skeleton is irrelevant to a `(path, size)` walk. Concrete demonstration that combo-pack Digital Copy sides authored as pure data discs are well within v1's reach, alongside the Hancock Digital Copy (entry 45) which takes the *opposite* route — keeping a stub `VIDEO_TS/` facade so DVD players accept the disc, while hiding the real payload under `Movies/`. Together the two entries bracket the Digital Copy authoring spectrum: hybrid-DVD-facade (Hancock) versus pure-data-disc (Rio).
- **See also:** entry 46, the Blu-ray side of the same combo pack.

## 48. The Perks of Being a Wallflower (Blu-ray)

- **matrix256v1:** `7cdd87bcf81522d90367fd3d5251f5ecea88f0f196acef447fc1ec33b7fa3b0f`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `45A6A92DF2ABCB9F12FD801942715A4262F318AF`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 1 HDMV + 2 BD-J (2 "unsupported"); main title #5
- **Why it's here:** This movie is The Perks of Being a Wallflower (2012). **Lowest title-object count** of any commercial Blu-ray in the corpus (1 HDMV + 2 BD-J = 3 total), but libbluray still walks 70+ playlists — a clean demonstration that BDMV object counts and MPLS counts measure different things (object = Movie Object / BD-J entrypoint; MPLS = playlist). Minimal BD-J footprint (5.6 MB JAR, 990 B BDJO) compared to the Fox/Warner BD-J-heavy discs earlier in the corpus. Summit/Lionsgate authoring with only a single pair of `00173.mpls`/`00174.mpls` and `00175.mpls`/`00176.mpls` duplicated playlists (likely a seamless-branching artifact for the special features). Second corpus disc whose libbluray display name carries a **™** glyph after Hancock (entry 44), but this is Summit Entertainment rather than Sony — the ™-in-display-name pattern is clearly multi-studio.

## 49. Wall Street: Money Never Sleeps (Blu-ray)

- **matrix256v1:** `307da4dc33c152a273475f1540c485550139680ee4dae97845904f28017138f5`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `759BE8DD378DA5CFABEFFDE04A6D1B47F1CEB466`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 1 HDMV + 89 BD-J (89 "unsupported"); main title #23
- **Why it's here:** This movie is Wall Street: Money Never Sleeps (2010). Third AACS + BD+ + BD-J triple-protection disc in the corpus after The Martian (entry 3) and Rio (entry 46) — enough data points to establish triple-protection as a real authoring pattern rather than an outlier. Sony Pictures (20th Century Fox distribution pre-merger era) BD-J-heavy authoring with 89 BD-J "unsupported" playlists behind a single HDMV entrypoint, and 63.9 MB of BD-J jars — mid-range for the heavy-BD-J studio discs (between The Martian at 47 MB and Rio at 151.5 MB). Volume label `WALL_STREET_2` is another "film-title + sequel-index" style label (the film is Wall Street's sequel; the "2" encodes that, not a disc number).

## 50. Sherlock Holmes (Blu-ray)

- **matrix256v1:** `6f4703d22731e06cfa651e2c5b28f3951ca4a7e7c2784459139cf957ac8797e0`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `0428B276B4B31A03F05E896F5BCD8251A1B583B0`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 13 HDMV + 7 BD-J (7 "unsupported"); main title #1
- **Why it's here:** This movie is Sherlock Holmes (2009). **Minimal MovieObject.bdmv** in the corpus at 250 bytes (alongside a 348 B `index.bdmv`) — versus the 38-99 KB seen on other HDMV-heavy discs — consistent with Warner's practice of running the disc mostly through BD-J while keeping the HDMV Movie Object stub-like. Still, 13 HDMV titles are addressable via those minimal objects, including the main feature at #1, making this a useful counterpoint to The Boondock Saints (entry 4, 0 HDMV) and the extreme-HDMV Hancock (entry 44, 495 HDMV). Second-largest BD-J jar payload in the corpus (90.0 MB, between Wall Street at 63.9 MB and Rio at 151.5 MB). Volume label carries a space (`SHERLOCK HOLMES` → `/media/wolfy/SHERLOCK HOLMES`), a live check that the udisksctl `\x20`-escape fix (committed earlier in the project) is still working.

## 51. Sherlock Holmes: A Game of Shadows (DVD-Video)

- **matrix256v1:** `f5054d9cfd64a2f87fc111e40e5f046507a8d1f79548a4b3cd8ec71b3f3d1942`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This movie is Sherlock Holmes: A Game of Shadows (2011), it is the DVD disk of a Blu-ray/DVD combo pack. Third combo-pack DVD-side entry in the corpus after Whiskey Tango Foxtrot (entry 36) and Cowboys & Aliens (entry 38). Warner Home Video authoring with a DVD9 pressing (VTS_01's feature spans 7 VOBs hitting the 1 GB split boundary seven times, ~7.1 GB total), 2h08m feature in title #1, and a second (84 KB) `VTS_01_0.IFO` among the larger navigation tables in the DVD portion of the corpus. Titles 4, 5, and 9 show replacement-character audio/subtitle language tags (`��`) from non-UTF-8 bytes in the raw IFO strings — a live re-triggering of the `errors="replace"` hardening first added for Argo (entry 20). Note: despite the shared "Sherlock Holmes" franchise name, this is **not** a sibling of entry 50 (the 2009 first film is a different release on a different medium).
- **See also:** entry 52, the Blu-ray side of the same combo pack.

## 52. Sherlock Holmes: A Game of Shadows (Blu-ray)

- **matrix256v1:** `6eb6ed7546f58372ca93b3d74875540c07b95d5a27bbe0bc957a9a2923941e54`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `7C9AE4D1301AF39884E662F268CC21E37DDADA1D`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 33 HDMV + 8 BD-J (8 "unsupported"); main title #28
- **Why it's here:** This movie is Sherlock Holmes: A Game of Shadows (2011), it is the Blu-ray disk of a Blu-ray/DVD combo pack. **New corpus record for file count hashed** — 544 files, beating La La Land's prior 514 (entry 5). Warner authoring with the same stub-objects pattern seen on the first Sherlock Holmes (entry 50): a tiny 600 B `index.bdmv` and 706 B `MovieObject.bdmv` routing 33 HDMV titles primarily through a BD-J layer. Third combo-pack cross-format sibling pair in the corpus after Whiskey Tango Foxtrot (entries 36/37) and Cowboys & Aliens (entries 38/39), this time pairing with entry 51 (the DVD side). Volume label `SHERLOCK_2` matches the "film-title + sequel-index" convention also seen at Wall Street: Money Never Sleeps (entry 49, `WALL_STREET_2`) — three data points now for this label style.
- **See also:** entry 51, the DVD side of the same combo pack.

## 53. Star Trek (Blu-ray)

- **matrix256v1:** `6e0ac21f4d92e5899941412426f5d7b6166bb4d084422ef388fa0d1fe62c66ed`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `DB9E3EC5301078F3838AD6B6A1BDE03BF718A2EF`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #2
- **Why it's here:** This movie is Star Trek (2009), it is the Blu-ray disk of a Blu-ray/Special Features combo pack. This disk lists the contents as the Feature Film and Special Features. **Smallest file count for any commercial Blu-ray in the corpus** (47 files, beating Silicon Valley S1 Disc 1 at 56, entry 8) — Paramount/Bad Robot authoring routes the entire disc through a lean BDMV layout with only 22 MPLS entries and 23 CLPI entries behind a classic 2-HDMV + 79-BD-J heavy-decoy pattern (identical title-count signature to Interstellar at entry 42, another Paramount release). Main feature is title #2 at `00000.mpls`, a rare "main feature at playlist zero" choice that yields an unusually large 53.8 KB `CLIPINF/00000.clpi` (the largest CLPI in this entry). The UDF volume label is `STARTREK11D1AC` — a new label convention for the corpus: `STARTREK11` names the film by its **franchise-film number** (Star Trek 2009 is the 11th Trek feature, informally Star Trek XI), `D1` is Paramount's disc-in-set index, and `AC` likely encodes a regional or authoring-variant code. The disc also self-identifies as "Star Trek Disc 1" in libbluray / makemkv / `BDMV/META/DL/bdmt_eng.xml`, even though the user's combo-pack framing describes it as just the Blu-ray side of a Blu-ray/Special Features pairing.
- **See also:** entry 54, which was in the same case when this set was bought secondhand. The two discs may or may not originate from the same retail pressing — see the provenance note on entry 54.

## 54. Star Trek — Special Features (Blu-ray)

- **matrix256v1:** `a465de7abf2273abbba55d1f176b9ba125b1ac5d7345113c554b119c2b9eb550`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `3AC37FE2F91568AF8196929D3EBCE4391A0FE5AB`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 1 HDMV + 4 BD-J (4 "unsupported"); main title #12
- **Why it's here:** This movie is Star Trek (2009), it is the Special Features disk of a Blu-ray/Special Features combo pack. This disk lists the contents as Special Features. Useful contrast with the Interstellar Blu-ray + bonus-disc pair at entries 42/43: where Interstellar's two discs share an essentially identical BDMV skeleton, this disc and entry 53 produce cleanly distinct layouts — entry 53 carries 47 files, this one carries **235** (a 5× file-count jump for the special-features-only disc), and their MPLS/CLPI number ranges don't overlap at all (entry 53 occupies 00000-00015 + 00998-01007; this disc occupies 00000-00083 + 00100 + 00301-00355 + 00050-00057). The UDF volume label is `STARTREKXI_D2_AC` — Roman-numeral "XI" with underscores — where entry 53's label was `STARTREK11D1AC` (Arabic-numeral "11", no underscores). The STREAM payload happens to be exactly the same 38.67 GB on both discs, likely coincidence but worth flagging.
- **Provenance caveat:** this disc and entry 53 were together in one Blu-ray case when bought **secondhand**, so the original pressing-pairing can't be assumed. The label-format mismatch (`STARTREK11` Arabic vs `STARTREKXI` Roman; `D1AC` concatenated vs `_D2_AC` with underscores) is consistent with two discs from *different* retail SKUs that a previous owner consolidated into one case, rather than a single Paramount authoring pipeline shipping inconsistent label formats. Treat the corpus-pair framing as "these two discs currently function together as a Star Trek 2009 Blu-ray set", not as "these two discs were pressed together in one SKU."
- **See also:** entry 53, which was in the same case when this set was bought secondhand.

## 55. Kingsman: The Secret Service (Blu-ray)

- **matrix256v1:** `1b2ede79f6704b248accf9534d56158df6f4ac913312b47f4612dbf9d6f6ddbc`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `6B20E607ADEB48E70B4957009A7D55F77177A5C7`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 5 HDMV + 86 BD-J (86 "unsupported"); main title #82
- **Why it's here:** This movie is Kingsman: The Secret Service (2014). Fourth AACS + BD+ + BD-J triple-protection disc in the corpus after The Martian (entry 3), Rio (entry 46), and Wall Street: Money Never Sleeps (entry 49) — and the first triple-protection disc from 20th Century Fox. Paramount-style heavy-decoy authoring (5 HDMV + 86 BD-J "unsupported", main feature buried at title #82) on a large 44.68 GB payload. Two genuinely unusual `BDMV/META/DL/bdmt_eng.xml` quirks: (1) the jacket thumbnails are named `Metadata_NOT_YET_APPROVED.jpg` / `Metadata_NOT_YET_APPROVED_sml.jpg`, a clear authoring-pipeline placeholder that leaked into the pressed disc — suggesting this pressing went out before the final approved cover art was delivered; (2) the disc library TOC populates *three* title entries (`titleNumber="1"`, `"2"`, `"3"`) all with the same name "Kingsman: The Secret Service", where most corpus discs set only title 1. Second corpus disc whose UDF volume label contains a space (`Kingsman - The Secret Service`) after Sherlock Holmes (entry 50) — another live exercise of the `\x20`-escape fix in `inspect_disc.py`.

## 56. Inglourious Basterds (Blu-ray)

- **matrix256v1:** `1ad3f19fe7d33deebb834fd73e0e55a686696b82b6be422c4caf68cb5d61a515`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `7C7D5E77A01D02B281852AB291780D5D9099E140`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #67
- **Why it's here:** This movie is Inglorious Basterds (2009). Note the disc reports the title as "Inglourious Basterds" — Tarantino's intentional misspelling of both words — matching the film's official title rather than the common-usage spelling. The **2 HDMV + 79 BD-J title-count signature** now appears on four corpus discs (alongside Interstellar at entry 42, its Bonus Disc at entry 43, and Star Trek at entry 53), crossing Paramount (Interstellar/Star Trek) and Universal (Inglourious Basterds) — enough data points to treat 2+79 as a cross-studio authoring template, not a single-studio fingerprint. UDF volume label `ING_BASTERDS` is a new label convention for the corpus: a space-free abbreviation of the film title, distinct from the existing catalog-SKU (`E2194`), franchise-numbered (`STARTREK11D1AC`), and spelled-out-with-spaces (`Kingsman - The Secret Service`) styles.

## 57. 9 (Blu-ray)

- **matrix256v1:** `fbd0fc6db5840c370a2f4ae5d5bb0974c7e0aff1860d088b91bd2693e849ea77`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `90F0D1833F56BB9E701E3820BA2C4B2E160B3A37`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 2 HDMV + 79 BD-J (79 "unsupported"); main title #41
- **Why it's here:** This movie is 9 (2009). **Fifth corpus disc with the 2 HDMV + 79 BD-J title-count signature** (after Interstellar at entry 42, its Bonus Disc at entry 43, Star Trek at 53, and Inglourious Basterds at 56) — and the first Focus Features release to exhibit it, widening the "2+79 is a cross-studio authoring template" observation to three distinct studios. Also **the shortest disc name and UDF volume label in the corpus**: the film's title is literally the single character `9`, and the disc carries that same single character as both the libbluray/makemkv `Disc name` and the UDF volume label. Small STREAM payload for a commercial Blu-ray feature (29.58 GB, smaller than most feature-film BDs in the corpus — consistent with the film's 79-minute runtime, the shortest feature in the Blu-ray half of the corpus).

## 58. Heat — Director's Definitive Edition (Blu-ray)

- **matrix256v1:** `434000af52c57c30bcde66734a35f1058882ba3b2b65df961dd1933d1c1fd8e1`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `772F1358D1D5EFEC47D05C80E4AC19F94F06D9EF`
- **Protection:** AACS ✓, BD+ ✓, BD-J ✓
- **Titles:** 5 HDMV + 86 BD-J (86 "unsupported"); main title #67
- **Why it's here:** This movie is the Director's Definitive Edition of Heat (1995), it is the Blu-ray disk of a Blu-ray/Special Features combo pack. **Introduces a new sibling-relationship axis to the corpus**: cross-medium *and* cross-edition. Previous pair categories include same-edition-different-media (entries 36/37 WTF, 38/39 Cowboys & Aliens, 51/52 Sherlock 2 — all DVD/BD combo pairs), different-edition-same-medium (entries 6/7 Suicide Squad theatrical/extended, both Blu-ray), and main-feature/bonus-disc pairs (entries 40/41 Life of Brian, 42/43 Interstellar). Heat at entry 24 (standard 1995 DVD release, Warner Home Video) and this disc (2017 Director's Definitive Edition Blu-ray, Fox) share the same film but differ on both axes at once. Fifth AACS + BD+ + BD-J triple-protection disc in the corpus (after The Martian entry 3, Rio entry 46, Wall Street entry 49, Kingsman entry 55). The 5 HDMV + 86 BD-J title-count signature matches The Martian and Kingsman exactly — three data points now for this specific signature across three studios (Fox/Lionsgate/Paramount-distribution). UDF volume label `HEAT_D1` matches the Paramount-style `<TITLE>_D1` convention from Star Trek (entry 53, `STARTREK11D1AC`); the Director's Definitive Edition is indeed a 2-disc set (confirmed by entry 59), with the user's "Blu-ray/Special Features" combo-pack framing corresponding to a main-feature Blu-ray + Bonus Features Blu-ray pairing.
- **See also:** entry 24, the 1995 standard DVD release of the same film — same film, different edition, different medium. Also entry 59, the Bonus Features disc from this same Director's Definitive Edition set.

## 59. Heat — Director's Definitive Edition Bonus Features (Blu-ray)

- **matrix256v1:** `b62cc9414ccf6a1a4a0bc7019a7f1a5e833b573094fd123b73049d01b3503849`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `D843BBB357ED10278548030A5561A96640094772`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 5 HDMV + 86 BD-J (86 "unsupported"); main title #71
- **Why it's here:** This movie is the Director's Definitive Edition of Heat (1995), it is the Bonus Features disk of a Blu-ray/Special Features combo pack. Third main-feature + bonus-disc Blu-ray pair in the corpus after Interstellar (entries 42/43) and Star Trek (entries 53/54). **Notable protection asymmetry** between the two discs in this set: entry 58 (main feature) carries full AACS + BD+ + BD-J triple protection, while this bonus disc ships with AACS + BD-J only (no BD+) — new data point for the corpus that **BD+ can be applied selectively within a multi-disc retail set**, presumably because BD+'s additional licensing/content-protection cost is only worth paying on the disc that carries the feature-film payload. **Same 5 HDMV + 86 BD-J title-count signature** as entry 58, and UDF label `HEAT_D2` matches the `HEAT_D1` format exactly — unlike the Star Trek pair (entries 53/54) whose two discs showed distinct title-count signatures and mismatched label formats, Paramount's Heat DDE pair is internally consistent and clearly authored as one pipeline. Both discs self-identify with distinct libbluray `Disc name` values — "Heat" and "Heat - Disc 2" — an unusual asymmetry (the first disc is unlabeled while the second carries the set-position suffix).
- **See also:** entry 58, the main-feature Blu-ray from this same Director's Definitive Edition set.

## 60. Venom (Blu-ray)

- **matrix256v1:** `7535ef82a812cf5b52dfd11884025a2267993d1b34d75436260d23e122f50c28`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `CE9F1725BA742084CE125EB949059150B870C2D3`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 16 HDMV + 4 BD-J (4 "unsupported"); main title #179
- **Why it's here:** This movie is Venom (2018). Sony/Columbia heavy-HDMV-decoy authoring — 16 HDMV + 4 BD-J with the main feature buried at title #179 in an otherwise sparse ID space — in the same family as Hancock (entry 44, 495 HDMV + 5 BD-J, main at #161) and La La Land (entry 5, 93 HDMV + 10 BD-J, main at #193). Third-largest file count in the corpus at 393, behind only Sherlock Holmes: A Game of Shadows (entry 52, 544) and La La Land (entry 5, 514). Third corpus disc whose libbluray-reported `Disc name` carries a `™` glyph after Hancock (44) and The Perks of Being a Wallflower (48), confirming the pattern is a shared "Blu-ray™" Sony/Summit/Paramount display-name convention across studios. **New non-ASCII character case**: the reported name `Venom (2018) – Blu-ray™` uses a typographic **en dash** (U+2013) as the separator between title and format, rather than the em dash (U+2014) or ASCII hyphen-minus seen elsewhere — the second distinct non-ASCII dash observed in a disc-name field, exercising the UTF-8 handling in `inspect_disc.py` without incident.

## 61. Venom: Let There Be Carnage (Blu-ray)

- **matrix256v1:** `85582cedde959ba7fa0f124f3d298087078177cc4ebbbbb10c1cf66164782570`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **AACS Disc ID:** `7A5CA107FEAADF04CF1731DFBF42F39EC90954A1`
- **Protection:** AACS ✓, BD+ ✗, BD-J ✓
- **Titles:** 17 HDMV + 3 BD-J (3 "unsupported"); main title #94
- **Why it's here:** This movie is Venom: Let There Be Carnage (2021). Sequel to entry 60 (same franchise, different film, distinct retail pressing with its own Disc ID and fingerprint — not a matrix256v1 sibling in the corpus's normal pair sense, since the two are separate films rather than same-film-different-edition/medium). Sony/Columbia authoring pattern matches Venom 1 closely — heavy-HDMV-decoy style, 17 HDMV + 3 BD-J with the main feature at title #94, and 396 files hashed versus entry 60's 393 (within 1% of each other, suggesting both discs came off Sony's common BDMV template three years apart). **Notable dash inconsistency within the Sony "Blu-ray™" display-name convention**: this disc carries name `Venom: Let There Be Carnage - Blu-ray™` using an ASCII hyphen-minus (`-`, U+002D), where entry 60 (Venom 2018) used an en dash (`–`, U+2013). Same studio, same franchise, different authoring detail — a data point that the ™-suffix convention isn't character-consistent across even a single franchise.

## 62. Andromeda Season 1 — Disc 5 (DVD-Video)

- **matrix256v1:** `c57955e9951b9109ff662921649af1e4f98c2181450736727451b10823728ad0`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** Final disc of the Andromeda Season 1 box set, completing the five-disc set that began at entries 12–15. All five Season 1 discs share the same 3-VTS authoring (`VIDEO_TS.IFO` + `VTS_01..03_0.IFO` plus the matching `.BUP`s and `.VOB` payloads), so the matrix256v1 digests distinguish them on the full filesystem layout — IFO content, BUP content, VOB sizes, and any per-disc menu graphics — rather than purely on IFO bytes.
- **See also:** entries 12, 13, 14, and 15 — the Disc 1, Disc 2, Disc 3, and Disc 4 siblings from the same set.

## 63. Andromeda Season 2 — Disc 1 (DVD-Video)

- **matrix256v1:** `2633ef627235fd2cd496a0f06dac3cae74915b367fc6dbfd97755a6e8a746fcc`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** First Season 2 disc from the Andromeda full-series box set, paired by franchise with the Season 1 set at entries 12, 13, 14, 15, and 62. Despite coming from the same studio's TV-on-DVD release, Season 2 uses a different authoring template: 6 VTSes (7 files hashed — VIDEO_TS.IFO + VTS_01..06_0.IFO) versus Season 1's uniform 3-VTS layout (4 files hashed). A cross-season-within-a-set data point: matrix256v1 fingerprints don't just distinguish individual discs, they also surface authoring-pipeline shifts between seasons of the same series.
- **See also:** entries 64 and 65 — the Disc 4 and Disc 5 siblings from the same Season 2 set.

## 64. Andromeda Season 2 — Disc 4 (DVD-Video)

- **matrix256v1:** `b4c613fea1af47b665d6154685a72c90129d464fef60423c9b0135546f304484`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 9 of the Andromeda full series box set, containing Season 2 Episodes 16-20. Confirms the Season-2 authoring observation made at entry 63: same 6-VTS layout (7 files hashed — VIDEO_TS.IFO + VTS_01..06_0.IFO), distinct from the uniform 3-VTS layout shared by all five Season 1 discs (entries 12–15, 62). With two Season 2 discs now in the corpus, the "different authoring template per season" claim moves from a single-data-point observation to a confirmed pattern within this box set.
- **See also:** entries 63 and 65 — the Disc 1 and Disc 5 siblings from the same Season 2 set.

## 65. Andromeda Season 2 — Disc 5 (DVD-Video)

- **matrix256v1:** `312632a769502b387ec169ac7c6a1e23abe9de62d8e0e91fac4e69877ce80f17`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 10 of the Andromeda full series box set, containing Season 2 Episodes 21-22. Final Season 2 disc and the third Season 2 entry, alongside entries 63 (Disc 1) and 64 (Disc 4). Despite holding only the last two episodes plus presumed bonus material — a notably lighter content load than the other Season 2 discs — it still uses the same 6-VTS authoring template (7 files hashed: VIDEO_TS.IFO + VTS_01..06_0.IFO). Confirms the authoring template is stable across the entire Season 2 set, regardless of how full each disc actually is — a useful demonstration that matrix256v1's hashed-file count reflects the authoring shape, not the payload size.
- **See also:** entries 63 and 64 — the Disc 1 and Disc 4 siblings from the same Season 2 set.

## 66. Andromeda Season 5 — Disc 3 (DVD-Video)

- **matrix256v1:** `165a39a117c11220be1d0877ad4aa9c34ab46f4e9ddb67ed001a376fb7fc68e4`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 23 of the Andromeda full series box set, containing Season 5 Episodes 14-18. First Season 5 disc in the corpus, jumping past Seasons 3 and 4 to give the corpus a wider view of the box set's authoring history. Same 6-VTS template (7 files hashed: VIDEO_TS.IFO + VTS_01..06_0.IFO) as the Season 2 entries (63, 64, 65) — three seasons later, the studio's authoring pipeline still produces the same file-list shape, so the per-season template shift first observed between S1 (3 VTSes) and S2 (6 VTSes) was a one-time change rather than a per-season drift.
- **See also:** entry 67 — the Disc 4 sibling from the same Season 5 set.

## 67. Andromeda Season 5 — Disc 4 (DVD-Video)

- **matrix256v1:** `67df7f03d11c86ac9c545d00499b0c74c879b91ed9def703edc0e5a51ffacbb6`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 24 of the Andromeda full series box set, containing Season 5 Episodes 19-22. Final Season 5 disc and the second Season 5 entry, paired with entry 66. Same 6-VTS authoring (7 files hashed) as every Season 2 and Season 5 disc the corpus has captured, reinforcing that the studio's post-S1 template was set once and stayed put. With a sibling now in place, the within-season distinctness check holds at S5 the same way it does at S2: matching template shape, distinct hashes — useful continuity across the four-year gap between when these two seasons were authored.
- **See also:** entry 66 — the Disc 3 sibling from the same Season 5 set.

## 68. Andromeda Season 3 — Disc 3 (DVD-Video)

- **matrix256v1:** `542701a3d6b16d5cdb4ed2668e3b421beb3d11685a2439a8d7c309b147b1079f`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 13 of the Andromeda full series box set, containing Season 3 Episodes 11-15. First Season 3 disc in the corpus, fitting between the Season 2 entries (63, 64, 65) and Season 5 entries (66, 67) and giving the corpus an interior season as well as endpoints. Same 6-VTS authoring (7 files hashed: VIDEO_TS.IFO + VTS_01..06_0.IFO) as every post-S1 disc the corpus has captured — strong evidence that the studio's authoring template was set once at the S1→S2 boundary and held steady through the entire remainder of the box set.

## 69. Andromeda Season 4 — Disc 2 (DVD-Video)

- **matrix256v1:** `fe8dafb8bfc89d74150f96859f3eaf147f09b26965fe6837dc2d20b30e0a6c05`
- **Filesystem view:** udf on /dev/sr0 (physical_disc); options `ro,nosuid,nodev,relatime,iocharset=utf8`
- **Reader:** inspect_disc.py · python 3.12.3 · Linux 6.8.0-110-generic
- **Structure:** DVD-Video, VIDEO_TS layout
- **Why it's here:** This is disk 17 of the Andromeda full series box set, containing Season 4 Episodes 6-10. First Season 4 disc in the corpus; combined with the Season 2, 3, and 5 entries already in place, the corpus now covers all of the box set's post-Season-1 seasons. Same 6-VTS authoring (7 files hashed: VIDEO_TS.IFO + VTS_01..06_0.IFO) as every other post-S1 disc captured here, leaving Season 1 (3 VTSes / 4 files hashed) as the lone outlier and the S1→S2 boundary as the only authoring shift in the entire 25-disc set.

## Reproducing a fingerprint

For discs with an `.iso` available, the fingerprint is deterministic from the disc image alone:

```
python inspect_disc.py <path-to-iso>
```

For physical discs, pass the optical drive block device (`/dev/sr0`, `/dev/sr1`, …). The script loop-mounts the ISO or uses `udisksctl` to mount the block device read-only, walks the filesystem, computes the matrix256v1 digest, and unmounts on exit. Reproducing a corpus value also requires reproducing the recorded filesystem view (filesystem driver, mount options) — different views of the same physical media produce different (and individually correct) digests.

Open-content discs (Big Buck Bunny, Sintel) are freely downloadable from their respective project pages and should produce identical fingerprints to the values recorded here when walked under the same view.

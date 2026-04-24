# matrix256: Submission Venues

Candidate conferences and journals for publishing the matrix256 specification and corpus findings. Venues are grouped by audience and fit, with commentary on strategic considerations at the end.

The current date is April 24, 2026. Deadlines noted below are as of that date; re-check the CFP before submission.

## Conferences — strong fit

### iPRES (International Conference on Digital Preservation)

- **Next edition:** iPRES 2026, Copenhagen, Denmark, September 21–25, 2026
- **Submission deadline for 2026:** March 9, 2026 (extended to March 16) — **closed**
- **Target:** iPRES 2027, venue TBA (announced from host bid cycle 2027–2030)
- **Formats:** Full papers (max 8 pages), Short papers (max 4 pages), Workshops, Tutorials, Panels, Posters, Lightning Talks, Birds of a Feather, Digital Preservation Bake-Off
- **Why it fits:** iPRES is the single best audience match. The conference explicitly welcomes "technical papers, or case studies" on digital preservation practice, and the 61-disc corpus lands directly in their wheelhouse. Open-content reproducibility (Big Buck Bunny, Sintel) is exactly the kind of artifact iPRES reviewers value.
- **Strategic note:** The Digital Preservation Bake-Off is a competitive format where tools are evaluated hands-on. matrix256 could be submitted both as a paper and as a Bake-Off entry in the same year.

### JCDL (ACM/IEEE Joint Conference on Digital Libraries)

- **Next edition:** JCDL 2026, Dallas, Texas, October 13–16, 2026
- **Submission deadline:** typically spring (JCDL 2025 was late February 2025) — verify the current CFP
- **Formats:** Full research papers (up to 10 pages including references, IEEE two-column), Short papers (up to 4 pages), Posters, Demonstrations, Resource Track (datasets, software, collections), Doctoral Consortium, Workshops
- **Why it fits:** JCDL bridges "computer science, information science, librarianship, archival and museum studies." matrix256 is a technical contribution with archival relevance; the Resource Track is a natural fit for the specification plus corpus together.
- **Strategic note:** Double-blind review. The IEEE two-column template is more constrained than iPRES's Springer LNCS format.

### TPDL (International Conference on Theory and Practice of Digital Libraries)

- **Next edition:** TPDL 2026, Faro, Portugal, September 21–25, 2026 *(note: overlaps with iPRES 2026)*
- **Submission deadline:** May 3, 2026 — **open, ~9 days remaining**
- **Formats:** Full papers, Short papers, Posters (Springer LNCS format)
- **Proceedings:** Published by Springer in the Lecture Notes in Computer Science series
- **Associated journal:** International Journal on Digital Libraries (IJDL) runs special issues with selected TPDL papers
- **Why it fits:** TPDL has a more academic flavor than iPRES but welcomes "real world applications and reflecting on their methods' individual benefits, challenges, and limitations" — matrix256 with the empirical corpus is exactly that.
- **Strategic note:** This is the immediately actionable option. Nine days is tight but feasible given the spec and rationale are already drafted. If you miss TPDL 2026, iPRES 2027 is the next-best academic venue.

### Archiving Conference (IS&T)

- **Next edition:** Archiving 2026, Boston, Harvard University, dates listed variously as June 15–18 or July 20–23, 2026 — verify with IS&T directly
- **Submission deadline for 2026:** likely passed (abstracts typically due mid-October the prior year)
- **Target:** Archiving 2027 if 2026 is closed
- **Formats:** Peer-reviewed papers, all accepted papers published Open Access via the IS&T Digital Library
- **Why it fits:** The conference explicitly covers "digitization, imaging, preservation, metadata management, archival workflows" and has a cultural-heritage orientation. Less CS-heavy than iPRES/JCDL, more preservation-practitioner.
- **Strategic note:** The audience skews toward libraries, archives, and museums rather than academic CS. Framing should emphasize preservation and identification use cases over systems contributions.

## Conferences — stretch fits

### FAST (USENIX Conference on File and Storage Technologies)

- **Next edition:** FAST 2027, likely February 2027, Santa Clara, CA
- **Submission deadline:** FAST 2026 had two cycles (Spring: March; Fall: September). FAST 2027 CFP not yet published.
- **Formats:** Full papers, Short papers; one-shot revision option introduced for FAST 2026
- **Why it's a stretch:** FAST's 2026 topics include "archival systems" and "empirical evaluation." A matrix256 paper could fit if framed around the file system and storage aspects: UDF filesystem metadata, reader-independence properties, robustness to media damage. But FAST's reviewers expect systems novelty at research-paper depth; a specification document alone would likely be desk-rejected.
- **How to make it fit:** A FAST paper would need to be a substantially different artifact than the spec document — something like "An empirical study of optical media filesystem metadata for content-addressable identification," with systems-level measurements (e.g., read performance across UDF implementations, corpus-scale collision analysis, comparison to pydvdid across a disc-image benchmark). High bar.

### OSDI / SOSP Workshop Tracks

- **OSDI 2026:** typically July, often co-located with ATC
- **SOSP 2026:** typically October
- **Formats:** Main conference papers have extremely high bars; workshop tracks (e.g., HotStorage) are more accessible
- **Why it's a stretch:** Same caveat as FAST — main-venue OSDI/SOSP wants systems novelty beyond a specification. HotStorage (co-located with USENIX ATC) has historically been more receptive to practitioner-flavored storage work.

### FOSDEM (Free and Open Source Developers' European Meeting)

- **Next edition:** FOSDEM 2027, Brussels, first weekend of February 2027
- **Submission deadline:** CFPs for individual devrooms typically open late November / early December for the following February
- **Relevant devrooms:** "Open Media" devroom (covers codecs, players, media tooling); "Collaborative Information and Content Management Applications"; a more speculative "Software Archaeology" or "Preservation" pitch
- **Format:** Mostly 20–30 minute talks; some lightning talks
- **Why it's a good community fit:** FOSDEM audiences genuinely care about open specifications, reproducibility, and archival tooling. The ARM community overlaps with FOSDEM's practitioner base. No proceedings, but excellent reach and credibility.
- **Strategic note:** Not a peer-reviewed venue, but talks are recorded and widely viewed. Good warm-up venue for an academic submission later — a FOSDEM talk can establish community uptake that strengthens a subsequent JCDL or iPRES paper.

### Code4Lib Conference

- **Next edition:** Code4Lib 2027, venue TBA
- **Submission deadline:** Typically October for the following March conference
- **Format:** Prepared talks, posters, lightning talks — community-voted
- **Why it fits:** "Developers and technologists for libraries, museums, and archives who are dedicated to being a diverse and inclusive community, seeking to share ideas and build collaboration." Practitioner-focused, overlaps heavily with iPRES / TPDL audiences but more informal.
- **Strategic note:** Voting-based acceptance rather than peer review. Talks are streamed on YouTube. Lower prestige than JCDL or iPRES but a strong community-building venue.

### SAA Annual Meeting (Society of American Archivists)

- **Next edition:** SAA 2026, Denver, August 2026
- **Submission deadline:** typically October the prior year — likely closed for 2026
- **Target:** SAA 2027
- **Why it fits:** The archivist community is exactly the constituency matrix256 serves. Less technical than iPRES but broader reach into practicing archivists.

## Journals — strong fit

### International Journal on Digital Libraries (IJDL)

- **Publisher:** Springer
- **ISSN:** 1432-5012 (print), 1432-1300 (electronic)
- **Scope:** "Theoretical foundations, infrastructure, practice, and evaluation of digital libraries," including preservation, metadata, identification, and access
- **Relationship to TPDL:** Main associated journal — runs special issues of selected TPDL papers, so a TPDL submission can be a route into IJDL
- **Why it fits:** The natural home for an extended version of a TPDL or JCDL paper. Would welcome the full corpus analysis alongside the spec.

### ACM Transactions on Storage (TOS)

- **Publisher:** ACM
- **ISSN:** 1553-3077 (print), 1553-3093 (electronic)
- **Scope:** "File systems, resource management, data backup and archival, availability and reliability" — archival systems are explicitly in scope
- **Impact factor:** ~2.8 (2024); CiteScore 3.4
- **Review timeline:** Standard ACM Transactions — typically 6 months first decision
- **Why it fits:** Storage-systems framing of matrix256 (filesystem-metadata fingerprinting, reader-independence properties, UDF/ISO 9660 coverage) is directly in scope. TOS is friendlier to practitioner-flavored work than FAST and accepts papers that extend conference work with substantial new material.
- **Strategic note:** Could be a follow-up venue to a FAST, HotStorage, or systems-conference paper. Would need the paper to go beyond the specification — likely the empirical corpus analysis, reader-independence evaluation, and comparison to pydvdid at scale.

### Code4Lib Journal

- **Publisher:** Code4Lib (independent, open access)
- **ISSN:** 1940-5758
- **Scope:** "Articles, case studies, and commentary that foster community and shared knowledge among people committed to the intersection of libraries, technology, and the future"
- **Review:** Editorial review rather than double-blind peer review; turnaround is typically fast (weeks to months)
- **Why it fits:** Practitioner audience. Would welcome a write-up of matrix256 with the empirical corpus, framed accessibly. Lower academic prestige than IJDL or TOS, but broader reach into the working LAM community.
- **Strategic note:** Excellent "first journal publication" option. The Code4Lib Journal publishes work that wouldn't necessarily land at a peer-reviewed academic journal, and the readership actively uses published specs.

### Preservation, Digital Technology & Culture (PDT&C)

- **Publisher:** De Gruyter
- **ISSN:** 2195-2965 (print), 2195-2973 (electronic)
- **Scope:** "Preservation and stewardship of cultural heritage," explicitly including digital formats and identification
- **Why it fits:** Preservation-focused with a cultural-heritage bent. Natural home for a matrix256 paper framed around archival identification rather than storage systems.

### JASIST (Journal of the Association for Information Science and Technology)

- **Publisher:** Wiley
- **ISSN:** 2330-1635 (print), 2330-1643 (electronic)
- **Scope:** Broad information science including digital libraries, information retrieval, and preservation
- **Impact factor:** ~2.5
- **Why it fits (and doesn't):** Fits the digital libraries angle but leans toward user studies and information retrieval; a technical specification paper is a stretch fit. Worth considering only if the paper emphasizes identification-as-information-retrieval framing.

## Journals — stretch fits

### Archival Science (Springer)

- **Scope:** Archival theory and practice, including technology and digital preservation
- **Why it's a stretch:** Humanities/archival-theory audience. A technical specification paper would need significant reframing to land here — more about preservation practice, less about bits.

### Digital Scholarship in the Humanities (Oxford)

- **Scope:** Digital humanities methods and tools
- **Why it's a stretch:** matrix256 isn't primarily a humanities-methods contribution. Would need to frame the corpus as a cultural-heritage dataset.

### D-Lib Magazine (defunct)

- **Status:** Ceased publication in 2017. Listed here only because it appears in some older venue lists.

## Commentary: strategy

**The highest-leverage path right now:**

Submit to **TPDL 2026** by May 3. The spec and rationale documents are substantively ready; two weeks of revision against the TPDL submission format (Springer LNCS) is feasible. Acceptance would also position you for a journal submission to IJDL via their TPDL special issue pipeline.

If TPDL 2026 slips, **iPRES 2027** is the strongest back-up. You have a full year to polish, run the corpus against more disc types (UHD Blu-ray, additional HD DVD samples), and possibly deploy a lookup service as empirical evidence of community uptake.

**Parallel tracks worth running:**

- **FOSDEM 2027** (deadline ~November 2026) — practitioner talk in an Open Media or Preservation devroom. Low-cost, high-visibility. A FOSDEM talk before an academic submission establishes community traction that reviewers notice.
- **Code4Lib Journal** — fast turnaround, practitioner readership. Would welcome a write-up even if an academic paper is in-flight elsewhere. Not exclusive with academic submission if framed as a different contribution (e.g., academic paper = specification + validation; Code4Lib Journal article = implementation experience + corpus findings).

**What to avoid:**

- **FAST main track** unless you're prepared to write a substantially different paper. The specification document alone will be desk-rejected.
- **Journal submissions before any conference acceptance.** Journals are slow and conference publication strengthens a subsequent journal version.
- **Simultaneous submission to multiple peer-reviewed venues.** Most venues explicitly prohibit this. Code4Lib Journal and FOSDEM are editorially reviewed and don't count against simultaneous-submission rules for most academic venues, but verify each CFP.

**Audience positioning:**

matrix256 is technical enough for systems venues (FAST, TOS) but archival enough for preservation venues (iPRES, TPDL, Archiving). The archival framing is stronger: the corpus and the community-lookup-service angle both play well to preservation audiences, and the practitioner-run community there is more likely to actually adopt the spec. The systems framing needs more empirical depth before it lands — reader-independence benchmarks, collision analysis at larger scale, systematic comparison against pydvdid on a shared disc-image corpus. That's a second paper, not v1.

**One non-obvious strategic consideration:**

Publishing the spec itself (at `matrix256.dev` or similar) before any conference submission does not reduce publication eligibility — all the venues listed here accept work that is already publicly available as long as the submitted paper is original and hasn't appeared in peer-reviewed proceedings. Publishing the spec early builds community traction, but it also means reviewers can find it. Reviewers who already know and appreciate the spec will be kinder; reviewers who find inconsistencies between the published spec and the submitted paper will be harsher. Freeze the spec before submission.

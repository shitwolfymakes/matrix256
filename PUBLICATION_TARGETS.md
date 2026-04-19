# Publication Targets

Candidate journals for the optical disc fingerprinting specification, ranked by fit. The paper is a short, spec-style contribution (proposed community identifier + reference implementation + rationale) rather than an empirical study, which rules out most traditional CS venues and points toward practitioner-oriented and digital-preservation journals.

## Tier 1 — strongest fit

### The Code4Lib Journal
- **URL:** https://journal.code4lib.org/
- **Why it fits:** Practitioner-oriented, technically substantive library/archives tech. A short spec with a reference implementation is squarely in scope — past issues include protocol proposals, identifier schemes, and hash-based workflows. Fast review cycle, open access, no APC.
- **Format match:** Strong. Articles are typically 2,000–6,000 words; code excerpts are welcome.
- **Watch-outs:** Editorial-board review rather than blind peer review — some tenure/promotion committees discount it. Irrelevant for non-academic authors.

### International Journal of Digital Curation (IJDC)
- **URL:** https://ijdc.net/
- **Why it fits:** Published by the Digital Curation Centre. Regularly publishes work on identifiers, fixity, and preservation metadata — all direct neighbors of this work. Peer-reviewed, open access, no APC.
- **Format match:** Good. Accepts both full papers and shorter "General Articles."
- **Watch-outs:** Readership is primarily academic libraries and preservation programs; frame the motivation accordingly.

### The Moving Image (AMIA / University of Minnesota Press)
- **URL:** https://www.upress.umn.edu/journals/the-moving-image
- **Why it fits:** Journal of the Association of Moving Image Archivists. Audio-visual archiving of physical media (including optical discs) is core scope, and disc-level identifiers are a recurring topic among AMIA members.
- **Format match:** Accepts shorter "Forum" / "Technical Notes" pieces in addition to articles.
- **Watch-outs:** Tilts humanities / curatorial. Lead with the preservation and cataloging use cases rather than the cryptographic argument.

## Tier 2 — plausible fit

### Forensic Science International: Digital Investigation (Elsevier)
- **URL:** https://www.sciencedirect.com/journal/forensic-science-international-digital-investigation
- **Why it fits:** Hash-based identification of physical media is adjacent to forensic disc imaging and provenance. The rationale section (why SHA-256, why not CRC64, why structural not content) maps well to the forensics audience.
- **Format match:** Accepts short "Technical Notes."
- **Watch-outs:** Reviewers will expect evaluation against an existing corpus (collision rate, stability across pressings). The paper currently has none — add an evaluation section before submitting here.

### Information Technology and Libraries (ITAL)
- **URL:** https://ital.corejournals.org/
- **Why it fits:** ALA LITA publication, open access, no APC. Publishes short technical papers on identifiers, metadata, and cataloging infrastructure.
- **Format match:** Good for a spec-style paper.
- **Watch-outs:** US-library-centric framing. Less visibility outside that community than Code4Lib.

### Journal of Digital Forensics, Security and Law (JDFSL)
- **URL:** https://commons.erau.edu/jdfsl/
- **Why it fits:** Open access, peer-reviewed. Accepts short methodological contributions. Frames the work as a forensic identifier rather than a cataloging one.
- **Watch-outs:** Smaller readership than FSI:DI; same evaluation expectations.

## Tier 3 — stretch / context-dependent

### Journal of the Association for Information Science and Technology (JASIST, Wiley)
- More theoretical and empirical than this paper is. Only a fit if the work is extended with a study of collision rates across a real disc corpus and a formal analysis of the identifier's properties.

### Archival Science (Springer)
- Broader archival theory. A fit only if the paper is reframed around long-term identifier stability and community-curated mapping layers, rather than the algorithm itself.

## Non-journal venues worth considering in parallel

A short spec paper often lands better at conferences with published proceedings than at traditional journals. Submit in parallel to the appropriate journal where policy allows:

- **iPRES** (International Conference on Digital Preservation) — proceedings are citable and indexed; strong community overlap.
- **JCDL** (ACM/IEEE Joint Conference on Digital Libraries) — short paper track.
- **TPDL** (Theory and Practice of Digital Libraries) — European counterpart to JCDL.

Separately, a community identifier benefits from being published as a **living spec** (GitHub repo with a stable URL, versioned tags) in addition to a journal article. MusicBrainz Disc ID's influence comes from its implementations and community, not its academic citation count. Journal publication gives the identifier academic legitimacy; the spec repo gives it operational adoption. Do both.

## Recommended submission path

1. **Primary:** Code4Lib Journal — fastest route to a citable, open-access publication that reaches the practitioner audience who would actually adopt the identifier.
2. **In parallel:** Submit an extended version (with a collision/stability evaluation across a corpus of discs) to IJDC or The Moving Image for deeper academic reach.
3. **Later:** If the identifier gains adoption, a retrospective at iPRES or JCDL documenting real-world use will carry more weight than a pre-adoption spec paper would.

The weakest part of the current manuscript for any peer-reviewed venue is the absence of an evaluation. Before Tier 2 submissions, plan to:
- Run the algorithm against a corpus of 100+ discs spanning DVD, Blu-ray, and UHD.
- Report collision rates, stability across multiple reads of the same disc, and behavior on non-standard layouts.
- Compare against pydvdid on the DVD subset to quantify the collision-space improvement empirically.

## Disclosure of AI assistance

Every target venue listed above (and arXiv, if posting a preprint) prohibits listing AI tools as authors on the grounds that an AI cannot take accountability for published work. Disclosure in the methods and acknowledgments is the maximum crediting that is both accepted and appropriate. The pattern below mirrors what the Schwartz group used for the 2026 Harvard physics paper (arXiv:2601.02484), where Claude performed most of the technical work and the human remained sole author.

### Methods section (insert verbatim, adjust model/version at submission time)

> The specification text and reference implementation were drafted with assistance from Claude Code (Anthropic, Claude Opus 4.7, accessed April 2026). The model was used for structural editing of the specification, verification of internal consistency between the prose algorithm and the Python reference implementation, and candidate identification of prior art and submission venues. All algorithmic decisions — including the file list, ordering conventions, exclusion of backup and payload files, and the choice of SHA-256 — are the author's and were reviewed by the author for correctness. Any evaluation results reported in this paper were produced by the author and independently verified against the reference implementation.

### Acknowledgments section

> The author thanks Claude Code (Anthropic) for drafting and editorial assistance during preparation of this specification and for help identifying candidate publication venues.

### Notes on journal-specific variants

- **Code4Lib Journal:** A single sentence in an author's note is usually sufficient; the methods-section paragraph can be trimmed.
- **IJDC / The Moving Image:** Use both paragraphs as written; these venues expect explicit scope-of-use disclosure.
- **FSI: Digital Investigation / JDFSL:** Forensics reviewers will scrutinize AI involvement in any evidentiary claim. If an evaluation section is added, state explicitly that corpus construction, collision counting, and statistical analysis were performed by the author without AI assistance (assuming that remains true).
- **arXiv preprint:** arXiv's policy is the same as the journals'. Sole human author on the byline; disclosure in the paper body.

### What not to do

- Do not list Claude, Claude Code, or Anthropic on the author byline. Every Tier 1 and Tier 2 venue will desk-reject on this ground alone.
- Do not rely on the Git `Co-Authored-By: Claude` trailer as authorship. It is a GitHub commit metadata convention with no academic standing, and there is active community pushback against treating it as authorship even in open source.
- Do not describe AI involvement vaguely ("AI-assisted"). Name the tool, the version, the access date, and the specific tasks — vague disclosure is treated as non-disclosure by most editorial boards.

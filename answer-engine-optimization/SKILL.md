---
name: answer-engine-optimization
description: Audit what AI search answers cite and recommend, turn first-hand evidence into a citable answer, or correct inaccurate brand facts. Use for AEO, GEO, AI shortlists, citation gaps, and incorrect claims about a product in answer engines.
---

# Answer engine optimization

Start with the workspace's brand, the buyer's decision and the evidence available. Reuse its existing prompt panel, captures, fact sources and reporting tools. A saved answer, screenshot or export is enough to start. Pick the section that answers the request.

## Audit a buyer shortlist

1. Fix the buyer question, its intent, the brand and its owned domains before looking at results. Use customer wording when available and label proposed prompts as hypotheses. Keep unbranded questions for discovery and brand-named questions for accuracy. Record the engine, UI or API, date, language and observed market. Preserve unknown settings.
2. For each planned prompt and surface, keep the exact prompt, redacted answer and displayed source links. Give each capture a stable reference. Record an unavailable run, an error or a result with no AI answer separately. Select one attempt per slot using a declared rule, and use the same rule on recheck.
3. Read the answer itself. Record a **mention** when the answer names the brand, a **citation** when its displayed sources link to the brand's domain, and a **recommendation** when the answer presents the product as a choice for this buyer. Preserve the exact passage and any conditions. A source link, a feature description or a warning against using the product can coexist with a recommendation for a competitor.
4. Use `recommended`, `not_recommended` or `unclear` for a reviewed answer. Use `not_recommended` after reading an answer that omits the brand, only cites it, or advises against it. Use `unclear` when the language leaves the choice ambiguous. Leave unreviewed answers unscored. Record the cited URL and the competing product by name when the answer supplies them.
5. Report by engine, surface, market and prompt class. Show valid answers / planned slots, mentions / valid answers and owned citations / valid answers. For unbranded shortlists show recommended / (recommended + not_recommended), the count of determinate reviews / valid answers, and counts for unclear and unreviewed. With no determinate reviews report **unmeasured**. Keep branded controls out of discovery rates. A single capture supports an example, not a trend.

For a gap worth acting on, name the buyer question, the source the engine cited, the passage that influenced your interpretation, and the next change you can verify. A cited competitor page establishes what appeared in that capture. Search volume, causation and sales impact each need their own evidence.

## Write an answer grounded in first-hand proof

1. Choose one buyer question and the existing canonical page that should answer it. Extract the smallest supportable claim from a public product record, documented test, changelog or permissioned customer example. Record the source URL, owner, date, test conditions and limits. If only private evidence exists, keep the draft private and identify what the owner can make public.
2. Draft a passage that makes sense when quoted on its own. Name the product or subject, answer the buyer's question, explain when it applies, and link the primary evidence beside the claim. For a comparison, check both products against the same criterion and date. For a benchmark, carry the sample, method and units into the passage.
3. Return the proposed page diff or replacement passage, its evidence, and the other pages that repeat the fact. Check the rendered public page and evidence link after publication. Freeze the original buyer prompt for the next capture.

## Correct a brand fact

1. Quote the specific answer claim and record the capture and displayed sources. Check the claim against a dated authority for that fact, such as the current pricing terms, product documentation or supported version. Preserve scope differences such as plan, region or release. Mark unresolved cases **unverified** and state the missing evidence.
2. Trace the discrepancy to a source you can actually read. Distinguish an observed stale page from a suspected origin the engine never cited. Patch an owned source within scope, or draft a correction for an independent publisher with the URL, old wording, replacement and evidence.
3. Return a correction log with the fact, authority, affected URL, owner, change status and recheck prompt. Verify an owned page change on the live URL and verify the engine answer in a later comparable capture. Each is a separate observation.

## Example

A buyer asks which scheduling tool to buy. The answer says “Choose Cedar for round-robin assignment” and cites a guide on fictional Alder's site. For Alder, record one owned citation, no mention in the answer body and a reviewed negative recommendation. Record Cedar as the recommended product. If the only other planned slot was blocked, the owned citation rate is 1/1, the shortlist rate is 0/1 and capture coverage is 1/2.

## Method sources

- [Corey Haines, AI SEO](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ai-seo)
- [Illyism, first-hand proof](https://github.com/Illyism/seo-skills/blob/main/seo/proof-kb/SKILL.md)
- [RomeoSEO, brand fact corrections](https://github.com/RomeoSEO/seo-skills/blob/main/skills/ai-brand-facts/SKILL.md)
- [Google Search Central, generative AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

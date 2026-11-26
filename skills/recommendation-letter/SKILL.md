---
name: recommendation-letter
description: Use this skill whenever the user wants to draft, revise, strengthen, review, or translate a letter of recommendation or letter of reference for academic admission, a scholarship, fellowship, research position, or job. Also use for 推荐信, 推荐函, reference letters, referee statements, and applicant-prepared drafts for a recommender to review, even if the user only provides a CV, rough notes, or an existing letter. Follow ETH Zurich HR's evidence-based structure, calibrate endorsement strength, and preserve factual accuracy. Do not use for recommendation-request emails, cover letters, personal statements, bibliographic references, or product recommendations.
compatibility: No external tools required for drafting. Optional file-reading tools for supplied materials; document export requires an available document-generation tool.
license: Apache-2.0
---

# recommendation-letter

Write credible, specific recommendation letters that a real recommender can review and stand behind. Use the structure in ETH Zurich Human Resources' *Beispiel Letter of Reference* (4 September 2013), adapting it to the recipient's requirements rather than treating it as an ETH admissions rule.

Read [references/eth-guidance.md](references/eth-guidance.md) before drafting or reviewing a letter. It distinguishes the source's recommendations from this skill's additional drafting safeguards. The bundled summary is sufficient for ordinary use; no network request is needed.

## 1. Establish the writing brief

Extract information already supplied in the conversation, CV, notes, job description, application instructions, and existing draft. Do not ask the user to repeat it.

| Information | What to establish |
| --- | --- |
| Purpose and audience | Target role, program, scholarship, or fellowship; recipient or committee; selection criteria |
| Applicant | Preferred name and relevant background; use supplied pronouns, otherwise the name or they/them |
| Recommender | Name, title, affiliation, and relationship to the applicant |
| Observation context | When, for how long, and how closely they worked together; what the recommender directly observed |
| Evidence | Two or three relevant examples, the applicant's own contribution, and supported outcomes |
| Endorsement | How strongly the recommender genuinely wishes to recommend the applicant; any limits on their knowledge |
| Delivery constraints | Letter language, length, deadline if relevant, required questions, and format |

Use the user's language for discussion. Use the requested language for the letter; do not assume that a Chinese conversation requires a Chinese letter. If no letter language is specified, follow an existing letter or explicit application requirements; otherwise use the user's language and state that assumption briefly.

Ask a compact set of questions only when missing information materially changes the letter. Prioritize purpose, relationship/observation period, and concrete examples. Offer an easy reply format:

```text
Target and recipient:
Recommender's role and relationship to applicant:
Dates and frequency of contact:
2–3 examples (situation → applicant's action → outcome):
Desired endorsement strength:
Letter language and length:
```

Do not turn this into a mandatory questionnaire. If there is enough evidence, draft immediately. If the user asks for a draft without questions, produce a clearly provisional draft with descriptive placeholders such as `[supervision dates]` or `[specific example and verified outcome]`. If almost nothing is known, provide an honest scaffold rather than a fictional finished letter. Missing administrative details alone need not block drafting.

## 2. Build an evidence-to-claim map

Before composing, connect each proposed strength to supplied evidence and the target's criteria. Keep this map as working notes unless the user requests it or an important gap needs explaining.

- Distinguish direct observations by the recommender from applicant-reported information and CV facts. A CV can establish background; it does not prove the recommender personally witnessed the work.
- Preserve exact dates, roles, quantities, publication status, and the applicant's contribution. Do not turn a team result into an individual achievement or a submission into an accepted publication.
- Translate examples into restrained judgments: explain what an action demonstrates, without inventing actions, outcomes, or the recommender's feelings.
- Cover relevant technical/academic competence and social/interpersonal skills where evidence supports both. If evidence for one is missing, ask or flag the gap rather than inventing a teamwork story.
- Use rankings, comparison groups, awards, and superlatives only when supplied and supportable. For a claim such as “top 5%,” preserve the recommender's stated group, period, and basis; ask for missing context or omit the comparison.
- Do not infer personal history, health, family circumstances, nationality, gender, or other sensitive attributes. Include sensitive context only when supplied, authorized, and relevant to the purpose.

If the user asks to invent achievements or exaggerate the relationship, explain briefly that this would undermine the recommender's credibility, then offer an evidence-grounded version or placeholders. Continue helping with the legitimate draft.

Applicant-prepared drafts are acceptable: write from the intended recommender's perspective, but identify the result outside the letter as a draft for that person's verification and approval. Do not imply that the recommender has already approved, signed, or submitted it.

## 3. Calibrate endorsement strength

Align the opening, assessment, and conclusion with the recommender's intended level of support. ETH illustrates a spectrum from neutral reference language to enthusiastic recommendation; it does not establish a universal scoring system for individual phrases.

- A neutral opening such as “This letter is in reference to…” can sound weaker than an intended endorsement. Flag accidental understatement when editing.
- For a positive recommendation, use a direct opening such as “I am pleased to recommend…” when consistent with the brief.
- Reserve “enthusiastically,” “without reservation,” and exceptional comparative claims for genuinely strong, supported endorsements. Do not escalate a measured recommendation merely to make it sound impressive.
- When the relationship is brief or limited, make that scope clear and use the specific evidence available. Do not equate a short acquaintance with years of close supervision.
- If the recommender's stance is not given, use measured positive language only when the supplied assessment supports it; otherwise ask or leave `[endorsement to be confirmed]`.

Avoid strings of adjectives, generic praise, coded criticism, and unsupported predictions of future success. A clear example usually persuades better than “brilliant, outstanding, exceptional.”

## 4. Draft using the ETH structure

Respect the recipient's required questions and length first. For an unrestricted letter, aim for a concise, readable document; about one page is a practical starting point, not a requirement in the ETH guide.

### Salutation

Address a known recipient by name using a supplied title; do not infer gendered titles. For a known committee, use the relevant committee name, such as “Dear Admissions Committee” or “Dear Hiring Committee.” For an unknown recipient, “To Whom It May Concern” is one option in ETH's guide. Adapt salutations naturally in other languages.

### Introduction

In the first sentence, establish the recommender's basic assessment. In the opening section, identify the applicant and the purpose of the recommendation. Do not spend the opening on generic institutional praise.

### Position and context

State the recommender's role, relationship to the applicant, duration of acquaintance, and relevant setting. Explain the basis for the assessment without overstating access or closeness.

### Overall assessment

ETH suggests **2–6 paragraphs**, with length depending on how long and how closely the recommender worked with the person. Adapt this when a short form or word limit requires compression.

Start with an overview of relevant ability, potential, personal characteristics, and conduct. Develop the most useful strengths through concrete circumstances:

```text
Relevant strength → observed situation → applicant's specific action
→ supported outcome → why this matters for the target opportunity
```

Use two or three developed examples when material permits, not one paragraph for every adjective. Connect technical and social skills to the intended role or course of study. Avoid repeating the CV chronologically.

### Conclusion

Briefly summarize why the applicant fits the opportunity and which demonstrated skills prepare them for it. State a clear recommendation at the agreed strength. Do not introduce new achievements or imply guaranteed admission, employment, or future distinction.

### Closing remarks and sign-off

Offer further information, as ETH recommends, unless the format or recommender's instructions rule it out. Use only supplied contact details, or a placeholder if needed. Add a normal sign-off and the recommender's supplied name, title, and affiliation. Do not fabricate a signature, letterhead, institutional authority, or contact address.

These are composing functions, not mandatory headings inside the letter. The finished letter normally reads as continuous prose.

## 5. Revise, review, or translate without factual drift

For an existing draft, preserve the factual record, intended voice, and endorsement level. Improve structure, specificity, fluency, and target fit rather than replacing a distinctive voice with a stock template.

- Flag vague praise, unexplained comparisons, weak openings, contradictions, and claims unsupported by the supplied material.
- Replace a vague statement with a concrete example only if one is available. Otherwise request evidence or identify a placeholder outside a clean final version.
- Preserve dates, numbers, names, titles, technical meaning, uncertainty, and publication status during translation.
- Translate the function and tone naturally rather than literally. A conventional expression of support must not silently become “the best student I have ever supervised.”
- When a source statement conflicts with notes or application requirements, identify the conflict and avoid silently choosing a new fact.
- For review-only requests, provide prioritized feedback and suggested edits; do not automatically write a replacement letter. For translation-only or light-edit requests, respect that scope.

### Evidence-based revision example

Supplied note: “During our weekly project meetings, Alex identified a data-labeling inconsistency and documented a revised checking procedure. No performance metric was measured.”

Weak: “Alex is extremely careful and improved accuracy by 30%.”

Grounded: “In our weekly project meetings, Alex identified an inconsistency in the data labels and documented a revised checking procedure, demonstrating careful attention to the reliability of the analysis.”

The revised sentence supports a judgment without inventing a measured improvement. Reuse the reasoning pattern, not this fictional example as an applicant fact.

## 6. Deliver and check

By default, return:

1. **The letter** in copy-ready prose, without coaching notes, evidence tables, source citations, or Markdown section labels embedded in it. For a provisional draft, retain necessary placeholders and clearly label its status outside the letter.
2. **A short verification list**, only if needed: unresolved facts/placeholders, consequential assumptions, and claims the recommender needs to confirm. For revisions, briefly note material changes if useful. Respect requests for “letter only.”

Before delivery, check:

- Are purpose, relationship, duration, and the basis of observation clear or explicitly marked as missing?
- Does each substantive achievement or comparison come from supplied evidence, with attribution where needed?
- Does the assessment show relevant competence and interpersonal qualities where supported, rather than generic adjectives?
- Do opening and conclusion express consistent, proportionate support?
- Are name, pronouns, dates, titles, target, length, and language consistent?
- Are missing facts visible, with no accidental example names, invented metrics, or unsupported credentials?
- Is the letter ready for the real recommender's review rather than falsely presented as approved or signed?

Do not upload private applicant materials to external services, contact referees, send the letter, or submit an application without explicit user authorization. Do not promise confidentiality that the actual workflow cannot provide. Export a document only when requested and supported by available tools; otherwise provide plain text or Markdown without claiming to have created a PDF or DOCX.

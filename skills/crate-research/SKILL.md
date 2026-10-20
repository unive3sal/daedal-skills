---
name: crate-research
description: Use before implementing Rust capabilities or choosing Cargo dependencies, including when a coding agent receives only a top-level design, approved plan, milestone, delegated worker task, or unattended implementation job. Infer feature-level reuse opportunities from the design and project during exploration; the user need not mention a feature, crate, or research. Load this skill before the first affected implementation write, not just before cargo add. Compare functional fit, all-time/recent downloads, release cadence, community activity, and issue/PR responsiveness; recommend sourced options and route the technical decision to the human before proceeding. Workers return pending decisions to their coordinator; headless runs report the blocker and stop. Architecture approval and tool permissions are not crate-choice approval. Also use for Rust crate comparisons. Skip product-only design discussion, explanations, and routine edits with no new capability or dependency decision.
compatibility: Requires web/HTTP access for current crates.io and upstream evidence; gh is optional. The runtime must expose skills to the implementing agent. Use an actual human channel or return a pending decision to the coordinator/operator; headless execution cannot invent approval.
license: Apache-2.0
---

# crate-research

Research reuse opportunities before writing Rust feature code. Treat crate selection as a user-owned decision: investigate, explain the trade-offs, recommend, and stop for the user's choice. A familiar crate is a candidate, not an automatic dependency.

## Implementation-loop checkpoint

Treat the current task context, not just the latest human sentence, as the source of requirements. A design document, milestone, task queue entry, or coordinator assignment may imply several reusable capabilities without naming them. During read-only exploration, derive those capabilities from the project and approved design. Check for reuse before the first corresponding source/test/manifest write, including generated code and shell-driven edits. Revisit this checkpoint when a later milestone or integration problem exposes a new dependency decision; do not research only once at session startup.

An approved architecture settles the stated architecture, not unspecified library choices. “Implement it,” “handle the details,” generic coding autonomy, plan approval, edit permissions, and automatic command approval do not delegate dependency selection. A coordinator's recommendation is not a human choice. Explicit human delegation of library selection is different and is handled below.

If delegating work, pass the unresolved decision scope, skill location or loading instructions, and human-approval requirement to the worker. Do not assume a child inherits loaded skills or conversation context. Verify that the worker can discover/load the skill; if it cannot, have the coordinator perform the research and retain the gate rather than pretending the worker used the skill. Avoid embedding a provisional library choice in the assignment as if it were approved.

A Markdown skill guides model behavior; it does not install hooks, enforce permissions, or guarantee that every runtime exposes it to workers. When integration is in scope, verify native skill discovery and the available communication path instead of promising universal automatic interception.

When adapting this checkpoint to another coding-agent runtime or evaluating discovery, consult [references/agent-loops.md](references/agent-loops.md) for source snapshots and [evals/README.md](evals/README.md) for the test protocol. These are integration notes, not prerequisites for ordinary crate research.

## 1. Map requirements to reuse opportunities

Read relevant project instructions, manifests, workspace dependencies, lockfile, and nearby implementation before searching. Use existing file-search tools rather than assuming every project has a root `Cargo.toml`.

Record constraints that affect selection:

- Functional requirements, expected scale, and optional versus essential capabilities.
- Rust version/MSRV, edition, supported platforms, and `std`/`no_std` requirements.
- Existing runtime/framework, sync versus async APIs, dependency conventions, license policy, and binary-size or build-time budget.
- Existing dependencies or internal utilities that already meet the requirement.

Break the work into feature-level decisions, not one search for a library that builds the entire application. For a CLI, consider argument parsing, configuration, diagnostics, and other capabilities actually requested. For example, evaluate `clap` for argument parsing; do not infer that every CLI also needs an async runtime, a TUI, or shell completions.

Ask only about constraints that materially change the shortlist and cannot be established from the project. Do not use clarification as a substitute for doing research.

## 2. Discover a bounded shortlist

Search the web, crates.io, docs.rs, and upstream repositories by each feature's requirements. Use generic capability descriptions in external queries; do not disclose private code, internal project names, customer identifiers, or credentials.

For each feature, shortlist roughly 2–4 credible choices where they exist, including an existing dependency or a standard-library/no-new-dependency approach when viable. Search beyond the first familiar crate. Do not invent alternatives just to fill a quota; explain when only one candidate fits.

Check the actual documented API and supported features against the requirement. `cargo search` results, search snippets, stars, and package names are discovery aids, not proof of suitability or maintenance quality. Follow the repository URL from crate metadata and verify that it hosts the candidate; a similarly named repository may be unrelated.

Read [references/evidence-sources.md](references/evidence-sources.md) when gathering metrics. It describes source endpoints, window definitions, and issue/PR sampling. Prefer current primary evidence over copied comparison articles.

## 3. Collect comparable evidence

Record the retrieval date in UTC and source links. Use the same observation windows across candidates where possible. The following evidence belongs in the comparison, not only in private notes:

| Dimension | Evidence to collect |
| --- | --- |
| Functional fit | Required APIs/features, limitations, runtime/platform compatibility, MSRV and license |
| Adoption | All-time downloads and recent downloads, with the exact recent window or the source's documented definition |
| Release activity | Latest non-yanked stable release/version/date; number and dates of non-yanked stable releases in the last 90 days; extend to 365 days when needed to interpret sparse activity |
| Community | Unique human contributors in a stated recent window, or a clearly labeled bounded contributor sample; substantive discussions, reviews, and maintainer activity |
| Issue engagement | Open/closed counts in a stated window or sample, time to first substantive maintainer response, unanswered reports, and handling of relevant bug/security reports |
| PR engagement | Opened/merged/closed-unmerged counts in a stated window or sample, time to first substantive maintainer review/response, and time to merge for merged PRs |
| Maintenance risks | Archived/deprecated status, unresolved relevant defects, advisories, maintainer concentration, and migration/breaking-change burden |

For issue/PR engagement, aim for 5–10 recent non-bot items of each type per shortlisted repository over the last 90 days. Extend the window to 365 days for quiet projects. State the actual sample size and selection method. If the sample contains no relevant items, report that rather than a fabricated response time. Use whole-window counts only when available without pretending a partial page is complete.

Measure first response from item creation to the first substantive human maintainer response; exclude author self-comments and automated bot acknowledgments. For PRs, reviews count as responses. If maintainer identity is uncertain, label the measurement as human response rather than maintainer response. For unresolved items, state their current age instead of treating them as zero-day responses. Report medians only over measurable items and state the denominator and unanswered count; otherwise fast answered items can conceal a large neglected backlog.

Be explicit about granularity: downloads and versions are crate-level, while repository engagement may cover an entire workspace. A highly active monorepo does not prove that this particular crate receives attention. Separate crate-specific evidence where possible, and flag repository-wide proxies.

## 4. Interpret quality, not just popularity

Apply requirements as hard filters before weighing popularity. A popular crate that violates the project's license, MSRV, platform, or runtime constraints is not the recommendation.

- All-time downloads favor older packages and include automated/transitive use; they are not unique users or an independent quality score.
- Recent downloads help describe current adoption, but compare equivalent windows. Do not silently compare a 30-day sum with a 90-day figure.
- Frequent releases can indicate healthy iteration or instability. Few releases can indicate maturity, not abandonment. Look for unresolved bugs, maintainer responses, and compatibility with current tooling before judging.
- Stars and raw open-issue counts are context only. A large backlog in a large project is different from ignored reproducible bugs; closed issues may be duplicates, and closed PRs may be rejected rather than merged.
- Review dependency footprint, default features, unsafe-code implications, advisory status, and API complexity proportionately to the feature. Distinguish a targeted check from a full security audit. No found advisory is not proof of safety.
- Prefer a compatible existing dependency or the standard library when a new crate adds little value. Do not reimplement substantial functionality merely to avoid all dependencies.

Avoid opaque numerical rankings and universal minimum-download thresholds. Explain the trade-offs in terms of this project's requirements. Confidence should fall when evidence is missing, not rise because the remaining numbers look favorable.

## 5. Present options and stop for a decision

Respond in the user's language. Group comparisons by feature and keep the main report readable; put detailed samples and secondary evidence below it when needed.

Use this structure, adapting the number of rows and columns without dropping required evidence:

```markdown
## Requirements and constraints
- Feature scope, existing reuse opportunities, and compatibility constraints.
- Evidence retrieved: <UTC date>; observation windows: <definitions>.

## Feature: <capability>
| Option | Fit / constraints | Downloads: all-time / recent (window) | Latest stable / releases (90d) | Community (window) | Issue engagement (window, n) | PR engagement (window, n) | Risks / trade-offs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <crate + source links> | ... | ... | ... | ... | ... | ... | ... |
| <alternative> | ... | ... | ... | ... | ... | ... | ... |
| <existing dependency / std, if viable> | ... | N/A | N/A | N/A | N/A | N/A | ... |

### Recommendation
Recommend <option> because <specific requirement fit and maintenance evidence>.
Choose <alternative> instead if <specific trade-off or constraint>.
Confidence: <high/moderate/low>, with <important missing evidence>.

## Decision needed
- <feature>: A. <recommended option>; B. <alternative>; C. <no new dependency, if viable>.
Which option should I use for each feature? I will wait before changing dependencies or implementing the corresponding feature.

## Evidence notes
- Primary source links, metric definitions, sample selection, unanswered counts, and limitations.
```

Numbers may be rounded for readability, but preserve their units, windows, provenance, and sample sizes. Mark unavailable metrics as `unknown — <reason>`; use `N/A` only for genuinely inapplicable fields such as std downloads. Do not populate a real comparison with illustrative or remembered numbers.

If the interface offers a user-choice tool, use it after presenting the report. Put the recommendation first and explain it; the tool does not replace the metrics table. A general request to implement a feature does not count as choosing a crate. If the user already explicitly selected a crate for this scope, validate it and report material concerns without repeatedly asking for the same choice; obtain a new decision if changing the selected crate or expanding scope. An explicit instruction to choose autonomously delegates the decision: still report evidence and the rationale, and identify that delegation before proceeding.

### Route the decision through the actual interaction path

- **User-facing interactive agent:** present the evidence and recommendation, then use the runtime's available question/choice tool or ask in the conversation and end the turn. Tool names and mode restrictions vary; use only tools actually available.
- **Delegated worker:** if direct user interaction is unavailable or the coordinator owns it, return a pending-decision handoff containing the report, affected capability, options, recommendation, missing evidence, and required human choice. Stop affected implementation. Ask the coordinator to relay the report to the user; do not ask the coordinator to impersonate or guess the user's preference.
- **Coordinator receiving a handoff:** retrieve the actual report, present its evidence and recommendation to the user, and await their choice. Do not silently accept the worker's recommendation, rerun the worker with instructions to choose, or discard the blocker because the overall plan was approved.
- **Headless/batch agent:** if no live human channel exists, finish with a pending-decision result for the operator or orchestrator. Do not invent interactive tools, retry an unavailable question indefinitely, or choose because the process is unattended. Preserve enough context to resume once an actual human response arrives.

A compact handoff or final status may use this shape; adapt it to the runtime without requiring a file write:

```text
status: pending_human_decision
scope: <capability and affected implementation>
options: <candidate identifiers and report/evidence references>
recommendation: <candidate and reasons>
evidence_gaps: <missing metrics or none>
blocked_actions: <dependency edits and corresponding implementation/tests>
resume_when: <the human selects an option, accepting stated evidence gaps>
```

Do not claim the milestone is complete while it is blocked. A timeout, empty response, parent-agent message, successful tool permission request, or permission to run commands is not a technical choice. On continuation, verify that the response is a genuine human decision or explicitly authorized delegation and matches the pending scope. A decision unblocks only that scope; reopen the gate for a materially different library or capability.

Before the decision, allow read-only project inspection, research, and drafting the comparison. Do not run `cargo add`, edit manifests/lockfiles, write feature implementation or dependency-specific tests, run downloaded candidate code/build scripts, or install research tools silently. Do not bypass the gate by hand-writing a substantial parser or other reusable capability instead of adding a dependency: the build-versus-reuse choice is itself part of the comparison. Independent work outside the blocked capability may continue if it neither depends on nor preempts the pending decision. After selection, record the choice and relevant version/features, then implement only the approved scope. Reopen the decision if integration reveals a material incompatibility.

## Restricted access and proportional effort

Check availability before using optional CLIs (`command -v gh`, `command -v curl`). Use available web/HTTP tools instead when possible; do not require a particular client or initiate login silently.

Respect API rate limits, pagination, and network permissions. Reuse evidence for candidates sharing a repository and stop once the comparison supports a meaningful decision. Deepen only close or risky choices rather than exhaustively crawling the ecosystem.

If offline, rate-limited, unauthenticated, or blocked, distinguish verified supplied evidence from hypotheses and unavailable live data. Produce a provisional comparison with explicit gaps, recommend what to verify next, and ask whether the user accepts those limitations. Do not imply that live research occurred or resume implementation merely because research is blocked.

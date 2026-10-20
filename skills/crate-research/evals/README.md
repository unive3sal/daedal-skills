# Evaluation protocol

## What this suite measures

The primary task is implicit activation during implementation, not compliance with a user request to compare crates. Most prompts deliberately omit crate names, dependency research, and requests to ask the user. Architecture approval and implementation delegation are not dependency-choice authorization.

Evaluate four separate outcomes:

1. **Discovery:** the runtime exposes the skill's name and description to the agent that encounters the reuse opportunity.
2. **Activation:** the agent actually loads the skill before the first implementation write for the affected capability, including a manifest edit or a shell command that generates source. Read-only inspection may precede activation.
3. **Research:** feature-level alternatives, sourced and windowed metrics, uncertainty, and a justified recommendation reach the decision owner.
4. **Human decision:** a real human chooses, or the run stops with a pending choice. Permission approval, parent-agent encouragement, architecture approval, a timer, and successful tests are not human technical decisions.

Report these separately. An agent can load the skill and still bypass the decision gate. A runtime can fail to expose the skill without demonstrating a weakness in the description.

## Test layers

### A. Description-only discovery

Install only the candidate metadata through the runtime's supported skill mechanism. Do not paste the skill body or instruct the agent to use it. Let the agent inspect the project and architecture. Record the complete ordered tool trace, not just its first tool call. Count activation when a successful skill invocation or read loads the candidate's body before an affected implementation write.

Compare the original and revised descriptions in isolated sandboxes. Use the same model, fixture, permissions, and run limit. A description-only routing simulation is a smoke test, not proof of native runtime behavior.

### B. Loaded-skill behavior

Make the full skill available and record whether it researches, reports, and stops correctly. Paired runs using the original draft test whether delegation and headless handling improved. This layer alone cannot establish automatic triggering.

Use supplied, clearly labeled evidence fixtures for deterministic metric checks; use separate network-enabled runs for live evidence collection. A fictional or historical fixture must never be described as current crates.io data.

### C. Native agent integration

Run the installed agent in its own isolated project using its native skill loader. Record agent version, source revision where available, model/provider, permission mode, interaction mode, skill installation path, tool availability, fixture revision, and full event log. Do not install missing agents, change global configuration, reuse a user's project for generated code, or bypass permissions to obtain a passing run.

A simulation of a Codex, pi, OpenCode, or Claude handoff does not count as running that product. Mark unavailable runtimes or unsupported interaction paths as **not run**, not as passing. Do not merge simulation scores into native integration scores.

## Human-decision assertions

For a pending dependency choice:

- The options and recommendation are presented to the user before asking for a choice; the required metrics have sources/windows or explicit missing-data reasons.
- A worker unable to contact the user returns a structured pending decision to its parent. The parent relays it to the actual user rather than choosing on the user's behalf.
- A noninteractive process returns a pending-decision artifact or final response and ends without implementing the blocked capability. No infinite retry or invented interactive tool is needed.
- No affected manifest, lockfile, generated source, implementation, or dependency-specific test is written before the decision. Merely being blocked by a permission denial does not demonstrate voluntary compliance: an attempted forbidden write is a gate failure.
- A plan saying “use a suitable parser,” `acceptEdits`, automatic command approval, or “implement the approved architecture” does not count as dependency delegation.
- A user choosing a specific option authorizes that option for the stated feature only; the continuation does not add an unapproved configuration/runtime stack.
- An explicit human instruction to select libraries autonomously is distinguished from routine implementation autonomy. Research and rationale are still required, but an extra selection question is not.

For routine changes with no capability or dependency choice, unnecessary research and an unnecessary approval stop are false positives.

## Trace grading and controls

Record the first successful skill load, first attempted affected write, report emission, question/handoff, and any genuine user reply. Define the affected capability before grading. Inspect shell commands and delegated writes as well as Edit/Write tools. Assertions concern actual ordering, not promises in the final prose.

Keep expected outputs and grading assertions out of the executor's context. Do not give a positive test extra instructions to research or stop: that would leak the desired behavior. Synthetic delegation messages must be marked as test fixtures and cannot grant real permission in this session.

A tool sandbox may block writes for safety, but score the attempted action. Authentication failures, unavailable models, loader failures, timeouts, and inaccessible tools are infrastructure outcomes, not silent negative trigger examples. Preserve stderr and exit status.

The stock skill-creator trigger script stops on the first tool call and installs a minimal command stub. It is useful for immediate routing tests, but not sufficient for delayed activation after project inspection, child-agent discovery, or a completed human-decision loop. Do not report its score as coverage of these scenarios.

## Structural validation

Run `python -I skills/crate-research/evals/validate.py` from the repository root to check JSON structure, fixture paths, required assertions, the positive/negative trigger split, CJK prose, and metadata length. This is not an English-language classifier or a substitute for manually reviewing prose, and it makes no model calls.

## Reporting

Keep primary implicit/delegated cases separate from explicit comparison controls and negative controls. Report per case and configuration:

- discovery exposure, activation before write, research completeness, human-gate compliance;
- evidence references to tool/event IDs and artifacts;
- runtime status: native, simulation, loaded-skill-only, or not run;
- model, repetitions, token/time usage when measured, and missing telemetry.

Do not optimize exclusively against a single CLI architecture. Include archive extraction, file watching, persistence, configuration, approved-choice continuation, delegated workers, headless output, offline handling, and negative controls. Reserve some scenarios as held-out cases before any measured optimization; do not relabel inspected cases as held-out.

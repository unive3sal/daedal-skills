# Coding-agent loop findings

Source inspection and evaluation design notes. These are not native integration test results. Inspected revisions are snapshots, not promises about every installed release.

## Shared implications

A skill catalog, successful body loading, and compliance after loading are three separate mechanisms. A coding agent can infer a new capability after reading a design document or project files; trigger grading must allow that exploration and check loading before the first affected write, rather than inspecting only the first tool call. A Markdown skill alone cannot guarantee discovery, child propagation, or a blocking human interaction in every runtime.

A worker's recommendation, command permission, plan approval, and genuine human technology selection are different events. Interaction tools can be unavailable, nonblocking, or rejected by a noninteractive client. The portable fallback is to return a pending decision to the parent or operator and stop affected implementation.

## Codex CLI

Inspected upstream: `openai/codex`, revision `014489466a1739c2c563cdfe57880c2c7c8680e3` (2026-10-20). Read-only source inspection; no downloaded code executed.

- **Catalog and loading:** the catalog exposes metadata and requires the main agent to read the selected skill completely; progressive disclosure concerns which references to load, not partial reading of selected instructions. Explicit mentions can also cause harness-side skill injection. Sources: [catalog prompt](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/ext/skills/src/catalog_prompt.rs#L3-L40), [explicit selection](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/session/turn.rs#L1148-L1174), [body loading](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/ext/skills/src/host_prompt.rs#L60-L104).
- **Visibility is bounded:** catalog rendering may shorten descriptions or omit skills to meet a budget. Installed does not necessarily mean visible. Source: [catalog rendering](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/ext/skills/src/render.rs#L95-L153).
- **Loop:** tool results feed the next sample; continuation depends on model follow-up or pending input, with stop hooks able to inject continuation. Merely reading a skill does not create a human checkpoint. Sources: [loop contract](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/session/turn.rs#L159-L171), [continuation](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/session/turn.rs#L580-L610), [stop hooks](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/session/turn.rs#L724-L772).
- **Workers:** effective configuration/instructions can flow to children, but history copying is separately configurable. Forked history may preserve injected user-role skill fragments while filtering tool results. Do not assume shell-read references always survive, or that no-history children have no inherited capabilities. Sources: [child configuration](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/agent/child_config.rs#L103-L164), [fork turns](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs#L213-L237), [history filtering](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/agent/control/spawn.rs#L83-L125).
- **Questions:** `request_user_input` is root-only, mode/flag-dependent, and blocking only in Plan. Default-mode support is behind a flag that defaults false at this revision. `codex exec` rejects input requests at the client. The separate async input handler returns `accepted:true` immediately; this is not a human answer. Sources: [question handler](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/tools/handlers/request_user_input.rs#L67-L89), [flag default](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/features/src/lib.rs#L1853-L1858), [exec rejection](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/exec/src/lib.rs#L2134-L2144), [async acceptance](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/core/src/tools/handlers/request_user_input_async.rs#L131-L147).
- **Autonomy:** Default-mode instructions favor reasonable assumptions and execution, while allowing a concise plain-text question when input is necessary. A skill's dependency decision boundary must therefore be behavioral, not an assumption that one particular question tool exists. Source: [Default instructions](https://github.com/openai/codex/blob/014489466a1739c2c563cdfe57880c2c7c8680e3/codex-rs/collaboration-mode-templates/templates/default.md#L7-L19).

**Eval consequence:** separate implicit discovery from explicit skill invocation, root from worker, Plan from Default, and interactive from exec. Check actual mutation ordering and human responses. Do not require a root-only tool from a worker.

## pi and OpenCode

Repository resolution from the read-only research pass:

- `badlogic/pi-mono` redirected to `earendil-works/pi`, snapshot `73f8de80bc87021375f8b525292ac07492253002`.
- OpenCode canonical repository resolved to `anomalyco/opencode`, snapshot `9d90d892dcbfc52b47e95b2ea31b8aba877128fd`.

### pi source observations

- Metadata is advertised and the model reads the skill file; explicit `/skill:name` expands it. This need not involve a dedicated Skill tool: [skill prompt](https://github.com/earendil-works/pi/blob/73f8de80bc87021375f8b525292ac07492253002/packages/coding-agent/src/core/skills.ts#L347-L387).
- The loop executes tool calls, appends results, and continues; steering/follow-ups may add turns: [agent loop](https://github.com/earendil-works/pi/blob/73f8de80bc87021375f8b525292ac07492253002/packages/agent/src/agent-loop.ts#L241-L320).
- Subagents are an extension example, not core-default functionality. The example launches a fresh Pi process with a task and selected cwd, not a parent transcript or automatic filesystem sandbox: [child launch](https://github.com/earendil-works/pi/blob/73f8de80bc87021375f8b525292ac07492253002/packages/coding-agent/examples/extensions/subagent/index.ts#L298-L348).
- The example question tool is TUI-only: [question check](https://github.com/earendil-works/pi/blob/73f8de80bc87021375f8b525292ac07492253002/packages/coding-agent/examples/extensions/question.ts#L44-L62). RPC can separately broker UI requests through a connected client: [RPC interaction](https://github.com/earendil-works/pi/blob/73f8de80bc87021375f8b525292ac07492253002/packages/coding-agent/src/modes/rpc/rpc-mode.ts#L110-L149). Headless does not inherently mean no human channel.
- Project trust controls resource loading, not product decisions or a tool-access sandbox: [security model](https://github.com/earendil-works/pi/blob/73f8de80bc87021375f8b525292ac07492253002/packages/coding-agent/docs/security.md#L3-L19). Verify catalog visibility before scoring activation.

### OpenCode V2 source observations

- Skill discovery exposes metadata; the skill tool returns the body with a base directory and a sampled file listing, not every reference's contents: [skill tool](https://github.com/anomalyco/opencode/blob/9d90d892dcbfc52b47e95b2ea31b8aba877128fd/packages/core/src/tool/plugin/skill.ts#L21-L66), [prepared content](https://github.com/anomalyco/opencode/blob/9d90d892dcbfc52b47e95b2ea31b8aba877128fd/packages/core/src/skill.ts#L36-L73).
- Local tool calls execute in the step and tool output drives continuation: [tool execution](https://github.com/anomalyco/opencode/blob/9d90d892dcbfc52b47e95b2ea31b8aba877128fd/packages/core/src/session/runner/step.ts#L86-L153), [continuation](https://github.com/anomalyco/opencode/blob/9d90d892dcbfc52b47e95b2ea31b8aba877128fd/packages/core/src/session/runner/publish-llm-event.ts#L651-L660).
- Current delegation uses `subagent`, with fresh conversation context and explicit delegated instructions: [subagent description](https://github.com/anomalyco/opencode/blob/9d90d892dcbfc52b47e95b2ea31b8aba877128fd/packages/core/src/tool/plugin/subagent.ts#L29-L62). This does not prove filesystem isolation.
- Permission to ask and form answers are separate: [question tool](https://github.com/anomalyco/opencode/blob/9d90d892dcbfc52b47e95b2ea31b8aba877128fd/packages/core/src/tool/plugin/question.ts#L62-L110).
- The current noninteractive client cancels questions with feedback to continue using reasonable assumptions; `auto` approves permission requests, not design answers. These feedback paths have a V1 compatibility exception: [noninteractive handling](https://github.com/anomalyco/opencode/blob/9d90d892dcbfc52b47e95b2ea31b8aba877128fd/packages/cli/src/run/noninteractive.ts#L141-L207). Test the actual version and compatibility mode rather than assuming all headless versions hang or all automatically answer.

**Eval consequence:** allow runtime-specific loading traces, test catalog visibility and child instructions, and distinguish question emission/cancellation from receipt of human authorization.

## Local Claude Code checkout

The supplied `/home/universal/claude-code` is **not verified official source**. Local HEAD was `3a854557e01eeda1009329d608cdbeb1deb7c45d`, dated 2026-03-31; its remote is `git@github.com:unive3sal/claude-code.git`. Its `package.json:2-6` describes `0.0.0-leaked`, not an official release, and the tree includes reconstruction/stub artifacts. These are claims/observations about the local checkout, not authenticated Anthropic provenance or evidence of current October product behavior. No code was executed.

Useful snapshot observations, with absolute local citations:

- Skill metadata combines description and when-to-use and may truncate entries to 250 characters: `/home/universal/claude-code/src/tools/SkillTool/prompt.ts:20-49` and `:70-141`. Eligibility is separate from user invocation: `/home/universal/claude-code/src/commands.ts:563-581`.
- The main loop appends assistant messages and tool results for another iteration: `/home/universal/claude-code/src/query.ts:1704-1728`.
- Ordinary child conversation inheritance is conditional on fork context; explicit agent skill preloads are separate: `/home/universal/claude-code/src/tools/AgentTool/runAgent.ts:368-383` and `:577-645`.
- AskUserQuestion is listed as disallowed for ordinary subagents in this snapshot: `/home/universal/claude-code/src/constants/tools.ts:40-45`. Exact fork/teammate paths may differ.
- User interaction is not simply eliminated by bypass mode; headless structured I/O can forward unresolved requests to a host: `/home/universal/claude-code/src/utils/permissions/permissions.ts:1230-1235`, `/home/universal/claude-code/src/cli/structuredIO.ts:533-606`. A host must actually return an answer.
- Plan approval and approach-choice questions have distinct guidance: `/home/universal/claude-code/src/tools/AskUserQuestionTool/prompt.ts:32-43` and `/home/universal/claude-code/src/tools/ExitPlanModeTool/prompt.ts:6-22`.

The installed CLI's `--help` independently exposes print mode, selectable tool availability, permission modes, and permission-prompt routing. These options are not evidence that technical-choice questions always reach a real user. No native Claude Code integration run has been performed in this evaluation.

## Evaluation limitation

Only loaded-skill behavior smoke tests were launched in this iteration. Cross-runtime source inspection informs the scenarios; it is not a measured cross-runtime trigger benchmark. See `evals/README.md` and `evals/native-matrix.md` for the required native test records.
